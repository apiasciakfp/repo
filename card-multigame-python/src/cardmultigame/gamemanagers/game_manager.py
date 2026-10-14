from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.technical.parsers.selected_parser import SelectedParser
from cardmultigame.usecases.influencestate.query_game_state import QueryGameState

if TYPE_CHECKING:
    from cardmultigame.entities.gamestates.game_state import GameState
    from cardmultigame.gamemanagers.selectedrules.played_game_rules import PlayedGameRules


class GameManager:
    def __init__(self, initial_state: GameState, rules: PlayedGameRules) -> None:
        self._current_game_state = initial_state
        self._game_rules = rules

    def execute_orders(self, order_string: str) -> None:
        orders = SelectedParser().properly_parse(order_string)

        for order in orders:
            if QueryGameState.is_game_finished(self._current_game_state):
                return

            for game_action in self._game_rules.game_actions:
                if game_action.should_react_to(order[0]):
                    game_action.change_game_state(self._current_game_state, self._game_rules, order[1])

                    self._game_rules.check_victory_conditions(self._current_game_state)
                    self._game_rules.check_game_stop_conditions(self._current_game_state)

    def current_state(self) -> GameState:
        return self._current_game_state
