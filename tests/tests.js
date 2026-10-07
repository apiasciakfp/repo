// All tests, grouped by slice.
(function () {
  var NF = window.NotForFish;
  var test = NF.test, assert = NF.assert, assertEqual = NF.assertEqual;

  // Pins the hidden card through the same injection point the UI uses.
  function pinned(text) {
    return function () { return NF.parseCard(text); };
  }

  function contains(text, part) {
    assert(text.indexOf(part) !== -1, JSON.stringify(text) + " should contain " + JSON.stringify(part));
  }

  // --- Slice 0: walking skeleton ---------------------------------------
  test("smoke: deep equality ignores key order", function () {
    assertEqual({ a: 1, b: 2 }, { b: 2, a: 1 });
  });

  // --- Slice 1: game starts with a hidden card -------------------------
  test("DECK has 24 unique cards, none with rank 2-8", function () {
    assertEqual(NF.DECK.length, 24);
    var seen = {};
    NF.DECK.forEach(function (c) {
      var s = NF.cardToString(c);
      assert(!seen[s], "duplicate " + s);
      seen[s] = true;
      assert(["2", "3", "4", "5", "6", "7", "8"].indexOf(c.rank) === -1, "low rank in deck: " + s);
    });
  });

  test("RANKS and SUITS", function () {
    assertEqual(NF.RANKS, ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]);
    assertEqual(NF.SUITS, ["H", "D", "S", "C"]);
  });

  test("parseCard: valid card, invalid → null", function () {
    assertEqual(NF.parseCard("QH"), { rank: "Q", suit: "H" });
    assertEqual(NF.parseCard("ZZ"), null);
    assertEqual(NF.parseCard(""), null);
  });

  test("cardToString and sameCard", function () {
    assertEqual(NF.cardToString({ rank: "10", suit: "D" }), "10D");
    assert(NF.sameCard({ rank: "Q", suit: "H" }, { rank: "Q", suit: "H" }), "QH = QH");
    assert(!NF.sameCard({ rank: "Q", suit: "H" }, { rank: "Q", suit: "S" }), "QH != QS");
  });

  test("new game: PLAYING, 0 used, 5 left, nothing revealed", function () {
    var state = NF.createGame(pinned("QH")).getState();
    assertEqual(state, {
      status: "PLAYING", triesUsed: 0, maxTries: 5, triesLeft: 5, guessed: [], revealed: null
    });
  });

  test("drawCard is called exactly once", function () {
    var calls = 0;
    var game = NF.createGame(function () { calls++; return NF.parseCard("QH"); });
    game.getState();
    game.getState();
    assertEqual(calls, 1);
  });

  test("hidden card is not exposed while PLAYING", function () {
    var game = NF.createGame(pinned("QH"));
    assert(!("hidden" in game), "no public hidden field");
    assert(JSON.stringify(game.getState()).indexOf("QH") === -1 &&
      JSON.stringify(game.getState()).indexOf('"Q"') === -1, "state must not leak the card");
  });

  test("getState returns fresh objects with a copy of guessed", function () {
    var game = NF.createGame(pinned("QH"));
    var a = game.getState();
    a.guessed.push({ rank: "2", suit: "C" });
    a.status = "WON";
    assert(game.getState() !== a, "fresh object");
    assertEqual(game.getState().guessed, []);
    assertEqual(game.getState().status, "PLAYING");
  });

  test("D1: opening says 5 tries and how to type", function () {
    var text = NF.createConsole(NF.createGame(pinned("QH"))).opening();
    contains(text, "24-card deck");
    contains(text, "9 to A");
    contains(text, "5 tries");
    contains(text, "Guess QH;");
    contains(text, "EXIT");
  });

  // --- Slice 2: a correct guess wins ------------------------------------
  test("parseCard handles 10D and lower case", function () {
    assertEqual(NF.parseCard("10D"), { rank: "10", suit: "D" });
    assertEqual(NF.parseCard("10d"), { rank: "10", suit: "D" });
    assertEqual(NF.parseCard("qh"), { rank: "Q", suit: "H" });
    assertEqual(Object.keys(NF.parseCard("qh")), ["rank", "suit"]);
  });

  test("pinned QH: Guess QH; wins on try 1", function () {
    var game = NF.createGame(pinned("QH"));
    var res = NF.createConsole(game).handle("Guess QH;");
    contains(res.text, "Hit!");
    contains(res.text, "QH");
    contains(res.text, "won");
    contains(res.text, "1 try");
    assertEqual(res.exit, false);
    var state = game.getState();
    assertEqual(state.status, "WON");
    assertEqual(state.triesUsed, 1);
    assertEqual(state.revealed, { rank: "Q", suit: "H" });
  });

  test("game.guess HIT result", function () {
    var game = NF.createGame(pinned("QH"));
    assertEqual(game.guess(NF.parseCard("QH")), {
      outcome: "HIT", repeated: false, triesUsed: 1, triesLeft: 4, revealed: { rank: "Q", suit: "H" }
    });
  });

  test("D3: pinned 10D + lower-case guess 10d; wins", function () {
    var game = NF.createGame(pinned("10D"));
    var res = NF.createConsole(game).handle("guess 10d;");
    contains(res.text, "Hit!");
    contains(res.text, "10D");
    assertEqual(game.getState().status, "WON");
  });

  // --- Slice 3: a wrong guess misses -------------------------------------
  test("D8: pinned QH, Guess 2C; (not in deck) is a normal miss", function () {
    var game = NF.createGame(pinned("QH"));
    var res = NF.createConsole(game).handle("Guess 2C;");
    contains(res.text, "Miss");
    contains(res.text, "4 tries left");
    assertEqual(res.text, "Miss. 4 tries left.", "no not-in-deck warning");
    var state = game.getState();
    assertEqual(state.status, "PLAYING");
    assertEqual(state.triesUsed, 1);
    assertEqual(state.revealed, null);
  });

  test("game.guess MISS result reveals nothing", function () {
    var game = NF.createGame(pinned("QH"));
    assertEqual(game.guess(NF.parseCard("2C")), {
      outcome: "MISS", repeated: false, triesUsed: 1, triesLeft: 4, revealed: null
    });
  });

  test("same rank, other suit is a miss", function () {
    var game = NF.createGame(pinned("QH"));
    contains(NF.createConsole(game).handle("Guess QS;").text, "Miss");
    assertEqual(game.getState().status, "PLAYING");
  });

  test("section-6 session part 1: miss 2C then win with QH in 2 tries", function () {
    var game = NF.createGame(pinned("QH"));
    var con = NF.createConsole(game);
    var s0 = game.getState();
    assertEqual([s0.triesUsed, s0.maxTries], [0, 5]);
    contains(con.handle("Guess 2C;").text, "Miss");
    var s1 = game.getState();
    assertEqual([s1.status, s1.triesUsed], ["PLAYING", 1]);
    var res = con.handle("Guess QH;");
    contains(res.text, "Hit!");
    contains(res.text, "in 2 tries");
    var s2 = game.getState();
    assertEqual([s2.status, s2.triesUsed], ["WON", 2]);
    assertEqual(s2.guessed, [{ rank: "2", suit: "C" }, { rank: "Q", suit: "H" }]);
  });

  test("singular: 1 try left after 4 misses", function () {
    var con = NF.createConsole(NF.createGame(pinned("QH")));
    ["9H", "10H", "JH"].forEach(function (c) { con.handle("Guess " + c + ";"); });
    assertEqual(con.handle("Guess KH;").text, "Miss. 1 try left.");
  });

  // --- Slice 4: five misses lose and reveal the card --------------------
  test("pinned QH: five misses lose and reveal QH", function () {
    var game = NF.createGame(pinned("QH"));
    var con = NF.createConsole(game);
    var texts = ["9H", "10H", "JH", "KH", "AH"].map(function (c) {
      return con.handle("Guess " + c + ";").text;
    });
    texts.slice(0, 4).forEach(function (t, i) {
      assertEqual(t, "Miss. " + (4 - i) + (i === 3 ? " try" : " tries") + " left.", "response " + (i + 1));
    });
    contains(texts[4], "lost");
    contains(texts[4], "QH");
    contains(texts[4], "No tries left");
    assertEqual(game.getState(), {
      status: "LOST", triesUsed: 5, maxTries: 5, triesLeft: 0,
      guessed: ["9H", "10H", "JH", "KH", "AH"].map(NF.parseCard),
      revealed: { rank: "Q", suit: "H" }
    });
  });

  test("game.guess LOST result on the 5th miss", function () {
    var game = NF.createGame(pinned("QH"));
    ["9H", "10H", "JH", "KH"].forEach(function (c) {
      assertEqual(game.guess(NF.parseCard(c)).outcome, "MISS");
    });
    assertEqual(game.guess(NF.parseCard("AH")), {
      outcome: "LOST", repeated: false, triesUsed: 5, triesLeft: 0, revealed: { rank: "Q", suit: "H" }
    });
  });

  test("a hit on the 5th try wins, not loses", function () {
    var game = NF.createGame(pinned("QH"));
    var con = NF.createConsole(game);
    ["9H", "10H", "JH", "KH"].forEach(function (c) { con.handle("Guess " + c + ";"); });
    contains(con.handle("Guess QH;").text, "in 5 tries");
    assertEqual(game.getState().status, "WON");
  });

  // --- Slice 5: guesses after the game ends change nothing --------------
  test("D5 / section-6 session complete: guess after a win is ignored", function () {
    var game = NF.createGame(pinned("QH"));
    var con = NF.createConsole(game);
    contains(con.handle("Guess 2C;").text, "Miss");
    contains(con.handle("Guess QH;").text, "in 2 tries");
    var before = game.getState();
    var res = con.handle("Guess KH;");
    contains(res.text, "game is over");
    assertEqual(res.exit, false);
    var after = game.getState();
    assertEqual(after, before);
    assertEqual([after.status, after.triesUsed], ["WON", 2]);
  });

  test("D5: guess after a loss is ignored, still LOST", function () {
    var game = NF.createGame(pinned("QH"));
    var con = NF.createConsole(game);
    ["9H", "10H", "JH", "KH", "AH"].forEach(function (c) { con.handle("Guess " + c + ";"); });
    var before = game.getState();
    contains(con.handle("Guess QH;").text, "game is over");
    assertEqual(game.getState(), before);
    assertEqual(game.getState().status, "LOST");
  });

  test("game.guess IGNORED echoes state and reveals the card", function () {
    var game = NF.createGame(pinned("QH"));
    game.guess(NF.parseCard("2C"));
    game.guess(NF.parseCard("QH"));
    assertEqual(game.guess(NF.parseCard("2C")), {
      outcome: "IGNORED", repeated: false, triesUsed: 2, triesLeft: 3, revealed: { rank: "Q", suit: "H" }
    });
  });

  // --- Slice 6: EXIT ----------------------------------------------------
  function exitsWith(con, line) {
    assertEqual(con.handle(line), { text: "Goodbye.", exit: true }, line);
  }

  test("D6: EXIT before any guess", function () {
    exitsWith(NF.createConsole(NF.createGame(pinned("QH"))), "EXIT");
  });

  test("D6: EXIT mid-game (after 1 miss)", function () {
    var con = NF.createConsole(NF.createGame(pinned("QH")));
    assertEqual(con.handle("Guess 2C;").exit, false);
    exitsWith(con, "EXIT");
  });

  test("D6: EXIT after a win", function () {
    var con = NF.createConsole(NF.createGame(pinned("QH")));
    assertEqual(con.handle("Guess QH;").exit, false);
    exitsWith(con, "EXIT");
  });

  test("D6: EXIT after a loss", function () {
    var con = NF.createConsole(NF.createGame(pinned("QH")));
    ["9H", "10H", "JH", "KH", "AH"].forEach(function (c) {
      assertEqual(con.handle("Guess " + c + ";").exit, false);
    });
    assertEqual(con.handle("Guess KH;").exit, false, "ignored guess");
    exitsWith(con, "EXIT");
  });

  test("D3/D6: exit is case-insensitive; EXIT; is invalid", function () {
    var con = NF.createConsole(NF.createGame(pinned("QH")));
    exitsWith(con, "exit");
    exitsWith(con, "Exit");
    var res = con.handle("EXIT;");
    assertEqual(res.exit, false);
    contains(res.text, "I don't understand");
    assertEqual(con.handle("hello").exit, false);
  });

  // --- Slice 7: invalid input is rejected without using a try -----------
  var INVALID = ["Guess ZZ;", "Guess QH", "Guess 1H;", "Guess 11H;", "Guess QX;", "hello", "", "   "];

  INVALID.forEach(function (line) {
    test("D2: " + JSON.stringify(line) + " is rejected, no try used", function () {
      var game = NF.createGame(pinned("QH"));
      var con = NF.createConsole(game);
      con.handle("Guess 2C;");
      var before = game.getState();
      var res = con.handle(line);
      contains(res.text, "Guess QH;");
      contains(res.text, "No try was used");
      assertEqual(res.exit, false);
      assertEqual(game.getState(), before);
    });
  });

  test("D2: invalid text quotes the trimmed line; empty line has its own text", function () {
    var con = NF.createConsole(NF.createGame(pinned("QH")));
    assertEqual(con.handle("  hello  ").text,
      'I don\'t understand "hello". Type: Guess QH;  or  EXIT. No try was used.');
    assertEqual(con.handle("   ").text, "Type: Guess QH;  or  EXIT. No try was used.");
  });

  test("D2: invalid line after game over is still the invalid message", function () {
    var game = NF.createGame(pinned("QH"));
    var con = NF.createConsole(game);
    con.handle("Guess QH;");
    var before = game.getState();
    var res = con.handle("Guess ZZ;");
    contains(res.text, "I don't understand");
    assert(res.text.indexOf("game is over") === -1, "not the game-over text");
    assertEqual(game.getState(), before);
  });

  test("D2: surrounding spaces are fine; next miss still says 4 tries left", function () {
    var game = NF.createGame(pinned("QH"));
    var con = NF.createConsole(game);
    con.handle("Guess ZZ;");
    assertEqual(con.handle("  Guess 2C;  ").text, "Miss. 4 tries left.");
    contains(con.handle(" Guess QH; ").text, "Hit!");
  });
})();
