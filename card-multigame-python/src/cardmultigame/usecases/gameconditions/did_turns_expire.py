from cardmultigame.entities.gamestates.game_state import GameState
from cardmultigame.usecases.gameconditions.i_game_condition import IGameCondition
from cardmultigame.usecases.influencestate.modify_game_state import ModifyGameState
from cardmultigame.usecases.influencestate.query_game_state import QueryGameState


class DidTurnsExpire(IGameCondition):
    """If currentTurn >= maxTurns, declare the game lost."""

    def check_and_update(self, current_game_state: GameState) -> None:
        current_turn = QueryGameState.current_turn(current_game_state)
        max_turns = QueryGameState.maximum_turns(current_game_state)

        if current_turn >= max_turns:
            ModifyGameState.declare_game_to_be_lost(current_game_state)
