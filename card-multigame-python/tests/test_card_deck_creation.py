"""CardDeck creation (CreateCardDeck factories) and core CardDeck behaviour."""

from cardmultigame.entities.cards.card import Card
from cardmultigame.entities.decks.create_card_deck import CreateCardDeck
from cardmultigame.technical.rangens.always_first_selector import AlwaysFirstSelector
from cardmultigame.technical.rangens.always_last_selector import AlwaysLastSelector

ALL_COLOURS = ["S", "H", "D", "C"]


def _sigils(cards: list[Card]) -> list[str]:
    return [card.rank + card.colour for card in cards]


# --- Creation -----------------------------------------------------------------


def test_simple9_to_a_deck_holds_every_rank_9_to_a_in_every_colour_exactly_once():
    # Arrange
    ranks = ["9", "10", "J", "Q", "K", "A"]
    expected = sorted(rank + colour for rank in ranks for colour in ALL_COLOURS)

    # Act
    deck = CreateCardDeck().simple9_to_a_with_4_colours()

    # Assert
    assert deck.cards_left() == 24
    assert sorted(_sigils(deck.all_cards())) == expected


def test_simple2_to_a_deck_is_a_full_52_card_deck_without_duplicates():
    # Arrange
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    expected = sorted(rank + colour for rank in ranks for colour in ALL_COLOURS)

    # Act
    deck = CreateCardDeck().simple2_to_a_with_4_colours()

    # Assert
    assert deck.cards_left() == 52
    assert sorted(_sigils(deck.all_cards())) == expected


def test_empty_deck_has_no_cards():
    # Arrange
    factory = CreateCardDeck()

    # Act
    deck = factory.empty()

    # Assert
    assert deck.cards_left() == 0
    assert deck.all_cards() == []


def test_deck_from_given_cards_keeps_the_cards_in_the_given_order():
    # Arrange
    cards_in_deck = "KH, 2C, 10D, AS"

    # Act
    deck = CreateCardDeck().from_given_cards(cards_in_deck)

    # Assert
    assert _sigils(deck.all_cards()) == ["KH", "2C", "10D", "AS"]


def test_deck_from_given_cards_accepts_semicolon_and_space_separated_cards():
    # Arrange
    semicolon_separated = "JH; QH; KH"
    space_separated = "JH QH KH"

    # Act
    semicolon_deck = CreateCardDeck().from_given_cards(semicolon_separated)
    space_deck = CreateCardDeck().from_given_cards(space_separated)

    # Assert
    assert _sigils(semicolon_deck.all_cards()) == ["JH", "QH", "KH"]
    assert _sigils(space_deck.all_cards()) == ["JH", "QH", "KH"]


def test_deck_from_given_cards_skips_tokens_that_are_not_cards():
    # Arrange
    cards_in_deck = "JH, XX, 1H, 11S, QZ, QH"

    # Act
    deck = CreateCardDeck().from_given_cards(cards_in_deck)

    # Assert
    assert _sigils(deck.all_cards()) == ["JH", "QH"]


def test_deck_from_text_without_any_card_is_empty():
    # Arrange
    cards_in_deck = "no cards here"

    # Act
    deck = CreateCardDeck().from_given_cards(cards_in_deck)

    # Assert
    assert deck.cards_left() == 0


def test_each_created_deck_is_independent_of_other_created_decks():
    # Arrange
    factory = CreateCardDeck()
    first_deck = factory.simple9_to_a_with_4_colours()
    second_deck = factory.simple9_to_a_with_4_colours()

    # Act
    first_deck.draw_random_card()

    # Assert
    assert first_deck.cards_left() == 23
    assert second_deck.cards_left() == 24

    # Cleanup
    del first_deck, second_deck



def test_deck_created_after_setting_a_selector_draws_with_that_selector():
    # Arrange
    factory = CreateCardDeck()
    factory.set_card_selector(AlwaysLastSelector())
    deck = factory.from_given_cards("9H, 10H, JH")

    # Act
    drawn = deck.draw_random_card()

    # Assert
    assert drawn.rank + drawn.colour == "JH"

    # Cleanup
    del deck



# --- Behaviour ----------------------------------------------------------------


def test_drawing_a_card_removes_exactly_that_card_from_the_deck():
    # Arrange
    factory = CreateCardDeck()
    factory.set_card_selector(AlwaysFirstSelector())
    deck = factory.from_given_cards("9H, 10H, JH")

    # Act
    drawn = deck.draw_random_card()

    # Assert
    assert drawn.rank + drawn.colour == "9H"
    assert _sigils(deck.all_cards()) == ["10H", "JH"]
    assert deck.cards_left() == 2

    # Cleanup
    del deck



def test_drawing_the_whole_deck_randomly_yields_every_card_exactly_once():
    # Arrange
    deck = CreateCardDeck().simple9_to_a_with_4_colours()
    expected = sorted(_sigils(deck.all_cards()))

    # Act
    drawn = [deck.draw_random_card() for _ in range(24)]

    # Assert
    assert sorted(_sigils(drawn)) == expected
    assert deck.cards_left() == 0

    # Cleanup
    del deck



def test_added_card_is_the_one_drawn_as_last_added():
    # Arrange
    deck = CreateCardDeck().from_given_cards("9H, 10H")
    queen_of_hearts = Card("Q", "H")

    # Act
    deck.add_a_single_card(queen_of_hearts)
    count_after_adding = deck.cards_left()
    drawn = deck.draw_last_added_card()

    # Assert
    assert count_after_adding == 3
    assert drawn is queen_of_hearts
    assert _sigils(deck.all_cards()) == ["9H", "10H"]

    # Cleanup
    del deck



def test_adding_a_card_to_an_empty_deck_makes_it_drawable():
    # Arrange
    deck = CreateCardDeck().empty()

    # Act
    deck.add_a_single_card(Card("A", "S"))
    drawn = deck.draw_random_card()

    # Assert
    assert drawn.rank + drawn.colour == "AS"
    assert deck.cards_left() == 0

    # Cleanup
    del deck



def test_deck_text_lists_every_card_in_order():
    # Arrange
    deck = CreateCardDeck().from_given_cards("9H, AS")

    # Act
    text = str(deck)

    # Assert
    assert text == "Deck: ||r: 9 c: H||r: A c: S"
