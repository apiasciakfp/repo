# Card Multigame — Python

A faithful **surface-Pythonic port** of the C# CardMultigame — a deliberately over-engineered
GoF design-patterns showcase (a card guessing game). Behaviour, structure and **warts** match the
C# original; only the syntax is Pythonic. Built on [`uv`](https://docs.astral.sh/uv/).

> This is a teaching artifact. The brittleness is intentional and preserved — do not "fix" it.

## Run

```bash
uv run cardmultigame
```

Requires Python 3.12+ (pinned to 3.14 via `.python-version`). `uv` syncs the environment automatically.

Without `uv` (no third-party dependencies needed):

```bash
PYTHONPATH=src python -m cardmultigame.program          # macOS / Linux
$env:PYTHONPATH="src"; python -m cardmultigame.program  # Windows PowerShell
```

## Test

```bash
uv run pytest
```

Ports the Java suite (TestParsers, TestDeck, TestEndToEnd, TestGuessACard, Batch100, Batch200,
SmokeTest) to pytest, plus one extra property test for the `RandomCardSelector` (the one wart the
Java suite can't see).

## REPL

Text REPL — type a setup string ending in `SETUP`, then `Guess <card>` commands.

```text
Play GuessACard; SetDeck JH,QH,KH; SetMaxTurns 5; SETUP
Guess QH;
EXIT
```

### Setup commands

| Command | Example | Effect |
|---|---|---|
| `Play` | `Play GuessACard` | Selects the game (only `GuessACard`). |
| `SetDeck` | `SetDeck JH,QH,KH` | Custom deck (rank `2`-`10`,`J`,`Q`,`K`,`A` + suit `S`,`H`,`D`,`C`). Default: 9-to-A ×4 suits (24 cards). |
| `SetMaxTurns` | `SetMaxTurns 5` | Max guesses before defeat (default 5). |
| `GameVariant` | `GameVariant RedBlack` | Switches comparison to red/black colour only (`H`,`D`=red; `S`,`C`=black). |

Separators `,` `;` `-` are interchangeable; the parser auto-detects the first one present.

### Gameplay

| Command | Example | Effect |
|---|---|---|
| `Guess` | `Guess QH` | A card is drawn from the deck and compared to your guess. |
| `EXIT` | `EXIT` | Quit. |

Win when a guess matches; lose when turns run out. State is printed after every command.

## Fidelity

Source of truth is the C#; the Java port was the structural template. See the task docs under
`_applications/_tasks/260616-01-python-version/` for the exact-behaviour analysis, the
transliteration contract, and the differential verification against the C# binary.
