from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.entities.cards.create_cards import CreateCards
from cardmultigame.usecases.gameactions.i_game_action import IGameAction
from cardmultigame.usecases.influencestate.modify_game_state import ModifyGameState
from cardmultigame.usecases.influencestate.query_game_state import QueryGameState

if TYPE_CHECKING:
    from cardmultigame.entities.gamestates.game_state import GameState
    from cardmultigame.gamemanagers.selectedrules.played_game_rules import PlayedGameRules


class GuessCardAction(IGameAction):
    def __init__(self) -> None:
        self._identifier = "Guess"

    def change_game_state(
        self, current_game_state: GameState, rules: PlayedGameRules, order_params: str
    ) -> None:
        candidate = CreateCards().create_single(order_params)

        deck = QueryGameState.extract_card_deck(current_game_state)
        actually_drawn_card = deck.draw_random_card()

        comparator = rules.card_comparator()

        are_the_same = comparator.are_the_same(candidate, actually_drawn_card)

        if are_the_same:
            current_game_state[self._identifier] = True
        else:
            current_game_state[self._identifier] = False

        ModifyGameState.add_turn(current_game_state)

    def should_react_to(self, order_name: str) -> bool:
        return self._identifier.lower() == order_name.lower()
