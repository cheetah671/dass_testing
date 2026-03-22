"""Integration and decision-path tests for game flow."""

import pytest

from moneypoly.game import Game


def _make_game():
    return Game(["A", "B", "C"])


@pytest.mark.parametrize(
    "balance_delta,expected_success",
    [
        (-1, False),
        (0, True),
        (100, True),
    ],
)
def test_buy_property_balance_threshold(balance_delta, expected_success):
    """buy_property should branch on affordability threshold."""
    game = _make_game()
    player = game.players[0]
    prop = game.board.properties[0]
    player.balance = prop.price + balance_delta

    result = game.buy_property(player, prop)

    assert result is expected_success


def test_pay_rent_transfers_money_to_owner():
    """Rent payment should move funds from tenant to owner."""
    game = Game(["Owner", "Tenant"])
    owner, tenant = game.players
    prop = game.board.properties[0]
    prop.owner = owner
    owner.add_property(prop)

    tenant_start = tenant.balance
    owner_start = owner.balance
    rent = prop.get_rent()

    game.pay_rent(tenant, prop)

    assert tenant.balance == tenant_start - rent
    assert owner.balance == owner_start + rent


def test_pay_rent_skips_when_property_mortgaged():
    """Mortgaged property should not transfer rent."""
    game = Game(["Owner", "Tenant"])
    owner, tenant = game.players
    prop = game.board.properties[0]
    prop.owner = owner
    owner.add_property(prop)
    prop.is_mortgaged = True

    tenant_start = tenant.balance
    owner_start = owner.balance

    game.pay_rent(tenant, prop)

    assert tenant.balance == tenant_start
    assert owner.balance == owner_start


@pytest.mark.parametrize(
    "seller_owns,buyer_balance,cash,expected",
    [
        (False, 1000, 200, False),
        (True, 50, 200, False),
        (True, 1000, 200, True),
    ],
)
def test_trade_decision_paths(seller_owns, buyer_balance, cash, expected):
    """trade should enforce ownership and buyer affordability checks."""
    game = Game(["Seller", "Buyer"])
    seller, buyer = game.players
    prop = game.board.properties[0]
    buyer.balance = buyer_balance

    if seller_owns:
        prop.owner = seller
        seller.add_property(prop)

    result = game.trade(seller, buyer, prop, cash)

    assert result is expected


def test_find_winner_returns_highest_net_worth_player():
    """Winner selection should pick maximum net worth."""
    game = Game(["A", "B", "C"])
    game.players[0].balance = 1200
    game.players[1].balance = 1800
    game.players[2].balance = 1600

    winner = game.find_winner()

    assert winner is game.players[1]


def test_check_bankruptcy_removes_player_and_resets_properties():
    """Bankrupt player should be removed and their properties released."""
    game = Game(["A", "B"])
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)
    player.balance = 0

    game._check_bankruptcy(player)

    assert player not in game.players
    assert prop.owner is None
    assert prop.is_mortgaged is False


def test_apply_card_collect_and_pay_paths():
    """collect/pay card actions should route through bank and player balances."""
    game = Game(["A", "B"])
    player = game.players[0]
    start = player.balance

    game._apply_card(player, {"description": "c", "action": "collect", "value": 40})
    assert player.balance == start + 40

    game._apply_card(player, {"description": "p", "action": "pay", "value": 25})
    assert player.balance == start + 15


def test_apply_card_jail_and_jail_free_paths():
    """jail/jail_free card actions should set expected jail state fields."""
    game = Game(["A", "B"])
    player = game.players[0]

    game._apply_card(player, {"description": "j", "action": "jail", "value": 0})
    assert player.in_jail is True

    game._apply_card(player, {"description": "jf", "action": "jail_free", "value": 0})
    assert player.get_out_of_jail_cards == 1


def test_apply_card_move_to_awards_go_salary_when_wrapping():
    """move_to card should award salary when moving from high to low index."""
    game = Game(["A", "B"])
    player = game.players[0]
    player.position = 35
    start = player.balance

    game._apply_card(player, {"description": "m", "action": "move_to", "value": 3})

    assert player.balance == start + 200


def test_apply_card_birthday_and_collect_from_all_paths():
    """Multi-player transfer cards should move money between players."""
    game = Game(["A", "B", "C"])
    player = game.players[0]
    b = game.players[1]
    c = game.players[2]
    b.balance = 20
    c.balance = 3

    start = player.balance
    game._apply_card(player, {"description": "b", "action": "birthday", "value": 10})
    assert player.balance == start + 10

    start2 = player.balance
    game._apply_card(
        player,
        {"description": "cfa", "action": "collect_from_all", "value": 5},
    )
    assert player.balance == start2 + 5


@pytest.mark.parametrize(
    "choice,expected_method",
    [
        ("b", "buy_property"),
        ("a", "auction_property"),
        ("s", None),
    ],
)
def test_handle_property_tile_purchase_decisions(monkeypatch, choice, expected_method):
    """Input choice on unowned property should follow buy/auction/skip branches."""
    game = Game(["A", "B"])
    player = game.players[0]
    prop = game.board.properties[0]

    calls = []

    def fake_buy(*_):
        calls.append("buy_property")
        return True

    def fake_auction(*_):
        calls.append("auction_property")

    monkeypatch.setattr("builtins.input", lambda *_: choice)
    monkeypatch.setattr(game, "buy_property", fake_buy)
    monkeypatch.setattr(game, "auction_property", fake_auction)

    game._handle_property_tile(player, prop)

    if expected_method is None:
        assert calls == []
    else:
        assert calls == [expected_method]
