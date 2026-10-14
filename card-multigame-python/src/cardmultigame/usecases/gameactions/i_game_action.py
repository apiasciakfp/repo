from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cardmultigame.entities.gamestates.game_state import GameState
    from cardmultigame.gamemanagers.selectedrules.played_game_rules import PlayedGameRules


class IGameAction(ABC):
    @abstractmethod
    def should_react_to(self, item1: str) -> bool: ...

    @abstractmethod
    def change_game_state(
        self, current_game_state: GameState, game_rules: PlayedGameRules, order_params: str
    ) -> None: ...
