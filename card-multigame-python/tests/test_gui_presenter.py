"""GUI presenter: the display-free logic behind the tkinter front-end (no window is opened)."""

from cardmultigame.interface.gui_presenter import (
    GuiSession,
    asset_file_for,
    guess_command,
    setup_command,
)


def test_asset_file_names_map_ranks_to_numbers():
    assert asset_file_for("QH") == "H-12.png"
    assert asset_file_for("10C") == "C-10.png"
    assert asset_file_for("AS") == "S-1.png"
    assert asset_file_for("9D") == "D-9.png"


def test_every_default_deck_card_has_an_asset():
    session = GuiSession()
    session.start(5, False)

    from importlib.resources import files

    assets = files("cardmultigame") / "assets"
    assert len(session.all_cards) == 24
    assert all((assets / asset_file_for(code)).is_file() for code in session.all_cards)


def test_click_becomes_the_typed_command_with_its_separator():
    assert guess_command("QH") == "Guess QH;"


def test_setup_command_carries_turns_and_optional_variant():
    assert setup_command(5, False) == "Play GuessACard; SetMaxTurns 5; SETUP"
    assert setup_command(3, True) == "Play GuessACard; SetMaxTurns 3; GameVariant RedBlack; SETUP"


def test_each_guess_reveals_the_card_that_left_the_deck():
    session = GuiSession()
    session.start(24, False)

    guess_round = session.guess("2C")  # not in the deck: always a miss

    assert guess_round is not None
    assert guess_round.hit is False
    assert guess_round.drawn in session.all_cards
    assert session.drawn_cards() == {guess_round.drawn}
    assert session.status_text().startswith("Turn 1/24 — Miss: you guessed 2C, the Magician drew ")


def test_running_out_of_turns_is_a_defeat_and_later_clicks_are_ignored():
    session = GuiSession()
    session.start(2, False)

    session.guess("2C")
    session.guess("2C")

    assert session.outcome() == "Defeat"
    assert session.status_text().endswith("Defeat.")
    assert session.guess("2C") is None
    assert len(session.history) == 2


def test_a_hit_wins_the_game():
    session = GuiSession()
    session.start(24, True)

    # Red/Black variant: guessing a red card hits as soon as a red card is drawn.
    while not session.is_finished():
        session.guess("QH")

    assert session.history[-1].hit is True
    assert session.outcome() == "Victory"
    assert session.status_text().endswith("Victory!")
