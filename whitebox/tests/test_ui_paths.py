"""Expanded white-box tests for UI helper decision paths."""

from types import SimpleNamespace

import pytest

from moneypoly import ui


class _DummyPlayer:
    def __init__(self, name="P", in_jail=False, jail_turns=0, jail_cards=0, props=None):
        self.name = name
        self.balance = 1500
        self.position = 7
        self.in_jail = in_jail
        self.jail_turns = jail_turns
        self.get_out_of_jail_cards = jail_cards
        self.properties = props or []

    def net_worth(self):
        return self.balance + 100

    def count_properties(self):
        return len(self.properties)


class _DummyProperty:
    def __init__(self, name, pos, price, rent, owner=None, mortgaged=False):
        self.name = name
        self.position = pos
        self.price = price
        self._rent = rent
        self.owner = owner
        self.is_mortgaged = mortgaged

    def get_rent(self):
        return self._rent


def test_print_banner_outputs_title(capsys):
    ui.print_banner("My Title")
    out = capsys.readouterr().out
    assert "My Title" in out
    assert "=" in out


def test_print_player_card_with_no_properties(capsys):
    player = _DummyPlayer(props=[])
    ui.print_player_card(player)
    out = capsys.readouterr().out
    assert "Properties: none" in out
    assert "IN JAIL" not in out


def test_print_player_card_with_jail_and_properties(capsys):
    prop = _DummyProperty("Avenue", 1, 100, 10, mortgaged=True)
    player = _DummyPlayer(in_jail=True, jail_turns=2, jail_cards=1, props=[prop])

    ui.print_player_card(player)

    out = capsys.readouterr().out
    assert "IN JAIL" in out
    assert "Jail cards: 1" in out
    assert "[MORTGAGED]" in out


def test_print_standings_sorts_by_net_worth_and_marks_jailed(capsys):
    p1 = _DummyPlayer(name="A")
    p2 = _DummyPlayer(name="B", in_jail=True)
    p3 = _DummyPlayer(name="C")
    p1.balance = 1200
    p2.balance = 1800
    p3.balance = 1600

    ui.print_standings([p1, p2, p3])

    out = capsys.readouterr().out
    assert "1. B" in out
    assert "[JAILED]" in out


def test_print_board_ownership_with_owner_and_mortgage(capsys):
    owner = SimpleNamespace(name="Owner")
    board = SimpleNamespace(
        properties=[
            _DummyProperty("One", 1, 100, 10, owner=owner, mortgaged=True),
            _DummyProperty("Two", 3, 120, 12, owner=None, mortgaged=False),
        ]
    )

    ui.print_board_ownership(board)

    out = capsys.readouterr().out
    assert "Property Register" in out
    assert "*Owner" in out
    assert "---" in out


@pytest.mark.parametrize(
    "amount,expected",
    [
        (0, "$0"),
        (1500, "$1,500"),
        (-30, "$-30"),
    ],
)
def test_format_currency(amount, expected):
    assert ui.format_currency(amount) == expected


def test_safe_int_input_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "42")
    assert ui.safe_int_input("prompt", default=7) == 42


@pytest.mark.parametrize("typed", ["abc", "", "7.2"])
def test_safe_int_input_invalid_returns_default(monkeypatch, typed):
    monkeypatch.setattr("builtins.input", lambda *_: typed)
    assert ui.safe_int_input("prompt", default=9) == 9


@pytest.mark.parametrize(
    "typed,expected",
    [
        ("y", True),
        ("Y", True),
        ("n", False),
        ("yes", False),
    ],
)
def test_confirm_variants(monkeypatch, typed, expected):
    monkeypatch.setattr("builtins.input", lambda *_: typed)
    assert ui.confirm("?") is expected
