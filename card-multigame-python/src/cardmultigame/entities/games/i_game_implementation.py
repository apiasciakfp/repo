from abc import ABC, abstractmethod

from cardmultigame.entities.decks.card_deck import CardDeck
from cardmultigame.entities.gamestates.game_state import GameState
from cardmultigame.usecases.cardcomparison.i_card_comparison_strategy import ICardComparisonStrategy
from cardmultigame.usecases.gameactions.i_game_action import IGameAction
from cardmultigame.usecases.gameconditions.i_game_condition import IGameCondition


class IGameImplementation(ABC):
    @abstractmethod
    def title(self) -> str: ...

    @abstractmethod
    def card_deck(self) -> CardDeck: ...

    @abstractmethod
    def available_actions(self) -> list[IGameAction]: ...

    @abstractmethod
    def victory_conditions(self) -> list[IGameCondition]: ...

    @abstractmethod
    def game_stop_conditions(self) -> list[IGameCondition]: ...

    @abstractmethod
    def initial_game_state(self) -> GameState: ...

    @abstractmethod
    def card_comparison_strategy(self) -> ICardComparisonStrategy: ...
