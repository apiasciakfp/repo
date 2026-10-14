from __future__ import annotations

from typing import TYPE_CHECKING

from cardmultigame.entities.decks.create_card_deck import CreateCardDeck
from cardmultigame.gamemanagers.selectedrules.creationcommands.i_create_game_rules_command import (
    ICreateGameRulesCommand,
)

if TYPE_CHECKING:
    from cardmultigame.gamemanagers.game_manager_internals_builder import (
        GameManagerInternalsBuilder,
    )


class SetDeck(ICreateGameRulesCommand):
    def __init__(self) -> None:
        self._identifier = "SetDeck"

    def change_game_ruleset(self, builder: GameManagerInternalsBuilder, parameters: str) -> None:
        deck = CreateCardDeck().from_given_cards(parameters)
        builder.set_deck(deck)

    def should_react_to(self, outer_command_name: str) -> bool:
        return self._identifier.lower() == outer_command_name.lower()
