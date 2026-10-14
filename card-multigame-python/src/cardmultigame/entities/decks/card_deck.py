from cardmultigame.entities.cards.card import Card
from cardmultigame.technical.rangens.i_card_selector import ICardSelector


class CardDeck:
    def __init__(self, selector: ICardSelector, cards: list[Card]) -> None:
        self._selector = selector
        self._cards = cards

    def all_cards(self) -> list[Card]:
        return self._cards

    def cards_left(self) -> int:
        return len(self._cards)

    def draw_random_card(self) -> Card:
        drawn = self._selector.draw_card(self._cards)
        self._cards.remove(drawn)
        return drawn

    def draw_last_added_card(self) -> Card:
        drawn = self._cards[len(self._cards) - 1]
        self._cards.remove(drawn)
        return drawn

    def add_a_single_card(self, card: Card) -> None:
        self._cards.append(card)

    def __str__(self) -> str:
        card_faces = ""
        for card in self._cards:
            card_faces = card_faces + "||" + str(card)
        return f"Deck: {card_faces}"
