/* أبو محمد معلم بلك ومباني — سكربت الموقع */
(function () {
  "use strict";

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ============ 1 — قائمة الجوال ============ */
  var toggle = $("[data-nav-toggle]");
  var nav = $("[data-nav]");
  if (toggle && nav) {
    var label = $(".nav-toggle-text", toggle);
    var setNav = function (open) {
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (label) label.textContent = open ? "إغلاق" : "القائمة";
    };
    toggle.addEventListener("click", function () {
      setNav(!nav.classList.contains("is-open"));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a") && window.innerWidth <= 1080) setNav(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setNav(false);
        toggle.focus();
      }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 1080 && nav.classList.contains("is-open")) setNav(false);
    });
  }

  /* ============ 2 — ظل الهيدر ============ */
  var header = $("[data-header]");
  if (header) {
    var onScroll = function () {
      document.body.classList.toggle("scrolled", window.scrollY > 6);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ============ 3 — تصفية الأعمال ============ */
  var workFilters = $("[data-work-filters]");
  if (workFilters) {
    workFilters.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-work-filter]");
      if (!btn) return;
      $$("[data-work-filter]", workFilters).forEach(function (b) {
        b.classList.toggle("is-on", b === btn);
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      var cat = btn.getAttribute("data-work-filter");
      $$("[data-work-grid] .work-card").forEach(function (card) {
        var show = cat === "الكل" || card.getAttribute("data-cat") === cat;
        card.classList.toggle("is-hidden", !show);
      });
    });
  }

  /* ============ 4 — معرض الصور ============ */
  var lb = null, lbImg = null, lbCap = null, lbItems = [], lbIndex = 0;

  function buildLightbox() {
    lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "صورة مكبرة");
    lb.innerHTML =
      '<button class="lb-close" type="button" aria-label="إغلاق">✕</button>' +
      '<button class="lb-prev" type="button" aria-label="السابق">›</button>' +
      '<button class="lb-next" type="button" aria-label="التالي">‹</button>' +
      '<img alt="">' +
      '<p class="lb-cap"></p>';
    document.body.appendChild(lb);
    lbImg = $("img", lb);
    lbCap = $(".lb-cap", lb);
    $(".lb-close", lb).addEventListener("click", closeLb);
    $(".lb-prev", lb).addEventListener("click", function () { move(1); });
    $(".lb-next", lb).addEventListener("click", function () { move(-1); });
    lb.addEventListener("click", function (e) {
      if (e.target === lb) closeLb();
    });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") closeLb();
      if (e.key === "ArrowLeft") move(1);
      if (e.key === "ArrowRight") move(-1);
    });
    // سحب باللمس
    var sx = 0, sy = 0;
    lb.addEventListener("touchstart", function (e) {
      sx = e.touches[0].clientX; sy = e.touches[0].clientY;
    }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      var dx = e.changedTouches[0].clientX - sx;
      var dy = e.changedTouches[0].clientY - sy;
      if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy)) move(dx > 0 ? 1 : -1);
      else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) closeLb();
    }, { passive: true });
  }

  function showLb(i) {
    if (!lbItems.length) return;
    lbIndex = (i + lbItems.length) % lbItems.length;
    var card = lbItems[lbIndex];
    var img = card.querySelector("img");
    var pic = card.querySelector("picture");
    var webp = pic && pic.querySelector("source");
    lbImg.src = (webp && webp.getAttribute("srcset")) || img.getAttribute("src");
    lbImg.alt = img.getAttribute("alt") || "";
    lbCap.textContent = card.getAttribute("data-cap") || img.getAttribute("alt") || "";
  }

  function move(d) { showLb(lbIndex + d); }

  function openLb(cards, card) {
    if (!lb) buildLightbox();
    lbItems = cards;
    lb.classList.add("is-open");
    document.body.classList.add("lb-open");
    showLb(cards.indexOf(card));
    $(".lb-close", lb).focus();
  }

  function closeLb() {
    if (!lb) return;
    lb.classList.remove("is-open");
    document.body.classList.remove("lb-open");
  }

  $$("[data-work-grid]").forEach(function (grid) {
    grid.addEventListener("click", function (e) {
      var card = e.target.closest("[data-lightbox]");
      if (!card) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey) return; // يفتح في تبويب جديد لو أراد
      e.preventDefault();
      var visible = $$("[data-lightbox]", grid).filter(function (c) {
        return !c.classList.contains("is-hidden");
      });
      openLb(visible, card);
    });
  });

  /* ============ 5 — بطاقات حراج ============ */
  var ads = window.HARAJ_ADS || [];
  var profile = window.HARAJ_PROFILE || "";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function adCard(ad) {
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
        '<a class="btn btn-outline btn-sm" href="' + esc(ad.url) + '" target="_blank" rel="noopener">افتح الإعلان</a>' +
      '</div>' +
    '</article>';
  }

  var full = $("[data-haraj-list]");
  if (full) {
    if (!ads.length) {
      full.innerHTML = '<p class="empty">لا إعلانات منشورة حالياً. الحساب في حراج: ' +
        '<a href="' + esc(profile) + '" target="_blank" rel="noopener">' + esc(profile.replace(/^https?:\/\//, "")) + '</a></p>';
    } else {
      full.innerHTML = ads.map(adCard).join("");
    }
  }
  var mini = $("[data-haraj-mini]");
  if (mini) mini.innerHTML = ads.slice(0, 3).map(adCard).join("");

  var filterBox = $("[data-haraj-filters]");
  if (filterBox && ads.length) {
    var cats = ["الكل"].concat(Array.from(new Set(ads.map(function (a) { return a.category; }))));
    filterBox.innerHTML = cats.map(function (c, i) {
      return '<button type="button" class="chip' + (i === 0 ? " is-on" : "") + '" data-cat="' + esc(c) +
        '" aria-pressed="' + (i === 0 ? "true" : "false") + '">' + esc(c) + '</button>';
    }).join("");
    filterBox.addEventListener("click", function (e) {
      var b = e.target.closest("[data-cat]");
      if (!b) return;
      $$(".chip", filterBox).forEach(function (c) {
        c.classList.remove("is-on");
        c.setAttribute("aria-pressed", "false");
      });
      b.classList.add("is-on");
      b.setAttribute("aria-pressed", "true");
      var cat = b.getAttribute("data-cat");
      var shown = cat === "الكل" ? ads : ads.filter(function (a) { return a.category === cat; });
      var list = $("[data-haraj-list]");
      if (list) list.innerHTML = shown.map(adCard).join("");
    });
  }

  /* ============ 6 — نموذج واتساب ============ */
  var form = $("[data-wa-form]");
  if (form) {
    var setErr = function (field, msg) {
      var box = form.querySelector('[data-err="' + field.id + '"]');
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
      var name = $("#f-name"), city = $("#f-city"), work = $("#f-work");
      var size = $("#f-size"), place = $("#f-place"), hp = $("#f-hp");

      if (hp && hp.value.trim() !== "") ok = false;
      if (!name.value.trim() || name.value.trim().length < 2) { setErr(name, "اكتب اسمك أو كنية تناديك بها"); ok = false; } else setErr(name, "");
      if (!city.value.trim()) { setErr(city, "اكتب الحي أو المدينة"); ok = false; } else setErr(city, "");
      if (!work.value) { setErr(work, "اختر نوع الشغل"); ok = false; } else setErr(work, "");
      if (!size.value.trim()) { setErr(size, "اكتب الطول والارتفاع التقريبي"); ok = false; } else setErr(size, "");
      if (!place.value.trim()) { setErr(place, "اكتب وصف المكان بسطر واحد"); ok = false; } else setErr(place, "");

      if (!ok) {
        if (status) {
          status.className = "form-status is-bad";
          status.textContent = "راجع الحقول المطلوبة فوق.";
        }
        var bad = form.querySelector('[aria-invalid="true"]');
        if (bad) bad.focus();
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
        status.innerHTML = 'جهزنا رسالتك. <a href="' + url.replace(/&/g, "&amp;") +
          '" target="_blank" rel="noopener">اضغط هنا لتفتح واتساب</a> — وإذا ما فتح تلقائياً فالرقم <span dir="ltr">0531060401</span>.';
      }
      window.open(url, "_blank", "noopener");
    });

    form.addEventListener("input", function (e) {
      var t = e.target;
      if (t.getAttribute && t.getAttribute("aria-invalid") === "true" && t.value.trim()) {
        setErr(t, "");
      }
    });
  }

  /* ============ 7 — نسخ الرقم ============ */
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-copy");
      var done = function () {
        var old = b.textContent;
        b.textContent = "تم النسخ";
        setTimeout(function () { b.textContent = old; }, 1700);
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
