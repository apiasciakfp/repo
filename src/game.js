// Rules and state. Pure logic; never touches randomness or the DOM.
(function () {
  var NotForFish = window.NotForFish = window.NotForFish || {};

  var MAX_TRIES = 5;

  function copyCard(card) {
    return card ? { rank: card.rank, suit: card.suit } : null;
  }

  // drawCard: () => card. Called exactly once, here.
  NotForFish.createGame = function (drawCard) {
    var hidden = copyCard(drawCard());
    var status = "PLAYING";
    var guessed = [];

    function getState() {
      return {
        status: status,
        triesUsed: guessed.length,
        maxTries: MAX_TRIES,
        triesLeft: MAX_TRIES - guessed.length,
        guessed: guessed.map(copyCard),
        revealed: status === "PLAYING" ? null : copyCard(hidden)
      };
    }

    return { getState: getState };
  };
})();
