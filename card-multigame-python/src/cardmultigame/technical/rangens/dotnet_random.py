import datetime
import random


class DotNetRandom:
    """Mirrors .NET System.Random's seeding and Next(min, max) semantics."""

    def __init__(self) -> None:
        self._random = random.Random(datetime.datetime.now().microsecond // 1000)

    def next(self, min_value: int, max_value: int) -> int:
        if max_value < min_value:
            raise ValueError("maxValue must be greater than or equal to minValue")
        if min_value == max_value:
            return min_value
        return self._random.randrange(min_value, max_value)
