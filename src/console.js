// Command parsing and all player-facing text. Never touches the DOM.
(function () {
  var NotForFish = window.NotForFish = window.NotForFish || {};

  var OPENING =
    "The Magician has drawn one card from a 24-card deck (9 to A, all four suits). " +
    "It lies face down. You have 5 tries.\n" +
    "Type: Guess QH;  (rank 2-10, J, Q, K, A + suit H, D, S, C)  or  EXIT";

  var GUESS_PATTERN = /^guess\s+(\S+?)\s*;$/i;

  function tries(n) {
    return n + (n === 1 ? " try" : " tries");
  }

  function guessText(card, result) {
    var prefix = result.repeated ? "You already guessed " + NotForFish.cardToString(card) + ". " : "";
    return prefix + outcomeText(result);
  }

  function outcomeText(result) {
    if (result.outcome === "IGNORED") {
      return "The game is over. Nothing happens. Type EXIT to leave.";
    }
    if (result.outcome === "HIT") {
      return "Hit! The card was " + NotForFish.cardToString(result.revealed) +
        ". You have won, in " + tries(result.triesUsed) + ".";
    }
    if (result.outcome === "LOST") {
      return "Miss. No tries left. The Magician turns the card over: it was " +
        NotForFish.cardToString(result.revealed) + ". You have lost.";
    }
    return "Miss. " + tries(result.triesLeft) + " left.";
  }

  NotForFish.createConsole = function (game) {
    function handle(line) {
      var trimmed = String(line).trim();
      if (trimmed.toUpperCase() === "EXIT") return { text: "Goodbye.", exit: true };
      if (trimmed === "") return { text: "Type: Guess QH;  or  EXIT. No try was used.", exit: false };
      var match = GUESS_PATTERN.exec(trimmed);
      var card = match && NotForFish.parseCard(match[1]);
      if (card) return { text: guessText(card, game.guess(card)), exit: false };
      return {
        text: "I don't understand \"" + trimmed + "\". Type: Guess QH;  or  EXIT. No try was used.",
        exit: false
      };
    }

    return {
      opening: function () { return OPENING; },
      handle: handle
    };
  };
})();
