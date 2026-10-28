#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""مولّد صفحات الموقع.

كل صفحات الموقع تُبنى من هنا: رأس واحد وتذييل واحد وقائمة واحدة وصور أعمال واحد.
النصوص بلهجة سعودية طبيعية وتتبع الهوية/قواعد-الكتابة.md.

الاستخدام:
    python3 أدوات/بناء-الصفحات.py

لا تعدّل ملفات HTML مباشرة، عدّل هنا ثم أعد التوليد.
"""
from pathlib import Path

BASE = "https://engmohammeda.github.io/abu-mohammed/"
HARAJ = "https://haraj.com.sa/@workbuild"
WA = "https://wa.me/966531060401"
TEL = "0531060401"
OUT = Path(__file__).resolve().parent.parent / "موقع"

NAV = [
    ("index.html", "الرئيسية"),
    ("balk.html", "معلم بلك"),
    ("khadamat.html", "الخدمات"),
    ("aamal.html", "أعمالنا"),
    ("ads.html", "حراج"),
    ("about.html", "عن المعلم"),
    ("sayr.html", "طريقة الشغل"),
    ("tawasel.html", "تواصل"),
]

# أعمال حقيقية — كل صورة من إعلانات حراج الحالية
# (الملف، العنوان، الوصف القصير، التصنيف، alt)
WORK = [
    ("سور-بلك-طويل", "سور بلك بطول الشارع", "خط مستقيم من أول السور لآخره", "بلك",
     "سور بلك رمادي بطول الشارع في الرياض"),
    ("سور-بلك-حوش", "سور على حوش البيت", "الدور محاط من الجهتين ومربوط من الزاوية", "بلك",
     "سور بلك حول حوش بيت مزروع في الرياض"),
    ("سور-بلك-قريب", "سور بلك من قريب", "ارتفاع المدماك واحد من البداية للنهاية", "بلك",
     "تفصيلة قريبة لسور بلك بسماكة واحدة"),
    ("حجر-واجهة-قريب", "حجر واجهة", "ملمس الحجر وسمكه واضح من قريب", "حجر",
     "واجهة حجر تراثي ملمسها قريب من الكاميرا"),
    ("بوابة-حجر-نجدي", "بوابة حجر نجدي", "الزخرفة والأقواس والشرافات على الطراز النجدي", "حجر",
     "بوابة حجر بزخرفة نجدي وباب خشب في الرياض"),
    ("جدار-حجر-منحني", "جدار حجر منحني", "القوس مرسوم على الأرض قبل أول مدماك", "حجر",
     "جدار حجر منحني على شكل قوس في حوش"),
    ("جدار-حجر-قيد-الشغل", "قوس الحجر داخل الحوش", "الشغل على الطبيعة داخل الحوش نفسه", "حجر",
     "جدار حجر منحني قيد التنفيذ داخل حوش"),
    ("مشب-طوب", "مشب طوب", "مشب مبني بالطوب بفتحة قوس ومدخنة", "مشبات وأفران",
     "مشب طوب أحمر بفتحة قوس داخل مجلس"),
    ("فرن-طوب-داخلي", "فرن طوب للخبز", "الفتحة والقاعدة والحرارة تحت السيطرة", "مشبات وأفران",
     "فرن طوب أحمر للخبز داخل مطبخ أو حوش"),
]
WORK_CAT = ["الكل", "بلك", "حجر", "مشبات وأفران"]

SCHEMA_BIZ = """{
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "أبو محمد معلم بلك ومباني",
    "alternateName": ["أبو محمد معلم مباني", "معلم بلك الرياض", "معلم بناء الرياض"],
    "description": "معلم بلك ومباني في الرياض. بلك باليومية أو المقطوعية وأعمال الحجر والمشبات والأفران. كامل الرياض.",
    "url": "%s",
    "telephone": "+966531060401",
    "image": "%sصور/og.jpg",
    "logo": "%sصور/شعار.png",
    "address": {"@type": "PostalAddress", "addressLocality": "الرياض", "addressRegion": "منطقة الرياض", "addressCountry": "SA"},
    "areaServed": [{"@type": "City", "name": "الرياض"}, {"@type": "City", "name": "الخرج"}, {"@type": "City", "name": "المزاحمية"}, {"@type": "City", "name": "الدرعية"}, {"@type": "City", "name": "رماح"}, {"@type": "City", "name": "الحوطة"}],
    "sameAs": ["https://haraj.com.sa/@workbuild"],
    "priceRange": "على المكان"
  }""" % (BASE, BASE, BASE)


def head(title, desc, path, extra_schema=""):
    url = BASE + path
    img = BASE + "صور/og.jpg"
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="author" content="أبو محمد معلم بلك ومباني">
  <meta name="geo.region" content="SA-01">
  <meta name="geo.placename" content="الرياض">
  <meta name="theme-color" content="#121212">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="أبو محمد معلم بلك ومباني">
  <meta property="og:locale" content="ar_SA">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="أبو محمد معلم بلك ومباني في الرياض 0531060401">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{img}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="صور/شعار.png">
  <link rel="preload" href="خطوط/plex-600.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/site.css">
  <script type="application/ld+json">
  {SCHEMA_BIZ}
  </script>{extra_schema}
</head>
<body data-page="{Path(path).stem}">
  <a class="skip" href="#content">تجاوز إلى المحتوى</a>

  <header class="site-header" data-header>
    <div class="wrap">
      <a class="brand" href="index.html" aria-label="أبو محمد معلم بلك ومباني — الصفحة الرئيسية">
        <img src="صور/شعار.png" alt="" width="44" height="44">
        <span class="brand-copy">
          <strong>أبو محمد</strong>
          <span>معلم بلك ومباني</span>
        </span>
      </a>
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="nav">
        <span class="bars" aria-hidden="true"></span>
        <span class="nav-toggle-text">القائمة</span>
      </button>
      <nav class="nav" id="nav" data-nav aria-label="التنقل الرئيسي">
{nav_links(path)}
      </nav>
      <a class="header-phone ltr" href="tel:{TEL}">{TEL}</a>
    </div>
  </header>

  <main id="content">
"""


def nav_links(current):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'        <a href="{href}"{cur}>{label}</a>')
    return "\n".join(out)


FOOTER = f"""
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="صور/شعار.png" alt="" width="52" height="52" loading="lazy">
          <div>
            <strong>أبو محمد معلم بلك ومباني</strong>
            <p>بلك وحجر وأسوار ومشبات وأفران<br>كامل الرياض</p>
            <a class="ltr footer-phone" href="tel:{TEL}">{TEL}</a>
          </div>
        </div>
        <div>
          <strong>الصفحات</strong>
          <ul>
            <li><a href="balk.html">معلم بلك</a></li>
            <li><a href="khadamat.html">الخدمات</a></li>
            <li><a href="aamal.html">أعمالنا</a></li>
            <li><a href="ads.html">حراج</a></li>
            <li><a href="about.html">عن المعلم</a></li>
            <li><a href="sayr.html">طريقة الشغل</a></li>
            <li><a href="tawasel.html">تواصل</a></li>
          </ul>
        </div>
        <div>
          <strong>تواصل</strong>
          <ul>
            <li><a href="tel:{TEL}">اتصال <span class="ltr">{TEL}</span></a></li>
            <li><a href="{WA}" target="_blank" rel="noopener">واتساب</a></li>
            <li><a href="{HARAJ}" target="_blank" rel="noopener">حراج @workbuild</a></li>
          </ul>
        </div>
      </div>
      <p class="fine">
        <span>أبو محمد معلم بلك ومباني — الرياض</span>
        <span>الصور من شغل حقيقي في الرياض</span>
        <span class="ltr">{TEL}</span>
      </p>
    </div>
  </footer>

  <div class="dock">
    <a href="tel:{TEL}">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .57 3.6 1 1 0 0 1-.25 1z"/></svg>
      اتصل
    </a>
    <a href="{WA}" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.8-1.4A10 10 0 1 0 12 2m0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.8.8-2.8-.2-.3A8 8 0 1 1 12 20m4.5-5.9c-.2-.1-1.4-.7-1.6-.8s-.4-.1-.5.1-.6.8-.7 1-.3.2-.5.1a6.5 6.5 0 0 1-1.9-1.2 7.2 7.2 0 0 1-1.3-1.7c-.1-.2 0-.4.1-.5l.4-.5.2-.4v-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a1 1 0 0 0-.7.3A2.9 2.9 0 0 0 7 9.5a5 5 0 0 0 1 2.7 11.5 11.5 0 0 0 4.4 3.9 14 14 0 0 0 1.5.6 3.5 3.5 0 0 0 1.6.1 2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .1-1.2c0-.1-.2-.2-.4-.3"/></svg>
      واتساب
    </a>
    <a href="{HARAJ}" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h4v6h10V4h4v16h-4v-6H7v6H3z"/></svg>
      حراج
    </a>
  </div>

  <script src="js/ads.js"></script>
  <script src="js/site.js"></script>
</body>
</html>
"""


# ===================== تنظيف الترقيم (قاعدة الهوية 6) =====================
import re as _re

_PUNCT_MAP = {
    ".": "", "،": "", ",": "", ";": "", "؛": "", ":": "", "؟": "", "!": "",
    "«": "", "»": "", '"': "", "…": "", "(": "", ")": "", "-": " ",
}


def _clean_text(seg: str) -> str:
    """يحذف الترقيم من نص يراه الزبون ويحوّل الشرطة إلى فراغ."""
    for a, b in _PUNCT_MAP.items():
        seg = seg.replace(a, b)
    # ضغط الفراغات والمسافات قبل نهاية السطر
    seg = _re.sub(r"[ \t]{2,}", " ", seg)
    seg = _re.sub(r" +\n", "\n", seg)
    return seg


def strip_punct(html: str) -> str:
    """يطبّق التنظيف على العقد النصية فقط: يتجاهل الوسوم والسكربت والستايل."""
    parts = _re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", html, flags=_re.S)
    out = []
    for i, seg in enumerate(parts):
        if i % 2 == 1:                      # وسم أو سكربت: كما هو
            out.append(seg)
        else:
            out.append(_clean_text(seg))
    return "".join(out)


def write(path, body, title, desc, extra_schema=""):
    p = OUT / path
    html = head(title, desc, path, extra_schema) + body + FOOTER
    p.write_text(strip_punct(html), encoding="utf-8")
    print(f"  ✓ {path}")


def wa_cta(h2="أرسل صورة المكان ونشوف السعر المناسب لشغلك", sub="صورة واحدة تكفي عشان نعرف نوع الشغل ومقاسه"):
    return f"""
    <section class="section">
      <div class="wrap">
        <div class="cta-box">
          <div class="cta-text">
            <p class="eyebrow light">للطلب</p>
            <h2>{h2}</h2>
            <p>{sub}</p>
          </div>
          <div class="cta-act">
            <a class="phone-xl ltr" href="tel:{TEL}">{TEL}</a>
            <div class="actions">
              <a class="btn btn-gold" href="{WA}" target="_blank" rel="noopener">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.8-1.4A10 10 0 1 0 12 2m0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.8.8-2.8-.2-.3A8 8 0 1 1 12 20"/></svg>
                واتساب
              </a>
              <a class="btn btn-ghost" href="{HARAJ}" target="_blank" rel="noopener">حراج</a>
            </div>
          </div>
        </div>
      </div>
    </section>
"""


def work_card(slug, title, desc, cat, alt, ratio="4/3"):
    return f"""<a class="work-card" href="صور/أعمال/{slug}.jpg" data-cat="{cat}" data-lightbox data-cap="{title}">
            <span class="work-frame" style="--ratio:{ratio}">
              <picture>
                <source srcset="صور/أعمال/{slug}.webp" type="image/webp">
                <img src="صور/أعمال/{slug}.jpg" alt="{alt}" width="900" height="600" loading="lazy" decoding="async">
              </picture>
              <span class="work-tag">{cat}</span>
              <span class="work-zoom" aria-hidden="true">＋</span>
            </span>
            <span class="work-meta"><strong>{title}</strong><small>{desc}</small></span>
          </a>"""


def chips():
    return "".join(
        f'<button type="button" class="chip{" is-on" if i == 0 else ""}" data-work-filter="{c}" '
        f'aria-pressed="{"true" if i == 0 else "false"}">{c}</button>'
        for i, c in enumerate(WORK_CAT)
    )


# ============================== الرئيسية ==============================

INDEX = f"""
    <section class="hero">
      <div class="hero-copy">
        <p class="kicker">الرياض</p>
        <h1>معلم بلك ومباني في الرياض</h1>
        <p class="lede">أشتغل بيدي في البلك والحجر والأسوار<br>والمشبات والأفران وغيرها<br>ويومية أو مقطوعية على حسب اللي يريحك</p>
        <div class="actions">
          <a class="btn btn-gold" href="{WA}" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.8-1.4A10 10 0 1 0 12 2m0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.8.8-2.8-.2-.3A8 8 0 1 1 12 20"/></svg>
            أرسل صورة المكان
          </a>
          <a class="btn btn-outline" href="aamal.html">شوف أعمالنا</a>
        </div>
        <p class="hero-note">أرد على الجوال بنفسي — <span class="ltr">{TEL}</span></p>
      </div>
      <div class="hero-media">
        <picture>
          <source srcset="صور/أعمال/سور-بلك-طويل.webp" type="image/webp">
          <img src="صور/أعمال/سور-بلك-طويل.jpg" alt="سور بلك رمادي بطول الشارع في الرياض" width="900" height="504" fetchpriority="high">
        </picture>
        <span class="hero-badge">سور بلك — كامل الرياض</span>
      </div>
    </section>

    <section class="strip" aria-label="معلومات سريعة">
      <div><span class="ic" aria-hidden="true">◈</span><strong>كامل الرياض</strong><small>والخرج والمزاحمية والدرعية ورماح والحوطة عند الطلب</small></div>
      <div><span class="ic" aria-hidden="true">✋</span><strong>الشغل بيدي</strong><small>من أول مدماك لآخر مدماك</small></div>
      <div><span class="ic" aria-hidden="true">◷</span><strong>يومية أو مقطوعية</strong><small>على حسب اللي يريحك</small></div>
      <div><span class="ic" aria-hidden="true">☎</span><strong class="ltr">{TEL}</strong><small>الجوال يرد عليه أبو محمد</small></div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head-row">
          <div>
            <p class="eyebrow">أعمالنا</p>
            <h2>هذا شغل قريب من اللي تسأل عنه</h2>
            <p class="sub">صور من مواقع شغل في الرياض<br>اضغط أي صورة تكبر معك</p>
          </div>
          <a class="more" href="aamal.html">كل الأعمال</a>
        </div>
        <div class="work-grid" data-work-grid>
          {work_card("سور-بلك-طويل", "سور بلك بطول الشارع", "خط مستقيم من أول السور لآخره", "بلك", "سور بلك رمادي بطول الشارع في الرياض", "4/3")}
          {work_card("بوابة-حجر-نجدي", "بوابة حجر نجدي", "الزخرفة والأقواس على الطراز النجدي", "حجر", "بوابة حجر بزخرفة نجدي وباب خشب في الرياض", "4/3")}
          {work_card("مشب-طوب", "مشب طوب", "مشب مبني بالطوب بفتحة قوس ومدخنة", "مشبات وأفران", "مشب طوب أحمر بفتحة قوس داخل مجلس", "4/3")}
          {work_card("جدار-حجر-منحني", "جدار حجر منحني", "القوس مرسوم على الأرض قبل أول مدماك", "حجر", "جدار حجر منحني على شكل قوس في حوش", "4/3")}
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <div class="head-row">
          <div>
            <p class="eyebrow">الخدمات</p>
            <h2>أربعة أبواب تدخل منها</h2>
            <p class="sub">وكل باب تحته شغل كثير<br>اسأل عن اللي تبي وأنت مرتاح</p>
          </div>
        </div>
        <div class="svc-grid">
          <a class="svc" href="khadamat.html#block">
            <picture>
              <source srcset="صور/أعمال/سور-بلك-حوش.webp" type="image/webp">
              <img src="صور/أعمال/سور-بلك-حوش.jpg" alt="سور بلك حول حوش بيت في الرياض" width="864" height="494" loading="lazy">
            </picture>
            <span class="svc-body"><strong>البلك</strong><span>سور وجدار وغرفة وملحق ومخزن وبوابة وغيرها</span></span>
          </a>
          <a class="svc" href="khadamat.html#hajar">
            <picture>
              <source srcset="صور/أعمال/حجر-واجهة-قريب.webp" type="image/webp">
              <img src="صور/أعمال/حجر-واجهة-قريب.jpg" alt="واجهة حجر تراثي في الرياض" width="900" height="383" loading="lazy">
            </picture>
            <span class="svc-body"><strong>الحجر</strong><span>واجهات وجدران وأسوار وبوابات وكل الأعمال الأخرى</span></span>
          </a>
          <a class="svc" href="khadamat.html#fence">
            <picture>
              <source srcset="صور/أعمال/جدار-حجر-منحني.webp" type="image/webp">
              <img src="صور/أعمال/جدار-حجر-منحني.jpg" alt="جدار حجر منحني في حوش" width="810" height="472" loading="lazy">
            </picture>
            <span class="svc-body"><strong>الأسوار والجدران</strong><span>سور على الحد وجدار بين الجيران وأقواس وأركان</span></span>
          </a>
          <a class="svc" href="khadamat.html#others">
            <picture>
              <source srcset="صور/أعمال/فرن-طوب-داخلي.webp" type="image/webp">
              <img src="صور/أعمال/فرن-طوب-داخلي.jpg" alt="فرن طوب للخبز" width="825" height="757" loading="lazy">
            </picture>
            <span class="svc-body"><strong>مشبات وأفران</strong><span>مشب وفرن بالطوب وفتحة القوس والمدخنة</span></span>
          </a>
        </div>
      </div>
    </section>

    <section class="section dark">
      <div class="wrap">
        <div class="head-row">
          <div>
            <p class="eyebrow light">طريقة الشغل</p>
            <h2>أربع خطوات وتخلص</h2>
          </div>
          <a class="more light" href="sayr.html">التفاصيل</a>
        </div>
        <div class="steps">
          <article><span>01</span><h3>ترسل صورة</h3><p>صورة المكان مع المقاس التقريبي تكفي</p></article>
          <article><span>02</span><h3>نشوف السعر</h3><p>نشوف السعر المناسب لشغلك بعد ما تتضح الصورة</p></article>
          <article><span>03</span><h3>نتفق</h3><p>نتفق من أولها على النوع والسعر والبداية</p></article>
          <article><span>04</span><h3>أبدأ</h3><p>أشتغل من الزوايا والأساس لآخر مدماك</p></article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head-row">
          <div>
            <p class="eyebrow">حراج</p>
            <h2>إعلاناتي في حراج</h2>
            <p class="sub">حسابي <span dir="ltr">@workbuild</span><br>كل إعلان فيه صور وتفاصيل</p>
          </div>
          <a class="more" href="ads.html">كل الإعلانات</a>
        </div>
        <div class="haraj-stack" data-haraj-mini></div>
        <div class="center-actions">
          <a class="btn btn-dark" href="{HARAJ}" target="_blank" rel="noopener">افتح حسابي في حراج</a>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="eyebrow">النطاق</p>
        <h2>وين أشتغل</h2>
        <div class="cities" aria-label="نطاق الشغل">
          <span class="is-home">كامل الرياض</span>
          <span>الخرج</span>
          <span>المزاحمية</span>
          <span>الدرعية</span>
          <span>رماح</span>
          <span>الحوطة</span>
          <span class="note">وعند الطلب خارجها</span>
        </div>
      </div>
    </section>
{wa_cta()}
"""

# ============================== بلك ==============================

BALK = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">بلك</p>
        <h1>معلم بلك في الرياض</h1>
        <p class="lede">أبني السور والجدار والغرفة والملحق والمخزن<br>وأضبط المدماك والزوايا وأنا واقف على الشغل<br>يومية أو مقطوعية وأنت تختار</p>
        <div class="actions">
          <a class="btn btn-gold" href="{WA}" target="_blank" rel="noopener">أرسل صورة المكان</a>
          <a class="btn btn-outline" href="tel:{TEL}">اتصل <span class="ltr">{TEL}</span></a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="two-col">
          <div>
            <p class="eyebrow">الأجرة</p>
            <h2>يومية أو مقطوعية</h2>
            <p>إذا الشغل ما يتحدد بسهولة من أولها نمشي باليومية<br>وإذا كان واضح مثل السور أو الجدار أو الغرفة نمشي بالمقطوعية<br>الفرق بسيط وواضح من أول مكالمة</p>
            <a class="btn btn-dark" href="tawasel.html">احسبها معي</a>
          </div>
          <div class="compare">
            <div class="cmp">
              <strong>باليومية</strong>
              <p>أشتغل عندك بعدد أيام وتحسبها بالأيام<br>تناسب الشغل اللي يتغير وهو ماشي</p>
            </div>
            <div class="cmp">
              <strong>بالمقطوعية</strong>
              <p>سعر واحد للشغل كامل بعد ما أشوف المكان والمقاس<br>تناسب السور والجدار والغرفة</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="eyebrow">المقاسات</p>
        <h2>البلك 10 و15 و20</h2>
        <p class="sub">الاختيار على حسب الشغل مو على حسب السعر</p>
        <div class="bricks" role="list">
          <div class="brick" role="listitem"><span>10</span><strong>بلك 10</strong><p>للقواطع والأجزاء اللي ما تحمل ثقل</p></div>
          <div class="brick" role="listitem"><span>15</span><strong>بلك 15</strong><p>الأكثر استخداماً في الأسوار والجدران</p></div>
          <div class="brick" role="listitem"><span>20</span><strong>بلك 20</strong><p>للجدران اللي تحتاج سماكة وحمل أكثر</p></div>
        </div>
        <p class="note-line">المقاس النهائي ما يحدده أحد من بعيد<br>أنا أشوف المكان وأقول لك اللي يمشي</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head-row">
          <div>
            <p class="eyebrow">أمثلة</p>
            <h2>من شغل البلك</h2>
            <p class="sub">وباقي الشغل كثير غير هذا</p>
          </div>
          <a class="more" href="aamal.html">شوف الأعمال</a>
        </div>
        <div class="work-grid three">
          {work_card("سور-بلك-طويل", "سور بطول الشارع", "الخط واحد من البداية للنهاية", "بلك", "سور بلك بطول الشارع", "4/3")}
          {work_card("سور-بلك-حوش", "سور على الحوش", "محاط من الجهتين ومربوط من الزاوية", "بلك", "سور بلك حول حوش بيت", "4/3")}
          {work_card("سور-بلك-قريب", "تفصيلة السور", "سماكة المدماك واحدة", "بلك", "تفصيلة قريبة لسور بلك", "4/3")}
        </div>
      </div>
    </section>

    <section class="section dark">
      <div class="wrap">
        <p class="eyebrow light">الحساب</p>
        <h2>إيش اللي يحدد السعر</h2>
        <div class="steps">
          <article><span>01</span><h3>الطول</h3><p>كم متر طول السور أو الجدار</p></article>
          <article><span>02</span><h3>الارتفاع</h3><p>كم مدماك يرتفع فوق الأرض</p></article>
          <article><span>03</span><h3>الأرض</h3><p>مستوية أو منحدرة أو فيها خندق</p></article>
          <article><span>04</span><h3>الدخول</h3><p>المكان يسمح بالشغل وسهولة الوصول</p></article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">أسئلة</p>
        <h2>يسألها الزبون قبل ما يبدأ</h2>
        <div class="faq">
          <details><summary>أشتغل باليومية ولا مقطوعية؟</summary><p>الاثنين متاحين. اليومية تحسب بالأيام والمقطوعية سعر واحد للشغل كامل بعد ما أشوف المكان.</p></details>
          <details><summary>كم يجلس السور؟</summary><p>ما أعطيك مدة قبل ما أشوف المكان والمقاس، لأن الطول والارتفاع والدخول يغيرون الحساب كله.</p></details>
          <details><summary>تشتغل خارج الرياض؟</summary><p>الرياض كاملة. والخرج والمزاحمية والدرعية ورماح والحوطة عند الطلب.</p></details>
          <details><summary>كيف أعرف السعر؟</summary><p>أرسل صورة المكان واكتب الطول والارتفاع التقريبي ونشوف السعر المناسب لشغلك.</p></details>
          <details><summary>إيش تحتاج مني في المكان؟</summary><p>المكان يحتاج ماء وكهرباء. والأدوات أجيبها معي.</p></details>
        </div>
      </div>
    </section>
{wa_cta("قل لي نوع الشغل وأنا أقولك كيف نمشي")}
"""

# ============================== الخدمات ==============================

KHADAMAT = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">الخدمات</p>
        <h1>إيش أشتغل بالضبط</h1>
        <p class="lede">بلك وحجر وأسوار وجدران ومشبات وأفران وتشطيب<br>وكل شغل المباني اللي يفهمه المعلم بيده<br>إذا شغلك مو مذكور كلّمني وأقولك</p>
      </div>
    </section>

    <section class="section" id="block">
      <div class="wrap">
        <div class="split">
          <div>
            <p class="eyebrow">الأول</p>
            <h2>البلك</h2>
            <p>البلك هو أصل الشغل في المباني. أبني السور والجدار والغرفة والملحق والمخزن والبوابة وغيرها وأضبط المدماك من أول مدماك لآخره حتى يطلع الخط مستقيم والزوايا مربوطة.</p>
            <ul class="ticks">
              <li>سور حول البيت أو الأرض على الشارع أو على الجيران</li>
              <li>غرفة ومخزن وملحق مستقل</li>
              <li>قواطع داخلية وفصل الغرف</li>
              <li>بوابات دخول وأعمدة</li>
            </ul>
            <a class="btn btn-dark" href="balk.html">تفاصيل البلك والمقاسات</a>
          </div>
          <figure class="split-media">
            <picture>
              <source srcset="صور/أعمال/سور-بلك-حوش.webp" type="image/webp">
              <img src="صور/أعمال/سور-بلك-حوش.jpg" alt="سور بلك حول حوش بيت في الرياض" width="864" height="494" loading="lazy">
            </picture>
            <figcaption>سور على حوش البيت — كامل الرياض</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section alt" id="hajar">
      <div class="wrap">
        <div class="split flip">
          <div>
            <p class="eyebrow">الثاني</p>
            <h2>الحجر</h2>
            <p>الحجر يعطي الواجهة والمدخل شخصية. أشتغل الحجر على الجدران والواجهات والأسوار والبوابات وأهتم بسمك المدماك والخط بينه وبين اللي بعده، والقوس إذا كان في الجدار لازم يترسم على الأرض قبل أول حجر.</p>
            <ul class="ticks">
              <li>واجهات حجر على البيت</li>
              <li>جدران حجر داخل الحوش</li>
              <li>أسوار وبوابات على الطراز النجدي</li>
              <li>أقواس وجدران منحنية</li>
            </ul>
            <a class="btn btn-dark" href="aamal.html">شوف صور الحجر</a>
          </div>
          <figure class="split-media">
            <picture>
              <source srcset="صور/أعمال/بوابة-حجر-نجدي.webp" type="image/webp">
              <img src="صور/أعمال/بوابة-حجر-نجدي.jpg" alt="بوابة حجر بزخرفة نجدي وباب خشب" width="864" height="514" loading="lazy">
            </picture>
            <figcaption>بوابة حجر نجدي — كامل الرياض</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section" id="fence">
      <div class="wrap">
        <div class="split">
          <div>
            <p class="eyebrow">الثالث</p>
            <h2>الأسوار والجدران</h2>
            <p>السور أول شي يشوفه الجار والزائر. أبنيه على الحد مباشرة وأضبط الأركان والزوايا وأختم بميلان يصرّف ماء المطر بعيد عن الأساس.</p>
            <ul class="ticks">
              <li>سور على الحد النظامي للأرض</li>
              <li>جدار بلك أو حجر بين الجيران</li>
              <li>سور قصير حول الحوش</li>
              <li>جدار منحني لجمال الحوش</li>
            </ul>
          </div>
          <figure class="split-media">
            <picture>
              <source srcset="صور/أعمال/جدار-حجر-منحني.webp" type="image/webp">
              <img src="صور/أعمال/جدار-حجر-منحني.jpg" alt="جدار حجر منحني على شكل قوس" width="810" height="472" loading="lazy">
            </picture>
            <figcaption>جدار منحني — كامل الرياض</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section dark" id="others">
      <div class="wrap">
        <p class="eyebrow light">الرابع</p>
        <h2>مشبات وأفران وتشطيب وغيرها</h2>
        <div class="plain-grid four">
          <div class="plain"><span>مشب</span><h3>مشبات</h3><p>مشب طوب أو حجر في المجلس أو الحوش</p></div>
          <div class="plain"><span>فرن</span><h3>أفران</h3><p>فرن طوب للخبز والجريش والمندي</p></div>
          <div class="plain"><span>تشطيب</span><h3>تشطيب</h3><p>تشطيب الجدران والأسوار بعد البناء</p></div>
          <div class="plain"><span>أخرى</span><h3>وغيرها</h3><p>أي شغل في المباني اسأل وأنا أقولك</p></div>
        </div>
        <div class="work-grid three mt">
          {work_card("مشب-طوب", "مشب طوب", "فتحة قوس ومدخنة ومكان الحطب", "مشبات وأفران", "مشب طوب أحمر بفتحة قوس", "4/3")}
          {work_card("فرن-طوب-داخلي", "فرن طوب", "الفتحة والقاعدة والحرارة", "مشبات وأفران", "فرن طوب أحمر للخبز", "4/3")}
          {work_card("حجر-واجهة-قريب", "حجر واجهة", "الملمس والسمك من قريب", "حجر", "واجهة حجر بملمس قريب", "4/3")}
        </div>
      </div>
    </section>
{wa_cta("اختر الباب اللي يخصك وكلّمني")}
"""

# ============================== أعمالنا ==============================

def build_aamal():
    cards = "\n          ".join(work_card(*w, ratio="4/3") for w in WORK)
    grid_schema = """\n  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "ImageGallery",
    "name": "أعمال أبو محمد معلم بلك ومباني في الرياض",
    "about": "أعمال بلك وحجر ومشبات وأفران في الرياض",
    "image": [""" + ", ".join(f'"{BASE}صور/أعمال/{w[0]}.jpg"' for w in WORK) + """]
  }
  </script>"""
    return f"""
    <section class="page-head gallery-head">
      <div class="wrap">
        <p class="eyebrow">أعمالنا</p>
        <h1>أعمالنا في الرياض</h1>
        <p class="lede">أعمال حقيقية من مواقع شغل في الرياض<br>بلك وحجر وأسوار ومشبات وأفران<br>اختر النوع وشوف اللي يخصك</p>
      </div>
    </section>

    <section class="section tight">
      <div class="wrap">
        <div class="chips" role="group" aria-label="تصفية الأعمال حسب النوع" data-work-filters>
          {chips()}
        </div>
        <div class="work-grid" data-work-grid>
          {cards}
        </div>
        <p class="center-note">الصور كلها من شغل في الرياض<br>وما فيها أسماء مواقع ولا أسماء زبائن</p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="eyebrow">القراءة</p>
        <h2>كيف تعرف الشغل الزين من الصورة</h2>
        <div class="inspect">
          <div class="insp"><span>01</span><h3>الخط</h3><p>استقامة المدماك على طول الجدار ووضوح الأفق في أعلى السور</p></div>
          <div class="insp"><span>02</span><h3>الركن</h3><p>كيف تربط الزاوية بين جدارين، وهذا اللي يمسك الشكل كامل</p></div>
          <div class="insp"><span>03</span><h3>الميلان</h3><p>نهاية السور المسؤولة عن تصريف الماء بعيد عن الأساس</p></div>
          <div class="insp"><span>04</span><h3>الحجر</h3><p>تساوي السمك بين المدماك والمدماك وسلامة القوس في المنحني</p></div>
        </div>
      </div>
    </section>
{wa_cta("شفت اللي يعجبك؟ كلّمني عليه", "أرسل صورة مكانك وأنا أقرب لك اللي شفته")}
""", grid_schema


# ============================== حراج ==============================

ADS = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">حراج</p>
        <h1>إعلاناتي في حراج</h1>
        <p class="lede">كل إعلان أنزله في حراج يجي هنا<br>من الأحدث للأقدم<br>والرابط يفتح الإعلان في مكانه الأصلي</p>
        <div class="actions">
          <a class="btn btn-dark" href="{HARAJ}" target="_blank" rel="noopener">حسابي <span dir="ltr">@workbuild</span></a>
          <a class="btn btn-outline" href="tel:{TEL}">اتصل <span class="ltr">{TEL}</span></a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head-row">
          <div>
            <p class="eyebrow">القائمة</p>
            <h2>كل الإعلانات</h2>
            <p class="sub">اضغط نوع الشغل يظهر لك إعلاناته</p>
          </div>
        </div>
        <div class="chips" data-haraj-filters role="group" aria-label="تصفية الإعلانات حسب النوع"></div>
        <div class="haraj-grid" data-haraj-list>
          <noscript><p class="empty">القائمة تحتاج تفعيل الجافاسكربت، وتقدر تفتح الحساب مباشرة من <a href="{HARAJ}">haraj.com.sa/@workbuild</a></p></noscript>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="eyebrow">الحساب</p>
        <h2>حسابي في حراج</h2>
        <table class="info-table">
          <tr><th>الاسم في حراج</th><td>أبو محمد معلم مباني</td></tr>
          <tr><th>المعرّف</th><td><span dir="ltr">@workbuild</span></td></tr>
          <tr><th>المدينة</th><td>كامل الرياض</td></tr>
          <tr><th>الرابط</th><td><a href="{HARAJ}" target="_blank" rel="noopener">haraj.com.sa/@workbuild</a></td></tr>
        </table>
      </div>
    </section>
{wa_cta("إعلانك اللي يخصك موجود على حراج")}
"""

# ============================== عن المعلم ==============================

ABOUT = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">التعريف</p>
        <h1>أبو محمد معلم بلك ومباني</h1>
        <p class="lede">أنا معلم مباني أشتغل بيدي<br>ما عندي مكتب ولا موظفين<br>أتابع الشغل وأرد على جوالك بنفسي</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="split">
          <div>
            <p class="eyebrow">من أنا</p>
            <h2>تعرفني قبل ما تكلّمني</h2>
            <p>اسمي أبو محمد ومعلم بلك ومباني في الرياض. شغلي كله في البلك والحجر والأسوار والجدران والملاحق والغرف ومعه المشبات والأفران والتشطيب وغيرها.</p>
            <p>أشتغل يومية أو مقطوعية على حسب اللي يريحك وأحدد السعر بعد ما أشوف المكان وأعرف الطول والارتفاع.</p>
            <p>ما عندي مكتب ولا موظفين. أنا اللي يجيك وأنا اللي يبني وأنا اللي يرد على جوالك.</p>
            <div class="sig">
              <strong>أبو محمد</strong>
              <span>معلم بلك ومباني — الرياض</span>
              <a class="ltr" href="tel:{TEL}">{TEL}</a>
            </div>
          </div>
          <figure class="split-media tall">
            <picture>
              <source srcset="صور/أعمال/حجر-واجهة-قريب.webp" type="image/webp">
              <img src="صور/أعمال/حجر-واجهة-قريب.jpg" alt="واجهة حجر بسمك متساوٍ بين المدماك والمدماك" width="900" height="383" loading="lazy">
            </picture>
            <figcaption>الحجر ما ينفع فيه استعجال — كامل الرياض</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section dark">
      <div class="wrap">
        <p class="eyebrow light">الشارة</p>
        <h2>الأهم الثقة والأمانة</h2>
        <p class="big-line">الثقة ما تنكتب في إعلان، تنبنى مدماك ورا مدماك<br>إذا قلت لك سعر فهو السعر وإذا قلت لك يوم جيت فيه<br>وإذا في المكان شي ما يخدم الشغل أقولك قبل ما أبدأ</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head-row">
          <div>
            <p class="eyebrow">الحدود</p>
            <h2>إيش ما أقوله</h2>
            <p class="sub">الكلام اللي ما أنطقه أحفظه كما أحفظ الشغل</p>
          </div>
        </div>
        <ul class="ticks big">
          <li>ما أوصف الشغل بكلام، لأن الشغل يتشاف ما يتقال</li>
          <li>ما أوعد بمدة قبل ما أشوف المكان</li>
          <li>ما أذكر أسماء أحياء ولا أسماء زبائن</li>
          <li>ما أنشر صورة من عندك قبل إذنك</li>
          <li>ما أضيف رقمي على شغل غيري</li>
        </ul>
      </div>
    </section>
{wa_cta("تعرفني الآن، كلّمني")}
"""

# ============================== طريقة الشغل ==============================

SAYR = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">طريقة الشغل</p>
        <h1>من الصورة إلى التسليم</h1>
        <p class="lede">سبع خطوات واضحة<br>تعرف في كل خطوة وين أنت<br>وإيش اللي عليك وإيش اللي عليّ</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <ol class="timeline">
          <li><span>01</span><div><h3>الصورة</h3><p>ترسل صورة المكان من بعيد ومن قريب إذا قدرت.</p></div></li>
          <li><span>02</span><div><h3>القياس</h3><p>تكتب الطول والارتفاع التقريبي وأنا أسألك عن الأرض والدخول.</p></div></li>
          <li><span>03</span><div><h3>النوع</h3><p>نتفق يومية أو مقطوعية، وكل نوع له حسابه.</p></div></li>
          <li><span>04</span><div><h3>السعر</h3><p>نشوف السعر المناسب لشغلك بعد ما تتضح الصورة كاملة.</p></div></li>
          <li><span>05</span><div><h3>الاتفاق</h3><p>نتفق من أولها على البداية والنوع والسعر.</p></div></li>
          <li><span>06</span><div><h3>الشغل</h3><p>أبدأ بالزوايا والأساس وأكمل مدماك ورا مدماك.</p></div></li>
          <li><span>07</span><div><h3>التسليم</h3><p>تشوف الشغل كامل قبل ما نقفل الحساب.</p></div></li>
        </ol>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <div class="head-row">
          <div>
            <p class="eyebrow">الرسالة</p>
            <h2>إيش ترسل في أول رسالة</h2>
            <p class="sub">أربع أشياء تكفي</p>
          </div>
          <a class="more" href="tawasel.html">افتح النموذج</a>
        </div>
        <table class="info-table">
          <tr><th>صورة المكان</th><td>صورة واحدة على الأقل ويفضّل اثنتين.</td></tr>
          <tr><th>الطول والارتفاع</th><td>تقديري ولو بعدد الخطوات.</td></tr>
          <tr><th>نوع الشغل</th><td>سور أو جدار أو غرفة أو ملحق أو حجر أو غيرها.</td></tr>
          <tr><th>الحي أو المدينة</th><td>اسم الحي يكفي وما ينشر في الموقع.</td></tr>
        </table>
      </div>
    </section>

    <section class="section dark">
      <div class="wrap">
        <p class="eyebrow light">بعد الاتفاق</p>
        <h2>إيش يصير بعد ما نتفق</h2>
        <div class="steps">
          <article><span>01</span><h3>البداية</h3><p>أحدد يوم البداية معك بعد الاتفاق</p></article>
          <article><span>02</span><h3>الأدوات</h3><p>أجيب أدواتي والمكان يحتاج ماء وكهرباء</p></article>
          <article><span>03</span><h3>المتابعة</h3><p>تشوف الشغل كل يوم وتقول لي ملاحظتك</p></article>
          <article><span>04</span><h3>الختام</h3><p>نراجع الشغل مع بعض قبل الإغلاق</p></article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">أسئلة</p>
        <h2>أسئلة على الطريقة</h2>
        <div class="faq">
          <details><summary>لازم تجي تشوف المكان؟</summary><p>الأفضل أشوف المكان على الطبيعة. وإذا تعذر فالصور والمقاسات تكفي في الغالب.</p></details>
          <details><summary>كيف تكون طريقة الدفع؟</summary><p>نتفق عليها في الاتفاق نفسه وكل شي يكون واضح من أولها.</p></details>
          <details><summary>إيش اللي تحتاجه مني في المكان؟</summary><p>ماء وكهرباء ومكان يسمح بالشغل. والأدوات أجيبها معي من عندي.</p></details>
        </div>
      </div>
    </section>
{wa_cta("ابدأ من الصورة", "صورة واحدة على الواتساب ونمشي من هناك")}
"""

# ============================== تواصل ==============================

TAWASEL = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">تواصل</p>
        <h1>كلّمني بأي طريقة تريحك</h1>
        <p class="lede">الرقم واحد<br>اتصال أو واتساب أو رسالة عبر حراج<br>والجوال يرد عليه أبو محمد نفسه</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="channels">
          <a class="channel call" href="tel:{TEL}">
            <span class="ch-ic" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .57 3.6 1 1 0 0 1-.25 1z"/></svg>
            </span>
            <strong>اتصال</strong>
            <span class="ltr big-num">{TEL}</span>
            <span class="ch-note">الأسرع إذا عندك سؤال قصير</span>
          </a>
          <a class="channel wa" href="{WA}" target="_blank" rel="noopener">
            <span class="ch-ic" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.8-1.4A10 10 0 1 0 12 2m0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.8.8-2.8-.2-.3A8 8 0 1 1 12 20"/></svg>
            </span>
            <strong>واتساب</strong>
            <span class="ltr big-num">{TEL}</span>
            <span class="ch-note">أرسل الصور والمقاسات هنا</span>
          </a>
          <a class="channel hr" href="{HARAJ}" target="_blank" rel="noopener">
            <span class="ch-ic" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M3 4h4v6h10V4h4v16h-4v-6H7v6H3z"/></svg>
            </span>
            <strong>حراج</strong>
            <span class="ltr big-num">@workbuild</span>
            <span class="ch-note">كل الإعلانات في مكان واحد</span>
          </a>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <div class="contact-grid">
          <div class="contact-aside">
            <p class="eyebrow">النموذج</p>
            <h2>جهّز رسالتك هنا</h2>
            <p>املأ الحقول وبنجهز لك رسالة واتساب كاملة ما تحتاج تكتب شي من جديد.</p>
            <p class="mini-note">ما نحفظ بياناتك في أي مكان، الرسالة ترسل من جوالك على واتساب.</p>
            <a class="phone-xl ltr" href="tel:{TEL}">{TEL}</a>
            <button class="btn btn-outline copy-btn" type="button" data-copy="0531060401">انسخ الرقم</button>
          </div>
          <form class="form" data-wa-form novalidate>
            <p class="form-legend">كل الحقول المطلوبة معلّمة بـ<span class="req">*</span></p>
            <div class="row">
              <div class="field">
                <label for="f-name">الاسم أو الكنية <span class="req">*</span></label>
                <input id="f-name" name="name" type="text" autocomplete="name" placeholder="مثال أبو سعد" required>
                <p class="field-error" data-err="f-name"></p>
              </div>
              <div class="field">
                <label for="f-city">الحي أو المدينة <span class="req">*</span></label>
                <input id="f-city" name="city" type="text" autocomplete="address-level2" placeholder="مثال الرياض" required>
                <p class="field-error" data-err="f-city"></p>
              </div>
            </div>
            <div class="row">
              <div class="field">
                <label for="f-work">نوع الشغل <span class="req">*</span></label>
                <select id="f-work" name="work" required>
                  <option value="">اختر نوع الشغل</option>
                  <option>سور بلك</option>
                  <option>جدار بلك</option>
                  <option>غرفة أو ملحق</option>
                  <option>حجر وواجهات</option>
                  <option>بوابة</option>
                  <option>مشب أو فرن</option>
                  <option>غير ذلك</option>
                </select>
                <p class="field-error" data-err="f-work"></p>
              </div>
              <div class="field">
                <label for="f-size">الطول والارتفاع <span class="req">*</span></label>
                <input id="f-size" name="size" type="text" placeholder="مثال ٢٠ متر طول و٢ متر ارتفاع" required>
                <p class="field-error" data-err="f-size"></p>
              </div>
            </div>
            <div class="field">
              <label for="f-place">وصف المكان <span class="req">*</span></label>
              <textarea id="f-place" name="place" placeholder="سطر واحد: إيش تبي تبني ووين بالضبط والأرض مستوية أو منحدرة" required></textarea>
              <p class="field-error" data-err="f-place"></p>
            </div>
            <div class="hp" aria-hidden="true">
              <label for="f-hp">اتركه فارغاً</label>
              <input id="f-hp" name="hp" type="text" tabindex="-1" autocomplete="off">
            </div>
            <button class="btn btn-gold wide" type="submit">جهّز رسالة واتساب</button>
            <p class="form-status" data-status role="status" aria-live="polite"></p>
            <p class="mini-note center">الصور ترسلها بعد فتح واتساب</p>
          </form>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">الروابط</p>
        <h2>أرقام وروابط</h2>
        <table class="info-table">
          <tr><th>الجوال</th><td><a class="ltr" href="tel:{TEL}">{TEL}</a></td></tr>
          <tr><th>واتساب</th><td><a href="{WA}" target="_blank" rel="noopener">wa.me/966531060401</a></td></tr>
          <tr><th>حراج</th><td><a href="{HARAJ}" target="_blank" rel="noopener">haraj.com.sa/@workbuild</a></td></tr>
          <tr><th>النطاق</th><td>كامل الرياض والخرج والمزاحمية والدرعية ورماح والحوطة عند الطلب</td></tr>
          <tr><th>الأجرة</th><td>يومية أو مقطوعية</td></tr>
        </table>
      </div>
    </section>
{wa_cta("الرقم واحد والطريق واحد")}
"""

# ============================== 404 ==============================

NOTFOUND = f"""
    <section class="page-head tall">
      <div class="wrap">
        <p class="eyebrow">404</p>
        <h1>هذي الصفحة ما هي موجودة</h1>
        <p class="lede">الرابط اللي فتحته يمكن تغيّر أو انكتب بغير شكله<br>ما عليه، ارجع من هنا</p>
        <div class="actions">
          <a class="btn btn-gold" href="index.html">الرئيسية</a>
          <a class="btn btn-outline" href="aamal.html">أعمالنا</a>
          <a class="btn btn-outline" href="tel:{TEL}">اتصل <span class="ltr">{TEL}</span></a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">الصفحات</p>
        <h2>وين تقدر تروح</h2>
        <div class="plain-grid">
          <a class="plain" href="balk.html"><span>01</span><h3>معلم بلك</h3><p>اليومية والمقطوعية والمقاسات</p></a>
          <a class="plain" href="khadamat.html"><span>02</span><h3>الخدمات</h3><p>بلك وحجر وأسوار وغيرها</p></a>
          <a class="plain" href="aamal.html"><span>03</span><h3>أعمالنا</h3><p>صور من شغل حقيقي</p></a>
          <a class="plain" href="ads.html"><span>04</span><h3>حراج</h3><p>كل الإعلانات</p></a>
          <a class="plain" href="about.html"><span>05</span><h3>عن المعلم</h3><p>من أنا وإيش ما أقوله</p></a>
          <a class="plain" href="sayr.html"><span>06</span><h3>طريقة الشغل</h3><p>من الصورة إلى التسليم</p></a>
        </div>
      </div>
    </section>
"""


PAGES = [
    ("index.html", INDEX, "أبو محمد معلم بلك ومباني في الرياض",
     "أبو محمد معلم بلك ومباني في الرياض. بلك باليومية أو المقطوعية وأعمال الحجر والأسوار والمشبات والأفران. كامل الرياض. 0531060401", ""),
    ("balk.html", BALK, "معلم بلك في الرياض يومية أو مقطوعية",
     "معلم بلك في الرياض باليومية أو المقطوعية. سور وجدار وغرفة وملحق ومقاسات البلك 10 و15 و20 وأسئلة الزبون قبل الشغل. 0531060401", ""),
    ("khadamat.html", KHADAMAT, "خدمات معلم البلك والمباني في الرياض",
     "خدمات معلم البلك والمباني في الرياض: البلك والحجر والأسوار والجدران والمشبات والأفران والتشطيب وغيرها. كامل الرياض. 0531060401", ""),
    ("ads.html", ADS, "إعلانات أبو محمد في حراج الرياض",
     "إعلانات أبو محمد معلم مباني في حراج: بناء بلك وحجر تراثي ومباني ومشبات وأفران في الرياض. كل الإعلانات بروابطها. 0531060401", """\n  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": "%s"},
      {"@type": "ListItem", "position": 2, "name": "حراج", "item": "%sads.html"}
    ]
  }
  </script>""" % (BASE, BASE)),
    ("about.html", ABOUT, "عن أبو محمد معلم بلك ومباني في الرياض",
     "عن أبو محمد معلم بلك ومباني في الرياض: معلم مباني يعمل بيده في البلك والحجر والأسوار والمشبات. يومية أو مقطوعية. 0531060401", ""),
    ("sayr.html", SAYR, "طريقة الشغل من الصورة إلى التسليم",
     "طريقة الشغل مع أبو محمد معلم بلك في الرياض: الصورة والقياس والنوع والسعر والاتفاق والشغل والتسليم في سبع خطوات واضحة. 0531060401", ""),
    ("tawasel.html", TAWASEL, "تواصل مع أبو محمد معلم بلك ومباني",
     "تواصل مع أبو محمد معلم بلك ومباني في الرياض: اتصال وواتساب وحساب حراج ونموذج رسالة جاهز يفتح واتساب بكل التفاصيل. 0531060401", ""),
    ("404.html", NOTFOUND, "الصفحة غير موجودة | أبو محمد معلم بلك",
     "", ""),
]


def main():
    print("== توليد الصفحات ==")
    for name, body, title, desc, extra in PAGES:
        write(name, body, title, desc, extra)
    aamal_body, aamal_schema = build_aamal()
    write("aamal.html", aamal_body, "أعمالنا في الرياض بلك وحجر ومشبات وأفران",
          "أعمال أبو محمد معلم بلك ومباني في الرياض بالصور: أسوار بلك وبوابات حجر وجدران منحنية ومشبات وأفران من شغل حقيقي. 0531060401",
          aamal_schema)

    # 404 بلا canonical وبلا OG عن قصد
    import re
    p = OUT / "404.html"
    t = p.read_text(encoding="utf-8")
    t = re.sub(r'\n  <link rel="canonical".*?(?=\n  <link rel="icon")', "", t, flags=re.S)
    t = re.sub(r'\n  <meta property="og:[^\n]*', "", t)
    t = re.sub(r'\n  <meta name="twitter:[^\n]*', "", t)
    p.write_text(t, encoding="utf-8")
    print("  ✓ 404.html بلا canonical وبلا وسوم مشاركة")
    print("  أطوال: " + " | ".join(f"{n} {len(ti)}/{len(de)}" for n, _, ti, de, _ in PAGES if de))


if __name__ == "__main__":
    main()
