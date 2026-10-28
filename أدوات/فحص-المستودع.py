#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص المستودع قبل النشر.
يشغّل قواعد المستودع نفسها على الإعلانات والموقع والصور والروابط.
لا يعدّل أي ملف. يطبع النتائج ويخرج بالرمز 1 إذا وجد خطأ حرجاً.

الاستخدام:
    python3 أدوات/فحص-المستودع.py
    python3 أدوات/فحص-المستودع.py --صور     # يضيف فحص أحجام الصور
"""

from __future__ import annotations

import re
import sys
import os
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHONE = "0531060401"

FORBIDDEN = [
    ("ترميم", "كلمة ممنوعة: ترميم"),
    ("صغير", "كلمة ممنوعة: صغير"),
    ("خصم", "كلمة ممنوعة: خصم"),
    ("معاينة", "كلمة ممنوعة: معاينة"),
    ("مجاني", "كلمة ممنوعة: مجاني"),
    ("أسبوع", "وعد بمدة"),
    ("يومين", "وعد بمدة"),
    ("بسرعة", "وعد بمدة"),
    ("شغل سريع", "وعد بمدة"),
    ("السعر ثابت", "شعار السعر القديم"),
    ("ما يتغير", "شعار السعر القديم"),
    ("بدون مفاجآت", "شعار السعر القديم"),
    ("دفعة أولى", "شعار دفع"),
    ("الباقي بالتسليم", "شعار دفع"),
    ("قبل البدء", "شعار دفع"),
    ("يكتب من البداية", "شعار السعر القديم"),
    # إضافة 28 أكتوبر 2026 — صفات الشغل على الصور وفي أي نص مرئي
    ("فواصل مرتبة", "كتابة عن الفواصل"),
    ("فواصل مستقيمة", "كتابة عن الفواصل"),
    ("فواصل نظيفة", "كتابة عن الفواصل"),
    ("فواصل داخلية", "كتابة عن الفواصل"),
    ("الفواصل تبين", "كتابة عن الفواصل"),
    ("مكنوس", "وصف مكان مكنوس"),
    ("شغل نظيف", "صفة نظافة"),
    ("شغل مرتب", "صفة ترتيب"),
    ("نظيف ومرتب", "صفة نظافة"),
    ("نظيف", "صفة نظافة"),
    ("مرتب", "صفة ترتيب"),
    # وعود زمنية مقنّعة
    ("دقة في المواعيد", "التزام زمني"),
    ("المواعيد", "التزام زمني"),
    ("في الموعد", "التزام زمني"),
    ("الالتزام بالوقت", "التزام زمني"),
    ("جودة في التنفيذ", "صفة عامة بلا دليل"),
    # قواعد الكتابة المعتمدة 28 أكتوبر 2026
    ("أمشي على كلامنا", "عبارة ليست من اللهجة السعودية — البديل نتفق من أولها"),
    ("المواد على صاحب", "لا تُذكر المواد في نص يراه الزبون"),
    ("المواد عليك", "لا تُذكر المواد في نص يراه الزبون"),
    ("المواد منك", "لا تُذكر المواد في نص يراه الزبون"),
    ("أقولك السعر", "البديل نشوف السعر المناسب لشغلك"),
    ("أعطيك السعر", "البديل نشوف السعر المناسب لشغلك"),
    ("تسليم هندسي", "عبارة مو غريبة على الزبون — البديل الشغل على أصول المهنة"),
]

PUNCT = ".,،؛:؟!\"«»…"
TITLE_MIN, TITLE_MAX = 50, 70
DESC_MIN, DESC_MAX = 8, 14
META_MIN, META_MAX = 120, 155

SKIP_DIRS = {".git", ".obsidian", "__pycache__", "node_modules"}
RULES_FILES = {
    "الهوية/الكلمات-الممنوعة.md",
    "الهوية/اللهجة-والأسلوب.md",
    "العمليات/تحسين-محركات-البحث.md",
    "العمليات/قواعد-الدفع.md",
    "العمليات/تمييز-الزبون.md",
    "الانتشار/انتشار-حراج.md",
    "ابدأ-من-هنا.md",
    "README.md",
}

issues: list[tuple[str, str, str]] = []  # (severity, file, message)


def add(sev: str, path: Path | str, msg: str) -> None:
    issues.append((sev, str(path), msg))


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def extract_block(text: str, heading: str) -> str:
    m = re.search(rf"##\s*{re.escape(heading)}[^\n]*\n+```\n(.*?)\n```", text, re.S)
    return m.group(1).strip() if m else ""


def visible_text(html: str) -> str:
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&[a-zA-Z]+;", " ", html)
    return re.sub(r"\s+", " ", html)


def scan_forbidden(text: str) -> list[str]:
    hits = []
    for term, label in FORBIDDEN:
        if term in text:
            hits.append(f"{label}")
    # عرض وحدها، مع استثناء معروض
    if re.search(r"(?<!م)(?<!ال)عرض(?!\s*\.)", text):
        hits.append("كلمة ممنوعة: عرض")
    if re.search(r"(?<!م)(?<!ال)عروض", text):
        hits.append("كلمة ممنوعة: عروض")
    return sorted(set(hits))


def check_ads() -> None:
    print("== الإعلانات ==")
    for f in sorted(ROOT.glob("إعلانات/*/إعلان-*.md")):
        rel = f.relative_to(ROOT)
        t = read(f)
        title = extract_block(t, "العنوان")
        desc = extract_block(t, "الوصف — انسخه كما هو") or extract_block(t, "الوصف")
        if not title:
            add("P0", rel, "لا يوجد عنوان في كتلة مستقلة")
        else:
            n = len(title)
            if not (TITLE_MIN <= n <= TITLE_MAX):
                add("P1", rel, f"طول العنوان {n} حرفاً، والمطلوب {TITLE_MIN}–{TITLE_MAX}")
        if not desc:
            add("P1", rel, "لا يوجد وصف في كتلة مستقلة")
        else:
            lines = [x for x in desc.splitlines() if x.strip()]
            if not (DESC_MIN <= len(lines) <= DESC_MAX):
                add("P1", rel, f"الوصف {len(lines)} سطراً، والمطلوب {DESC_MIN}–{DESC_MAX}")
            if PHONE not in desc:
                add("P0", rel, "الرقم غير موجود في الوصف")
            last_two = "\n".join(lines[-2:])
            if "الرياض" not in last_two:
                add("P1", rel, "المدينة غير موجودة في آخر سطرين")
            for hit in scan_forbidden(desc):
                sev = "P0" if hit.startswith("كلمة ممنوعة") or "شعار" in hit else "P1"
                add(sev, rel, f"الوصف: {hit}")
            bad = sorted({c for c in desc if c in PUNCT})
            if bad:
                add("P1", rel, "الوصف فيه ترقيم: " + " ".join(bad))
        # الصور
        img_dir = f.parent / "صور"
        imgs = []
        if img_dir.exists():
            imgs = [p for p in img_dir.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
        refs = re.findall(r"!\[[^\]]*\]\((صور/[^)]+)\)", t)
        missing = [r for r in refs if not (f.parent / r).exists()]
        for m in missing:
            add("P0", rel, f"صورة مذكورة وغير موجودة: {m}")
        print(f"  {rel}: عنوان {len(title)} | وصف {len([x for x in desc.splitlines() if x.strip()])} سطراً | صور {len(imgs)}")


def check_head_basics() -> None:
    """أساسيات لا يعمل الموقع بدونها: الترميز والتجاوب والستايل والسكربت."""
    print("\n== أساسيات الصفحات ==")
    need = {
        'charset="utf-8"': "الترميز charset مطلوب وإلا تظهر العربية مشوّهة",
        'name="viewport"': "viewport مطلوب وإلا يفشل العرض على الجوال",
        'css/site.css': "ملف الستايل غير مربوط",
        'rel="canonical"': "canonical مطلوب للسيو",
    }
    for f in sorted(Path("موقع").glob("*.html")):
        html = f.read_text(encoding="utf-8")
        # صفحة 404 ليست صفحة محتوى: لا تحتاج canonical ولا وسوم مشاركة
        keys = {k: v for k, v in need.items() if not (f.name == "404.html" and k == 'rel="canonical"')}
        missing = [msg for key, msg in keys.items() if key not in html]
        if missing:
            add("P0", f.relative_to(ROOT) if f.is_absolute() else f, " و ".join(missing))
    n = len(list(Path("موقع").glob("*.html")))
    print(f"  فُحص {n} صفحة")


def check_name() -> None:
    """يتحقق أن الاسم الظاهر يجمع معلم بلك ومعلم مباني معاً."""
    print("\n== الاسم الظاهر ==")
    must = ["معلم بلك", "معلم مباني"]
    targets = [Path("README.md"), Path("00-لوحة-التحكم.md"),
               Path("إعلانات/معلم-بلك-يومية-ومقطوعية/إعلان-معلم-بلك-يومية-ومقطوعية.md")]
    targets += list(Path("موقع").glob("*.html"))
    for f in targets:
        if not f.exists():
            continue
        txt = f.read_text(encoding="utf-8")
        if "أبو محمد" in txt:
            missing = [m for m in must if m not in txt]
            if missing:
                add("P2", f, f"الاسم ناقص: {' و'.join(missing)}")
    print("  تحقق الاسم في", len([t for t in targets if t.exists()]), "ملفاً")


def check_image_texts() -> None:
    """فحص نصوص الصور المسجلة، لأن الصورة نفسها لا تُقرأ بالـ OCR."""
    print("\n== نصوص الصور ==")
    files = sorted(ROOT.glob("إعلانات/*/نصوص-الصور.md"))
    if not files:
        add("P1", "إعلانات", "لا يوجد ملف نصوص-الصور.md في أي إعلان")
        return
    for f in files:
        rel = f.relative_to(ROOT)
        t = read(f)
        for hit in scan_forbidden(t):
            add("P0", rel, f"نص صورة ممنوع: {hit}")
        blocks = re.findall(r"```\n(.*?)\n```", t, re.S)
        visible = "\n".join(blocks)
        bad_visible = sorted({c for c in visible if c in PUNCT})
        if bad_visible:
            add("P1", rel, "ترقيم في نص صورة: " + " ".join(bad_visible))
        if PHONE not in t:
            add("P1", rel, "الرقم غير مذكور في ملف نصوص الصور")
        print(f"  {rel}: {len(blocks)} كتلة نص | ممنوعات {len(scan_forbidden(t))}")


def check_site() -> None:
    print("\n== الموقع ==")
    pages = sorted(ROOT.glob("موقع/*.html"))
    if not pages:
        add("P1", "موقع", "لا توجد صفحات HTML")
        return
    for f in pages:
        rel = f.relative_to(ROOT)
        t = read(f)
        title = re.search(r"<title>(.*?)</title>", t, re.S)
        desc = re.search(r'name="description"\s+content="(.*?)"', t, re.S)
        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        if title:
            n = len(title.group(1).strip())
            if n > 60:
                add("P2", rel, f"عنوان الصفحة {n} حرفاً، الأفضل ≤ 60")
        else:
            add("P1", rel, "لا يوجد title")
        is_404 = rel.name == "404.html"
        if desc and not is_404:
            n = len(desc.group(1).strip())
            if not (META_MIN <= n <= META_MAX):
                add("P1", rel, f"وصف الصفحة {n} حرفاً، والمطلوب {META_MIN}–{META_MAX}")
        elif not is_404:
            add("P1", rel, "لا يوجد meta description")
        if len(h1) != 1:
            add("P1", rel, f"عدد عناوين H1 = {len(h1)}، والمطلوب واحد")
        # صفحة 404 تُترك بلا canonical وبلا Open Graph عن قصد:
        # لا يُفهرس عنوان غير موجود، والوسوم عليه تُضلل محركات البحث.
        if not is_404 and 'rel="canonical"' not in t:
            add("P2", rel, "لا يوجد canonical")
        if not is_404 and 'property="og:title"' not in t:
            add("P2", rel, "لا توجد وسوم Open Graph")
        for src in re.findall(r'src="([^"]+)"', t):
            if src.startswith(("http", "data:")):
                continue
            if not (f.parent / src).exists():
                add("P0", rel, f"ملف مفقود: {src}")
        for href in re.findall(r'href="([^"]+\.html)"', t):
            if href.startswith(("http://", "https://")):
                continue
            if not (f.parent / href).exists():
                add("P0", rel, f"رابط داخلي مكسور: {href}")
        if rel.name != "404.html":
            for name in ("index.html", "khadamat.html", "aamal.html", "sayr.html", "tawasel.html"):
                if f'>{name}<' in t or f'"{name}"' in t:
                    pass
        text = visible_text(t)
        for hit in scan_forbidden(text):
            add("P1", rel, f"نص ظاهر: {hit}")
        print(f"  {rel}: title {len(title.group(1).strip()) if title else 0} | desc {len(desc.group(1).strip()) if desc else 0} | H1 {len(h1)}")


def check_links() -> None:
    print("\n== الروابط الداخلية ==")
    names = {p.stem for p in ROOT.rglob("*.md") if ".git" not in p.parts}
    broken: dict[str, list[str]] = {}
    for f in ROOT.rglob("*.md"):
        if ".git" in f.parts:
            continue
        t = read(f)
        for link in re.findall(r"\[\[([^\]|#]+)", t):
            link = link.strip()
            if link.endswith(".csv") or link.endswith(".png") or link.endswith(".jpg"):
                continue
            if link not in names:
                broken.setdefault(link, []).append(str(f.relative_to(ROOT)))
    for link, files in sorted(broken.items()):
        add("P1", files[0], f"رابط ويكيلنك لملف غير موجود: {link}")
        print(f"  مكسور: [[{link}]] في {files[0]}")


def check_images(with_sizes: bool = False) -> None:
    print("\n== الصور ==")
    total = 0
    big = 0
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or not p.is_file():
            continue
        if p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        total += 1
        size = p.stat().st_size
        if size > 700_000:
            big += 1
            if with_sizes:
                add("P2", p.relative_to(ROOT), f"حجم الصورة {size/1024/1024:.1f} ميجابايت")
    print(f"  عدد الصور {total} | فوق 700 كيلوبايت: {big}")


def check_sizes() -> None:
    """يتحقق صراحة من المقاسات المعتمدة لكل صورة في الإعلانات."""
    print("\n== المقاسات ==")
    # (اسم الملف، العرض، الارتفاع، التسمية)
    rules = [
        ("01-الغلاف.jpg", 1080, 1080, "صورة إعلان"),
        ("02-السور.jpg", 1080, 1080, "صورة إعلان"),
        ("03-الغرفة.jpg", 1080, 1080, "صورة إعلان"),
        ("04-الجدار.jpg", 1080, 1080, "صورة إعلان"),
        ("05-البوابة.jpg", 1080, 1080, "صورة إعلان"),
        ("06-الملاحق.jpg", 1080, 1080, "صورة إعلان"),
        ("07-الزاوية.jpg", 1080, 1080, "صورة إعلان"),
        ("08-بطاقة-يومية-ومقطوعية.png", 1080, 1080, "بطاقة"),
        ("09-بطاقة-خطوات-السعر.png", 1080, 1080, "بطاقة"),
        ("10-ستوري.jpg", 1080, 1920, "ستوري"),
        ("11-ستوري-الغرفة.jpg", 1080, 1920, "ستوري"),
        ("غلاف-1500.jpg", 1500, 1500, "غلاف المنصة"),
        ("صورة-الحساب-400.png", 400, 400, "صورة الحساب"),
    ]
    try:
        from PIL import Image
    except ImportError:
        print("  Pillow غير مثبت، تخطي فحص المقاسات")
        return

    for ad in sorted((ROOT / "إعلانات").glob("*/صور")):
        if not ad.is_dir():
            continue
        found = 0
        for name, w, h, label in rules:
            f = ad / name
            if not f.exists():
                continue
            found += 1
            real = Image.open(f).size
            if real != (w, h):
                add("P0", f.relative_to(ROOT),
                    f"{label} مقاسها {real[0]}×{real[1]} والمطلوب {w}×{h}")
        missing = [n for n, *_ in rules if not (ad / n).exists()]
        if missing:
            add("P1", ad.relative_to(ROOT), f"صور ناقصة: {', '.join(missing)}")
        print(f"  {ad.relative_to(ROOT)}: تحقق {found} صورة | ناقص {len(missing)}")


def main() -> int:
    check_ads()
    check_head_basics()
    check_name()
    check_image_texts()
    check_site()
    check_links()
    check_sizes()
    check_images("--صور" in sys.argv)
    print("\n== النتيجة ==")
    if not issues:
        print("  لا ملاحظات آلية.")
        return 0
    order = {"P0": 0, "P1": 1, "P2": 2}
    for sev, path, msg in sorted(issues, key=lambda x: (order[x[0]], x[1])):
        print(f"  [{sev}] {path}: {msg}")
    counts = {s: sum(1 for i in issues if i[0] == s) for s in ("P0", "P1", "P2")}
    print(f"\n  حرج {counts['P0']} | مهم {counts['P1']} | تحسين {counts['P2']}")
    return 1 if counts["P0"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
