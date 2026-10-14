from cardmultigame.usecases.cardcomparison.always_fail_comparison_strategy import (
    AlwaysFailComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.black_red_colour_only_comparison_strategy import (
    BlackRedColourOnlyComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.colour_card_comparison_strategy import (
    ColourCardComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.i_card_comparison_strategy import ICardComparisonStrategy
from cardmultigame.usecases.cardcomparison.rank_card_comparison_strategy import (
    RankCardComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.strict_card_comparison_strategy import (
    StrictCardComparisonStrategy,
)


class CreateCardComparisonStrategy:
    def create(self, selector: str) -> ICardComparisonStrategy:
        if selector == "strict":
            return StrictCardComparisonStrategy()
        if selector == "colour":
            return ColourCardComparisonStrategy()
        if selector == "blackred":
            return BlackRedColourOnlyComparisonStrategy()
        if selector == "rank":
            return RankCardComparisonStrategy()
        else:
            return AlwaysFailComparisonStrategy()

    def none(self) -> ICardComparisonStrategy:
        return AlwaysFailComparisonStrategy()
