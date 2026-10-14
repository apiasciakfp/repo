from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.entities.games.guessing.guess_a_card_game import GuessACardGame
from cardmultigame.gamemanagers.selectedrules.creationcommands.i_create_game_rules_command import (
    ICreateGameRulesCommand,
)

if TYPE_CHECKING:
    from cardmultigame.entities.games.i_game_implementation import IGameImplementation
    from cardmultigame.gamemanagers.game_manager_internals_builder import (
        GameManagerInternalsBuilder,
    )


class SelectGame(ICreateGameRulesCommand):
    def __init__(self) -> None:
        self._identifier = "Play"

    def change_game_ruleset(self, builder: GameManagerInternalsBuilder, parameters: str) -> None:
        game_impl = self._select_game_implementation(parameters)

        builder.set_name(game_impl.title())
        builder.set_deck(game_impl.card_deck())
        builder.set_available_actions(game_impl.available_actions())
        builder.set_victory_conditions(game_impl.victory_conditions())
        builder.set_game_stop_conditions(game_impl.game_stop_conditions())
        builder.set_initial_game_state(game_impl.initial_game_state())
        builder.set_card_comparison_strategy(game_impl.card_comparison_strategy())

    def should_react_to(self, outer_command_name: str) -> bool:
        return self._identifier.lower() == outer_command_name.lower()

    @staticmethod
    def _select_game_implementation(parameters: str) -> IGameImplementation:
        game_impl = None
        if parameters.lower() == "GuessACard".lower():
            game_impl = GuessACardGame()

        if game_impl is None:
            raise ValueError(
                "Either the game is not registered in factory or game identifier has a typo. Got: "
                + parameters
            )

        return game_impl
