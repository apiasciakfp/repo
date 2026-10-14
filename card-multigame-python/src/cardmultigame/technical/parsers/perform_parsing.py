import re

from cardmultigame.technical.parsers.parsestrategies.i_parse_strategy import IParseStrategy


class PerformParsing:
    def __init__(self, parse_strategy: IParseStrategy) -> None:
        self._parse_strategy = parse_strategy

    def execute_on(self, order_string: str) -> list[tuple[str, str]]:
        records = self._parse_strategy.split_into_records(order_string)

        single_first_word = r"(\b\w+\b){1}"

        actions_with_params: list[tuple[str, str]] = []
        for record in records:
            match = re.search(single_first_word, record, re.MULTILINE)
            action_sigil = match.group() if match else ""
            params_sigil = record.replace(action_sigil, "")

            actions_with_params.append((action_sigil.strip(), params_sigil.strip()))

        return actions_with_params
