from cardmultigame.technical.parsers.parsestrategies.i_parse_strategy import IParseStrategy


class DashParseStrategy(IParseStrategy):
    def __init__(self) -> None:
        self._separator = "-"

    def separator(self) -> str:
        return self._separator

    def split_into_records(self, order_string: str) -> list[str]:
        records = order_string.split(self._separator)

        sanitized_records: list[str] = []
        for record in records:
            if record is not None and record != "":
                sanitized = record.strip()
                if record is not None and record != "":
                    sanitized_records.append(record)

        return sanitized_records
