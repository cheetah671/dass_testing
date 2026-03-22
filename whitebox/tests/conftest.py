"""Shared pytest fixtures for MoneyPoly white-box tests."""

from pathlib import Path
import sys

import pytest


# Ensure tests can import the package regardless of pytest invocation cwd.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PROJECT_ROOT / "moneypoly" / "moneypoly"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from moneypoly.game import Game


@pytest.fixture
def game_two_players():
    """Create a deterministic 2-player game fixture."""
    return Game(["Alice", "Bob"])


@pytest.fixture
def sample_property(game_two_players):
    """Return a purchasable board property from the game fixture."""
    return game_two_players.board.properties[0]
