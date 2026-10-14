from cardmultigame.entities.cards.card import Card
from cardmultigame.technical.rangens.i_card_selector import ICardSelector


class AlwaysLastSelector(ICardSelector):
    def draw_card(self, cards: list[Card]) -> Card:
        return cards[len(cards) - 1]
