from cardmultigame.entities.cards.create_cards import CreateCards
from cardmultigame.entities.decks.card_deck import CardDeck
from cardmultigame.technical.rangens.i_card_selector import ICardSelector
from cardmultigame.technical.rangens.random_card_selector import RandomCardSelector


class CreateCardDeck:
    def __init__(self) -> None:
        self._selected_card_selector: ICardSelector = RandomCardSelector()

    def from_given_cards(self, cards_in_deck: str) -> CardDeck:
        cards = CreateCards().create_collection(cards_in_deck)
        return CardDeck(self._selected_card_selector, cards)

    def simple9_to_a_with_4_colours(self) -> CardDeck:
        ranks = ["9", "10", "J", "Q", "K", "A"]
        colours = ["S", "H", "D", "C"]

        cards = []
        for rank in ranks:
            for colour in colours:
                card_prototype = rank + colour
                card = CreateCards().create_single(card_prototype)
                cards.append(card)

        return CardDeck(self._selected_card_selector, cards)

    def simple2_to_a_with_4_colours(self) -> CardDeck:
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        colours = ["S", "H", "D", "C"]

        cards = []
        for rank in ranks:
            for colour in colours:
                card_prototype = rank + colour
                card = CreateCards().create_single(card_prototype)
                cards.append(card)

        return CardDeck(self._selected_card_selector, cards)

    def empty(self) -> CardDeck:
        return CardDeck(self._selected_card_selector, [])

    def set_card_selector(self, selector: ICardSelector) -> None:
        self._selected_card_selector = selector
