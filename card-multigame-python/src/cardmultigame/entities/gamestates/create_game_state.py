from cardmultigame.entities.decks.card_deck import CardDeck
from cardmultigame.entities.decks.create_card_deck import CreateCardDeck
from cardmultigame.entities.gamestates.game_state import GameState
from cardmultigame.entities.gamestates.game_state_keys import GameStateKeys


class CreateGameState:
    def with_modifications(
        self, state_modifier: GameState | None = None, deck: CardDeck | None = None
    ) -> GameState:
        deck2 = self._sanitize_deck(deck)
        state_modifier2 = self._sanitize_state(state_modifier)

        constructed_state = self.default()
        for key, value in state_modifier2.items():
            constructed_state[key] = value

        constructed_state[GameStateKeys.CardDeck] = deck2
        return constructed_state

    def defaults_plus_deck(self, deck: CardDeck) -> GameState:
        constructed_state = self.default()
        constructed_state[GameStateKeys.CardDeck] = deck
        return constructed_state

    def defaults_with_full_deck(self) -> GameState:
        constructed_state = self.default()
        constructed_state[GameStateKeys.CardDeck] = CreateCardDeck().simple2_to_a_with_4_colours()
        return constructed_state

    def default(self) -> GameState:
        constructed_state = GameState()
        constructed_state[GameStateKeys.CardDeck] = CreateCardDeck().empty()
        constructed_state[GameStateKeys.CurrentTurn] = 0
        constructed_state[GameStateKeys.MaxTurns] = 0
        constructed_state[GameStateKeys.IsGameLost] = False
        constructed_state[GameStateKeys.IsGameWon] = False
        return constructed_state

    def _sanitize_state(self, state_modifier: GameState | None) -> GameState:
        if state_modifier is None:
            return GameState()
        return state_modifier

    def _sanitize_deck(self, deck: CardDeck | None) -> CardDeck:
        if deck is None:
            return CreateCardDeck().empty()
        return deck
