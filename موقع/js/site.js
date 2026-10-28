/* أبو محمد معلم بلك ومباني — سكربت الموقع */
(function () {
  "use strict";

  /* 1 — قائمة الجوال */
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    var setNav = function (open) {
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "إغلاق" : "القائمة";
    };
    toggle.addEventListener("click", function () {
      setNav(!nav.classList.contains("is-open"));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A" && window.innerWidth < 981) setNav(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setNav(false);
        toggle.focus();
      }
    });
  }

  /* 2 — ظل الهيدر عند التمرير */
  var header = document.querySelector("[data-header]");
  if (header) {
    var onScroll = function () {
      document.body.classList.toggle("scrolled", window.scrollY > 8);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* 3 — سنة الفوتر */
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();

  /* 4 — رسم بطاقات حراج من js/ads.js */
  var ads = window.HARAJ_ADS || [];
  var profile = window.HARAJ_PROFILE || "";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function card(ad) {
    var meta = [ad.city, ad.category].filter(Boolean).map(function (x) {
      return "<li>" + esc(x) + "</li>";
    }).join("");
    return '<article class="haraj-card">' +
      '<div class="haraj-top"><span class="haraj-tag">حراج</span>' +
        '<span class="haraj-cat">' + esc(ad.category) + '</span></div>' +
      '<div class="haraj-body">' +
        '<h3><a href="' + esc(ad.url) + '" target="_blank" rel="noopener">' + esc(ad.title) + '</a></h3>' +
        (ad.summary ? '<p>' + esc(ad.summary) + '</p>' : '') +
        '<ul class="haraj-meta">' + meta + '</ul>' +
        '<a class="btn btn-line btn-sm" href="' + esc(ad.url) + '" target="_blank" rel="noopener">افتح الإعلان في حراج</a>' +
      '</div>' +
    '</article>';
  }

  var full = document.querySelector("[data-haraj-list]");
  if (full) {
    if (!ads.length) {
      full.innerHTML = '<p class="empty">لا إعلانات منشورة حالياً. الحساب في حراج: <a href="' + esc(profile) + '" target="_blank" rel="noopener">' + esc(profile.replace(/^https?:\/\//, "")) + '</a></p>';
    } else {
      full.innerHTML = ads.map(card).join("");
    }
  }

  var mini = document.querySelector("[data-haraj-mini]");
  if (mini) {
    mini.innerHTML = ads.slice(0, 3).map(card).join("");
  }

  /* 5 — فلاتر صفحة الإعلانات */
  var filterBox = document.querySelector("[data-haraj-filters]");
  if (filterBox && ads.length) {
    var cats = ["الكل"].concat(Array.from(new Set(ads.map(function (a) { return a.category; }))));
    filterBox.innerHTML = cats.map(function (c, i) {
      return '<button type="button" class="chip' + (i === 0 ? " is-on" : "") + '" data-cat="' + esc(c) + '" aria-pressed="' + (i === 0) + '">' + esc(c) + '</button>';
    }).join("");
    filterBox.addEventListener("click", function (e) {
      var b = e.target.closest("[data-cat]");
      if (!b) return;
      filterBox.querySelectorAll(".chip").forEach(function (c) {
        c.classList.remove("is-on");
        c.setAttribute("aria-pressed", "false");
      });
      b.classList.add("is-on");
      b.setAttribute("aria-pressed", "true");
      var cat = b.getAttribute("data-cat");
      var shown = cat === "الكل" ? ads : ads.filter(function (a) { return a.category === cat; });
      var list = document.querySelector("[data-haraj-list]");
      if (list) list.innerHTML = shown.map(card).join("");
    });
  }

  /* 6 — نموذج التواصل عبر واتساب بفحص كامل */
  var form = document.querySelector("[data-wa-form]");
  if (form) {
    var setErr = function (field, msg) {
      var id = field.getAttribute("id");
      var box = form.querySelector('[data-err="' + id + '"]');
      if (msg) {
        field.setAttribute("aria-invalid", "true");
        if (box) { box.textContent = msg; box.classList.add("is-shown"); }
      } else {
        field.removeAttribute("aria-invalid");
        if (box) { box.textContent = ""; box.classList.remove("is-shown"); }
      }
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector("[data-status]");
      var ok = true;

      var name = form.querySelector("#f-name");
      var city = form.querySelector("#f-city");
      var work = form.querySelector("#f-work");
      var size = form.querySelector("#f-size");
      var place = form.querySelector("#f-place");
      var hp = form.querySelector("#f-hp");

      if (hp && hp.value.trim() !== "") { ok = false; }

      if (!name.value.trim() || name.value.trim().length < 2) { setErr(name, "اكتب اسمك أو كنية تناديك بها"); ok = false; } else setErr(name, "");
      if (!city.value.trim()) { setErr(city, "اكتب الحي أو المدينة"); ok = false; } else setErr(city, "");
      if (!work.value) { setErr(work, "اختر نوع الشغل"); ok = false; } else setErr(work, "");
      if (!size.value.trim()) { setErr(size, "اكتب الطول والارتفاع التقريبي"); ok = false; } else setErr(size, "");
      if (!place.value.trim()) { setErr(place, "اكتب وصف المكان بسطر واحد"); ok = false; } else setErr(place, "");

      if (!ok) {
        if (status) { status.className = "form-status is-bad"; status.textContent = "راجع الحقول المطلوبة أعلاه."; }
        var firstBad = form.querySelector('[aria-invalid="true"]');
        if (firstBad) firstBad.focus();
        return;
      }

      var lines = [
        "السلام عليكم أبو محمد",
        "",
        "الاسم: " + name.value.trim(),
        "الحي أو المدينة: " + city.value.trim(),
        "نوع الشغل: " + work.value,
        "الطول والارتفاع: " + size.value.trim(),
        "المكان: " + place.value.trim(),
        "",
        "أرسل لك صور المكان بعد هذا"
      ];
      var url = "https://wa.me/966531060401?text=" + encodeURIComponent(lines.join("\n"));

      if (status) {
        status.className = "form-status is-ok";
        status.innerHTML = 'جهّزنا رسالتك. <a href="' + url.replace(/&/g, "&amp;") + '" target="_blank" rel="noopener">اضغط هنا لتفتح واتساب</a> — وإن ما فتح تلقائياً فالرقم <span dir="ltr">0531060401</span>.';
      }
      window.open(url, "_blank", "noopener");
    });

    form.addEventListener("input", function (e) {
      if (e.target.getAttribute && e.target.getAttribute("aria-invalid") === "true") {
        var box = form.querySelector('[data-err="' + e.target.getAttribute("id") + '"]');
        if (e.target.value.trim()) {
          e.target.removeAttribute("aria-invalid");
          if (box) { box.textContent = ""; box.classList.remove("is-shown"); }
        }
      }
    });
  }

  /* 7 — نسخ الرقم */
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-copy");
      var done = function () {
        var old = b.textContent;
        b.textContent = "تم النسخ";
        setTimeout(function () { b.textContent = old; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(v).then(done, function () {});
      } else {
        var t = document.createElement("textarea");
        t.value = v; document.body.appendChild(t); t.select();
        try { document.execCommand("copy"); done(); } catch (err) {}
        document.body.removeChild(t);
      }
    });
  });
})();
