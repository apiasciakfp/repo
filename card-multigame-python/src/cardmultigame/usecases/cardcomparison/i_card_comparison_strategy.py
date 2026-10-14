from abc import ABC, abstractmethod

from cardmultigame.entities.cards.card import Card


class ICardComparisonStrategy(ABC):
    @abstractmethod
    def are_the_same(self, card1: Card, card2: Card) -> bool: ...
