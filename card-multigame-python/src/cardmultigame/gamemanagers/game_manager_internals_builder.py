from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.entities.gamestates.create_game_state import CreateGameState
from cardmultigame.entities.gamestates.game_state_keys import GameStateKeys
from cardmultigame.gamemanagers.selectedrules.create_played_game_rules import CreatePlayedGameRules

if TYPE_CHECKING:
    from cardmultigame.entities.decks.card_deck import CardDeck
    from cardmultigame.entities.gamestates.game_state import GameState
    from cardmultigame.gamemanagers.selectedrules.played_game_rules import PlayedGameRules
    from cardmultigame.usecases.cardcomparison.i_card_comparison_strategy import (
        ICardComparisonStrategy,
    )
    from cardmultigame.usecases.gameactions.i_game_action import IGameAction
    from cardmultigame.usecases.gameconditions.i_game_condition import IGameCondition


class GameManagerInternalsBuilder:
    def __init__(self) -> None:
        self._game_name = None
        self._deck = None
        self._actions = None
        self._victories = None
        self._game_stops = None
        self._initial_game_state = None
        # Specific to the Guessing Game.
        self._compare_cards = None

    def construct_ruleset(self) -> PlayedGameRules:
        return CreatePlayedGameRules().with_modifications(
            self._game_name, self._actions, self._victories, self._game_stops, self._compare_cards
        )

    def construct_game_state(self) -> GameState:
        return CreateGameState().with_modifications(self._initial_game_state, self._deck)

    def set_name(self, name: str) -> None:
        self._game_name = name

    def set_available_actions(self, actions: list[IGameAction]) -> None:
        self._actions = actions

    def set_victory_conditions(self, victories: list[IGameCondition]) -> None:
        self._victories = victories

    def set_game_stop_conditions(self, game_stops: list[IGameCondition]) -> None:
        self._game_stops = game_stops

    def set_deck(self, card_deck: CardDeck) -> None:
        self._deck = card_deck

    def set_initial_game_state(self, game_state: GameState) -> None:
        self._initial_game_state = game_state

    def set_max_turns(self, max_turns: int) -> None:
        self._initial_game_state[GameStateKeys.MaxTurns] = max_turns

    def get_card_deck(self) -> CardDeck:
        return self._deck

    # Specific to the Guessing Game. Should be more general, like with InternalState.
    def set_card_comparison_strategy(self, selected: ICardComparisonStrategy) -> None:
        self._compare_cards = selected
