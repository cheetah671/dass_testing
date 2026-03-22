"""White-box unit tests for Property and PropertyGroup rules."""

import pytest

from moneypoly.property import Property, PropertyGroup


def test_property_registers_itself_with_group_on_creation():
    """Property constructor should append itself to group when provided."""
    group = PropertyGroup("Test", "blue")
    prop = Property("A", 1, 100, 10, group)

    assert prop in group.properties


def test_get_rent_returns_zero_when_mortgaged():
    """Mortgaged property should not charge rent."""
    prop = Property("A", 1, 100, 10)
    prop.is_mortgaged = True

    assert prop.get_rent() == 0


def test_get_rent_doubles_with_full_group_ownership():
    """Rent should double when owner has full group."""
    group = PropertyGroup("Test", "blue")
    owner = object()
    p1 = Property("A", 1, 100, 10, group)
    p2 = Property("B", 2, 100, 10, group)
    p1.owner = owner
    p2.owner = owner

    assert p1.get_rent() == 20


def test_mortgage_first_time_and_repeat_call():
    """First mortgage should pay out; second should return zero."""
    prop = Property("A", 1, 120, 10)
    first = prop.mortgage()
    second = prop.mortgage()

    assert first == 60
    assert second == 0


def test_unmortgage_clears_flag_and_returns_cost():
    """Unmortgaging should return 110% of mortgage value and clear mortgage flag."""
    prop = Property("A", 1, 100, 10)
    prop.mortgage()

    cost = prop.unmortgage()

    assert cost == 55
    assert prop.is_mortgaged is False


def test_unmortgage_returns_zero_when_not_mortgaged():
    """Unmortgage on non-mortgaged property should return zero."""
    prop = Property("A", 1, 100, 10)
    assert prop.unmortgage() == 0


@pytest.mark.parametrize(
    "owner,is_mortgaged,expected",
    [
        (None, False, True),
        (object(), False, False),
        (None, True, False),
        (object(), True, False),
    ],
)
def test_is_available_combinations(owner, is_mortgaged, expected):
    """Availability should depend on both owner and mortgage state."""
    prop = Property("A", 1, 100, 10)
    prop.owner = owner
    prop.is_mortgaged = is_mortgaged

    assert prop.is_available() is expected


def test_add_property_links_group_both_ways():
    """add_property should update both group list and property.group."""
    group = PropertyGroup("Test", "blue")
    prop = Property("A", 1, 100, 10)

    group.add_property(prop)

    assert prop in group.properties
    assert prop.group is group


def test_all_owned_by_requires_full_group_ownership():
    """Group ownership should be true only when every property has the same owner."""
    group = PropertyGroup("Test", "blue")
    owner = object()
    p1 = Property("A", 1, 100, 10, group)
    Property("B", 2, 100, 10, group)

    p1.owner = owner

    assert group.all_owned_by(owner) is False


def test_all_owned_by_rejects_none_owner():
    """None owner should never count as full ownership."""
    group = PropertyGroup("Test", "blue")
    Property("A", 1, 100, 10, group)

    assert group.all_owned_by(None) is False


def test_owner_counts_and_group_size():
    """Owner count aggregation and size should reflect group composition."""
    group = PropertyGroup("Test", "blue")
    owner_a = object()
    owner_b = object()
    p1 = Property("A", 1, 100, 10, group)
    p2 = Property("B", 2, 100, 10, group)
    p3 = Property("C", 3, 100, 10, group)
    p1.owner = owner_a
    p2.owner = owner_a
    p3.owner = owner_b

    counts = group.get_owner_counts()

    assert counts[owner_a] == 2
    assert counts[owner_b] == 1
    assert group.size() == 3
