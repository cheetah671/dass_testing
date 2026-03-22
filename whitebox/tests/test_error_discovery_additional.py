"""Additional error-discovery tests to expand failing-case inventory before fixes."""

import pytest

from moneypoly.bank import Bank
from moneypoly.dice import Dice
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup


def test_error_discovery_collect_negative_should_not_change_funds():
    """Expected behavior: negative collect should be ignored."""
    bank = Bank()
    start = bank.get_balance()

    bank.collect(-5)

    assert bank.get_balance() == start


def test_error_discovery_loan_should_reduce_bank_balance():
    """Expected behavior: loan transfer should reduce bank reserves."""
    bank = Bank()
    player = Player("L")
    start = bank.get_balance()

    bank.give_loan(player, 10)

    assert bank.get_balance() == start - 10


def test_error_discovery_dice_should_use_six_sided_bounds(monkeypatch):
    """Expected behavior: randint bounds should be 1..6."""
    calls = []

    def fake_randint(low, high):
        calls.append((low, high))
        return 1

    monkeypatch.setattr("moneypoly.dice.random.randint", fake_randint)

    Dice().roll()

    assert calls == [(1, 6), (1, 6)]


def test_error_discovery_move_past_go_should_grant_salary():
    """Expected behavior: passing GO should grant salary even if not landing on 0."""
    player = Player("M")
    player.position = 38
    start = player.balance

    player.move(4)

    assert player.balance == start + 200


def test_error_discovery_group_full_ownership_requires_all_properties():
    """Expected behavior: all_owned_by should be false for partial ownership."""
    group = PropertyGroup("G", "blue")
    owner = object()
    p1 = Property("A", 1, 100, 10, group)
    Property("B", 2, 100, 10, group)
    Property("C", 3, 100, 10, group)
    p1.owner = owner

    assert group.all_owned_by(owner) is False


def test_control_pay_out_insufficient_still_raises():
    """Control pass: payout over reserves should raise ValueError."""
    bank = Bank()
    with pytest.raises(ValueError):
        bank.pay_out(bank.get_balance() + 99)


def test_control_mortgaged_property_still_skips_rent():
    """Control pass: mortgaged property should still skip rent."""
    game = Game(["A", "B"])
    owner, tenant = game.players
    prop = game.board.properties[0]
    prop.owner = owner
    owner.add_property(prop)
    prop.is_mortgaged = True

    owner_start = owner.balance
    tenant_start = tenant.balance

    game.pay_rent(tenant, prop)

    assert owner.balance == owner_start
    assert tenant.balance == tenant_start


def test_control_find_winner_with_empty_players_returns_none():
    """Control pass: no players should produce no winner."""
    game = Game(["A"])
    game.players = []

    assert game.find_winner() is None


def test_control_move_landing_on_go_still_awards_salary():
    """Control pass: exact GO landing salary behavior remains correct."""
    player = Player("S")
    player.position = 39
    start = player.balance

    player.move(1)

    assert player.balance == start + 200


def test_control_all_owned_by_none_owner_is_false():
    """Control pass: None owner must return false."""
    group = PropertyGroup("G2", "red")
    Property("X", 11, 120, 10, group)

    assert group.all_owned_by(None) is False
