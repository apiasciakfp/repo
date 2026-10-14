from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.gamemanagers.selectedrules.creationcommands.i_create_game_rules_command import (
    ICreateGameRulesCommand,
)

if TYPE_CHECKING:
    from cardmultigame.gamemanagers.game_manager_internals_builder import (
        GameManagerInternalsBuilder,
    )


class SetMaxTurns(ICreateGameRulesCommand):
    def __init__(self) -> None:
        self._identifier = "SetMaxTurns"

    def change_game_ruleset(self, builder: GameManagerInternalsBuilder, parameters: str) -> None:
        try:
            max_turns = int(parameters)
            was_successful = True
        except ValueError:
            was_successful = False

        if was_successful:
            builder.set_max_turns(max_turns)

    def should_react_to(self, outer_command_name: str) -> bool:
        return self._identifier.lower() == outer_command_name.lower()
