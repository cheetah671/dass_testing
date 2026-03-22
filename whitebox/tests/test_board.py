"""White-box unit tests for board tile and ownership logic."""

import pytest

from moneypoly.board import Board
from moneypoly.property import Property


@pytest.mark.parametrize(
    "position,expected",
    [
        (0, "go"),
        (2, "community_chest"),
        (4, "income_tax"),
        (5, "railroad"),
        (7, "chance"),
        (10, "jail"),
        (17, "community_chest"),
        (20, "free_parking"),
        (22, "chance"),
        (30, "go_to_jail"),
        (33, "community_chest"),
        (38, "luxury_tax"),
    ],
)
def test_get_tile_type_for_special_tiles(position, expected):
    """Special board positions should map to known tile names."""
    board = Board()
    assert board.get_tile_type(position) == expected


@pytest.mark.parametrize("position", [1, 3, 11])
def test_get_tile_type_returns_property_for_property_positions(position):
    """Known property positions should return 'property'."""
    board = Board()
    assert board.get_tile_type(position) == "property"


@pytest.mark.parametrize("position", [12, 28])
def test_get_tile_type_returns_blank_for_non_special_non_property(position):
    """Non-special positions without properties should be blank."""
    board = Board()
    assert board.get_tile_type(position) == "blank"


@pytest.mark.parametrize(
    "position,expected",
    [
        (0, True),
        (12, False),
        (30, True),
    ],
)
def test_is_special_tile(position, expected):
    """is_special_tile should follow SPECIAL_TILES mapping."""
    board = Board()
    assert board.is_special_tile(position) is expected


@pytest.mark.parametrize("position", [1, 39, 24])
def test_get_property_at_finds_property_by_position(position):
    """get_property_at should return the matching Property object."""
    board = Board()
    prop = board.get_property_at(position)
    assert isinstance(prop, Property)
    assert prop.position == position


def test_get_property_at_returns_none_for_missing_position():
    """No property should be returned for blank tile positions."""
    board = Board()
    assert board.get_property_at(12) is None


def test_is_purchasable_true_for_unowned_non_mortgaged_property():
    """Fresh property should be purchasable."""
    board = Board()
    assert board.is_purchasable(1) is True


def test_is_purchasable_false_for_non_property_position():
    """Non-property tile should not be purchasable."""
    board = Board()
    assert board.is_purchasable(12) is False


def test_is_purchasable_false_for_mortgaged_property():
    """Mortgaged property should not be marked purchasable."""
    board = Board()
    prop = board.get_property_at(1)
    prop.is_mortgaged = True

    assert board.is_purchasable(1) is False


def test_is_purchasable_false_for_owned_property():
    """Owned property should not be purchasable."""
    board = Board()
    prop = board.get_property_at(1)
    prop.owner = object()

    assert board.is_purchasable(1) is False


def test_properties_owned_by_returns_only_matching_owner_properties():
    """Ownership listing should include all and only player's properties."""
    board = Board()
    owner_a = object()
    owner_b = object()
    p1 = board.get_property_at(1)
    p2 = board.get_property_at(3)
    p3 = board.get_property_at(6)
    p1.owner = owner_a
    p2.owner = owner_a
    p3.owner = owner_b

    owned = board.properties_owned_by(owner_a)

    assert p1 in owned
    assert p2 in owned
    assert p3 not in owned


def test_unowned_properties_excludes_owned_tiles():
    """Unowned property list should shrink after ownership assignment."""
    board = Board()
    start_count = len(board.unowned_properties())
    board.get_property_at(1).owner = object()

    assert len(board.unowned_properties()) == start_count - 1
