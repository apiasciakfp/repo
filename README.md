# Card Guessing Game — Not For Fish (browser edition)

A Magician draws one card from a 24-card deck (9 to A, all four suits). You have 5 tries to guess it.

## How to run

Double-click `index.html`. It opens via `file://` — no server, no build step, no install.

Type commands in the `>` line and press Enter.

## How to test

Double-click `tests.html`. The page runs every test and shows ✔/✘ per test plus a summary
(`N passed / M failed`).

## Debug option: `?card=`

Open `index.html?card=QH` to pin the hidden card (any card in the 24-card deck, case-insensitive). A dim `[debug] hidden card pinned via ?card=` line is printed above the opening.
A value that isn't a card, or isn't in the deck (e.g. `?card=2C`, `?card=ZZ`), is ignored with a
warning in the browser console, and the card is drawn at random.

The pin goes through the same injection point the tests use (`createGame(drawCard)`); no rule changes.

## Design decisions

| # | Decision | Rationale |
|---|---|---|
| D1 | **Opening** tells the player a card was drawn, the deck (24 cards, 9–A), that they have 5 tries, and exactly how to type (`Guess QH;` / `EXIT`, ranks and suits). | A player who never read the brief must know what to type. |
| D7 | **`?card=XX` debug option** pins the hidden card via the same injection point tests use. Only cards in the deck are accepted; otherwise random. A dim `[debug]` line is printed when active. | Makes win/loss manually verifiable without changing rules. |
| D3 | **Case-insensitive** input: `guess qh;` = `Guess QH;`, `exit` = `EXIT`. Cards are always displayed upper-case. | Friendlier; still not a "clever parser". |
