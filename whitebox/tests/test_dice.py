"""White-box unit tests for dice behavior and edge conditions."""

import pytest

from moneypoly.dice import Dice


def test_roll_calls_randint_with_six_sided_bounds(monkeypatch):
    """Dice should call randint with 1..6 bounds for both dice."""
    calls = []

    def fake_randint(low, high):
        calls.append((low, high))
        return 6

    monkeypatch.setattr("moneypoly.dice.random.randint", fake_randint)

    dice = Dice()
    total = dice.roll()

    assert total == 12
    assert calls == [(1, 6), (1, 6)]


def test_doubles_streak_updates_across_rolls(monkeypatch):
    """Doubles streak should increment and reset correctly."""
    values = iter([2, 2, 3, 3, 4, 5])
    monkeypatch.setattr("moneypoly.dice.random.randint", lambda *_: next(values))

    dice = Dice()
    dice.roll()
    assert dice.doubles_streak == 1

    dice.roll()
    assert dice.doubles_streak == 2

    dice.roll()
    assert dice.doubles_streak == 0


@pytest.mark.parametrize(
    "die1,die2,is_doubles,total",
    [
        (1, 1, True, 2),
        (1, 6, False, 7),
        (3, 3, True, 6),
        (6, 2, False, 8),
    ],
)
def test_total_and_is_doubles_combinations(die1, die2, is_doubles, total):
    """total() and is_doubles() should reflect die faces exactly."""
    dice = Dice()
    dice.die1 = die1
    dice.die2 = die2

    assert dice.is_doubles() is is_doubles
    assert dice.total() == total


@pytest.mark.parametrize(
    "die1,die2,expected",
    [
        (2, 2, "2 + 2 = 4 (DOUBLES)"),
        (2, 5, "2 + 5 = 7"),
    ],
)
def test_describe_formats_output(die1, die2, expected):
    """describe() should include total and doubles tag when relevant."""
    dice = Dice()
    dice.die1 = die1
    dice.die2 = die2

    assert dice.describe() == expected


def test_reset_clears_faces_and_streak():
    """reset() should clear both die values and doubles streak."""
    dice = Dice()
    dice.die1 = 4
    dice.die2 = 6
    dice.doubles_streak = 2

    dice.reset()

    assert dice.die1 == 0
    assert dice.die2 == 0
    assert dice.doubles_streak == 0
