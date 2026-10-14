from cardmultigame.gamemanagers.game_manager_internals_builder import GameManagerInternalsBuilder
from cardmultigame.gamemanagers.selectedrules.creationcommands.game_variant import GameVariant
from cardmultigame.gamemanagers.selectedrules.creationcommands.i_create_game_rules_command import (
    ICreateGameRulesCommand,
)
from cardmultigame.gamemanagers.selectedrules.creationcommands.select_game import SelectGame
from cardmultigame.gamemanagers.selectedrules.creationcommands.set_deck import SetDeck
from cardmultigame.gamemanagers.selectedrules.creationcommands.set_max_turns import SetMaxTurns


class CreateGameStructure:
    def __init__(self) -> None:
        self._commands = self._register_available_creation_commands()

    def build_rules_and_initial_state(
        self, orders: list[tuple[str, str]]
    ) -> GameManagerInternalsBuilder:
        builder = GameManagerInternalsBuilder()
        for order in orders:
            for order_user in self._commands:
                if order_user.should_react_to(order[0]):
                    order_user.change_game_ruleset(builder, order[1])

        return builder

    def _register_available_creation_commands(self) -> list[ICreateGameRulesCommand]:
        return [SelectGame(), SetDeck(), SetMaxTurns(), GameVariant()]
