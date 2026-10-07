# Executor Brief — CardGuessingGameNotForFish (browser edition)

You are the **executor**. Your job: build this game, slice by slice, exactly as specified here, verifying each slice before moving on.
A **consultant** (another Claude session, reached through the user) owns the design. When this brief is silent or ambiguous, **do not invent — ask** (see §9).

Source of truth, in priority order:
1. This document (it records design decisions already made with the user).
2. The original brief: `docs/INSTRUCTIONS-cardguessinggame.html` (the game rules).

If the two ever conflict, stop and ask the consultant.

---

## 1. The game in one paragraph

A Magician draws **one** card at random from a **24-card deck** (ranks `9 10 J Q K A` × suits `H D S C`) before the first guess and never changes it. The player has **5 tries**. Each `Guess XX;` consumes one try. A guess **hits** only if rank **and** suit match. Hit → player **wins**, game over. Five misses → player **loses**, the hidden card is **revealed**, game over. After the game is over, further guesses **change nothing**. `EXIT` ends the session at any moment. Any well-formed card may be guessed, even one not in the deck (`Guess 2C;` is legal — and a guaranteed miss).

Card notation: rank then suit, no space. Ranks `2`–`10`, `J`, `Q`, `K`, `A`. Suits `H` hearts, `D` diamonds, `S` spades, `C` clubs. `10D` is three characters.

---

## 2. Hard constraints

- **Runs by double-clicking `index.html`** (opened via `file://`). No server, no build step, no npm, no Node at runtime, no CDN, no frameworks.
- **No ES modules** (`import`/`export` are blocked on `file://`). Use classic `<script>` tags. Each file attaches its API to one global namespace: `window.NotForFish` (create it if absent: `var NotForFish = window.NotForFish = window.NotForFish || {};`).
- **Tests also run in the browser**: double-click `tests.html`. Tiny hand-written runner; no test library.
- Vanilla HTML + CSS + JS only.
- **`game.js` never calls `Math.random`.** Randomness lives only at the edge (`ui.js`), injected as a function. Tests pin the card through that same injection point — **no rule ever changes for tests**.
- In product code, only `ui.js` touches the DOM. `card.js`, `game.js`, `console.js` are pure logic. (The test runner also renders to its page; that's fine.)
- Do **not** build a clever parser (see §5).

---

## 3. File layout

```
index.html        terminal-style page; final load order: src/card.js, src/game.js, src/console.js, src/ui.js
tests.html        final load order: tests/runner.js, src/card.js, src/game.js, src/console.js, tests/tests.js
style.css         terminal look (dark box, monospace, output log, single "> " input line)
README.md         how to run, how to test, the ?card= debug option, and the Design Decisions list (§6)
src/card.js       cards and deck
src/game.js       rules and state
src/console.js    command parsing + all player-facing text
src/ui.js         DOM wiring only
tests/runner.js   ~20-line test runner
tests/tests.js    all tests, grouped by slice
docs/             this brief + original instructions (do not modify)
```

**Add each `<script>` tag in the slice that creates its file.** Referencing a file that doesn't exist yet logs `ERR_FILE_NOT_FOUND` on `file://`, which fails the "no console errors" check.

---

## 4. Module contracts

These names/shapes are the contract. Tests are written against them. Small internal helpers are fine; don't rename the public API.

### `src/card.js`
```js
NotForFish.RANKS     // ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
NotForFish.SUITS     // ["H","D","S","C"]
NotForFish.DECK      // 24 cards: ranks 9,10,J,Q,K,A × suits H,D,S,C — array of { rank, suit }
NotForFish.parseCard(text)   // "qh" / "QH" / "10d" → { rank: "Q", suit: "H" } (normalized upper-case, keys in order rank, suit); invalid → null
NotForFish.cardToString(card) // { rank: "10", suit: "D" } → "10D"
NotForFish.sameCard(a, b)     // true iff rank and suit equal
```

### `src/game.js`
```js
var game = NotForFish.createGame(drawCard);   // drawCard: () => card. Called exactly once, inside createGame.
game.guess(card) → {
  outcome: "HIT" | "MISS" | "LOST" | "IGNORED",   // LOST = the 5th miss
  repeated: boolean,          // card was already guessed earlier in this game (try still consumed)
  triesUsed: number,
  triesLeft: number,
  revealed: card | null       // the hidden card on HIT or LOST; null otherwise
}
game.getState() → {
  status: "PLAYING" | "WON" | "LOST",
  triesUsed: number,          // 0..5
  maxTries: 5,
  triesLeft: number,
  guessed: [card, ...],       // in order
  revealed: card | null       // hidden card once the game is over; null while PLAYING
}
```
`IGNORED` = a guess while status is not `PLAYING`. It must not change any state (`triesUsed`, `guessed`, `status`). Its result echoes the current state: `triesUsed`/`triesLeft` unchanged, `repeated: false`, `revealed` = the hidden card.
`getState()` returns a fresh object each call, with a **copy** of `guessed` (callers can't mutate the game, and before/after snapshots really differ).
The hidden card must not be exposed while `PLAYING` (no public `hidden` field).

### `src/console.js`
```js
var con = NotForFish.createConsole(game);
con.opening() → string          // the opening text (§7)
con.handle(line) → { text: string, exit: boolean }
```
`handle` does parsing and wording. It never touches the DOM or `window`.

### `src/ui.js`
- Reads `?card=` from `location.search`. If present **and** it parses **and** it is in `DECK` → `drawCard = () => thatCard`, and print a dim line `[debug] hidden card pinned via ?card=` **before** the opening text. Otherwise (absent / invalid / not in deck) → `drawCard = () => DECK[Math.floor(Math.random() * DECK.length)]`; for an invalid/out-of-deck value also `console.warn` it.
- Creates game + console, prints `opening()`, echoes each entered line as `> <line>`, prints the response, clears and refocuses the input. On `exit: true` → disables the input.
- Autofocus the input on load.

### `tests/runner.js`
```js
NotForFish.test(name, fn)            // registers
NotForFish.assert(cond, message)
NotForFish.assertEqual(actual, expected, message)   // deep equality; object key order must not matter
NotForFish.runTests()                // runs all, renders ✔/✘ per test (with error text) into the page
```
`tests.html` calls `runTests()` on load. The summary element **must** be `<div id="summary" data-passed="N" data-failed="M">N passed / M failed</div>` so it can be checked headlessly. A thrown error in one test must not stop the others.

Test helper you'll want: `pinned("QH")` → `() => NotForFish.parseCard("QH")`.

---

## 5. Command grammar (deliberately simple)

Input line is trimmed first. Matching is **case-insensitive**.

| Input (after trim) | Meaning |
|---|---|
| `Guess <card>;` — regex `^guess\s+(\S+?)\s*;$` (i) with `<card>` accepted by `parseCard` | a guess |
| `EXIT` — exactly, case-insensitive | exit |
| empty | invalid (empty) |
| anything else — incl. `Guess ZZ;`, `Guess QH` (no `;`), `EXIT;`, `hello` | invalid |

Order of handling in `handle`: EXIT → empty → guess pattern → invalid.

**Before slices 6 and 7 exist**, every line that isn't a well-formed guess (including `EXIT` and empty lines) returns the §7 *Invalid* text with `exit: false`. Implement that fallback in slice 2. Slice 6 adds EXIT, and slice 7 adds the empty-line text and the full invalid-input tests. A well-formed guess after the game is over is passed to the game and comes back `IGNORED`. An invalid line is always just an error (regardless of game state).

---

## 6. Design decisions (already made — record each in README "Design decisions" and test each)

| # | Decision | Rationale |
|---|---|---|
| D1 | **Opening** tells the player a card was drawn, the deck (24 cards, 9–A), that they have 5 tries, and exactly how to type (`Guess QH;` / `EXIT`, ranks and suits). | Player who never read the brief must know what to type. |
| D2 | **Strange input** (malformed card, missing `;`, empty line, unknown command) is **rejected with a message showing the correct format**, and **does not consume a try**. | Typos shouldn't cost the game. |
| D3 | **Case-insensitive** input: `guess qh;` = `Guess QH;`, `exit` = `EXIT`. Cards are always displayed upper-case. | Friendlier; still not a "clever parser". |
| D4 | **Repeated guess** is legal and **consumes a try** (rules say so), but the response **warns** "You already guessed XX." | Respect the rules, help the player. |
| D5 | **Guesses after game over** are ignored **with a visible message** (not silent). | "Further guesses visibly change nothing." |
| D6 | **EXIT in a browser** prints `Goodbye.` and **disables the input** (a page can't close itself). Works before, during and after a game. Reload the page to play again. | Closest browser equivalent of ending the program. |
| D7 | **`?card=XX` debug option** pins the hidden card via the same injection point tests use. Only cards in the deck are accepted; otherwise random. A dim `[debug]` line is printed when active. | Makes win/loss manually verifiable without changing rules. |
| D8 | **Guessing a card not in the deck** (e.g. `2C`) is a normal miss; no warning. | Brief: noticing that is the player's job. |

---

## 7. Canonical messages

Use these texts. Tests should check the **facts** (hit/miss, tries left, won/lost, revealed card, "already guessed", "game is over", format hint), preferably via substrings, not entire strings — but use this wording.

| Situation | Text |
|---|---|
| Opening | `The Magician has drawn one card from a 24-card deck (9 to A, all four suits). It lies face down. You have 5 tries.`<br>`Type: Guess QH;  (rank 2-10, J, Q, K, A + suit H, D, S, C)  or  EXIT` |
| Miss | `Miss. 4 tries left.` (singular: `Miss. 1 try left.`) |
| Repeated miss | `You already guessed 2C. Miss. 3 tries left.` |
| Win | `Hit! The card was QH. You have won, in 2 tries.` (singular: `in 1 try.`) |
| Loss (5th miss) | `Miss. No tries left. The Magician turns the card over: it was QH. You have lost.` |
| Guess after game over | `The game is over. Nothing happens. Type EXIT to leave.` |
| Invalid | `I don't understand "<trimmed line>". Type: Guess QH;  or  EXIT. No try was used.` |
| Empty line | `Type: Guess QH;  or  EXIT. No try was used.` |
| EXIT | `Goodbye.` |
| Debug pin (ui only) | `[debug] hidden card pinned via ?card=` |

A repeated guess that is the 5th miss uses the loss text prefixed with `You already guessed XX. `.

---

## 8. Vertical slices — execute in order

Each slice is end-to-end (page → console → game) and has its own pass/fail check. **A slice is DONE only when:** its tests pass, **all earlier tests still pass** (`data-failed="0"`), its manual check passes, its README decision (if any) is written, and it is committed (one commit per slice: `Slice N: <title>`).

**Dependencies:** slices 0→1→2→3→4 form the core (start, win, miss, loss) and are strictly sequential. Slices 5, 6, 7 and 8 each need only the core (0–4), not each other. Do them in any order; a failure in one must not block the others. Recommended order: 5, 6, 7, 8.

### Slice 0 — Walking skeleton
- **Build:** `index.html` + `style.css` (terminal box, output log, `> ` input), `ui.js` echoing every entered line to the log; `tests.html` + `runner.js` + `tests.js` with one smoke test (`assertEqual({a:1,b:2}, {b:2,a:1})`, which also proves the runner's deep equality); `README.md` with how to run and test. Load only files that exist (see §3).
- **Tests:** smoke test passes; summary shows `1 passed / 0 failed`; a deliberately failing test (try it, then remove it) shows ✘ and `data-failed="1"`.
- **Manual:** double-click `index.html` → type `hello` → it appears in the log. Open `tests.html` → green.
- **Fails if:** anything needs a server, or the browser console shows errors.

### Slice 1 — Game starts with a hidden card
- **Build:** `card.js` (RANKS, SUITS, DECK, parseCard returning a card or `null` for invalid input, cardToString, sameCard), `createGame`, `getState`, `createConsole().opening()`, random source and `?card=` source in `ui.js` (D7).
- **Tests:** DECK has 24 unique cards, none with rank 2–8; `parseCard("ZZ")` → `null`; new game → `PLAYING`, 0 used, 5 left, `revealed: null`; `drawCard` called exactly once; opening contains `5 tries` and `Guess QH;` and `EXIT`.
- **Manual:** page load shows opening, no card revealed. `?card=QH` shows the debug line. `?card=2C` and `?card=ZZ` → no debug line, warning in browser console.
- **README:** D1, D7.

### Slice 2 — A correct guess wins
- **Build:** `parseCard` incl. `10D` and lower-case; `handle` for `Guess XX;`; `game.guess` HIT path; win text; the invalid-text fallback from §5.
- **Tests:** pinned `QH`: `handle("Guess QH;")` → text contains `Hit!`, `QH`, `won`, `1 try`; state `WON`, 1 used, `revealed` = QH. `parseCard("10D")` → `{rank:"10",suit:"D"}`; `parseCard("qh")` → Q/H. Pinned `10D` + `guess 10d;` wins.
- **Manual:** `index.html?card=10D` → `Guess 10D;` → win message.
- **README:** D3.

### Slice 3 — A wrong guess misses
- **Build:** MISS path with tries-left text.
- **Tests:** pinned `QH`: `Guess 2C;` → `Miss`, `4 tries left`, state `PLAYING`, 1 used (2C not in deck is still a normal miss — D8). `Guess QS;` (same rank, other suit) → miss. **Section-6 session part 1:** fresh pinned `QH` → 0/5 used → `Guess 2C;` miss, 1 used, still playing → `Guess QH;` HIT, `WON`, on try 2 (`in 2 tries`). Singular `1 try left` after 4 misses.
- **Manual:** `?card=QH` → `Guess 2C;` then `Guess QH;` → miss then win in 2 tries.
- **README:** D8.

### Slice 4 — Five misses lose and reveal the card
- **Build:** LOST path, loss text with reveal.
- **Tests:** pinned `QH`: five different misses (`9H`, `10H`, `JH`, `KH`, `AH`) → 5th response contains `lost` and `QH`; state `LOST`, 5 used, 0 left, `revealed` = QH. Responses 1–4 are plain misses.
- **Manual:** `?card=QH` → miss 5 times → card revealed, loss unmistakable.

### Slice 5 — Guesses after the game ends change nothing
- **Build:** IGNORED path and its message.
- **Tests:** **Section-6 session complete:** pinned `QH`: `2C` miss → `QH` win on try 2 → `Guess KH;` → text contains `game is over`; `getState()` identical before and after (status, triesUsed, guessed). Same after a **loss**: 6th guess → ignored, state unchanged, still `LOST`.
- **Manual:** win, guess again → "game is over", nothing else changes.
- **README:** D5.

### Slice 6 — EXIT
- **Build:** EXIT handling in `console.js`; input disabling in `ui.js`.
- **Tests:** `handle("EXIT")` → `{ text: "Goodbye.", exit: true }` before any guess, mid-game (after 1 miss), after a win, after a loss; `handle("exit")` also exits; `handle("EXIT;")` → invalid, `exit: false`. Every other response has `exit: false`.
- **Manual:** type `EXIT` → `Goodbye.`, input disabled.
- **README:** D6.

### Slice 7 — Invalid input is rejected without using a try
- **Build:** invalid and empty handling.
- **Tests:** pinned `QH`, for each of `Guess ZZ;`, `Guess QH` (no `;`), `Guess 1H;`, `Guess 11H;`, `Guess QX;`, `hello`, `""`, `"   "`: text contains `Guess QH;` and `No try was used`; `triesUsed` unchanged; status unchanged. Invalid line after game over → still the invalid message (not "game is over"). ` Guess QH; ` (surrounding spaces) is valid.
- **Manual:** `Guess ZZ;` → error with format; next valid miss still says `4 tries left`.
- **README:** D2.

### Slice 8 — Repeated guess warns but still uses a try
- **Build:** `guessed` list, `repeated` flag, warning prefix.
- **Tests:** pinned `QH`: `2C` → `2C` again → second text contains `already guessed 2C` and `3 tries left`; 2 used. Case-insensitive repeat (`2c`) is detected. A repeat as the 5th miss → loss text with the warning prefix and the reveal.
- **Manual:** guess the same card twice → warning, try consumed.
- **README:** D4.

---

## 9. Working with the consultant

- **Ask** (via the user) when: the brief and this document disagree; a test seems to require changing a rule; you want to change a public API name, a decision D1–D8, or a message's facts; you can't make a slice pass after a genuine root-cause attempt.
- **Don't ask** about: internal helper structure, CSS details, variable names, test grouping.
- **Question format:** `Slice N — <one-line question>`, then context (what you tried / what you observed), then your options with your recommendation. Keep it answerable without scrolling.
- After each slice, post a one-line status: `Slice N: DONE (X passed / 0 failed)` or `Slice N: BLOCKED — <reason>`.
- The consultant does not write code; they may spawn reviewers that read your commits. Expect review comments keyed by slice.

---

## 10. Verifying headlessly (in a cloud session without a visible browser)

Chromium + Playwright are preinstalled (`/opt/pw-browsers`, global `playwright` npm package). Keep verification scripts **outside the repo** (e.g. a scratch dir); they are tooling, not part of the product.

```js
// check-tests.js — run with: NODE_PATH=$(npm root -g) node check-tests.js /abs/path/to/repo
const { chromium } = require('playwright');
(async () => {
  const repo = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto('file://' + repo + '/tests.html');
  await page.waitForSelector('#summary[data-failed]', { timeout: 5000 });
  const s = page.locator('#summary');
  console.log(await s.textContent());
  const failed = Number(await s.getAttribute('data-failed'));
  const passed = Number(await s.getAttribute('data-passed'));
  if (!(passed > 0)) errors.push('no tests ran');
  if (errors.length) console.log('Console errors:', errors);
  await browser.close();
  process.exit(failed === 0 && errors.length === 0 ? 0 : 1);
})();
```
Do the manual checks the same way: open `file://.../index.html?card=QH`, `fill` the input, press `Enter`, read the log. A screenshot per slice is welcome but optional.

---

## 11. Definition of done (whole project)

Observable at the page or by running `tests.html`:
- On load, the player can tell a game is on and how many tries they have.
- After every guess: hit or miss is clear; after every miss, tries remaining are shown.
- A win is unmistakable. A loss is unmistakable and reveals the hidden card.
- After the game ends, further guesses visibly change nothing.
- `EXIT` ends the session (Goodbye + input disabled).
- `tests.html` shows `0 failed`, and the tests include: the pinned section-6 session, a lost game, and every decision D1–D8.
- Tests pin the hidden card only via `createGame(drawCard)` — no rule changed, no test-only branches in `game.js`.
- `index.html` and `tests.html` both work by double-click (`file://`), with no console errors.
- README contains run/test instructions, the `?card=` option, and D1–D8.

## 12. Do not

- Do not add dependencies, a build step, a server, ES modules, or `package.json` to the product.
- Do not call `Math.random` outside `ui.js`, or add test-only code paths to `game.js`.
- Do not skip, weaken, or delete a failing test to get green — fix the code or ask.
- Do not modify anything in `docs/`.
- Do not start slice N+1's features inside slice N.
