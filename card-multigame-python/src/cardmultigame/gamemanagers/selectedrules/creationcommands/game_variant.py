from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.gamemanagers.selectedrules.creationcommands.i_create_game_rules_command import (
    ICreateGameRulesCommand,
)
from cardmultigame.usecases.cardcomparison.black_red_colour_only_comparison_strategy import (
    BlackRedColourOnlyComparisonStrategy,
)

if TYPE_CHECKING:
    from cardmultigame.gamemanagers.game_manager_internals_builder import (
        GameManagerInternalsBuilder,
    )


class GameVariant(ICreateGameRulesCommand):
    def __init__(self) -> None:
        self._identifier = "GameVariant"

    def change_game_ruleset(self, builder: GameManagerInternalsBuilder, parameters: str) -> None:
        # First, the comparator
        builder.set_card_comparison_strategy(BlackRedColourOnlyComparisonStrategy())

    def should_react_to(self, outer_command_name: str) -> bool:
        return self._identifier.lower() == outer_command_name.lower()
