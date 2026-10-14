from cardmultigame.entities.gamestates.game_state import GameState
from cardmultigame.entities.gamestates.game_state_keys import GameStateKeys


class QueryGameState:
    """STATELESS FOREVER. Queries over the dictionary only — the 'Q' in CQS."""

    @staticmethod
    def maximum_turns(current_state: GameState) -> int:
        current_turn = current_state[GameStateKeys.MaxTurns]
        if current_turn is None:
            raise ValueError("Current turn cannot be a null")
        else:
            return current_turn

    @staticmethod
    def is_game_won(current_state: GameState) -> bool:
        return current_state[GameStateKeys.IsGameWon]

    @staticmethod
    def is_game_lost(current_state: GameState) -> bool:
        return current_state[GameStateKeys.IsGameLost]

    @staticmethod
    def is_game_finished(current_state: GameState) -> bool:
        return QueryGameState.is_game_won(current_state) or QueryGameState.is_game_lost(current_state)

    @staticmethod
    def current_turn(current_state: GameState) -> int:
        current_turn = current_state[GameStateKeys.CurrentTurn]
        if current_turn is None:
            raise ValueError("Current turn cannot be a null")
        else:
            return current_turn

    @staticmethod
    def amount_of_cards_left(current_state: GameState) -> int:
        return QueryGameState.extract_card_deck(current_state).cards_left()

    @staticmethod
    def game_undergoing(current_state: GameState) -> str:
        if current_state[GameStateKeys.IsGameWon]:
            return "Victory"
        elif current_state[GameStateKeys.IsGameLost]:
            return "Defeat"
        else:
            return "Undergoing"

    @staticmethod
    def extract_card_deck(current_state: GameState):
        return current_state[GameStateKeys.CardDeck]
