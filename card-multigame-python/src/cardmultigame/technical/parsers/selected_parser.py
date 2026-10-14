import sys

from cardmultigame.technical.parsers.parsestrategies.comma_parse_strategy import CommaParseStrategy
from cardmultigame.technical.parsers.parsestrategies.dash_parse_strategy import DashParseStrategy
from cardmultigame.technical.parsers.parsestrategies.i_parse_strategy import IParseStrategy
from cardmultigame.technical.parsers.parsestrategies.semicolon_parse_strategy import (
    SemicolonParseStrategy,
)
from cardmultigame.technical.parsers.perform_parsing import PerformParsing


class SelectedParser:
    def __init__(self) -> None:
        self._parse_strategies = self._register_possible_strategies()

    def properly_parse(self, order_string: str) -> list[tuple[str, str]]:
        selected_strategy = self._select_appropriate_strategy(order_string)

        if selected_strategy is None:
            raise ValueError(
                "Order string is wrong or appropriate parsing Strategy is not registered"
            )

        return PerformParsing(selected_strategy).execute_on(order_string)

    def _select_appropriate_strategy(self, order_string: str) -> IParseStrategy | None:
        last_position = sys.maxsize
        selected_strategy: IParseStrategy | None = None
        for strategy in self._parse_strategies:
            potential = strategy.separator()

            current_position = order_string.find(potential)
            if current_position > 0 and current_position < last_position:
                selected_strategy = strategy
                last_position = current_position

        return selected_strategy

    def _register_possible_strategies(self) -> list[IParseStrategy]:
        return [
            CommaParseStrategy(),
            SemicolonParseStrategy(),
            DashParseStrategy(),
        ]
