from abc import ABC, abstractmethod

from cardmultigame.entities.gamestates.game_state import GameState


class IGameCondition(ABC):
    @abstractmethod
    def check_and_update(self, current_game_state: GameState) -> None: ...
