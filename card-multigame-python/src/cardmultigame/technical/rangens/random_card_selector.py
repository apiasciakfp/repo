from cardmultigame.entities.cards.card import Card
from cardmultigame.technical.rangens.dotnet_random import DotNetRandom
from cardmultigame.technical.rangens.i_card_selector import ICardSelector


class RandomCardSelector(ICardSelector):
    def __init__(self) -> None:
        self._random = DotNetRandom()

    def draw_card(self, cards: list[Card]) -> Card:
        index = self._random.next(0, len(cards) - 1)
        drawn = cards[index]
        return drawn
