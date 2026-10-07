// Command parsing and all player-facing text. Never touches the DOM or window.
(function () {
  var NotForFish = window.NotForFish = window.NotForFish || {};

  var OPENING =
    "The Magician has drawn one card from a 24-card deck (9 to A, all four suits). " +
    "It lies face down. You have 5 tries.\n" +
    "Type: Guess QH;  (rank 2-10, J, Q, K, A + suit H, D, S, C)  or  EXIT";

  NotForFish.createConsole = function (game) {
    return {
      opening: function () { return OPENING; }
    };
  };
})();
