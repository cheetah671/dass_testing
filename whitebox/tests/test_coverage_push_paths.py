"""Targeted tests to maximize branch and line coverage without fixing app code."""

from pathlib import Path
from types import SimpleNamespace
import builtins
import runpy

import pytest

from moneypoly.bank import Bank
from moneypoly.board import Board
from moneypoly.dice import Dice
from moneypoly.game import Game
from moneypoly.property import Property, PropertyGroup


def _module_path(filename):
    return Path(__file__).resolve().parents[1] / "moneypoly" / "moneypoly" / "moneypoly" / filename


def _run_with_blocked_import(monkeypatch, blocked_names, filename):
    original_import = builtins.__import__

    def fake_import(name, globals_=None, locals_=None, fromlist=(), level=0):
        if name in blocked_names:
            raise ModuleNotFoundError(name)
        return original_import(name, globals_, locals_, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    return runpy.run_path(str(_module_path(filename)))


def test_bank_fallback_import_branch_executes(monkeypatch):
    module_globals = _run_with_blocked_import(
        monkeypatch,
        {"moneypoly.config"},
        "bank.py",
    )
    assert "Bank" in module_globals


def test_player_fallback_import_branch_executes(monkeypatch):
    module_globals = _run_with_blocked_import(
        monkeypatch,
        {"moneypoly.config"},
        "player.py",
    )
    assert "Player" in module_globals


def test_board_fallback_import_branch_executes(monkeypatch):
    module_globals = _run_with_blocked_import(
        monkeypatch,
        {"moneypoly.config"},
        "board.py",
    )
    assert "Board" in module_globals


def test_game_fallback_import_branch_executes(monkeypatch):
    module_globals = _run_with_blocked_import(
        monkeypatch,
        {"moneypoly"},
        "game.py",
    )
    assert "Game" in module_globals


def test_bank_summary_prints_all_lines(capsys):
    bank = Bank()
    bank.collect(100)
    bank.summary()
    out = capsys.readouterr().out
    assert "Bank reserves" in out
    assert "Total collected" in out
    assert "Loans issued" in out


def test_board_repr_includes_owned_count():
    board = Board()
    board.properties[0].owner = object()
    text = repr(board)
    assert "properties" in text
    assert "owned" in text


def test_dice_repr_contains_faces_and_streak():
    dice = Dice()
    dice.die1 = 2
    dice.die2 = 5
    dice.doubles_streak = 1
    assert "die1=2" in repr(dice)
    assert "streak=1" in repr(dice)


def test_property_get_rent_base_path_returns_base_rent():
    group = PropertyGroup("G", "blue")
    prop = Property("A", 1, 100, 10, group)
    prop.owner = None
    assert prop.get_rent() == 10


def test_property_repr_with_named_owner():
    prop = Property("A", 1, 100, 10)
    prop.owner = SimpleNamespace(name="Owner")
    text = repr(prop)
    assert "Owner" in text


def test_pay_rent_returns_when_owner_none(monkeypatch):
    game = Game(["A", "B"])
    prop = game.board.properties[0]
    prop.owner = None

    deducted = {"called": False}
    monkeypatch.setattr(game.players[0], "deduct_money", lambda *_: deducted.__setitem__("called", True))

    game.pay_rent(game.players[0], prop)

    assert deducted["called"] is False


def test_auction_property_branch_cannot_afford_bid(monkeypatch, capsys):
    game = Game(["A"])
    prop = game.board.properties[0]
    game.players[0].balance = 10

    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: 999)

    game.auction_property(prop)

    out = capsys.readouterr().out
    assert "cannot afford" in out


def test_handle_jail_turn_pay_fine_branch(monkeypatch):
    game = Game(["A", "B"])
    player = game.players[0]
    player.in_jail = True

    monkeypatch.setattr("moneypoly.ui.confirm", lambda *_: True)
    monkeypatch.setattr(game.dice, "roll", lambda: 4)
    monkeypatch.setattr(game.dice, "describe", lambda: "2 + 2 = 4")

    moved = {"count": 0}
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_: moved.__setitem__("count", moved["count"] + 1))

    game._handle_jail_turn(player)

    assert player.in_jail is False
    assert moved["count"] == 1


def test_check_bankruptcy_resets_current_index_when_needed():
    game = Game(["A", "B"])
    player = game.players[1]
    player.balance = 0
    game.current_index = 1

    game._check_bankruptcy(player)

    assert game.current_index == 0


def test_run_enters_loop_and_prints_standings(monkeypatch):
    game = Game(["A", "B"])

    play_calls = {"count": 0}
    standings_calls = {"count": 0}

    def fake_play_turn():
        play_calls["count"] += 1
        game.running = False

    monkeypatch.setattr(game, "play_turn", fake_play_turn)
    monkeypatch.setattr("moneypoly.ui.print_standings", lambda *_: standings_calls.__setitem__("count", standings_calls["count"] + 1))

    game.run()

    assert play_calls["count"] == 1
    assert standings_calls["count"] == 1


def test_interactive_menu_break_line_executed(monkeypatch):
    game = Game(["A", "B"])
    player = game.players[0]

    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: 0)

    game.interactive_menu(player)


def test_interactive_menu_loan_positive_calls_bank(monkeypatch):
    game = Game(["A", "B"])
    player = game.players[0]

    values = iter([6, 120, 0])
    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: next(values))

    called = {"count": 0}
    monkeypatch.setattr(game.bank, "give_loan", lambda *_: called.__setitem__("count", called["count"] + 1))

    game.interactive_menu(player)

    assert called["count"] == 1


def test_interactive_menu_loan_zero_does_not_call_bank(monkeypatch):
    game = Game(["A", "B"])
    player = game.players[0]

    values = iter([6, 0, 0])
    monkeypatch.setattr("moneypoly.ui.safe_int_input", lambda *_args, **_kwargs: next(values))

    called = {"count": 0}
    monkeypatch.setattr(game.bank, "give_loan", lambda *_: called.__setitem__("count", called["count"] + 1))

    game.interactive_menu(player)

    assert called["count"] == 0
