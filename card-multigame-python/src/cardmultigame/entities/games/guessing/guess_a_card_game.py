from cardmultigame.entities.decks.card_deck import CardDeck
from cardmultigame.entities.decks.create_card_deck import CreateCardDeck
from cardmultigame.entities.games.i_game_implementation import IGameImplementation
from cardmultigame.entities.gamestates.game_state import GameState
from cardmultigame.entities.gamestates.game_state_keys import GameStateKeys
from cardmultigame.usecases.cardcomparison.i_card_comparison_strategy import ICardComparisonStrategy
from cardmultigame.usecases.cardcomparison.strict_card_comparison_strategy import (
    StrictCardComparisonStrategy,
)
from cardmultigame.usecases.gameactions.guess_card_action import GuessCardAction
from cardmultigame.usecases.gameactions.i_game_action import IGameAction
from cardmultigame.usecases.gameconditions.did_guess_a_card import DidGuessACard
from cardmultigame.usecases.gameconditions.did_turns_expire import DidTurnsExpire
from cardmultigame.usecases.gameconditions.i_game_condition import IGameCondition


class GuessACardGame(IGameImplementation):
    def card_deck(self) -> CardDeck:
        return CreateCardDeck().simple9_to_a_with_4_colours()

    def available_actions(self) -> list[IGameAction]:
        return [GuessCardAction()]

    def game_stop_conditions(self) -> list[IGameCondition]:
        return [DidTurnsExpire()]

    def victory_conditions(self) -> list[IGameCondition]:
        return [DidGuessACard()]

    def initial_game_state(self) -> GameState:
        state = GameState()
        state[GameStateKeys.MaxTurns] = 5
        return state

    def title(self) -> str:
        return "Guess a Card!"

    def card_comparison_strategy(self) -> ICardComparisonStrategy:
        return StrictCardComparisonStrategy()
