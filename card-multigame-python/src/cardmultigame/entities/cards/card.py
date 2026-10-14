class Card:
    def __init__(self, rank: str, colour: str) -> None:
        self._rank = rank
        self._colour = colour

    @property
    def rank(self) -> str:
        return self._rank

    @property
    def colour(self) -> str:
        return self._colour

    def __str__(self) -> str:
        return f"r: {self.rank} c: {self.colour}"
