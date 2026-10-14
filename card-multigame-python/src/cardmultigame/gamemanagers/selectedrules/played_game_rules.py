from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cardmultigame.entities.gamestates.game_state import GameState
    from cardmultigame.usecases.cardcomparison.i_card_comparison_strategy import (
        ICardComparisonStrategy,
    )
    from cardmultigame.usecases.gameactions.i_game_action import IGameAction
    from cardmultigame.usecases.gameconditions.i_game_condition import IGameCondition


class PlayedGameRules:
    def __init__(
        self,
        game_name: str,
        actions: list[IGameAction],
        victories: list[IGameCondition],
        game_stops: list[IGameCondition],
        compare_cards: ICardComparisonStrategy,
    ) -> None:
        self._game_name = game_name
        self._actions = actions
        self._victory_conditions = victories
        self._game_stop_conditions = game_stops
        self._card_comparator = compare_cards

    def card_comparator(self) -> ICardComparisonStrategy:
        return self._card_comparator

    # Usually those three would remain private. But tests for patterns kind of need them.
    @property
    def game_actions(self) -> list[IGameAction]:
        return self._actions

    @property
    def victory_conditions(self) -> list[IGameCondition]:
        return self._victory_conditions

    @property
    def game_stop_conditions(self) -> list[IGameCondition]:
        return self._game_stop_conditions

    @property
    def game_name(self) -> str:
        return self._game_name

    def check_victory_conditions(self, current_game_state: GameState) -> None:
        for victory in self._victory_conditions:
            victory.check_and_update(current_game_state)

    def check_game_stop_conditions(self, current_game_state: GameState) -> None:
        for stop in self._game_stop_conditions:
            stop.check_and_update(current_game_state)
