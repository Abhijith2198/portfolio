// "Show grid" lays the 12-column layout grid over the page and labels key text
// with its live type settings: weight, width, size and line height.
(function () {
  var root = document.documentElement;
  var button = document.querySelector(".grid-toggle");
  if (!button) return;
  var overlay = null;

  function buildOverlay() {
    overlay = document.createElement("div");
    overlay.className = "grid-overlay";
    overlay.setAttribute("aria-hidden", "true");
    var cols = document.createElement("div");
    cols.className = "container grid-overlay__cols";
    for (var i = 0; i < 12; i++) cols.appendChild(document.createElement("span"));
    overlay.appendChild(cols);
    document.body.appendChild(overlay);
  }

  function labelText(el) {
    var cs = getComputedStyle(el);
    var size = parseFloat(cs.fontSize);
    var lh = cs.lineHeight === "normal" ? "normal" : (parseFloat(cs.lineHeight) / size).toFixed(2);
    return "wght " + cs.fontWeight + "  wdth " + cs.fontStretch + "  " + Math.round(size) + "px/" + lh;
  }

  function refreshLabels() {
    document.querySelectorAll("[data-spec]").forEach(function (el) {
      el.setAttribute("data-spec", labelText(el));
    });
  }

  button.addEventListener("click", function () {
    var on = !root.classList.contains("show-grid");
    if (on && !overlay) buildOverlay();
    if (on) refreshLabels();
    root.classList.toggle("show-grid", on);
    button.setAttribute("aria-pressed", String(on));
  });

  window.addEventListener("resize", function () {
    if (root.classList.contains("show-grid")) refreshLabels();
  });
})();
