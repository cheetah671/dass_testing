"""Additional white-box decision-path tests for game flow."""

from types import SimpleNamespace

import pytest

from moneypoly.game import Game


def _game(names=("A", "B", "C")):
    return Game(list(names))


def test_current_player_and_advance_turn_wrap():
    game = _game(("A", "B"))
    assert game.current_player().name == "A"
    game.advance_turn()
    assert game.current_player().name == "B"
    game.advance_turn()
    assert game.current_player().name == "A"
    assert game.turn_number == 2


def test_play_turn_jailed_player_calls_jail_handler_and_advances(monkeypatch):
    game = _game(("A", "B"))
    player = game.current_player()
    player.in_jail = True
    called = {"jail": 0}

    monkeypatch.setattr(game, "_handle_jail_turn", lambda p: called.__setitem__("jail", called["jail"] + 1))

    game.play_turn()

    assert called["jail"] == 1
    assert game.current_player().name == "B"


def test_play_turn_three_doubles_goes_to_jail(monkeypatch):
    game = _game(("A", "B"))
    player = game.current_player()

    monkeypatch.setattr(game.dice, "roll", lambda: 6)
    monkeypatch.setattr(game.dice, "describe", lambda: "3 + 3 = 6 (DOUBLES)")
    game.dice.doubles_streak = 3

    game.play_turn()

    assert player.in_jail is True
    assert game.current_player().name == "B"


def test_play_turn_doubles_grants_extra_turn(monkeypatch):
    game = _game(("A", "B"))

    monkeypatch.setattr(game.dice, "roll", lambda: 4)
    monkeypatch.setattr(game.dice, "describe", lambda: "2 + 2 = 4 (DOUBLES)")
    monkeypatch.setattr(game.dice, "is_doubles", lambda: True)
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_: None)

    game.play_turn()

    assert game.current_player().name == "A"


def test_play_turn_non_doubles_advances(monkeypatch):
    game = _game(("A", "B"))

    monkeypatch.setattr(game.dice, "roll", lambda: 5)
    monkeypatch.setattr(game.dice, "describe", lambda: "2 + 3 = 5")
    monkeypatch.setattr(game.dice, "is_doubles", lambda: False)
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_: None)

    game.play_turn()

    assert game.current_player().name == "B"


@pytest.mark.parametrize(
    "tile,position",
    [
        ("go_to_jail", 30),
        ("income_tax", 4),
        ("luxury_tax", 38),
        ("free_parking", 20),
        ("chance", 7),
        ("community_chest", 2),
        ("railroad", 5),
        ("property", 1),
    ],
)
def test_move_and_resolve_executes_tile_branches(monkeypatch, tile, position):
    game = _game(("A", "B"))
    player = game.players[0]

    monkeypatch.setattr(player, "move", lambda *_: position)
    monkeypatch.setattr(game.board, "get_tile_type", lambda *_: tile)

    handled = {"apply": 0, "prop": 0}
    monkeypatch.setattr(game, "_apply_card", lambda *_: handled.__setitem__("apply", handled["apply"] + 1))
    monkeypatch.setattr(game, "_handle_property_tile", lambda *_: handled.__setitem__("prop", handled["prop"] + 1))
    monkeypatch.setattr(game.board, "get_property_at", lambda *_: game.board.properties[0])

    game._move_and_resolve(player, 3)

    if tile in {"chance", "community_chest"}:
        assert handled["apply"] == 1
    if tile in {"railroad", "property"}:
        assert handled["prop"] == 1


def test_move_and_resolve_property_tile_with_no_property(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]

    monkeypatch.setattr(player, "move", lambda *_: 12)
    monkeypatch.setattr(game.board, "get_tile_type", lambda *_: "property")
    monkeypatch.setattr(game.board, "get_property_at", lambda *_: None)

    game._move_and_resolve(player, 3)


def test_handle_property_tile_owner_is_player(capsys):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player

    game._handle_property_tile(player, prop)

    out = capsys.readouterr().out
    assert "No rent due" in out


def test_handle_property_tile_owner_is_other_calls_pay_rent(monkeypatch):
    game = _game(("A", "B"))
    player, other = game.players
    prop = game.board.properties[0]
    prop.owner = other
    called = {"rent": 0}

    monkeypatch.setattr(game, "pay_rent", lambda *_: called.__setitem__("rent", called["rent"] + 1))

    game._handle_property_tile(player, prop)

    assert called["rent"] == 1


def test_mortgage_property_not_owner_returns_false(capsys):
    game = _game(("A", "B"))
    player, other = game.players
    prop = game.board.properties[0]
    prop.owner = other

    assert game.mortgage_property(player, prop) is False
    assert "does not own" in capsys.readouterr().out


def test_mortgage_property_already_mortgaged_returns_false(capsys):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)
    prop.mortgage()

    assert game.mortgage_property(player, prop) is False
    assert "already mortgaged" in capsys.readouterr().out


def test_mortgage_property_success_updates_state(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)
    before = player.balance

    collected = {"v": None}
    monkeypatch.setattr(game.bank, "collect", lambda v: collected.__setitem__("v", v))

    assert game.mortgage_property(player, prop) is True
    assert player.balance > before
    assert collected["v"] < 0


def test_unmortgage_property_not_owner_returns_false(capsys):
    game = _game(("A", "B"))
    player, other = game.players
    prop = game.board.properties[0]
    prop.owner = other

    assert game.unmortgage_property(player, prop) is False
    assert "does not own" in capsys.readouterr().out


def test_unmortgage_property_not_mortgaged_returns_false(capsys):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)

    assert game.unmortgage_property(player, prop) is False
    assert "is not mortgaged" in capsys.readouterr().out


def test_unmortgage_property_insufficient_funds_returns_false(capsys):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)
    prop.mortgage()
    player.balance = 1

    assert game.unmortgage_property(player, prop) is False
    assert "cannot afford" in capsys.readouterr().out


def test_unmortgage_property_success(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)
    prop.mortgage()

    collected = {"v": None}
    monkeypatch.setattr(game.bank, "collect", lambda v: collected.__setitem__("v", v))

    assert game.unmortgage_property(player, prop) is True
    assert collected["v"] > 0


def test_auction_property_no_valid_bids(monkeypatch, capsys):
    game = _game(("A", "B", "C"))
    prop = game.board.properties[0]
    bids = iter([0, 1, 0])
    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: next(bids))

    game.auction_property(prop)

    out = capsys.readouterr().out
    assert "remains unowned" in out


def test_auction_property_with_winner(monkeypatch):
    game = _game(("A", "B"))
    prop = game.board.properties[0]

    bids = iter([10, 40])
    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: next(bids))

    game.auction_property(prop)

    assert prop.owner is game.players[1]


def test_handle_jail_turn_uses_get_out_of_jail_card(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    player.in_jail = True
    player.get_out_of_jail_cards = 1

    confirms = iter([True])
    monkeypatch.setattr("moneypoly.ui.confirm", lambda *_: next(confirms))
    monkeypatch.setattr(game.dice, "roll", lambda: 4)
    monkeypatch.setattr(game.dice, "describe", lambda: "2 + 2 = 4")

    moved = {"count": 0}
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_: moved.__setitem__("count", moved["count"] + 1))

    game._handle_jail_turn(player)

    assert player.in_jail is False
    assert player.get_out_of_jail_cards == 0
    assert moved["count"] == 1


def test_handle_jail_turn_pays_fine_when_confirmed(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    player.in_jail = True

    confirms = iter([False, True])
    monkeypatch.setattr("moneypoly.ui.confirm", lambda *_: next(confirms))
    monkeypatch.setattr(game.dice, "roll", lambda: 3)
    monkeypatch.setattr(game.dice, "describe", lambda: "1 + 2 = 3")

    moved = {"count": 0}
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_: moved.__setitem__("count", moved["count"] + 1))

    game._handle_jail_turn(player)

    assert player.in_jail is False
    assert moved["count"] == 1


def test_handle_jail_turn_serves_time_when_no_action(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    player.in_jail = True
    player.jail_turns = 1

    confirms = iter([False, False])
    monkeypatch.setattr("moneypoly.ui.confirm", lambda *_: next(confirms))

    game._handle_jail_turn(player)

    assert player.in_jail is True
    assert player.jail_turns == 2


def test_handle_jail_turn_forced_release_after_three_turns(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    player.in_jail = True
    player.jail_turns = 2

    confirms = iter([False, False])
    monkeypatch.setattr("moneypoly.ui.confirm", lambda *_: next(confirms))
    monkeypatch.setattr(game.dice, "roll", lambda: 8)
    monkeypatch.setattr(game.dice, "describe", lambda: "4 + 4 = 8")

    moved = {"count": 0}
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_: moved.__setitem__("count", moved["count"] + 1))

    game._handle_jail_turn(player)

    assert player.in_jail is False
    assert player.jail_turns == 0
    assert moved["count"] == 1


def test_apply_card_none_returns_without_changes():
    game = _game(("A", "B"))
    player = game.players[0]
    start = player.balance

    game._apply_card(player, None)

    assert player.balance == start


def test_apply_card_move_to_non_property_no_prompt(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    player.position = 5

    monkeypatch.setattr(game.board, "get_tile_type", lambda *_: "blank")
    game._apply_card(player, {"description": "m", "action": "move_to", "value": 12})

    assert player.position == 12


def test_apply_card_move_to_property_without_prop_object(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]

    monkeypatch.setattr(game.board, "get_tile_type", lambda *_: "property")
    monkeypatch.setattr(game.board, "get_property_at", lambda *_: None)

    game._apply_card(player, {"description": "m", "action": "move_to", "value": 12})


@pytest.mark.parametrize("action", ["birthday", "collect_from_all"])
def test_apply_card_transfer_actions_skip_insufficient_players(action):
    game = _game(("A", "B", "C"))
    player = game.players[0]
    game.players[1].balance = 4
    game.players[2].balance = 3
    start = player.balance

    game._apply_card(player, {"description": "x", "action": action, "value": 5})

    assert player.balance == start


def test_check_bankruptcy_non_bankrupt_keeps_player():
    game = _game(("A", "B"))
    player = game.players[0]
    player.balance = 1

    game._check_bankruptcy(player)

    assert player in game.players


def test_find_winner_no_players_returns_none():
    game = _game(("A",))
    game.players = []

    assert game.find_winner() is None


def test_run_handles_no_players_path(capsys):
    game = _game(("A",))
    game.players = []
    game.run()
    assert "no players remaining" in capsys.readouterr().out


def test_run_winner_path_with_single_player(monkeypatch, capsys):
    game = _game(("Solo",))
    monkeypatch.setattr("moneypoly.ui.print_standings", lambda *_: None)

    game.run()

    out = capsys.readouterr().out
    assert "wins with a net worth" in out


def test_interactive_menu_routes_all_options(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]

    calls = []
    choices = iter([1, 2, 3, 4, 5, 6, 0])
    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: next(choices))
    monkeypatch.setattr("moneypoly.ui.print_standings", lambda *_: calls.append("standings"))
    monkeypatch.setattr("moneypoly.ui.print_board_ownership", lambda *_: calls.append("board"))
    monkeypatch.setattr(game, "_menu_mortgage", lambda *_: calls.append("mortgage"))
    monkeypatch.setattr(game, "_menu_unmortgage", lambda *_: calls.append("unmortgage"))
    monkeypatch.setattr(game, "_menu_trade", lambda *_: calls.append("trade"))
    monkeypatch.setattr(game.bank, "give_loan", lambda *_: calls.append("loan"))

    game.interactive_menu(player)

    assert calls == ["standings", "board", "mortgage", "unmortgage", "trade", "loan"]


def test_menu_mortgage_no_properties(capsys):
    game = _game(("A", "B"))
    game._menu_mortgage(game.players[0])
    assert "No properties available" in capsys.readouterr().out


def test_menu_mortgage_valid_selection(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)

    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: 1)
    called = {"mortgage": 0}
    monkeypatch.setattr(game, "mortgage_property", lambda *_: called.__setitem__("mortgage", called["mortgage"] + 1))

    game._menu_mortgage(player)

    assert called["mortgage"] == 1


def test_menu_unmortgage_no_mortgaged(capsys):
    game = _game(("A", "B"))
    game._menu_unmortgage(game.players[0])
    assert "No mortgaged properties" in capsys.readouterr().out


def test_menu_unmortgage_valid_selection(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)
    prop.mortgage()

    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: 1)
    called = {"unmortgage": 0}
    monkeypatch.setattr(game, "unmortgage_property", lambda *_: called.__setitem__("unmortgage", called["unmortgage"] + 1))

    game._menu_unmortgage(player)

    assert called["unmortgage"] == 1


def test_menu_trade_no_other_players(capsys):
    game = _game(("A",))
    game._menu_trade(game.players[0])
    assert "No other players" in capsys.readouterr().out


def test_menu_trade_invalid_partner_index(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: 0)

    game._menu_trade(player)


def test_menu_trade_player_without_properties(monkeypatch, capsys):
    game = _game(("A", "B"))
    player = game.players[0]
    choices = iter([1])
    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: next(choices))

    game._menu_trade(player)

    assert "has no properties" in capsys.readouterr().out


def test_menu_trade_invalid_property_index(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)

    choices = iter([1, 0])
    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: next(choices))

    game._menu_trade(player)


def test_menu_trade_success_calls_trade(monkeypatch):
    game = _game(("A", "B"))
    player = game.players[0]
    prop = game.board.properties[0]
    prop.owner = player
    player.add_property(prop)

    choices = iter([1, 1, 150])
    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: next(choices))

    called = {"trade": 0}
    monkeypatch.setattr(game, "trade", lambda *_: called.__setitem__("trade", called["trade"] + 1))

    game._menu_trade(player)

    assert called["trade"] == 1
