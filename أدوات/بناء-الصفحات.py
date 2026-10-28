#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""مولّد صفحات الموقع.

كل صفحات الموقع تُبنى من هذا الملف: رأس واحد وتذييل واحد وقائمة واحدة،
ونصوص فريدة لكل صفحة بلا تكرار في العناوين.

الاستخدام:
    python3 أدوات/بناء-الصفحات.py

لا تعدّل ملفات HTML مباشرة، عدّل هنا ثم أعد التوليد.
"""
# -*- coding: utf-8 -*-
"""مولد صفحات الموقع — مصدر واحد للهيدر والتذييل والميتا، ونصوص فريدة لكل صفحة."""
from pathlib import Path
import html as H

BASE = "https://engmohammeda.github.io/abu-mohammed/"
HARAJ = "https://haraj.com.sa/@workbuild"
WA = "https://wa.me/966531060401"
TEL = "0531060401"
OUT = Path(__file__).resolve().parent.parent / "موقع"

NAV = [
    ("index.html", "الرئيسية"),
    ("balk.html", "معلم بلك"),
    ("khadamat.html", "الخدمات"),
    ("aamal.html", "الأعمال"),
    ("ads.html", "الإعلانات"),
    ("about.html", "عن المعلم"),
    ("sayr.html", "طريقة العمل"),
    ("tawasel.html", "تواصل"),
]

SCHEMA_BIZ = """{
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "أبو محمد معلم بلك ومباني",
    "alternateName": ["أبو محمد معلم مباني", "معلم بلك الرياض"],
    "description": "معلم بلك ومباني في الرياض. بناء بلك باليومية أو المقطوعية وكل أعمال البلك والحجر.",
    "url": "%s",
    "telephone": "+966531060401",
    "image": "%sصور/og.jpg",
    "logo": "%sصور/شعار.png",
    "address": {"@type": "PostalAddress", "addressLocality": "الرياض", "addressRegion": "منطقة الرياض", "addressCountry": "SA"},
    "areaServed": [{"@type": "City", "name": "الرياض"}, {"@type": "City", "name": "الخرج"}, {"@type": "City", "name": "المزاحمية"}, {"@type": "City", "name": "الدرعية"}, {"@type": "City", "name": "رماح"}, {"@type": "City", "name": "الحوطة"}],
    "sameAs": ["https://haraj.com.sa/@workbuild"],
    "priceRange": "على المكان"
  }""" % (BASE, BASE, BASE)


def head(title, desc, path, screenshot=False):
    url = BASE + path
    img = BASE + "صور/og.jpg"
    extra_schema = ""
    if screenshot:
        extra_schema = """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": "%s"},
      {"@type": "ListItem", "position": 2, "name": "الإعلانات", "item": "%sads.html"}
    ]
  }
  </script>""" % (BASE, BASE)
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
  <meta name="theme-color" content="#202020">
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
        <img src="صور/شعار.png" alt="" width="40" height="40">
        <span class="brand-copy">
          <strong>أبو محمد</strong>
          <span>معلم بلك ومباني</span>
        </span>
      </a>
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="nav">القائمة</button>
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
        <div>
          <strong>أبو محمد معلم بلك ومباني</strong>
          <p>بلك · أسوار · حجر · جدران<br>كامل الرياض</p>
          <a class="ltr" href="tel:{TEL}">{TEL}</a>
        </div>
        <div>
          <strong>الصفحات</strong>
          <ul>
            <li><a href="balk.html">معلم بلك</a></li>
            <li><a href="khadamat.html">الخدمات</a></li>
            <li><a href="aamal.html">الأعمال</a></li>
            <li><a href="ads.html">الإعلانات</a></li>
            <li><a href="about.html">عن المعلم</a></li>
            <li><a href="tawasel.html">تواصل</a></li>
          </ul>
        </div>
        <div>
          <strong>حسابي في حراج</strong>
          <p><a href="{HARAJ}" target="_blank" rel="noopener">haraj.com.sa/@workbuild</a></p>
          <p><a href="{WA}" target="_blank" rel="noopener">واتساب</a></p>
        </div>
      </div>
      <p class="fine">الصور توضّح نوع الشغل<br>بلا أسماء أحياء وبلا دعاوى بلا دليل<br>الحكم للزبون بعد ما يشوف بعينه</p>
    </div>
  </footer>

  <div class="dock">
    <a href="tel:{TEL}">اتصال</a>
    <a href="{WA}" target="_blank" rel="noopener">واتساب</a>
    <a href="{HARAJ}" target="_blank" rel="noopener">حراج</a>
  </div>

  <script src="js/ads.js"></script>
  <script src="js/site.js"></script>
</body>
</html>
"""


def write(path, body, title, desc, screenshot=False):
    p = OUT / path
    p.write_text(head(title, desc, path, screenshot) + body + FOOTER, encoding="utf-8")
    print(f"  ✓ {path}")


def cta_block(h2="أرسل صورة المكان ونشوف السعر المناسب لشغلك"):
    return f"""
    <section class="section">
      <div class="wrap">
        <div class="cta">
          <div>
            <p class="eyebrow">للطلب</p>
            <h2>{h2}</h2>
          </div>
          <div>
            <a class="phone-xl ltr" href="tel:{TEL}">{TEL}</a>
            <div class="actions">
              <a class="btn btn-brick" href="{WA}" target="_blank" rel="noopener">واتساب</a>
              <a class="btn btn-ink" href="https://haraj.com.sa/@workbuild" target="_blank" rel="noopener">حراج</a>
            </div>
          </div>
        </div>
      </div>
    </section>
"""


# ============================ المحتوى ============================

INDEX = f"""
    <section class="hero">
      <div class="hero-copy">
        <p class="kicker">الرياض</p>
        <h1>معلم بلك ومباني في الرياض</h1>
        <p class="lede">معلم بلك باليومية أو المقطوعية<br>وكل أعمال البلك والحجر<br>أرسل صورة المكان ونشوف السعر المناسب لشغلك</p>
        <div class="actions">
          <a class="btn btn-brick" href="{WA}" target="_blank" rel="noopener">أرسل صورة المكان</a>
          <a class="btn btn-ink" href="{HARAJ}" target="_blank" rel="noopener">إعلاناتي في حراج</a>
        </div>
      </div>
      <div class="hero-media">
        <img src="صور/سور-بلك.jpg" alt="سور بلك رمادي مستقيم في الرياض" width="1408" height="768" fetchpriority="high">
      </div>
    </section>

    <section class="facts" aria-label="معلومات سريعة">
      <div><small>المدينة</small><strong>كامل الرياض</strong></div>
      <div><small>الشغل</small><strong>بيد المعلم</strong></div>
      <div><small>الأجرة</small><strong>يومية أو مقطوعية</strong></div>
      <div><small>للطلب</small><strong class="ltr">{TEL}</strong></div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">الخدمات</p>
            <h2>ما أشتغله</h2>
          </div>
          <p>ثلاثة أبواب تدخل منها<br>وكل باب تحته شغل كثير</p>
        </div>
        <div class="cards">
          <a class="card" href="khadamat.html#block">
            <img src="صور/سور-بلك.jpg" alt="سور بلك" width="400" height="260" loading="lazy">
            <div>
              <h3>بلك</h3>
              <p>سور وجدار وغرفة وملحق ومخزن وبوابة وغيرها</p>
            </div>
          </a>
          <a class="card" href="khadamat.html#hajar">
            <img src="صور/واجهة.jpg" alt="واجهة حجر تراثي" width="400" height="260" loading="lazy">
            <div>
              <h3>حجر</h3>
              <p>واجهات وجدران وبوابات وكل الأعمال الأخرى</p>
            </div>
          </a>
          <a class="card" href="khadamat.html#fence">
            <img src="صور/جدار-منحني.jpg" alt="جدار منحني" width="400" height="260" loading="lazy">
            <div>
              <h3>أسوار وجدران</h3>
              <p>سور حول الحوش أو الأرض وجدران منحنية</p>
            </div>
          </a>
        </div>
      </div>
    </section>

    <section class="section night">
      <div class="wrap">
        <p class="eyebrow">الخطوات</p>
        <h2>أربع خطوات</h2>
        <div class="steps">
          <article><span>01</span><h3>الصورة</h3><p>ترسل صورة المكان والمقاس</p></article>
          <article><span>02</span><h3>السعر</h3><p>نشوف السعر المناسب لشغلك</p></article>
          <article><span>03</span><h3>الاتفاق</h3><p>نتفق من أولها والكلام واضح</p></article>
          <article><span>04</span><h3>التسليم</h3><p>تسلّم الشغل كما اتفقنا</p></article>
        </div>
        <p class="section-cta"><a class="btn btn-light" href="sayr.html">تفاصيل طريقة العمل</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">حراج</p>
            <h2>إعلاناتي في حراج</h2>
          </div>
          <p>حسابي @workbuild<br>كل إعلان فيه صور وتفاصيل</p>
        </div>
        <div class="haraj-stack" data-haraj-mini></div>
        <p class="section-cta">
          <a class="btn btn-ink" href="{HARAJ}" target="_blank" rel="noopener">افتح حسابي في حراج</a>
          <a class="btn btn-line" href="ads.html">كل الإعلانات</a>
        </p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">الأعمال</p>
            <h2>صور من الشغل</h2>
          </div>
          <a href="aamal.html">كل الصور</a>
        </div>
        <div class="gallery">
          <a class="shot large" href="aamal.html">
            <img src="صور/جدار-منحني.jpg" alt="جدار حجر منحني في حوش بيت" width="1408" height="768" loading="lazy">
            <figcaption><strong>جدار منحني</strong><small>قوس على حوش البيت</small></figcaption>
          </a>
          <div class="stack-shots">
            <a class="shot" href="aamal.html">
              <img src="صور/بوابة.jpg" alt="بوابة حجر بطراز نجدي" width="1024" height="1024" loading="lazy">
              <figcaption><strong>بوابة حجر</strong><small>طراز نجدي</small></figcaption>
            </a>
            <a class="shot" href="aamal.html">
              <img src="صور/تفصيلة.jpg" alt="جدار بلك" width="1408" height="768" loading="lazy">
              <figcaption><strong>جدار بلك</strong><small>خط مستقيم</small></figcaption>
            </a>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">النطاق</p>
        <h2>كامل الرياض والمدن القريبة</h2>
        <div class="cities" aria-label="نطاق الشغل">
          <span class="is-home">كامل الرياض</span>
          <span>الخرج</span>
          <span>المزاحمية</span>
          <span>الدرعية</span>
          <span>رماح</span>
          <span>الحوطة</span>
          <span>وعند الطلب خارج الرياض</span>
        </div>
      </div>
    </section>

    <section class="section sand">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">كيف تطلب</p>
            <h2>ثلاثة أشياء تكفي</h2>
          </div>
          <p>لا تحتاج تجهّز شي<br>الجوال يكفي</p>
        </div>
        <div class="plain-grid">
          <div class="plain"><span>الأول</span><h3>صورة المكان</h3><p>من بعيد ومن قريب إن قدرت</p></div>
          <div class="plain"><span>الثاني</span><h3>الطول والارتفاع</h3><p>تقديري ولو بالخطوة</p></div>
          <div class="plain"><span>الثالث</span><h3>يومية أو مقطوعية</h3><p>قل لي أي نوع يريحك ونمشي عليه</p></div>
        </div>
      </div>
    </section>
"""


BALK = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">بلك</p>
        <h1>معلم بلك في الرياض يومية أو مقطوعية</h1>
        <p class="lede">أبني السور والجدار والغرفة والملحق والمخزن<br>وأشتغل بيدي من أول مدماك لآخر مدماك</p>
        <div class="actions">
          <a class="btn btn-brick" href="{WA}" target="_blank" rel="noopener">أرسل صورة المكان</a>
          <a class="btn btn-line" href="tel:{TEL}">اتصال</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">الأجرة</p>
            <h2>اليومية أو المقطوعية</h2>
          </div>
          <p>نوعان فقط<br>وأنت تختار واحد</p>
        </div>
        <table class="info-table">
          <tr><th>باليومية</th><td>أشتغل عندك بعدد أيام، وتحسبها بالأيام. تناسب الشغل اللي ما يتحدد بسهولة من أولها.</td></tr>
          <tr><th>بالمقطوعية</th><td>سعر واحد للشغل كامل بعد ما أشوف المكان وأعرف الطول والارتفاع. تناسب السور والجدار والغرفة.</td></tr>
        </table>
      </div>
    </section>

    <section class="section sand">
      <div class="wrap">
        <p class="eyebrow">الأمثلة</p>
        <h2>أنواع شغل البلك</h2>
        <div class="plain-grid">
          <div class="plain"><span>سور</span><h3>سور خارجي</h3><p>حول البيت أو الأرض، على الشارع أو على الجيران</p></div>
          <div class="plain"><span>غرفة</span><h3>غرفة ومخزن</h3><p>غرفة في السطح أو الحوش، ومخزن للأغراض</p></div>
          <div class="plain"><span>ملحق</span><h3>ملحق وبوابة</h3><p>ملحق مستقل وبوابات دخول على الشارع</p></div>
          <div class="plain"><span>قاطع</span><h3>قواطع داخلية</h3><p>فصل الغرف داخل البيت ببلك</p></div>
          <div class="plain"><span>جدار</span><h3>جدار استنادي</h3><p>جدار يمسك التراب في الأرض المنحدرة</p></div>
          <div class="plain"><span>وغيرها</span><h3>وأعمال أخرى</h3><p>قل لي وش عندك ونشوفها مع بعض</p></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">المقاسات</p>
            <h2>مقاسات البلك الثلاثة</h2>
          </div>
          <p>الاختيار على حسب الشغل<br>لا على حسب السعر</p>
        </div>
        <table class="info-table">
          <tr><th>البلك العادي</th><td>الأكثر استخداماً في الأسوار والجدران والغرف، وارتفاع المدماك معروف لأي معلم.</td></tr>
          <tr><th>البلك العازل</th><td>يُستعمل في الجدران اللي تحتاج عزل، ويحتاج وزن المدماك بشكل مختلف.</td></tr>
          <tr><th>البلك الخفيف</th><td>للأجزاء اللي تحتاج خفة في الوزن، ويُبنى بالكامل بخط واحد.</td></tr>
        </table>
        <p class="muted">المقاس لا يحدده الزبون وحده، أنا أشوف المكان وأقول لك اللي يمشي.</p>
      </div>
    </section>

    <section class="section night">
      <div class="wrap">
        <p class="eyebrow">الحساب</p>
        <h2>ما الذي يحدد السعر</h2>
        <div class="steps">
          <article><span>01</span><h3>الطول</h3><p>كم متر طول الجدار أو السور</p></article>
          <article><span>02</span><h3>الارتفاع</h3><p>كم مدماك ترتفع فوق الأرض</p></article>
          <article><span>03</span><h3>الأرض</h3><p>مستوية أو منحدرة أو فيها خندق</p></article>
          <article><span>04</span><h3>الدخول</h3><p>الموقع قريب والمكان يسمح بالشغل</p></article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">الأسئلة</p>
        <h2>أسئلة يسألها الزبون</h2>
        <div class="faq">
          <details><summary>أشتغل باليومية ولا مقطوعية؟</summary><p>الاثنان متاحان. اليومية تحسب بالأيام، والمقطوعية سعر واحد للشغل كامل بعد ما أشوف المكان.</p></details>
          <details><summary>كم يستغرق السور؟</summary><p>ما أعطي مدة قبل ما أشوف المكان والمقاس، لأن الطول والارتفاع والدخول يغيرون الحساب.</p></details>
          <details><summary>هل تشتغل خارج الرياض؟</summary><p>الرياض كاملة. والخرج والمزاحمية والدرعية ورماح والحوطة عند الطلب.</p></details>
          <details><summary>كيف أعرف السعر؟</summary><p>أرسل صورة المكان واكتب الطول والارتفاع التقريبي، ونشوف السعر المناسب لشغلك.</p></details>
          <details><summary>هل تحتاج أدوات؟</summary><p>أجيب أدواتي معي. المكان يحتاج ماء وكهرباء للشغل.</p></details>
        </div>
      </div>
    </section>
{cta_block("قل لي نوع الشغل وأنا أقولك كيف نمشي")}
"""

KHADAMAT = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">الخدمات</p>
        <h1>خدمات معلم المباني في الرياض</h1>
        <p class="lede">بلك وحجر وأسوار وجدران<br>وكل ما يخص المباني</p>
      </div>
    </section>

    <section class="section" id="block">
      <div class="wrap">
        <div class="split">
          <div>
            <p class="eyebrow">الباب الأول</p>
            <h2>أعمال البلك</h2>
            <p>البلك أساس أي شغل في المباني. أبني السور والجدار والغرفة والملحق والمخزن والبوابة وغيرها، وأوزن المدماك وأربط الزوايا حتى يطلع الخط مستقيم.</p>
            <ul class="ticks">
              <li>سور خارجي حول البيت أو الأرض</li>
              <li>جدار بين الجيران أو داخل الحوش</li>
              <li>غرفة ومخزن وملحق مستقل</li>
              <li>قواطع داخلية وفصل الغرف</li>
              <li>بوابات دخول على الشارع</li>
            </ul>
            <a class="btn btn-ink" href="balk.html">تفاصيل شغل البلك</a>
          </div>
          <figure class="split-media">
            <img src="صور/سور-بلك.jpg" alt="سور بلك مستقيم بطول الشارع" width="1408" height="768" loading="lazy">
          </figure>
        </div>
      </div>
    </section>

    <section class="section sand" id="hajar">
      <div class="wrap">
        <div class="split reverse">
          <div>
            <p class="eyebrow">الباب الثاني</p>
            <h2>أعمال الحجر</h2>
            <p>الحجر يعطي الواجهة والمدخل شخصية. أشتغل الحجر على الجدران والواجهات والأسوار والبوابات، وأهتم بميل السمك والخط بين المدماك والمدماك.</p>
            <ul class="ticks">
              <li>واجهات حجر على البيت</li>
              <li>جدران حجر داخل الحوش</li>
              <li>أسوار حجر حول الأرض</li>
              <li>بوابات حجر بطراز نجدي</li>
              <li>جدران منحنية على شكل قوس</li>
            </ul>
            <a class="btn btn-ink" href="aamal.html">شوف صور الحجر</a>
          </div>
          <figure class="split-media">
            <img src="صور/واجهة.jpg" alt="واجهة حجر تراثي بمداخل مستقيمة" width="1408" height="768" loading="lazy">
          </figure>
        </div>
      </div>
    </section>

    <section class="section" id="fence">
      <div class="wrap">
        <div class="split">
          <div>
            <p class="eyebrow">الباب الثالث</p>
            <h2>الأسوار والجدران</h2>
            <p>السور هو أول شي يشوفه الجار والزائر. أبنيه على الحد مباشرة وأضبط الزوايا والأركان، وأنتهي بالميلان اللي يصرّف ماء المطر بعيداً عن الأساس.</p>
            <ul class="ticks">
              <li>سور على الحد النظامي للأرض</li>
              <li>جدار بلك أو حجر بين الجيران</li>
              <li>سور قصير حول الحوش</li>
              <li>جدار منحني لجمال الحوش</li>
              <li>أركان وزوايا مربوطة بشكل صحيح</li>
            </ul>
          </div>
          <figure class="split-media">
            <img src="صور/جدار-منحني.jpg" alt="جدار حجر منحني على حوش بيت" width="1408" height="768" loading="lazy">
          </figure>
        </div>
      </div>
    </section>

    <section class="section night">
      <div class="wrap">
        <p class="eyebrow">الباب الرابع</p>
        <h2>أعمال أخرى</h2>
        <div class="plain-grid four on-dark">
          <div class="plain"><span>مشب</span><h3>مشبات</h3><p>مشب حجر أو طوب في المجلس أو الحوش</p></div>
          <div class="plain"><span>فرن</span><h3>أفران</h3><p>فرن حجر للمخبوزات والجريش</p></div>
          <div class="plain"><span>تشطيب</span><h3>تشطيب</h3><p>تشطيب الجدران والأسوار بعد البناء</p></div>
          <div class="plain"><span>أخرى</span><h3>وغيرها</h3><p>أي شغل في المباني، اسأل وأنا أقولك</p></div>
        </div>
      </div>
    </section>
{cta_block("اختر الباب اللي يخصك وكلّمني")}
"""


AAMAL = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">الأعمال</p>
        <h1>أعمال معلم مباني في الرياض</h1>
        <p class="lede">هذي صور من شغل قريب من طبيعة الشغل اللي أشتغله<br>بلك وحجر وأسوار وجدران<br>كل صورة تبيّن نوع الشغل فقط</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">حجر</p>
        <h2>حجر وواجهات</h2>
        <div class="gallery">
          <a class="shot large" href="صور/واجهة.jpg">
            <img src="صور/واجهة.jpg" alt="واجهة حجر تراثي بمداخل مستقيمة" width="1408" height="768" loading="lazy">
            <figcaption><strong>واجهة حجر</strong><small>مداخل مستقيمة وسمك متساوٍ</small></figcaption>
          </a>
          <div class="stack-shots">
            <a class="shot" href="صور/بوابة.jpg">
              <img src="صور/بوابة.jpg" alt="بوابة حجر بطراز نجدي" width="1024" height="1024" loading="lazy">
              <figcaption><strong>بوابة حجر</strong><small>طراز نجدي</small></figcaption>
            </a>
            <a class="shot" href="صور/جدار-منحني.jpg">
              <img src="صور/جدار-منحني.jpg" alt="جدار حجر منحني" width="1408" height="768" loading="lazy">
              <figcaption><strong>جدار منحني</strong><small>قوس على حوش البيت</small></figcaption>
            </a>
          </div>
        </div>
      </div>
    </section>

    <section class="section sand">
      <div class="wrap">
        <p class="eyebrow">بلك</p>
        <h2>بلك في مواقع مختلفة</h2>
        <div class="gallery two">
          <a class="shot" href="صور/سور-بلك.jpg">
            <img src="صور/سور-بلك.jpg" alt="سور بلك بطول الشارع" width="1408" height="768" loading="lazy">
            <figcaption><strong>سور بلك</strong><small>خط مستقيم على الشارع</small></figcaption>
          </a>
          <a class="shot" href="صور/تفصيلة.jpg">
            <img src="صور/تفصيلة.jpg" alt="تفصيلة جدار بلك" width="1408" height="768" loading="lazy">
            <figcaption><strong>تفصيلة جدار</strong><small>مدماك واحد بسماكة ثابتة</small></figcaption>
          </a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">القراءة</p>
        <h2>كيف تقرأ الصورة</h2>
        <table class="info-table">
          <tr><th>الخط</th><td>استقامة المدماك على طول الجدار، ووضوح الأفق في أعلى السور.</td></tr>
          <tr><th>الركن</th><td>الزوايا كيف تربط الجدارين، وهذا اللي يمسك الشكل كامل.</td></tr>
          <tr><th>الميلان</th><td>نهاية السور المسؤولة عن تصريف الماء بعيداً عن الأساس.</td></tr>
          <tr><th>الحجر</th><td>تساوي السمك بين المدماك والمدماك، وسلامة القوس في الجدار المنحني.</td></tr>
        </table>
        <p class="muted">الصورة ما فيها أسماء مواقع ولا أسماء زبائن، وهذا ما أعتمده.</p>
      </div>
    </section>
{cta_block("شفت اللي يعجبك؟ كلّمني عليه")}
"""


ADS = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">حراج</p>
        <h1>إعلاناتي في حراج</h1>
        <p class="lede">كل إعلان أنزله في حراج يجي هنا<br>من الأحدث إلى الأقدم<br>الرابط يفتح الإعلان بحسابه الأصلي</p>
        <div class="actions">
          <a class="btn btn-ink" href="{HARAJ}" target="_blank" rel="noopener">حسابي @workbuild</a>
          <a class="btn btn-line" href="tel:{TEL}">اتصال مباشر</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">القائمة</p>
            <h2>كل الإعلانات</h2>
          </div>
          <p>اضغط نوع الشغل<br>تظهر لك إعلاناته</p>
        </div>
        <div class="chips" data-haraj-filters role="group" aria-label="تصفية الإعلانات حسب نوع الشغل"></div>
        <div class="haraj-grid" data-haraj-list>
          <noscript><p class="empty">القائمة تحتاج تفعيل الجافاسكربت، ويمكن فتح الحساب مباشرة: <a href="{HARAJ}">haraj.com.sa/@workbuild</a></p></noscript>
        </div>
      </div>
    </section>

    <section class="section sand">
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

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">لماذا حراج</p>
        <h2>لماذا أنشر في حراج</h2>
        <div class="plain-grid">
          <div class="plain"><span>الرسائل</span><h3>محادثة مباشرة</h3><p>ترسل رسالة على الإعلان وتوصلني مع صور المكان</p></div>
          <div class="plain"><span>السجل</span><h3>إعلان ظاهر</h3><p>كل إعلان له رقم ووقت نشر، تقدر ترجع له</p></div>
          <div class="plain"><span>الصور</span><h3>صور لكل شغل</h3><p>كل إعلان فيه صور نوع الشغل اللي يخصه</p></div>
        </div>
        <p class="muted">حراج واجهة واحدة من قنواتي. الواتساب والاتصال يشتغلان في كل وقت.</p>
      </div>
    </section>
{cta_block("إعلانك اللي يخصك على حراج")}
"""


ABOUT = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">التعريف</p>
        <h1>أبو محمد معلم بلك ومباني</h1>
        <p class="lede">معلم مباني، لا مؤسسة ولا شركة<br>أشتغل بيدي وأتابع الشغل بنفسي<br>من أول مدماك لآخر مدماك</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="split">
          <div>
            <p class="eyebrow">من أنا</p>
            <h2>من أنا</h2>
            <p>اسمي أبو محمد، معلم بلك ومباني في الرياض. شغلي كله في البلك والحجر والأسوار والجدران والملاحق والغرف، ومعها المشبات والأفران والتشطيب وغيرها.</p>
            <p>أشتغل يومية أو مقطوعية على حسب اللي يريح الزبون، وأحدد السعر بعد ما أشوف المكان وأعرف الطول والارتفاع.</p>
            <p>ما عندي مكتب ولا موظفين. أنا اللي يجيك، وأنا اللي يبني، وأنا اللي يرد على جوالك.</p>
          </div>
          <figure class="split-media">
            <img src="صور/تفصيلة.jpg" alt="مدماك بلك واحد بسماكة ثابتة" width="1408" height="768" loading="lazy">
          </figure>
        </div>
      </div>
    </section>

    <section class="section night">
      <div class="wrap">
        <p class="eyebrow">الشارة</p>
        <h2>الأهم الثقة والأمانة</h2>
        <p class="lede">الثقة ما تنكتب في إعلان، تنبنى مدماك ورا مدماك<br>إذا قلت لك سعر فهو السعر<br>وإذا قلت لك يوم جيت فيه بلا أعذار<br>وإذا لقيت شي في المكان ما يخدم الشغل أقولك قبل ما أبدأ</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">الحدود</p>
            <h2>ما لا أقوله</h2>
          </div>
          <p>الكلام اللي ما أنطقه<br>أحفظه كما أحفظ الشغل</p>
        </div>
        <ul class="ticks big">
          <li>ما أوصف الشغل بكلام، لأن الشغل يتشاف ما يتقال</li>
          <li>ما أوعد بمدة قبل ما أشوف المكان</li>
          <li>ما أذكر أسماء أحياء ولا أسماء زبائن</li>
          <li>ما أنشر صورة وأقول هذي من عندك بلا إذنك</li>
          <li>ما أضيف رقمي على أعمال غيري</li>
        </ul>
        <p class="muted">الصور في الموقع توضح نوع الشغل، والحكم لك بعد ما تشوف بعينك.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="cta">
          <div>
            <p class="eyebrow">للطلب</p>
            <h2>الرقم المباشر لصاحب الشغل</h2>
            <p class="muted">الرقم يرد عليه أبو محمد نفسه<br>أرسل صورة المكان ونشوف السعر المناسب لشغلك</p>
          </div>
          <div>
            <a class="phone-xl ltr" href="tel:{TEL}">{TEL}</a>
            <div class="actions">
              <a class="btn btn-brick" href="{WA}" target="_blank" rel="noopener">واتساب</a>
              <button class="btn btn-line" type="button" data-copy="0531060401">انسخ الرقم</button>
            </div>
          </div>
        </div>
      </div>
    </section>
"""


SAYR = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">الطريقة</p>
        <h1>طريقة العمل من الصورة إلى التسليم</h1>
        <p class="lede">سبع خطوات واضحة<br>تعرف في كل خطوة وين أنت<br>وش اللي عليك وش اللي عليّ</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">الخطوات</p>
        <h2>سبع خطوات</h2>
        <ol class="timeline">
          <li><span>01</span><div><h3>الصورة</h3><p>ترسل صورة المكان من بعيد ومن قريب إن قدرت.</p></div></li>
          <li><span>02</span><div><h3>القياس</h3><p>تكتب الطول والارتفاع التقريبي، وأنا أسألك عن الأرض والدخول.</p></div></li>
          <li><span>03</span><div><h3>النوع</h3><p>نتفق يومية أو مقطوعية، وكل نوع له حسابه.</p></div></li>
          <li><span>04</span><div><h3>السعر</h3><p>نشوف السعر المناسب لشغلك بعد ما تتضح الصورة كاملة.</p></div></li>
          <li><span>05</span><div><h3>الاتفاق</h3><p>نتفق من أولها على كل شي: البداية والنوع والسعر.</p></div></li>
          <li><span>06</span><div><h3>الشغل</h3><p>أبدأ بالزوايا والأساس، وأكمل مدماك ورا مدماك.</p></div></li>
          <li><span>07</span><div><h3>التسليم</h3><p>تشوف الشغل كامل قبل ما نقفل الحساب.</p></div></li>
        </ol>
      </div>
    </section>

    <section class="section sand">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">الرسالة</p>
            <h2>ماذا ترسل في الرسالة الأولى</h2>
          </div>
          <a href="tawasel.html">افتح النموذج</a>
        </div>
        <table class="info-table">
          <tr><th>صورة المكان</th><td>صورة واحدة على الأقل، ويفضّل اثنتان.</td></tr>
          <tr><th>الطول والارتفاع</th><td>تقديري، ولو بعدد الخطوات.</td></tr>
          <tr><th>نوع الشغل</th><td>سور، جدار، غرفة، ملحق، حجر، أو غيرها.</td></tr>
          <tr><th>الحي أو المدينة</th><td>اسم الحي يكفي، ولا يُنشر في الموقع.</td></tr>
        </table>
      </div>
    </section>

    <section class="section night">
      <div class="wrap">
        <p class="eyebrow">الخطوة التالية</p>
        <h2>بعد الاتفاق</h2>
        <div class="steps">
          <article><span>01</span><h3>البداية</h3><p>أحدد يوم البداية معك بعد الاتفاق</p></article>
          <article><span>02</span><h3>الأدوات</h3><p>أجيب أدواتي، والمكان يحتاج ماء وكهرباء</p></article>
          <article><span>03</span><h3>المتابعة</h3><p>تشوف الشغل كل يوم وتقول لي ملاحظتك</p></article>
          <article><span>04</span><h3>الختام</h3><p>نراجع الشغل مع بعض قبل الإغلاق</p></article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">الأسئلة</p>
        <h2>أسئلة على الطريقة</h2>
        <div class="faq">
          <details><summary>هل تقدر تجي تشوف المكان؟</summary><p>أفضل شي أشوف المكان على الطبيعة. إذا تعذر، الصور والمقاسات تكفي في الغالب.</p></details>
          <details><summary>هل تقبض عربون؟</summary><p>طريقة الدفع تُتفق عليها معك في الاتفاق نفسه، وكل شي واضح من أولها.</p></details>
          <details><summary>من يشتري المواد؟</summary><p>هذا موضوع تفاصيله معك في المحادثة، وما أكتب عنه في الموقع.</p></details>
        </div>
      </div>
    </section>
{cta_block("ابدأ من الصورة")}
"""


TAWASEL = f"""
    <section class="page-head">
      <div class="wrap">
        <p class="eyebrow">تواصل</p>
        <h1>تواصل مع أبو محمد معلم بلك ومباني</h1>
        <p class="lede">الرقم واحد<br>اتصال أو واتساب أو رسالة حراج<br>اللي يريحك</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">القنوات</p>
        <h2>قنوات التواصل</h2>
        <div class="channels">
          <a class="channel" href="tel:{TEL}">
            <strong>اتصال</strong>
            <span class="ltr">{TEL}</span>
            <span>الأسرع إذا عندك سؤال قصير</span>
          </a>
          <a class="channel" href="{WA}" target="_blank" rel="noopener">
            <strong>واتساب</strong>
            <span class="ltr">{TEL}</span>
            <span>أرسل الصور والمقاسات هنا</span>
          </a>
          <a class="channel" href="{HARAJ}" target="_blank" rel="noopener">
            <strong>حراج</strong>
            <span class="ltr">@workbuild</span>
            <span>كل الإعلانات في مكان واحد</span>
          </a>
        </div>
      </div>
    </section>

    <section class="section sand">
      <div class="wrap">
        <div class="contact-grid">
          <div>
            <p class="eyebrow">النموذج</p>
            <h2>نموذج الرسالة</h2>
            <p>املأ الحقول وبنجهز لك رسالة واتساب كاملة، ما تحتاج تكتب كل شي من جديد.</p>
            <p class="muted">ما نحفظ بياناتك في أي مكان. الرسالة تُرسل من جوالك على واتساب.</p>
            <a class="phone-xl ltr" href="tel:{TEL}">{TEL}</a>
          </div>
          <form class="form" data-wa-form novalidate>
            <p class="form-legend">كل الحقول المطلوبة معلّمة بـ<span class="req">*</span></p>
            <div class="row">
              <div class="field">
                <label for="f-name">الاسم أو الكنية <span class="req">*</span></label>
                <input id="f-name" name="name" type="text" autocomplete="name" placeholder="مثال: أبو سعد" required>
                <p class="field-error text-danger" data-err="f-name"></p>
              </div>
              <div class="field">
                <label for="f-city">الحي أو المدينة <span class="req">*</span></label>
                <input id="f-city" name="city" type="text" autocomplete="address-level2" placeholder="مثال: الرياض" required>
                <p class="field-error text-danger" data-err="f-city"></p>
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
                <p class="field-error text-danger" data-err="f-work"></p>
              </div>
              <div class="field">
                <label for="f-size">الطول والارتفاع <span class="req">*</span></label>
                <input id="f-size" name="size" type="text" placeholder="مثال: ٢٠ متر طول و٢ متر ارتفاع" required>
                <p class="field-error text-danger" data-err="f-size"></p>
              </div>
            </div>
            <div class="field">
              <label for="f-place">وصف المكان <span class="req">*</span></label>
              <textarea id="f-place" name="place" placeholder="سطر واحد: وش تبي تبني، ووين بالضبط، والأرض مستوية أو منحدرة" required></textarea>
              <p class="field-error text-danger" data-err="f-place"></p>
            </div>
            <div class="hp" aria-hidden="true">
              <label for="f-hp">اتركه فارغاً</label>
              <input id="f-hp" name="hp" type="text" tabindex="-1" autocomplete="off">
            </div>
            <button class="btn btn-brick" type="submit">جهّز رسالة واتساب</button>
            <p class="form-status" data-status role="status" aria-live="polite"></p>
            <p class="muted">الصور ترسلها بعد فتح واتساب، لأن الواتساب أسرع في نقل الصور.</p>
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
          <tr><th>المدينة</th><td>كامل الرياض، والخرج والمزاحمية والدرعية ورماح والحوطة عند الطلب</td></tr>
          <tr><th>النطاق</th><td>كامل الرياض، والشغل يومية أو مقطوعية</td></tr>
        </table>
      </div>
    </section>
{cta_block("الرقم واحد والطريق واحد")}
"""


NOTFOUND = f"""
    <section class="page-head tall">
      <div class="wrap">
        <p class="eyebrow">404</p>
        <h1>الصفحة غير موجودة</h1>
        <p class="lede">الرابط اللي فتحته ما هو موجود في الموقع<br>يمكن تغيّر أو ينكتب بغير شكله<br>أبو محمد معلم مباني في الرياض</p>
        <div class="actions">
          <a class="btn btn-brick" href="index.html">الرئيسية</a>
          <a class="btn btn-ink" href="ads.html">الإعلانات</a>
          <a class="btn btn-line" href="tel:{TEL}">اتصل {TEL}</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">الصفحات</p>
        <h2>الصفحات الموجودة</h2>
        <div class="plain-grid">
          <a class="plain" href="balk.html"><span>01</span><h3>معلم بلك</h3><p>اليومية والمقطوعية والمقاسات</p></a>
          <a class="plain" href="khadamat.html"><span>02</span><h3>الخدمات</h3><p>بلك وحجر وأسوار وأعمال أخرى</p></a>
          <a class="plain" href="aamal.html"><span>03</span><h3>الأعمال</h3><p>صور من الشغل</p></a>
          <a class="plain" href="ads.html"><span>04</span><h3>الإعلانات</h3><p>كل إعلانات حراج</p></a>
          <a class="plain" href="about.html"><span>05</span><h3>عن المعلم</h3><p>من أنا وما لا أقوله</p></a>
          <a class="plain" href="sayr.html"><span>06</span><h3>طريقة العمل</h3><p>من الصورة إلى التسليم</p></a>
        </div>
      </div>
    </section>
"""


PAGES = [
    ("index.html", INDEX, "أبو محمد معلم بلك ومباني في الرياض",
     "أبو محمد معلم بلك ومباني في الرياض. معلم بلك باليومية أو المقطوعية وكل أعمال البلك والحجر والأسوار. كامل الرياض والمدن القريبة. 0531060401", False),
    ("balk.html", BALK, "معلم بلك في الرياض باليومية أو المقطوعية",
     "معلم بلك في الرياض باليومية أو المقطوعية. سور وجدار وغرفة وملحق ومخزن وبوابة، ومقاسات البلك الثلاثة، وأسئلة يسألها الزبون قبل الشغل. 0531060401", False),
    ("khadamat.html", KHADAMAT, "خدمات معلم المباني في الرياض بلك وحجر",
     "خدمات معلم المباني في الرياض: أعمال البلك والحجر والأسوار والجدران والملاحق والمشبات والأفران والتشطيب وغيرها. كامل الرياض. 0531060401", False),
    ("aamal.html", AAMAL, "أعمال معلم مباني في الرياض بالصور",
     "أعمال معلم مباني في الرياض بالصور: واجهات حجر وبوابات بطراز نجدي وأسوار بلك وجدران منحنية وملاحق. صور توضح نوع الشغل فقط. 0531060401", False),
    ("ads.html", ADS, "إعلانات أبو محمد في حراج الرياض",
     "إعلانات أبو محمد معلم مباني في حراج: بناء بلك وحجر تراثي ومباني ومشبات وأفران في الرياض. كل الإعلانات القديمة والحالية بروابطها. 0531060401", True),
    ("about.html", ABOUT, "عن أبو محمد معلم بلك ومباني في الرياض",
     "عن أبو محمد معلم بلك ومباني في الرياض: معلم مباني يعمل بيده في البلك والحجر والأسوار، يومية أو مقطوعية، وما يقوله وما لا يقوله. 0531060401", False),
    ("sayr.html", SAYR, "طريقة العمل من الصورة إلى التسليم",
     "طريقة العمل مع أبو محمد معلم بلك في الرياض: صورة المكان والقياس ونوع الشغل والسعر والاتفاق والشغل والتسليم في خطوات واضحة. 0531060401", False),
    ("tawasel.html", TAWASEL, "تواصل مع أبو محمد معلم بلك ومباني",
     "تواصل مع أبو محمد معلم بلك ومباني في الرياض: اتصال وواتساب وحساب حراج ونموذج رسالة جاهز يفتح لك واتساب بالتفاصيل. 0531060401", False),
    ("404.html", NOTFOUND, "الصفحة غير موجودة | أبو محمد معلم بلك",
     "", False),
]


def main():
    print("== توليد الصفحات ==")
    for name, body, title, desc, ss in PAGES:
        write(name, body, title, desc, ss)
    # 404 بلا canonical وبلا OG عن قصد
    p = OUT / "404.html"
    t = p.read_text(encoding="utf-8")
    import re
    t = re.sub(r'\n  <link rel="canonical".*?(?=\n</head>)', "\n  <link rel=\"icon\" href=\"favicon.svg\" type=\"image/svg+xml\">\n  <link rel=\"stylesheet\" href=\"css/site.css\">", t, flags=re.S)
    p.write_text(t, encoding="utf-8")
    print("  ✓ 404.html (بلا canonical وOG)")
    print(f"  أطوال: " + " | ".join(f"{n} title={len(ti)} desc={len(de)}" for n, _, ti, de, _ in PAGES if de))


if __name__ == "__main__":
    main()
