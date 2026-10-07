// Tiny hand-written test runner. Renders results into the page.
(function () {
  var NotForFish = window.NotForFish = window.NotForFish || {};
  var tests = [];

  function deepEqual(a, b) {
    if (a === b) return true;
    if (typeof a !== "object" || typeof b !== "object" || a === null || b === null) return false;
    if (Array.isArray(a) !== Array.isArray(b)) return false;
    var ka = Object.keys(a), kb = Object.keys(b);
    if (ka.length !== kb.length) return false;
    for (var i = 0; i < ka.length; i++) {
      if (!Object.prototype.hasOwnProperty.call(b, ka[i]) || !deepEqual(a[ka[i]], b[ka[i]])) return false;
    }
    return true;
  }

  NotForFish.test = function (name, fn) { tests.push({ name: name, fn: fn }); };

  NotForFish.assert = function (cond, message) {
    if (!cond) throw new Error(message || "assertion failed");
  };

  NotForFish.assertEqual = function (actual, expected, message) {
    if (!deepEqual(actual, expected)) {
      throw new Error((message ? message + ": " : "") +
        "expected " + JSON.stringify(expected) + ", got " + JSON.stringify(actual));
    }
  };

  NotForFish.runTests = function () {
    var out = document.getElementById("results");
    var passed = 0, failed = 0;
    tests.forEach(function (t) {
      var li = document.createElement("li");
      try {
        t.fn();
        passed++;
        li.className = "pass";
        li.textContent = "✔ " + t.name;
      } catch (e) {
        failed++;
        li.className = "fail";
        li.textContent = "✘ " + t.name + " — " + (e && e.message ? e.message : e);
      }
      out.appendChild(li);
    });
    var summary = document.getElementById("summary");
    summary.setAttribute("data-passed", passed);
    summary.setAttribute("data-failed", failed);
    summary.className = failed ? "fail" : "pass";
    summary.textContent = passed + " passed / " + failed + " failed";
  };
})();
