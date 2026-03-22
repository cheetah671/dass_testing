"""White-box unit tests for card deck behaviors."""

from moneypoly.cards import CardDeck, CHANCE_CARDS, COMMUNITY_CHEST_CARDS


def test_draw_cycles_through_deck():
    """Draw should loop back to start after reaching end of deck."""
    deck = CardDeck([{"id": 1}, {"id": 2}])

    assert deck.draw()["id"] == 1
    assert deck.draw()["id"] == 2
    assert deck.draw()["id"] == 1


def test_peek_does_not_advance_index():
    """peek should show next card without changing draw order."""
    deck = CardDeck([{"id": 10}, {"id": 20}])

    assert deck.peek()["id"] == 10
    assert deck.peek()["id"] == 10
    assert deck.draw()["id"] == 10


def test_empty_deck_draw_and_peek_return_none():
    """Empty deck should safely return None for draw and peek."""
    deck = CardDeck([])

    assert deck.draw() is None
    assert deck.peek() is None


def test_reshuffle_resets_index(monkeypatch):
    """reshuffle should call random.shuffle and reset index to 0."""
    called = {"value": False}

    def fake_shuffle(values):
        called["value"] = True
        values.reverse()

    monkeypatch.setattr("moneypoly.cards.random.shuffle", fake_shuffle)

    deck = CardDeck([{"id": 1}, {"id": 2}, {"id": 3}])
    deck.draw()
    deck.draw()
    assert deck.index == 2

    deck.reshuffle()

    assert called["value"] is True
    assert deck.index == 0


def test_cards_remaining_before_and_after_wrap():
    """cards_remaining should track remaining cards until cycle point."""
    deck = CardDeck([{"id": 1}, {"id": 2}, {"id": 3}])

    assert deck.cards_remaining() == 3
    deck.draw()
    assert deck.cards_remaining() == 2
    deck.draw()
    assert deck.cards_remaining() == 1
    deck.draw()
    assert deck.cards_remaining() == 3


def test_len_and_repr_reflect_deck_state():
    """Magic methods should expose card count and next index state."""
    deck = CardDeck([{"id": 1}, {"id": 2}])
    deck.draw()

    assert len(deck) == 2
    assert "CardDeck(2 cards" in repr(deck)


def test_chance_cards_have_required_fields():
    """Chance card definitions should include description/action/value."""
    for card in CHANCE_CARDS:
        assert "description" in card
        assert "action" in card
        assert "value" in card


def test_community_chest_cards_have_required_fields():
    """Community Chest cards should include description/action/value."""
    for card in COMMUNITY_CHEST_CARDS:
        assert "description" in card
        assert "action" in card
        assert "value" in card
