from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.usecases.gameactions.i_game_action import IGameAction
from cardmultigame.usecases.influencestate.query_game_state import QueryGameState

if TYPE_CHECKING:
    from cardmultigame.entities.gamestates.game_state import GameState
    from cardmultigame.gamemanagers.selectedrules.played_game_rules import PlayedGameRules


class DrawSingleCardAction(IGameAction):
    def change_game_state(
        self, current_game_state: GameState, game_rules: PlayedGameRules, order_params: str
    ) -> None:
        QueryGameState.extract_card_deck(current_game_state).draw_random_card()

        if QueryGameState.amount_of_cards_left(current_game_state) == 0:
            current_game_state["Guess"] = True

    def should_react_to(self, item1: str) -> bool:
        raise NotImplementedError()
