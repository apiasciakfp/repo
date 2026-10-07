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
})();
