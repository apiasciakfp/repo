from cardmultigame.entities.cards.card import Card
from cardmultigame.usecases.cardcomparison.i_card_comparison_strategy import ICardComparisonStrategy


class BlackRedColourOnlyComparisonStrategy(ICardComparisonStrategy):
    def are_the_same(self, card1: Card, card2: Card) -> bool:
        colour_map = {
            "H": "red",
            "D": "red",
            "C": "black",
            "S": "black",
        }

        card1_colour = colour_map[card1.colour]
        card2_colour = colour_map[card2.colour]

        if card1_colour == card2_colour:
            return True
        else:
            return False
