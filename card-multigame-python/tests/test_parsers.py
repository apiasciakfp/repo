"""Port of Java TestParsers — separator auto-detection, nested separators preserved."""

from cardmultigame.technical.parsers.selected_parser import SelectedParser


def test_parser_properly_selected_semicolon_separator():
    orders = "Play GuessACard; SetDeck JH, QH, KH; StartGame; Guess JH; Guess QH"
    result = SelectedParser().properly_parse(orders)
    assert result == [
        ("Play", "GuessACard"),
        ("SetDeck", "JH, QH, KH"),  # commas preserved inside a semicolon-split record
        ("StartGame", ""),
        ("Guess", "JH"),
        ("Guess", "QH"),
    ]


def test_parser_properly_selected_comma_separator():
    orders = "Play GuessACard, SetDeck JH; QH; KH, StartGame, Guess JH, Guess QH"
    result = SelectedParser().properly_parse(orders)
    assert result == [
        ("Play", "GuessACard"),
        ("SetDeck", "JH; QH; KH"),  # semicolons preserved inside a comma-split record
        ("StartGame", ""),
        ("Guess", "JH"),
        ("Guess", "QH"),
    ]
