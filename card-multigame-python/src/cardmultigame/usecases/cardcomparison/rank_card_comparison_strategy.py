from cardmultigame.entities.cards.card import Card
from cardmultigame.usecases.cardcomparison.i_card_comparison_strategy import ICardComparisonStrategy


class RankCardComparisonStrategy(ICardComparisonStrategy):
    def are_the_same(self, card1: Card, card2: Card) -> bool:
        if card1.rank == card2.rank:
            return True
        else:
            return False
