// DOM wiring only. The single place in product code that touches the page
// and the single place that uses Math.random.
(function () {
  var NotForFish = window.NotForFish = window.NotForFish || {};

  var log = document.getElementById("log");
  var form = document.getElementById("prompt");
  var input = document.getElementById("input");

  function print(text, className) {
    var div = document.createElement("div");
    div.className = "line" + (className ? " " + className : "");
    div.textContent = text;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
  }

  function randomDraw() {
    return NotForFish.DECK[Math.floor(Math.random() * NotForFish.DECK.length)];
  }

  // ?card=XX pins the hidden card (debug, D7). Only cards in the deck count.
  function pinnedCard() {
    var raw = new URLSearchParams(location.search).get("card");
    if (raw === null) return null;
    var card = NotForFish.parseCard(raw);
    var inDeck = card && NotForFish.DECK.some(function (c) { return NotForFish.sameCard(c, card); });
    if (!inDeck) {
      console.warn("Ignoring ?card=" + raw + ": not a card in the 24-card deck. Drawing at random.");
      return null;
    }
    return card;
  }

  var pinned = pinnedCard();
  var drawCard = pinned ? function () { return pinned; } : randomDraw;
  if (pinned) print("[debug] hidden card pinned via ?card=", "dim");

  var game = NotForFish.createGame(drawCard);
  var con = NotForFish.createConsole(game);
  print(con.opening());

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var line = input.value;
    print("> " + line, "echo");
    input.value = "";
    input.focus();
  });

  input.focus();
})();
