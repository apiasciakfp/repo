from abc import ABC, abstractmethod

from cardmultigame.entities.cards.card import Card


class ICardSelector(ABC):
    @abstractmethod
    def draw_card(self, cards: list[Card]) -> Card: ...
