from cardmultigame.entities.gamestates.game_state import GameState
from cardmultigame.entities.gamestates.game_state_keys import GameStateKeys


class ModifyGameState:
    """STATELESS FOREVER. Commands over the dictionary only — the 'C' in CQS."""

    @staticmethod
    def add_turn(current_game_state: GameState) -> None:
        current_turn = current_game_state[GameStateKeys.CurrentTurn]
        current_game_state[GameStateKeys.CurrentTurn] = current_turn + 1

    @staticmethod
    def declare_game_to_be_lost(current_game_state: GameState) -> None:
        current_game_state[GameStateKeys.IsGameLost] = True

    @staticmethod
    def declare_game_to_be_won(current_game_state: GameState) -> None:
        current_game_state[GameStateKeys.IsGameWon] = True
