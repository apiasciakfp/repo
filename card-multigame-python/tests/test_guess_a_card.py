"""Port of Java TestGuessACard — full game flow via the string/REPL construction path."""

from cardmultigame.gamemanagers.create_game_manager import CreateGameManager
from cardmultigame.usecases.influencestate.query_game_state import QueryGameState


def test_direct_card_guessing_works_for_three_cards_deck_failure():
    cards = ["JH", "QH", "KH"]
    card_outside_deck = "2C"
    second_separator = ","
    cards_in_deck = second_separator.join(cards)

    orders = (
        "Play GuessACard; SetDeck " + cards_in_deck + "; SetMaxTurns 3; "
        "Guess " + card_outside_deck + "; Guess " + card_outside_deck + "; Guess " + card_outside_deck
    )

    gm = CreateGameManager().defaults_with_orders(orders)
    gm.execute_orders(orders)
    result_received = gm.current_state()

    assert QueryGameState.game_undergoing(result_received) == "Defeat"
    assert QueryGameState.maximum_turns(result_received) == QueryGameState.current_turn(
        result_received
    )
    assert QueryGameState.amount_of_cards_left(result_received) == 0


def test_direct_card_guessing_works_for_three_cards_deck_failure_diff_separators():
    cards = ["JH", "QH", "KH"]
    card_outside_deck = "2C"
    second_separator = ";"
    cards_in_deck = second_separator.join(cards)

    orders = (
        "Play GuessACard, SetDeck " + cards_in_deck + ", SetMaxTurns 3, "
        "Guess " + card_outside_deck + ", Guess " + card_outside_deck + ", Guess " + card_outside_deck
    )

    gm = CreateGameManager().defaults_with_orders(orders)
    gm.execute_orders(orders)
    result_received = gm.current_state()

    assert QueryGameState.game_undergoing(result_received) == "Defeat"
    assert QueryGameState.maximum_turns(result_received) == QueryGameState.current_turn(
        result_received
    )
    assert QueryGameState.amount_of_cards_left(result_received) == 0


def test_direct_card_guessing_works_for_three_cards_deck_victory():
    cards = ["JH", "QH", "KH"]
    card_inside_deck = "JH"
    second_separator = ","
    cards_in_deck = second_separator.join(cards)

    orders = (
        "Play GuessACard; SetDeck " + cards_in_deck + "; SetMaxTurns 3; "
        "Guess " + card_inside_deck + "; Guess " + card_inside_deck + "; Guess " + card_inside_deck
    )

    gm = CreateGameManager().defaults_with_orders(orders)
    gm.execute_orders(orders)
    result_received = gm.current_state()

    assert QueryGameState.game_undergoing(result_received) == "Victory"


def test_card_red_black_guessing_works_for_three_cards_one_colour_deck_miss_miss_victory():
    cards = ["JH", "QH", "KH"]
    card_outside_deck = "2C"
    card_inside_deck = "2D"
    second_separator = ","
    cards_in_deck = second_separator.join(cards)

    orders = (
        "Play GuessACard; SetDeck " + cards_in_deck + "; GameVariant RedBlack; "
        "Guess " + card_outside_deck + "; Guess " + card_outside_deck + "; Guess " + card_inside_deck
    )

    gm = CreateGameManager().defaults_with_orders(orders)
    gm.execute_orders(orders)
    result_received = gm.current_state()

    assert QueryGameState.game_undergoing(result_received) == "Victory"
