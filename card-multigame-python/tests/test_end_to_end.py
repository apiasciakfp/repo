"""Port of Java TestEndToEnd — setup -> miss -> hit -> victory -> game ignores further commands.

Uses AlwaysFirstSelector for determinism (manual construction path).
"""

from cardmultigame.entities.gamestates.create_game_state import CreateGameState
from cardmultigame.entities.gamestates.game_state_keys import GameStateKeys
from cardmultigame.entities.decks.create_card_deck import CreateCardDeck
from cardmultigame.gamemanagers.game_manager import GameManager
from cardmultigame.gamemanagers.selectedrules.create_played_game_rules import CreatePlayedGameRules
from cardmultigame.technical.rangens.always_first_selector import AlwaysFirstSelector
from cardmultigame.usecases.cardcomparison.strict_card_comparison_strategy import (
    StrictCardComparisonStrategy,
)
from cardmultigame.usecases.gameactions.guess_card_action import GuessCardAction
from cardmultigame.usecases.gameconditions.did_guess_a_card import DidGuessACard
from cardmultigame.usecases.gameconditions.did_turns_expire import DidTurnsExpire
from cardmultigame.usecases.influencestate.query_game_state import QueryGameState


def test_full_scenario_setup_miss_hit_victory_then_game_ignores_commands():
    # "SetDeck JH,QH,KH" — three-card deck with deterministic draw order
    deck_factory = CreateCardDeck()
    deck_factory.set_card_selector(AlwaysFirstSelector())
    deck = deck_factory.from_given_cards("JH,QH,KH")

    # "SetMaxTurns 3"
    initial_state = CreateGameState().defaults_plus_deck(deck)
    initial_state[GameStateKeys.MaxTurns] = 3

    rules = CreatePlayedGameRules().with_modifications(
        "Guess a Card!",
        [GuessCardAction()],
        [DidGuessACard()],
        [DidTurnsExpire()],
        StrictCardComparisonStrategy(),
    )

    gm = GameManager(initial_state, rules)

    # initial state after setup
    state = gm.current_state()
    assert QueryGameState.amount_of_cards_left(state) == 3
    assert QueryGameState.maximum_turns(state) == 3
    assert QueryGameState.current_turn(state) == 0
    assert QueryGameState.is_game_finished(state) is False
    assert QueryGameState.game_undergoing(state) == "Undergoing"

    # Turn 1 — "Guess 2C;" — drew JH, miss
    gm.execute_orders("Guess 2C;")
    state = gm.current_state()
    assert state["Guess"] is False
    assert QueryGameState.current_turn(state) == 1
    assert QueryGameState.amount_of_cards_left(state) == 2
    assert QueryGameState.is_game_finished(state) is False
    assert QueryGameState.game_undergoing(state) == "Undergoing"

    # Turn 2 — "Guess QH;" — drew QH, hit -> Victory
    gm.execute_orders("Guess QH;")
    state = gm.current_state()
    assert state["Guess"] is True
    assert QueryGameState.current_turn(state) == 2
    assert QueryGameState.amount_of_cards_left(state) == 1
    assert QueryGameState.is_game_finished(state) is True
    assert QueryGameState.game_undergoing(state) == "Victory"

    # Turn 3 — "Guess KH;" — ignored, game already finished
    gm.execute_orders("Guess KH;")
    state = gm.current_state()
    assert QueryGameState.current_turn(state) == 2
    assert QueryGameState.amount_of_cards_left(state) == 1
    assert QueryGameState.game_undergoing(state) == "Victory"
