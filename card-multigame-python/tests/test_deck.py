"""Port of Java TestDeck."""

from cardmultigame.entities.cards.create_cards import CreateCards
from cardmultigame.entities.decks.create_card_deck import CreateCardDeck
from cardmultigame.usecases.cardcomparison.strict_card_comparison_strategy import (
    StrictCardComparisonStrategy,
)


def test_draw_card_from_deck_randomly_5_cards_until_0_left():
    card_sigils = ["9H", "10H", "JH", "QH", "KH"]
    separator = ","
    cards_in_deck = separator.join(card_sigils)

    cards = CreateCards().create_collection(cards_in_deck)
    deck = CreateCardDeck().from_given_cards(cards_in_deck)

    length_in_deck = 0
    length_of_drawn_cards = len(cards)

    drawn_cards = []
    for _ in range(len(card_sigils)):
        drawn_cards.append(deck.draw_random_card())

    cards_remaining = deck.all_cards()

    assert len(cards_remaining) == length_in_deck
    assert len(drawn_cards) == length_of_drawn_cards


def test_create_deck_with_standard_cards_9_to_a_with_4_colours():
    card_count_expected = 24
    deck = CreateCardDeck().simple9_to_a_with_4_colours()
    cards_received = deck.all_cards()
    assert len(cards_received) == card_count_expected


def test_create_deck_with_3_set_cards_in_comma_format():
    cards = ["JH", "QH", "KH"]
    separator = ","
    cards_in_deck = separator.join(cards)

    cards_expected = CreateCards().create_collection(cards_in_deck)
    deck = CreateCardDeck().from_given_cards(cards_in_deck)
    cards_received = deck.all_cards()

    assert len(cards_expected) == len(cards_received)
    for i in range(len(cards_expected)):
        assert (
            StrictCardComparisonStrategy().are_the_same(cards_expected[i], cards_received[i]) is True
        )
