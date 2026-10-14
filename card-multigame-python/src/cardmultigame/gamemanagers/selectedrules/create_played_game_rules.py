from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.gamemanagers.selectedrules.played_game_rules import PlayedGameRules
from cardmultigame.usecases.cardcomparison.create_card_comparison_strategy import (
    CreateCardComparisonStrategy,
)

if TYPE_CHECKING:
    from cardmultigame.usecases.cardcomparison.i_card_comparison_strategy import (
        ICardComparisonStrategy,
    )
    from cardmultigame.usecases.gameactions.i_game_action import IGameAction
    from cardmultigame.usecases.gameconditions.i_game_condition import IGameCondition


class CreatePlayedGameRules:
    def __init__(self) -> None:
        self._default_game_name = "No game selected"
        self._default_actions: list[IGameAction] = []
        self._default_victories: list[IGameCondition] = []
        self._default_game_stops: list[IGameCondition] = []
        self._default_card_comparators = CreateCardComparisonStrategy().none()

    def empty(self) -> PlayedGameRules:
        return PlayedGameRules(
            self._default_game_name,
            self._default_actions,
            self._default_victories,
            self._default_game_stops,
            self._default_card_comparators,
        )

    def with_modifications(
        self,
        game_name: str | None,
        actions: list[IGameAction] | None,
        victories: list[IGameCondition] | None,
        game_stops: list[IGameCondition] | None,
        compare_cards: ICardComparisonStrategy | None,
    ) -> PlayedGameRules:
        selected_name = self._default_game_name
        selected_actions = self._default_actions
        selected_victories = self._default_victories
        selected_game_stops = self._default_game_stops
        selected_card_comparators = self._default_card_comparators

        if game_name is not None:
            selected_name = game_name

        if actions is not None:
            selected_actions = actions

        if victories is not None:
            selected_victories = victories

        if game_stops is not None:
            selected_game_stops = game_stops

        if compare_cards is not None:
            selected_card_comparators = compare_cards

        return PlayedGameRules(
            selected_name,
            selected_actions,
            selected_victories,
            selected_game_stops,
            selected_card_comparators,
        )
