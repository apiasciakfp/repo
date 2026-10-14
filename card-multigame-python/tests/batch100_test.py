"""Port of Java Batch100Test — Strategy / FactoryMethod / NullObject.

(t108 needs GuessACardGame and lands in Slice 4.)
"""

from cardmultigame.entities.cards.card import Card
from cardmultigame.entities.cards.create_cards import CreateCards
from cardmultigame.entities.decks.card_deck import CardDeck
from cardmultigame.entities.decks.create_card_deck import CreateCardDeck
from cardmultigame.technical.parsers.selected_parser import SelectedParser
from cardmultigame.technical.rangens.always_first_selector import AlwaysFirstSelector
from cardmultigame.technical.rangens.always_last_selector import AlwaysLastSelector
from cardmultigame.usecases.cardcomparison.black_red_colour_only_comparison_strategy import (
    BlackRedColourOnlyComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.colour_card_comparison_strategy import (
    ColourCardComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.create_card_comparison_strategy import (
    CreateCardComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.rank_card_comparison_strategy import (
    RankCardComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.strict_card_comparison_strategy import (
    StrictCardComparisonStrategy,
)


def test_t101_strategy_basics():
    card1 = Card("J", "H")
    identical_card = Card("J", "H")
    different_card = Card("K", "H")
    assert StrictCardComparisonStrategy().are_the_same(card1, identical_card) is True
    assert StrictCardComparisonStrategy().are_the_same(card1, different_card) is False


def test_t102_implement_your_own_strategy():
    card1 = Card("J", "H")
    identical_card = Card("2", "H")
    different_card = Card("J", "D")
    assert ColourCardComparisonStrategy().are_the_same(card1, identical_card) is True
    assert ColourCardComparisonStrategy().are_the_same(card1, different_card) is False


def test_t103_implement_the_black_red_strategy():
    reference = Card("2", "H")
    identical1 = Card("2", "H")
    identical2 = Card("7", "D")
    different1 = Card("2", "S")
    different2 = Card("Q", "C")
    assert BlackRedColourOnlyComparisonStrategy().are_the_same(reference, identical1) is True
    assert BlackRedColourOnlyComparisonStrategy().are_the_same(reference, identical2) is True
    assert BlackRedColourOnlyComparisonStrategy().are_the_same(reference, different1) is False
    assert BlackRedColourOnlyComparisonStrategy().are_the_same(reference, different2) is False


def test_t104_power_of_polymorphism():
    card1 = Card("J", "H")
    card2 = Card("A", "H")
    assert StrictCardComparisonStrategy().are_the_same(card1, card2) is False
    assert ColourCardComparisonStrategy().are_the_same(card1, card2) is True
    assert RankCardComparisonStrategy().are_the_same(card1, card2) is False
    assert BlackRedColourOnlyComparisonStrategy().are_the_same(card1, card2) is True


def test_t105_factory_method_one_strategy_only():
    card1 = Card("J", "H")
    card2 = Card("A", "H")
    strategy = CreateCardComparisonStrategy().create("colour")
    assert strategy.are_the_same(card1, card2) is True


def test_t106_factory_method_all_strategies():
    card1 = Card("J", "H")
    card2 = Card("A", "H")
    assert CreateCardComparisonStrategy().create("strict").are_the_same(card1, card2) is False
    assert CreateCardComparisonStrategy().create("colour").are_the_same(card1, card2) is True
    assert CreateCardComparisonStrategy().create("rank").are_the_same(card1, card2) is False
    assert CreateCardComparisonStrategy().create("blackred").are_the_same(card1, card2) is True


def test_t107_null_object_we_all_love():
    card1 = Card("J", "H")
    card2 = Card("A", "H")
    strategies = [
        CreateCardComparisonStrategy().create("THIS IS A TYPO!"),
        CreateCardComparisonStrategy().create(""),
        CreateCardComparisonStrategy().create("al/fdkafklfhflsdhflhffhfh"),
        CreateCardComparisonStrategy().create("f;lff;kklfs;df"),
        CreateCardComparisonStrategy().create("don't else-if those cases please..."),
    ]
    for strategy in strategies:
        assert strategy.are_the_same(card1, card2) is False


def test_t109_card_deck_needs_different_creation_ways():
    low_card = Card("2", "C")
    high_card = Card("K", "H")

    deck = CreateCardDeck().simple2_to_a_with_4_colours()
    all_cards = deck.all_cards()

    found_small = False
    found_large = False
    for card in all_cards:
        if StrictCardComparisonStrategy().are_the_same(card, low_card):
            found_small = True
        if StrictCardComparisonStrategy().are_the_same(card, high_card):
            found_large = True

    assert found_small is True
    assert found_large is True


def test_t110_parsers_of_course_parsers():
    # Case 1: ';' main, ',' secondary
    expected = [
        ("Play", "GuessACard"),
        ("SetDeck", "JH, QH, KH"),
        ("StartGame", ""),
        ("Guess", "JH"),
        ("Guess", "QH"),
    ]
    received = SelectedParser().properly_parse(
        "Play GuessACard; SetDeck JH, QH, KH; StartGame; Guess JH; Guess QH"
    )
    assert received == expected

    # Case 2: ',' main, ';' secondary
    expected = [
        ("Play", "GuessACard"),
        ("SetDeck", "JH; QH; KH"),
        ("StartGame", ""),
        ("Guess", "JH"),
        ("Guess", "QH"),
    ]
    received = SelectedParser().properly_parse(
        "Play GuessACard, SetDeck JH; QH; KH, StartGame, Guess JH, Guess QH"
    )
    assert received == expected

    # Case 3: '-' main, ',' secondary
    expected = [
        ("Play", "GuessACard"),
        ("SetDeck", "JH, QH, KH"),
        ("StartGame", ""),
        ("Guess", "JH"),
        ("Guess", "QH"),
    ]
    received = SelectedParser().properly_parse(
        "Play GuessACard - SetDeck JH, QH, KH - StartGame - Guess JH - Guess QH"
    )
    assert received == expected


def test_t111_card_deck_can_have_configured_random_generator_first():
    selector = AlwaysFirstSelector()
    expected_cards = CreateCards().create_collection("9H, 10H, 9C, 10C, AD")
    copied_list = list(expected_cards)
    deck = CardDeck(selector, copied_list)

    actual_cards = []
    for _ in range(5):
        actual_cards.append(deck.draw_random_card())

    for i in range(5):
        assert expected_cards[i].colour == actual_cards[i].colour
        assert expected_cards[i].rank == actual_cards[i].rank


def test_t112_card_deck_can_have_configured_random_generator_last():
    selector = AlwaysLastSelector()
    expected_cards = CreateCards().create_collection("9H, 10H, 9C, 10C, AD")
    copied_list = list(expected_cards)
    deck = CardDeck(selector, copied_list)

    actual_cards = []
    for _ in range(5):
        actual_cards.append(deck.draw_random_card())

    for i in range(5):
        assert expected_cards[4 - i].colour == actual_cards[i].colour
        assert expected_cards[4 - i].rank == actual_cards[i].rank


def test_t113_card_deck_factory_can_reconfigure_random_generator():
    input_card_sigils = "JS, QH, KD, AC"
    expected_cards = CreateCards().create_collection(input_card_sigils)

    creator = CreateCardDeck()

    creator.set_card_selector(AlwaysFirstSelector())
    deck_with_always_first = creator.from_given_cards(input_card_sigils)

    actual_first_cards = []
    for _ in range(4):
        actual_first_cards.append(deck_with_always_first.draw_random_card())

    for i in range(4):
        assert expected_cards[i].colour == actual_first_cards[i].colour
        assert expected_cards[i].rank == actual_first_cards[i].rank

    creator.set_card_selector(AlwaysLastSelector())
    deck_with_always_last = creator.from_given_cards(input_card_sigils)

    actual_last_cards = []
    for _ in range(4):
        actual_last_cards.append(deck_with_always_last.draw_random_card())

    for i in range(4):
        assert expected_cards[3 - i].colour == actual_last_cards[i].colour
        assert expected_cards[3 - i].rank == actual_last_cards[i].rank


def test_t108_lets_prepare_the_strategy_for_the_future():
    from cardmultigame.entities.games.guessing.guess_a_card_game import GuessACardGame

    selected_strategy = GuessACardGame().card_comparison_strategy()
    assert isinstance(selected_strategy, StrictCardComparisonStrategy)
