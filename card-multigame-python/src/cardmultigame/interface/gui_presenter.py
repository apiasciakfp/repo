"""Display-free half of the GUI: turns clicks into the same order strings a REPL user would type.

Talks to the game only through UiLogicDispatcher; the engine is not touched. The engine does not
remember which card the Magician drew, so the presenter finds it by diffing the deck before and
after each guess (a read-only query of the state).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from cardmultigame.entities.gamestates.game_state_keys import GameStateKeys
from cardmultigame.interface.ui_logic_dispatcher import UiLogicDispatcher
from cardmultigame.usecases.influencestate.query_game_state import QueryGameState

BACK_FILE = "Back-R.png"

_RANK_TO_ASSET_NUMBER = {"A": "1", "J": "11", "Q": "12", "K": "13"}


def asset_file_for(card_code: str) -> str:
    """'QH' -> 'H-12.png', '10C' -> 'C-10.png', 'AS' -> 'S-1.png'."""
    rank, suit = card_code[:-1].upper(), card_code[-1].upper()
    return f"{suit}-{_RANK_TO_ASSET_NUMBER.get(rank, rank)}.png"


def guess_command(card_code: str) -> str:
    # The trailing ';' is required: the parser refuses an order string with no separator.
    return f"Guess {card_code};"


def setup_command(max_turns: int, red_black_variant: bool) -> str:
    variant = "GameVariant RedBlack; " if red_black_variant else ""
    return f"Play GuessACard; SetMaxTurns {max_turns}; {variant}SETUP"


@dataclass(frozen=True)
class GuessRound:
    guessed: str
    drawn: str | None
    hit: bool


class GuiSession:
    def __init__(self) -> None:
        self._dispatcher = UiLogicDispatcher()
        self.all_cards: list[str] = []
        self.history: list[GuessRound] = []

    def start(self, max_turns: int, red_black_variant: bool) -> None:
        self._dispatcher.setup_game(setup_command(max_turns, red_black_variant))
        self.all_cards = self._deck_codes()
        self.history = []

    def guess(self, card_code: str) -> GuessRound | None:
        if self.is_finished():
            return None

        deck_before = self._deck_codes()
        self._dispatcher.do_stuff(guess_command(card_code))
        missing = Counter(deck_before) - Counter(self._deck_codes())

        guess_round = GuessRound(
            guessed=card_code,
            drawn=next(iter(missing), None),
            hit=bool(self._state()["Guess"]),
        )
        self.history.append(guess_round)
        return guess_round

    def drawn_cards(self) -> set[str]:
        return {r.drawn for r in self.history if r.drawn is not None}

    def outcome(self) -> str:
        return QueryGameState.game_undergoing(self._state())

    def is_finished(self) -> bool:
        return QueryGameState.is_game_finished(self._state())

    def status_text(self) -> str:
        state = self._state()
        turn = f"Turn {state[GameStateKeys.CurrentTurn]}/{state[GameStateKeys.MaxTurns]}"

        if not self.history:
            return f"{turn} — click the card you think the Magician will draw."

        last = self.history[-1]
        verdict = "Hit" if last.hit else "Miss"
        line = f"{turn} — {verdict}: you guessed {last.guessed}, the Magician drew {last.drawn}."

        outcome = self.outcome()
        if outcome == "Victory":
            return f"{line} Victory!"
        if outcome == "Defeat":
            return f"{line} Defeat."
        return line

    def _state(self):
        return self._dispatcher.current_state()

    def _deck_codes(self) -> list[str]:
        deck = QueryGameState.extract_card_deck(self._state())
        return [card.rank + card.colour for card in deck.all_cards()]
