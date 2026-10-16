(function () {
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("nav-open", open);
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-open");
      });
    });
  }

  var form = document.querySelector("[data-quote]");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var data = new FormData(form);
    var lines = [
      "السلام عليكم",
      "أبي سعر على الشغل:",
      "النوع: " + data.get("type"),
      "المقاس: " + data.get("size"),
      "المكان: " + data.get("place")
    ];
    var note = String(data.get("note") || "").trim();
    if (note) lines.push("ملاحظة: " + note);
    var url = "https://wa.me/966531060401?text=" + encodeURIComponent(lines.join("\n"));
    window.open(url, "_blank", "noopener");
  });
})();
