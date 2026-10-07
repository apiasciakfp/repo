// DOM wiring only. The single place in product code that touches the page.
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

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var line = input.value;
    print("> " + line, "echo");
    input.value = "";
    input.focus();
  });

  input.focus();
})();
