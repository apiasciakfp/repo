from cardmultigame.entities.gamestates.create_game_state import CreateGameState
from cardmultigame.gamemanagers.game_manager import GameManager
from cardmultigame.gamemanagers.selectedrules.create_game_structure import CreateGameStructure
from cardmultigame.gamemanagers.selectedrules.create_played_game_rules import CreatePlayedGameRules
from cardmultigame.technical.parsers.selected_parser import SelectedParser


class CreateGameManager:
    def defaults_with_orders(self, order_string: str) -> GameManager:
        orders = SelectedParser().properly_parse(order_string)

        builder = CreateGameStructure().build_rules_and_initial_state(orders)

        rules = builder.construct_ruleset()
        initial_state = builder.construct_game_state()

        return GameManager(initial_state, rules)

    def empty(self) -> GameManager:
        initial_state = CreateGameState().default()
        rules = CreatePlayedGameRules().empty()

        return GameManager(initial_state, rules)
