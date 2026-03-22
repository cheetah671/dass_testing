"""White-box unit tests for player money, movement, and state paths."""

import pytest

from moneypoly.config import GO_SALARY
from moneypoly.player import Player


@pytest.mark.parametrize("amount", [0, 1, 200])
def test_add_money_updates_balance(amount):
    """add_money should increase balance for non-negative amounts."""
    player = Player("P")
    start = player.balance

    player.add_money(amount)

    assert player.balance == start + amount


def test_add_money_raises_for_negative_amount():
    """Negative add should raise ValueError."""
    player = Player("P")
    with pytest.raises(ValueError):
        player.add_money(-1)


@pytest.mark.parametrize("amount", [0, 1, 250])
def test_deduct_money_updates_balance(amount):
    """deduct_money should reduce balance for non-negative amounts."""
    player = Player("P")
    start = player.balance

    player.deduct_money(amount)

    assert player.balance == start - amount


def test_deduct_money_raises_for_negative_amount():
    """Negative deduction should raise ValueError."""
    player = Player("P")
    with pytest.raises(ValueError):
        player.deduct_money(-5)


@pytest.mark.parametrize(
    "start_pos,steps,expected_pos,collects_salary",
    [
        (0, 0, 0, True),
        (0, 5, 5, False),
        (39, 1, 0, True),
        (39, 2, 1, True),
        (10, 5, 15, False),
    ],
)
def test_move_position_and_salary_logic(start_pos, steps, expected_pos, collects_salary):
    """move should wrap around board and pay salary when crossing/landing on Go."""
    player = Player("P")
    player.position = start_pos
    start_balance = player.balance

    new_position = player.move(steps)

    assert new_position == expected_pos
    if collects_salary:
        assert player.balance == start_balance + GO_SALARY
    else:
        assert player.balance == start_balance


def test_go_to_jail_sets_expected_state():
    """go_to_jail should set jail state and jail position."""
    player = Player("P")
    player.jail_turns = 2

    player.go_to_jail()

    assert player.in_jail is True
    assert player.position == 10
    assert player.jail_turns == 0


@pytest.mark.parametrize("balance,expected", [(-1, True), (0, True), (1, False)])
def test_is_bankrupt_threshold(balance, expected):
    """is_bankrupt should return True only for zero or negative balance."""
    player = Player("P")
    player.balance = balance

    assert player.is_bankrupt() is expected


def test_property_add_remove_idempotent():
    """Property add/remove should behave safely for duplicates and missing values."""
    player = Player("P")
    prop = object()

    player.add_property(prop)
    player.add_property(prop)
    assert player.count_properties() == 1

    player.remove_property(prop)
    player.remove_property(prop)
    assert player.count_properties() == 0


def test_status_line_includes_jail_marker_only_when_jailed():
    """status_line should include [JAILED] conditionally."""
    player = Player("P")
    assert "[JAILED]" not in player.status_line()

    player.in_jail = True
    assert "[JAILED]" in player.status_line()


def test_net_worth_matches_balance_for_current_model():
    """net_worth currently tracks only cash balance."""
    player = Player("P")
    player.balance = 1337

    assert player.net_worth() == 1337
