from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.entities.cards.card import Card
from cardmultigame.usecases.gameactions.i_game_action import IGameAction
from cardmultigame.usecases.influencestate.query_game_state import QueryGameState

if TYPE_CHECKING:
    from cardmultigame.entities.gamestates.game_state import GameState
    from cardmultigame.gamemanagers.selectedrules.played_game_rules import PlayedGameRules


class AddQueenOfHeartsToDeck(IGameAction):
    def change_game_state(
        self, current_game_state: GameState, game_rules: PlayedGameRules, order_params: str
    ) -> None:
        deck = QueryGameState.extract_card_deck(current_game_state)
        deck.add_a_single_card(Card("Q", "H"))

    def should_react_to(self, item1: str) -> bool:
        raise NotImplementedError()
