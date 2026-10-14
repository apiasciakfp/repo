from cardmultigame.entities.cards.card import Card
from cardmultigame.usecases.cardcomparison.i_card_comparison_strategy import ICardComparisonStrategy


class AlwaysFailComparisonStrategy(ICardComparisonStrategy):
    # NullObject pattern.
    def are_the_same(self, card1: Card, card2: Card) -> bool:
        return False
