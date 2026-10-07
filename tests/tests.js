// All tests, grouped by slice.
(function () {
  var NF = window.NotForFish;
  var test = NF.test, assertEqual = NF.assertEqual;

  // --- Slice 0: walking skeleton ---------------------------------------
  test("smoke: deep equality ignores key order", function () {
    assertEqual({ a: 1, b: 2 }, { b: 2, a: 1 });
  });
})();
