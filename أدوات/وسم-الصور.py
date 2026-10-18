#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وسم صور الإعلانات بالهوية المعتمدة.
- قص مربع أو ستوري
- شريط علوي متدرج للعنوان
- شريط سفلي فيه الاسم والرقم
- علامة مائية قطرية داخل البكسلات
- بلا ترقيم وبلا تنصيص في أي نص مرئي

الاستخدام:
    python3 أدوات/وسم-الصور.py
"""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
import arabic_reshaper
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path(os.environ.get("MYDAD_FONTS", "/home/user/.cache/mydad-img"))

NAME = "البخيتي للبناء والمقاولات"
PHONE = "0531060401"

GOLD = (202, 156, 84)
CREAM = (240, 225, 210)
WHITE = (255, 255, 255)
INK = (16, 16, 16)

_reshaper = ArabicReshaper(
    {
        "use_unshaped_instead_of_isolated": True,
        "delete_harakat": True,
        "support_ligatures": True,
        "language": "Arabic",
    }
)


def ar(text: str) -> str:
    return get_display(_reshaper.reshape(text))


_fonts: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    key = (weight, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(str(FONT_DIR / f"Almarai-{weight}.ttf"), size)
    return _fonts[key]


def fit(text: str, weight: str, size: int, max_w: int, min_size: int = 30) -> ImageFont.FreeTypeFont:
    while size > min_size:
        f = font(weight, size)
        if f.getlength(ar(text)) <= max_w:
            return f
        size -= 2
    return font(weight, min_size)


def gradient_band(canvas: Image.Image, height: int, top_alpha: int = 232) -> None:
    band = Image.new("RGBA", (canvas.width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(band)
    for y in range(height):
        a = int(top_alpha * (1 - y / height) ** 1.25)
        d.line([(0, y), (canvas.width, y)], fill=(10, 10, 10, a))
    canvas.alpha_composite(band, (0, 0))


def bottom_bar(canvas: Image.Image, height: int = 128) -> None:
    w, h = canvas.size
    bar = Image.new("RGBA", (w, height), INK + (255,))
    d = ImageDraw.Draw(bar)
    d.line([(0, 0), (w, 0)], fill=GOLD + (210,), width=2)
    nf = fit(NAME, "Bold", 40, int(w * 0.62))
    d.text((w - 36, height // 2), ar(NAME), font=nf, fill=GOLD, anchor="rm")
    pf = font("Regular", 44)
    d.text((36, height // 2 + 2), PHONE, font=pf, fill=CREAM, anchor="lm")
    canvas.alpha_composite(bar, (0, h - height))


def watermark(canvas: Image.Image, angle: int = 32, opacity: int = 15) -> None:
    w, h = canvas.size
    tile = Image.new("RGBA", (w + 400, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    tf = font("Regular", 30)
    d.text(((w + 400) // 2, 110), ar(NAME + "  " + PHONE), font=tf, fill=(255, 255, 255, opacity), anchor="mm")
    tile = tile.rotate(angle, expand=True, resample=Image.BICUBIC)
    step_x, step_y = tile.width + 60, tile.height + 90
    for y in range(-tile.height, h + tile.height, step_y):
        for x in range(-tile.width, w + tile.width, step_x):
            canvas.alpha_composite(tile, (x, y))


def compose(
    src: Path,
    out: Path,
    title: str,
    subtitle: str = "",
    size: tuple[int, int] = (1080, 1080),
) -> None:
    W, H = size
    base = Image.open(src).convert("RGB")
    img = ImageOps.fit(base, (W, H), method=Image.LANCZOS, centering=(0.5, 0.45)).convert("RGBA")

    # تعتيم خفيف أسفل الصورة ليبان الشريط
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(int(H * 0.72), H):
        ratio = max(0.0, (y - H * 0.72) / (H * 0.28))
        a = int(110 * ratio ** 1.1)
        sd.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    img.alpha_composite(shade)

    gradient_band(img, int(H * 0.38), 208)

    d = ImageDraw.Draw(img)
    tf = fit(title, "Bold", 76 if H > 1100 else 70, int(W * 0.86))
    sf = fit(subtitle, "Regular", 44, int(W * 0.84)) if subtitle else None
    top = int(H * 0.095)
    tb = d.textbbox((W // 2, top), ar(title), font=tf, anchor="ma")
    bottom = tb[3] + (sf.size + 20 if sf else 0)
    pad_x, pad_y = 34, 22
    scrim_h = bottom - top + pad_y * 2
    scrim = Image.new("RGBA", (W, scrim_h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(scrim)
    for y in range(scrim_h):
        fade = max(0.0, 1.0 - (y / scrim_h) ** 1.6)
        a = int(165 * fade)
        sdraw.line([(0, y), (W, y)], fill=(12, 12, 12, a))
    img.alpha_composite(scrim, (0, top - pad_y))

    d = ImageDraw.Draw(img)
    d.text((W // 2, top), ar(title), font=tf, fill=WHITE, anchor="ma")
    if sf:
        d.text((W // 2, top + tf.size + 14), ar(subtitle), font=sf, fill=GOLD, anchor="ma")

    watermark(img, angle=32, opacity=15)
    bottom_bar(img)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  {out.relative_to(ROOT)}")


def card(out: Path, title: str, rows: list[tuple[str, str]], footer: str = "") -> None:
    """بطاقة نصية بخلفية داكنة، بلا أرقام أسعار."""
    W, H = 1080, 1080
    img = Image.new("RGBA", (W, H), (18, 18, 18, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 8)], fill=GOLD)
    d.rectangle([(0, H - 8), (W, H)], fill=GOLD)

    d.text((W // 2, 150), ar(NAME), font=font("Regular", 40), fill=GOLD, anchor="ma")
    d.text((W // 2, 250), ar(title), font=fit(title, "Bold", 82, W - 140), fill=WHITE, anchor="ma")

    y = 360
    for head, body in rows:
        box_h = 212
        d.rounded_rectangle([(90, y), (W - 90, y + box_h)], radius=10, outline=(202, 156, 84, 120), width=2)
        d.text((W // 2, y + 48), ar(head), font=font("Bold", 50), fill=GOLD, anchor="ma")
        for i, line in enumerate(body.split("\n")):
            d.text((W // 2, y + 122 + i * 44), ar(line), font=font("Regular", 34), fill=CREAM, anchor="ma")
        y += box_h + 34

    if footer:
        d.text((W // 2, 872), ar(footer), font=font("Regular", 32), fill=(184, 172, 158), anchor="ma")

    watermark(img, angle=32, opacity=13)
    bottom_bar(img)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  {out.relative_to(ROOT)}")


def brand_card(out: Path, headline: str, service: str) -> None:
    """بطاقة تعريف بالخدمة بدل صورة شغل غير حقيقية."""
    W, H = 1080, 1080
    img = Image.new("RGBA", (W, H), (18, 18, 18, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 6)], fill=GOLD)
    d.rectangle([(0, H - 6), (W, H)], fill=GOLD)
    d.rounded_rectangle([(46, 60), (W - 46, H - 236)], radius=6, outline=(202, 156, 84, 150), width=3)

    d.text((W // 2, 190), ar(NAME), font=font("Regular", 42), fill=GOLD, anchor="ma")
    d.line([(W // 2 - 90, 250), (W // 2 + 90, 250)], fill=(202, 156, 84, 140), width=2)
    d.text((W // 2, 380), ar(headline), font=fit(headline, "Bold", 108, W - 200), fill=WHITE, anchor="ma")
    d.text((W // 2, 540), ar(service), font=fit(service, "Regular", 50, W - 220), fill=CREAM, anchor="ma")

    d.text((W // 2, 690), ar("أرسل صورة المكان وأقولك السعر"), font=font("Regular", 40), fill=(186, 174, 160), anchor="ma")
    d.text((W // 2, 760), ar("إذا اتفقنا أمشي على كلامنا"), font=font("Regular", 40), fill=(186, 174, 160), anchor="ma")

    watermark(img, angle=32, opacity=13)
    bottom_bar(img)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  {out.relative_to(ROOT)}")


BASE = Path("/home/user/.cache/mydairaw")
ADS = ROOT / "إعلانات"

JOBS = [
    # أفران
    ("oven-clay.jpg", "أفران/صور/01-الطين.png", "فرن طين يجمع العيلة", "خبز ومندي ومشويات", (1080, 1080)),
    ("oven-clay.jpg", "أفران/صور/02-ستوري.png", "فرن حطب للبيت والمزرعة", "طين وحجر وطوب حراري", (1080, 1920)),
    # بناء بلك
    ("block-wall.jpg", "بناء-بلك/صور/01-الجدار.png", "بناء بلك في الرياض", "شغل نظيف ومرتب", (1080, 1080)),
    ("block-laying.jpg", "بناء-بلك/صور/02-اليومية.png", "يومية أو مقطوعية", "الفواصل مستقيمة", (1080, 1080)),
    ("block-wall.jpg", "بناء-بلك/صور/03-السور.png", "سور وحوش بلك", "مقاس 10 و15 و20", (1080, 1080)),
    ("partition-interior.jpg", "بناء-بلك/صور/04-الفواصل.png", "فواصل وغرف بلك", "مكان مكنوس وشغل مرتب", (1080, 1080)),
    ("block-joint-close.jpg", "بناء-بلك/صور/06-التفصيلة.png", "فواصل نظيفة", "شغل يد مرتب", (1080, 1080)),
    ("block-wall.jpg", "بناء-بلك/صور/07-ستوري.png", "بناء بلك", "شغل نظيف ومرتب", (1080, 1920)),
    # مشبات
    ("majlis-fireplace.jpg", "مشبات-الشتاء/صور/01-الحوش.png", "جهز مشبتك قبل البرد", "في البيت والحوش والمزرعة", (1080, 1080)),
    ("winter-majlis.jpg", "مشبات-الشتاء/صور/02-جهز.png", "جهز مشبتك للشتاء", "مشبات حطب وطوب وحجر", (1080, 1080)),
    ("winter-majlis.jpg", "مشبات-الشتاء/صور/03-ستوري.png", "جهز مشبتك قبل البرد", "مشبات الرياض", (1080, 1920)),
    ("firepit-majlis.jpg", "مشبات-الشتاء/صور/04-الجلسة.png", "جلسة شتوية مرتبة", "مشبة ومجلس على مقاس مكانك", (1080, 1080)),
    ("majlis-fireplace.jpg", "مشبات-الشتاء/صور/05-الليل.png", "ليالي الشتاء أحلى مع مشبة", "نار دافية ومجلس مرتب", (1080, 1080)),
    # فرن ومنضدة
    ("oven-brick-counter.jpg", "فرن-ومنضدة/صور/01-الطوب.png", "فرن ومنضدة بطوب", "شغل يد مرتب", (1080, 1080)),
]


def main() -> None:
    print("== توليد صور الإعلانات ==")
    for src, rel, title, sub, size in JOBS:
        compose(BASE / src, ADS / rel, title, sub, size)

    print("== بطاقة الفرق بين اليومية والمقطوعية ==")
    card(
        ADS / "بناء-بلك/صور/05-يومية-ومقطوعية.png",
        "يومية أو مقطوعية",
        [
            ("اليومية", "أجرة اليوم تتفق عليها من البداية\nوالمواد منك إلا إذا اتفقنا غير كذا"),
            ("المقطوعية", "سعر الشغلة يطلع على مكانك\nوإذا اتفقنا أمشي على كلامنا"),
        ],
        "أرسل نوع البلك والطول والارتفاع وصورة المكان",
    )

    print("== بطاقة تعريف إعلان الحجر ==")
    brand_card(
        ADS / "حجر-تراثي/صور/08-الأعمال.png",
        "حجر تراثي",
        "جدران وواجهات وأسوار وبوابات",
    )


if __name__ == "__main__":
    main()
