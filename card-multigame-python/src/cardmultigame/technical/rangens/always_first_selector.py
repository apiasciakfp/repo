from cardmultigame.entities.cards.card import Card
from cardmultigame.technical.rangens.i_card_selector import ICardSelector


class AlwaysFirstSelector(ICardSelector):
    def draw_card(self, cards: list[Card]) -> Card:
        return cards[0]
