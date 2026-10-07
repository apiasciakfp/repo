// Cards and deck. Pure logic.
(function () {
  var NotForFish = window.NotForFish = window.NotForFish || {};

  var RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];
  var SUITS = ["H", "D", "S", "C"];
  var DECK_RANKS = ["9", "10", "J", "Q", "K", "A"];

  var DECK = [];
  DECK_RANKS.forEach(function (rank) {
    SUITS.forEach(function (suit) {
      DECK.push({ rank: rank, suit: suit });
    });
  });

  // Rank then suit, no space: "QH", "qh", "10d". Normalized upper-case. Invalid → null.
  function parseCard(text) {
    if (typeof text !== "string" || text.length < 2) return null;
    text = text.toUpperCase();
    var rank = text.slice(0, -1);
    var suit = text.slice(-1);
    if (RANKS.indexOf(rank) === -1 || SUITS.indexOf(suit) === -1) return null;
    return { rank: rank, suit: suit };
  }

  function cardToString(card) {
    return card.rank + card.suit;
  }

  function sameCard(a, b) {
    return a.rank === b.rank && a.suit === b.suit;
  }

  NotForFish.RANKS = RANKS;
  NotForFish.SUITS = SUITS;
  NotForFish.DECK = DECK;
  NotForFish.parseCard = parseCard;
  NotForFish.cardToString = cardToString;
  NotForFish.sameCard = sameCard;
})();
