import re

from cardmultigame.entities.cards.card import Card


class CreateCards:
    def create_collection(self, card_strings: str) -> list[Card]:
        card_prototype_pattern = r"((\b\w{2,3}\b)+)"

        cards: list[Card] = []
        for match in re.finditer(card_prototype_pattern, card_strings, re.MULTILINE):
            prototype = match.group()
            if self._is_valid_card_prototype(prototype):
                cards.append(self.create_single(prototype))

        return cards

    def create_single(self, prototype: str) -> Card:
        if self._is_valid_card_prototype(prototype) is False:
            return self._damaged_card()

        rank = self._extract_rank(prototype)
        colour = self._extract_colour(prototype)

        return Card(rank, colour)

    def _extract_colour(self, prototype: str) -> str:
        colour_sign = prototype[len(prototype) - 1 :]

        if colour_sign.upper() == "S":
            return "S"
        if colour_sign.upper() == "H":
            return "H"
        if colour_sign.upper() == "D":
            return "D"
        if colour_sign.upper() == "C":
            return "C"

        raise ValueError("Colour extraction failed. Instead of SHDC we got: " + colour_sign)

    def _extract_rank(self, prototype: str) -> str:
        rank_sign = prototype[0 : len(prototype) - 1]
        return rank_sign

    def _damaged_card(self) -> Card:
        return Card("Damaged", "Damaged")

    def _is_valid_card_prototype(self, prototype: str) -> bool:
        exact_card_prototype_pattern = r"\b(10[shdcSHDC]|[2-9jqkaJQKA][shdcSHDC])\b"
        if re.search(exact_card_prototype_pattern, prototype, re.MULTILINE):
            return True
        return False
