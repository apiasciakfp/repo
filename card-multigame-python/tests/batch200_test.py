"""Port of Java Batch200Test — Command / ChainOfResponsibility / Builder / EncapsulatedContext.

(t201-t208 use the dormant special-rule actions and land in Slice 5.)
"""

from cardmultigame.entities.decks.create_card_deck import CreateCardDeck
from cardmultigame.entities.games.guessing.guess_a_card_game import GuessACardGame
from cardmultigame.entities.gamestates.create_game_state import CreateGameState
from cardmultigame.entities.gamestates.game_state_keys import GameStateKeys
from cardmultigame.gamemanagers.game_manager_internals_builder import GameManagerInternalsBuilder
from cardmultigame.gamemanagers.selectedrules.create_played_game_rules import CreatePlayedGameRules
from cardmultigame.gamemanagers.selectedrules.creationcommands.game_variant import GameVariant
from cardmultigame.gamemanagers.selectedrules.creationcommands.select_game import SelectGame
from cardmultigame.gamemanagers.selectedrules.creationcommands.set_deck import SetDeck
from cardmultigame.usecases.cardcomparison.always_fail_comparison_strategy import (
    AlwaysFailComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.black_red_colour_only_comparison_strategy import (
    BlackRedColourOnlyComparisonStrategy,
)
from cardmultigame.usecases.cardcomparison.strict_card_comparison_strategy import (
    StrictCardComparisonStrategy,
)
from cardmultigame.usecases.gameactions.add10c_or_draw_a_card import Add10COrDrawACard
from cardmultigame.usecases.gameactions.add_queen_of_hearts_to_deck import AddQueenOfHeartsToDeck
from cardmultigame.usecases.gameactions.create_game_actions import CreateGameActions
from cardmultigame.usecases.gameactions.draw_single_card_action import DrawSingleCardAction
from cardmultigame.usecases.gameactions.guess_card_action import GuessCardAction
from cardmultigame.usecases.gameconditions.did_guess_a_card import DidGuessACard
from cardmultigame.usecases.gameconditions.did_turns_expire import DidTurnsExpire
from cardmultigame.usecases.influencestate.modify_game_state import ModifyGameState
from cardmultigame.usecases.influencestate.query_game_state import QueryGameState


def test_t209_the_game_was_a_strategy_all_along():
    game = GuessACardGame()

    assert len(game.available_actions()) == 1
    assert len(game.game_stop_conditions()) == 1
    assert len(game.victory_conditions()) == 1

    assert isinstance(game.available_actions()[0], GuessCardAction)
    assert isinstance(game.game_stop_conditions()[0], DidTurnsExpire)
    assert isinstance(game.victory_conditions()[0], DidGuessACard)


def test_t210_builder_pattern_reveals_itself():
    builder = GameManagerInternalsBuilder()

    SelectGame().change_game_ruleset(builder, "GuessACard")

    rules = builder.construct_ruleset()

    assert isinstance(rules.card_comparator(), StrictCardComparisonStrategy)
    assert isinstance(rules.game_actions[0], GuessCardAction)
    assert isinstance(rules.game_stop_conditions[0], DidTurnsExpire)
    assert isinstance(rules.victory_conditions[0], DidGuessACard)


def test_t211_glory_of_deferred_construction():
    builder = GameManagerInternalsBuilder()

    commands = [SelectGame(), GameVariant()]
    arguments = ["GuessACard", "RedBlack"]

    for i in range(len(commands)):
        commands[i].change_game_ruleset(builder, arguments[i])

    rules = builder.construct_ruleset()

    assert isinstance(rules.card_comparator(), BlackRedColourOnlyComparisonStrategy)
    assert isinstance(rules.game_actions[0], GuessCardAction)
    assert isinstance(rules.game_stop_conditions[0], DidTurnsExpire)
    assert isinstance(rules.victory_conditions[0], DidGuessACard)


def test_t212_implement_guess_a_card_command():
    builder = GameManagerInternalsBuilder()

    commands = [SelectGame(), GameVariant(), SetDeck()]
    arguments = ["GuessACard", "RedBlack", "2H,2D,3H,3D"]

    for i in range(len(commands)):
        commands[i].change_game_ruleset(builder, arguments[i])

    rules = builder.construct_ruleset()
    game_state = builder.construct_game_state()

    assert QueryGameState.amount_of_cards_left(game_state) == 4

    action = GuessCardAction()

    # First guess 2S (black) vs a red card -> miss
    action.change_game_state(game_state, rules, "2S")
    assert game_state["Guess"] is False

    # Second guess 10H (red) vs a red card -> hit
    action.change_game_state(game_state, rules, "10H")
    assert game_state["Guess"] is True


def test_t213_one_more_factory_with_null_object():
    reference_rules = CreatePlayedGameRules().empty()

    assert len(reference_rules.game_actions) == 0
    assert len(reference_rules.victory_conditions) == 0
    assert len(reference_rules.game_stop_conditions) == 0
    assert isinstance(reference_rules.card_comparator(), AlwaysFailComparisonStrategy)

    game_name = "Random game"

    actual_rules = CreatePlayedGameRules().with_modifications(game_name, None, None, None, None)

    assert actual_rules.game_name == game_name
    assert len(actual_rules.game_actions) == len(reference_rules.game_actions)
    assert len(actual_rules.victory_conditions) == len(reference_rules.victory_conditions)
    assert len(actual_rules.game_stop_conditions) == len(reference_rules.game_stop_conditions)
    assert isinstance(actual_rules.card_comparator(), AlwaysFailComparisonStrategy)

    actions = [GuessCardAction()]
    victories = [DidGuessACard()]

    actual_rules = CreatePlayedGameRules().with_modifications(None, actions, victories, None, None)

    assert actual_rules.game_name == reference_rules.game_name
    assert isinstance(actual_rules.game_actions[0], GuessCardAction)
    assert isinstance(actual_rules.victory_conditions[0], DidGuessACard)
    assert len(actual_rules.game_stop_conditions) == len(reference_rules.game_stop_conditions)
    assert isinstance(actual_rules.card_comparator(), AlwaysFailComparisonStrategy)


def test_t201_gentle_introduction_to_command():
    # Tutorial: how to extract the CardDeck from the GameState
    tutorial_state = CreateGameState().defaults_with_full_deck()
    tutorial_deck = QueryGameState.extract_card_deck(tutorial_state)
    tutorial_deck.draw_random_card()

    deck = CreateCardDeck().from_given_cards("2H, 3H, 4H")
    game_state = CreateGameState().defaults_plus_deck(deck)

    assert QueryGameState.amount_of_cards_left(game_state) == 3
    amount_of_cards_after_drawing_one = QueryGameState.amount_of_cards_left(game_state) - 1

    DrawSingleCardAction().change_game_state(game_state, None, None)

    assert QueryGameState.amount_of_cards_left(game_state) == amount_of_cards_after_drawing_one


def test_t202_add_some_qh_into_the_card_deck():
    deck = CreateCardDeck().from_given_cards("2H, 3H, 4H")
    game_state = CreateGameState().defaults_plus_deck(deck)

    actions = [
        AddQueenOfHeartsToDeck(),
        AddQueenOfHeartsToDeck(),
        AddQueenOfHeartsToDeck(),
        AddQueenOfHeartsToDeck(),
        AddQueenOfHeartsToDeck(),
    ]

    assert QueryGameState.amount_of_cards_left(game_state) == 3
    amount_of_cards_after = QueryGameState.amount_of_cards_left(game_state) + len(actions)

    for action in actions:
        action.change_game_state(game_state, None, None)

    assert QueryGameState.amount_of_cards_left(game_state) == amount_of_cards_after

    retrieved_deck = QueryGameState.extract_card_deck(game_state)

    for _ in range(5):
        card = retrieved_deck.draw_last_added_card()
        assert card.rank == "Q"
        assert card.colour == "H"


def test_t203_chain_some_commands():
    deck = CreateCardDeck().from_given_cards("2H, 3H, 4H")
    game_state = CreateGameState().defaults_plus_deck(deck)

    actions = [
        DrawSingleCardAction(),
        DrawSingleCardAction(),
        DrawSingleCardAction(),  # now it should be empty
        AddQueenOfHeartsToDeck(),
        AddQueenOfHeartsToDeck(),
        Add10COrDrawACard(),  # adds +1 card, because even
        Add10COrDrawACard(),  # draws a card, because odd
    ]

    assert QueryGameState.amount_of_cards_left(game_state) == 3
    amount_of_cards_after = 2

    for action in actions:
        action.change_game_state(game_state, None, None)

    assert QueryGameState.amount_of_cards_left(game_state) == amount_of_cards_after


def test_t204_factorize_me():
    deck = CreateCardDeck().from_given_cards("2H, 3H, 4H")
    game_state = CreateGameState().defaults_plus_deck(deck)

    actions_to_perform = (
        "drawSingleCard, drawSingleCard, drawSingleCard, addQH, addQH, add10cOrDraw, add10cOrDraw"
    )
    actions = CreateGameActions().having_orders(actions_to_perform)

    assert QueryGameState.amount_of_cards_left(game_state) == 3
    amount_of_cards_after = 2

    for action in actions:
        action.change_game_state(game_state, None, None)

    assert QueryGameState.amount_of_cards_left(game_state) == amount_of_cards_after


def test_t205_commands_can_communicate_via_context():
    tutorial_state = CreateGameState().default()
    assert tutorial_state["SpecificKey"] is None
    tutorial_state["SpecificKey"] = "Capybara"
    assert tutorial_state["SpecificKey"] == "Capybara"

    deck = CreateCardDeck().from_given_cards("2H, 3H, 4H")
    game_state = CreateGameState().defaults_plus_deck(deck)

    actions = CreateGameActions().having_orders("drawSingleCard, drawSingleCard, drawSingleCard")

    assert QueryGameState.amount_of_cards_left(game_state) == 3

    for action in actions:
        action.change_game_state(game_state, None, None)

    assert game_state["Guess"] is True


def test_t206_query_game_state_cannot_change_a_thing():
    game_state = CreateGameState().default()
    game_state[GameStateKeys.IsGameWon] = False
    game_state[GameStateKeys.IsGameLost] = False

    assert QueryGameState.is_game_won(game_state) is False
    assert QueryGameState.is_game_lost(game_state) is False


def test_t207_modify_game_state_can_change_quite_a_lot():
    game_state = CreateGameState().default()
    game_state[GameStateKeys.IsGameWon] = False
    game_state[GameStateKeys.IsGameLost] = False

    assert QueryGameState.is_game_won(game_state) is False
    assert QueryGameState.is_game_lost(game_state) is False

    ModifyGameState.declare_game_to_be_won(game_state)
    ModifyGameState.declare_game_to_be_lost(game_state)

    assert QueryGameState.is_game_won(game_state) is True
    assert QueryGameState.is_game_lost(game_state) is True


def test_t208_win_condition_loss_condition():
    game_state = CreateGameState().defaults_with_full_deck()

    actions = CreateGameActions().having_orders("drawSingleCard, drawSingleCard")
    conditions = [DidGuessACard(), DidTurnsExpire()]

    while True:
        for action in actions:
            action.change_game_state(game_state, None, None)

        for condition in conditions:
            condition.check_and_update(game_state)

        if QueryGameState.is_game_finished(game_state):
            break

    assert QueryGameState.is_game_lost(game_state) is True
    assert QueryGameState.is_game_won(game_state) is False
