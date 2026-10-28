#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحسين محركات البحث لموقع «أبو محمد معلم مباني».

يعالج أكبر عائق: الموقع كان مكتوباً فيه اسم قديم «البخيتي للبناء والمقاولات»،
وهو اسم لا يبحث به أحد ولا يطابق اسم الإعلان في حراج. النتيجة أن من يبحث
«أبو محمد معلم مباني» لا يجد الموقع أبداً.

ما يفعله السكربت
    1 يوحّد الاسم الظاهر في كل الصفحات
    2 يعطي كل صفحة عنواناً ووصفاً خاصاً فيه الخدمة والمدينة
    3 يضع H1 فيه الكلمة التي يبحث بها الزبون
    4 يستبدل بيانات schema.org ببيانات كاملة محلية
    5 يضيف breadcrumb و روابط داخلية
    6 يحدّث robots.txt و sitemap.xml

الاستخدام
    python3 أدوات/تحسين-السيو.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "موقع"
BASE = "https://engmohammeda.github.io/mydad"

NAME = "أبو محمد معلم مباني"
PHONE = "0531060401"
PHONE_INTL = "+966531060401"

# الصفحة: (العنوان، الوصف، H1، سطر يُحفظ من العنوان القديم)
PAGES = {
    "404.html": (
        'الصفحة غير موجودة | أبو محمد معلم بلك ومباني في الرياض',
        'الصفحة المطلوبة غير موجودة. أبو محمد معلم بلك ومباني في الرياض. أرسل صورة المكان ونشوف السعر المناسب لشغلك. 0531060401',
        'الصفحة غير موجودة',
        None,
    ),
    "aamal.html": (
        'أعمال معلم بلك ومباني في الرياض',
        'صور من شغل البلك والحجر في الرياض. سور وجدار وغرفة وحجر تراثي وبوابة. أبو محمد معلم بلك ومباني. كامل الرياض والخارج عند الطلب. 0531060401',
        'أعمال معلم مباني في الرياض',
        None,
    ),
    "about.html": (
        'أبو محمد معلم بلك ومباني في الرياض',
        'أبو محمد معلم بلك ومباني في الرياض. أشتغل بيدي في كل أعمال البلك والحجر. يومية أو مقطوعية. كامل الرياض وعند الطلب خارجها. اتصل 0531060401',
        'أبو محمد معلم بلك ومباني',
        None,
    ),
    "balk.html": (
        'معلم بلك في الرياض يومية أو مقطوعية',
        'معلم بلك ومباني في الرياض باليومية أو المقطوعية. كل أعمال البلك والحجر. كامل الرياض والخرج والمزاحمية والدرعية ورماح والحوطة. 0531060401',
        'معلم بلك في الرياض يومية أو مقطوعية',
        None,
    ),
    "index.html": (
        'أبو محمد معلم بلك ومباني في الرياض',
        'أبو محمد معلم بلك ومباني في الرياض. معلم بلك باليومية أو المقطوعية وكل أعمال البلك والحجر. كامل الرياض وعند الطلب خارجها. 0531060401',
        'معلم مباني في الرياض',
        None,
    ),
    "khadamat.html": (
        'خدمات معلم بلك ومباني في الرياض',
        'خدمات معلم بلك ومباني في الرياض. كل أعمال البلك والحجر باليومية أو المقطوعية. كامل الرياض والخرج والمزاحمية والدرعية ورماح والحوطة. 0531060401',
        'خدمات معلم المباني في الرياض',
        None,
    ),
    "sayr.html": (
        'طريقة العمل معلم بلك ومباني في الرياض',
        'من صورة المكان إلى التسليم. أرسل صورة المكان ونشوف السعر المناسب لشغلك. أبو محمد معلم بلك ومباني في الرياض. كامل الرياض. 0531060401',
        'طريقة العمل من الصورة إلى التسليم',
        None,
    ),
    "tawasel.html": (
        'تواصل مع أبو محمد معلم بلك ومباني',
        'أرسل صورة المكان ونشوف السعر المناسب لشغلك. أبو محمد معلم بلك ومباني في الرياض للبلك والحجر. كامل الرياض والخارج عند الطلب. 0531060401',
        'تواصل مع أبو محمد معلم بلك ومباني',
        None,
    ),
}

SERVICES = [
    "بناء بلك",
    "سور بلك",
    "جدار بلك",
    "غرفة بلك",
    "ملحق ومخزن بلك",
    "أسوار وحوش",
    "حجر تراثي",
    "جدران منحنية",
    "بوابات حجر",
    "جدران حجر",
]

AREAS = ["الرياض", "الخرج", "المزاحمية", "الدرعية", "رماح", "الحوطة"]


def schema(title: str, desc: str, path: str) -> str:
    """رسم Schema.org كامل: النشاط والشخص والخدمات والتنقل."""
    url = f"{BASE}/{path}"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": f"{BASE}/about.html#person",
                "name": NAME,
                "jobTitle": "معلم مباني",
                "telephone": PHONE_INTL,
                "url": f"{BASE}/about.html",
                "knowsLanguage": "ar",
                "worksFor": {"@id": f"{BASE}/#business"},
            },
            {
                "@type": "HomeAndConstructionBusiness",
                "@id": f"{BASE}/#business",
                "name": NAME,
                "alternateName": ["أبو محمد معلم بلك", "معلم مباني الرياض"],
                "description": desc,
                "url": f"{BASE}/",
                "telephone": PHONE_INTL,
                "image": f"{BASE}/صور/غلاف.jpg",
                "logo": f"{BASE}/صور/شعار.png",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "الرياض",
                    "addressRegion": "منطقة الرياض",
                    "addressCountry": "SA",
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": 24.7136,
                    "longitude": 46.6753,
                },
                "areaServed": [
                    {"@type": "City", "name": a} for a in AREAS
                ],
                "founder": {"@id": f"{BASE}/about.html#person"},
                "knowsLanguage": "ar",
                "hasOfferCatalog": {
                    "@type": "OfferCatalog",
                    "name": "خدمات معلم المباني",
                    "itemListElement": [
                        {
                            "@type": "Offer",
                            "itemOffered": {
                                "@type": "Service",
                                "name": s,
                                "areaServed": {"@type": "City", "name": "الرياض"},
                                "provider": {"@id": f"{BASE}/#business"},
                            },
                        }
                        for s in SERVICES
                    ],
                },
            },
            {
                "@type": "WebPage",
                "@id": url,
                "url": url,
                "name": title,
                "description": desc,
                "inLanguage": "ar-SA",
                "isPartOf": {"@id": f"{BASE}/#business"},
                "about": {"@id": f"{BASE}/#business"},
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, indent=2)


def breadcrumb(path: str, label: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": f"{BASE}/index.html"},
            {"@type": "ListItem", "position": 2, "name": label, "item": f"{BASE}/{path}"},
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def meta_block(title: str, desc: str, path: str, page: str) -> str:
    canon = f"{BASE}/" if path == "index.html" else f"{BASE}/{path}"
    return f'''  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="author" content="{NAME}">
  <meta name="geo.region" content="SA-01">
  <meta name="geo.placename" content="الرياض">
  <meta name="theme-color" content="#202020">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{NAME}">
  <meta property="og:locale" content="ar_SA">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{BASE}/صور/غلاف.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <script type="application/ld+json">
{schema(title, desc, path)}
  </script>
'''


def rebrand(html: str) -> str:
    """توحيد الاسم الظاهر وحذف ألفاظ المقاولات."""
    html = html.replace("<strong>البخيتي</strong>", f"<strong>أبو محمد</strong>")
    html = html.replace("<span>للبناء والمقاولات</span>", "<span>معلم مباني</span>")
    html = html.replace("البخيتي للبناء والمقاولات", NAME)
    html = html.replace("البخيتي", "أبو محمد")
    return html


NAV_EXTRA = '        <a href="balk.html">معلم بلك</a>\n        <a href="about.html">عن المعلم</a>\n'


def fix_nav(html: str, page: str) -> str:
    """إضافة صفحتي معلم بلك وعن المعلم إلى قائمة التنقل في كل صفحة."""
    if "balk.html</a>" in html and "about.html</a>" in html:
        return html
    anchor = '        <a href="aamal.html">الأعمال</a>'
    if anchor in html:
        extra = ""
        if page != "balk.html":
            extra += '        <a href="balk.html">معلم بلك</a>\n'
        if page != "about.html":
            extra += '        <a href="about.html">عن المعلم</a>\n'
        html = html.replace(anchor, extra + anchor, 1)
    return html


def fix_joints(html: str) -> str:
    """إزالة كلمة فواصل لصالح قواطع لأن الفواصل مشغلة الزبون بلا فائدة."""
    return (html.replace("فواصل الحجر", "جدار الحجر")
                .replace("فواصل وغرف", "قواطع وغرف")
                .replace("جدران وفواصل وسور", "جدران وقواطع وأسوار")
                .replace("فواصل وطوق وأعمدة", "قواطع وطوق وأعمدة")
                .replace("طول الفاصل", "طول القاطع")
                .replace("أو فاصل", "أو قاطع"))


def main() -> None:
    changed = []

    for page, (title, desc, h1, keep) in PAGES.items():
        f = SITE / page
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        before = t

        t = rebrand(t)
        t = fix_nav(t, page)
        t = fix_joints(t)

        # إعادة بناء <head> كاملة مع الحفاظ على الأيقونات والخطوط والستايل
        m = re.search(r"<head>(.*?)</head>", t, re.S)
        if m:
            head = m.group(1)
            keep_lines = []
            for line in head.split("\n"):
                s = line.strip()
                if s.startswith("<meta charset") or s.startswith("<meta name=\"viewport\"") \
                   or (s.startswith("<link rel=") and "canonical" not in s):
                    keep_lines.append("  " + s)
            new_head = "<head>\n" + "\n".join(keep_lines) + "\n" + meta_block(title, desc, page, page) + "</head>"
            t = t[:m.start()] + new_head + t[m.end():]

        # H1
        if h1:
            t = re.sub(r"<h1>.*?</h1>", f"<h1>{h1}</h1>", t, count=1, flags=re.S)
            if keep:
                t = re.sub(r"(</h1>\s*\n\s*)<p>", r"\1<p><strong>" + keep + "</strong><br>", t, count=1)

        if t != before:
            f.write_text(t, encoding="utf-8")
            changed.append(page)

    # robots.txt
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n",
        encoding="utf-8",
    )

    # sitemap.xml
    prio = {"index.html": "1.0", "balk.html": "0.9", "khadamat.html": "0.9",
            "aamal.html": "0.8", "about.html": "0.8", "sayr.html": "0.6", "tawasel.html": "0.7"}
    urls = []
    for page in ["index.html", "balk.html", "khadamat.html", "aamal.html",
                 "about.html", "sayr.html", "tawasel.html"]:
        if (SITE / page).exists():
            urls.append(
                f"  <url><loc>{BASE}/{page}</loc>"
                f"<lastmod>2026-10-28</lastmod>"
                f"<changefreq>weekly</changefreq>"
                f"<priority>{prio.get(page, '0.5')}</priority></url>"
            )
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n",
        encoding="utf-8",
    )

    print("صفحات عُدّلت:", ", ".join(changed) if changed else "لا شيء")
    print("robots.txt و sitemap.xml محدّثان")


if __name__ == "__main__":
    main()
