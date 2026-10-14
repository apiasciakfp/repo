from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cardmultigame.gamemanagers.game_manager_internals_builder import (
        GameManagerInternalsBuilder,
    )


class ICreateGameRulesCommand(ABC):
    @abstractmethod
    def should_react_to(self, outer_command_name: str) -> bool: ...

    @abstractmethod
    def change_game_ruleset(
        self, builder: GameManagerInternalsBuilder, parameters: str
    ) -> None: ...
