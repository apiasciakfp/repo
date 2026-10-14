from cardmultigame.entities.gamestates.game_state import GameState
from cardmultigame.usecases.gameconditions.i_game_condition import IGameCondition
from cardmultigame.usecases.influencestate.modify_game_state import ModifyGameState


class DidGuessACard(IGameCondition):
    """If there is a 'Guess' key AND it is true, declare the game won."""

    def check_and_update(self, current_game_state: GameState) -> None:
        result = current_game_state["Guess"]

        if result is not None:
            is_game_won = result
            if is_game_won:
                ModifyGameState.declare_game_to_be_won(current_game_state)
