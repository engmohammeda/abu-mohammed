#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وسم صور إعلان «معلم بلك باليومية والمقطوعية» بالهوية المعتمدة.

المقاسات المعتمدة في هذا الإعلان
    1080x1080   صور الإعلان المربعة
    1080x1920   الستوري
    1500x1500   غلاف المنصة      من أدوات/تجهيز-أصول-الحساب.py
    400x400     صورة الحساب       من أدوات/تجهيز-أصول-الحساب.py

العلامة المائية ثلاث طبقات
    1 شريط سفلي مقروء فيه الاسم والرقم
    2 ختم صغير داخل البكسلات فوق الشريط فيه الاسم والرقم
    3 تكرار قطري بشفافية 18 بالمئة بنفس النص

لا تكتب على الصور أي عبارة عن الفواصل أو المكنوس أو النظافة أو الترتيب.
الصورة نفسها تتكلم. النص على الصور إنساني وقصير وبلا ترقيم.

الاستخدام
    python3 أدوات/وسم-معلم-بلك-يومية-ومقطوعية.py
    python3 أدوات/تجهيز-أصول-الحساب.py
"""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from arabic_reshaper import ArabicReshaper

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path(os.environ.get("MYDAD_FONTS", "/home/user/fonts"))
RAW = ROOT / "إعلانات" / "معلم-بلك-يومية-ومقطوعية" / "خام"
OUT = ROOT / "إعلانات" / "معلم-بلك-يومية-ومقطوعية" / "صور"

NAME = "أبو محمد معلم بلك ومباني"
PHONE = "0531060401"

GOLD = (202, 156, 84)
CREAM = (240, 225, 210)
WHITE = (255, 255, 255)
INK = (16, 16, 16)
CARD_BG = (18, 18, 18)
MUTED = (188, 174, 160)

_reshaper = ArabicReshaper(
    {
        "use_unshaped_instead_of_isolated": True,
        "delete_harakat": True,
        "support_ligatures": True,
        "language": "Arabic",
    }
)


def ar(text: str) -> str:
    # Raqm يتولى اتجاه الكتابة، نكتفي بتشكيل الحروف
    return _reshaper.reshape(text)


_fonts: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    key = (weight, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(str(FONT_DIR / f"Almarai-{weight}.ttf"), size)
    return _fonts[key]


def fit(text: str, weight: str, size: int, max_w: int, min_size: int = 20) -> ImageFont.FreeTypeFont:
    while size > min_size:
        f = font(weight, size)
        if f.getlength(ar(text)) <= max_w:
            return f
        size -= 2
    return font(weight, min_size)


def scale(value: int, W: int) -> int:
    """قياس العناصر بالنسبة لعرض 1080 حتى تعمل على كل المقاسات."""
    return max(1, round(value * W / 1080))


def gradient_band(canvas: Image.Image, height: int, top_alpha: int = 232) -> None:
    band = Image.new("RGBA", (canvas.width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(band)
    for y in range(height):
        a = int(top_alpha * (1 - y / height) ** 1.25)
        d.line([(0, y), (canvas.width, y)], fill=(10, 10, 10, a))
    canvas.alpha_composite(band, (0, 0))


def bottom_bar(canvas: Image.Image, height: int) -> None:
    w, h = canvas.size
    bar = Image.new("RGBA", (w, height), INK + (255,))
    d = ImageDraw.Draw(bar)
    d.line([(0, 0), (w, 0)], fill=GOLD + (220,), width=max(2, scale(2, w)))
    nf = fit(NAME, "Bold", scale(40, w), int(w * 0.60))
    d.text((w - scale(36, w), height // 2), ar(NAME), font=nf, fill=GOLD, anchor="rm")
    pf = font("Regular", scale(44, w))
    d.text((scale(36, w), height // 2 + scale(2, w)), PHONE, font=pf, fill=CREAM, anchor="lm")
    canvas.alpha_composite(bar, (0, h - height))


def stamp(canvas: Image.Image, bar_height: int) -> None:
    """ختم مقروء داخل البكسلات فوق الشريط، الاسم والرقم معاً."""
    w, h = canvas.size
    pad = scale(16, w)
    box_w = scale(392, w)
    box_h = scale(88, w)
    x1 = w - scale(36, w) - box_w
    y1 = h - bar_height - box_h - scale(18, w)
    x2, y2 = x1 + box_w, y1 + box_h
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([(x1, y1), (x2, y2)], radius=scale(6, w), fill=(12, 12, 12, 205), outline=GOLD + (200,), width=max(1, scale(2, w)))
    nf = fit(NAME, "Bold", scale(30, w), box_w - pad * 2)
    d.text(((x1 + x2) // 2, y1 + scale(31, w)), ar(NAME), font=nf, fill=GOLD, anchor="mm")
    pf = font("Bold", scale(31, w))
    d.text(((x1 + x2) // 2, y1 + scale(64, w)), PHONE, font=pf, fill=CREAM, anchor="mm")
    canvas.alpha_composite(layer)


def watermark(canvas: Image.Image, angle: int = 32, opacity: int = 46) -> None:
    """تكرار قطري بنص الاسم والرقم، شفافية 18 بالمئة."""
    w, h = canvas.size
    tile_w = w + scale(400, w)
    tile_h = scale(220, w)
    tile = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    tf = font("Regular", scale(30, w))
    d.text((tile_w // 2, tile_h // 2), ar(NAME + "  " + PHONE), font=tf, fill=(255, 255, 255, opacity), anchor="mm")
    tile = tile.rotate(angle, expand=True, resample=Image.BICUBIC)
    step_x, step_y = tile.width + scale(60, w), tile.height + scale(90, w)
    for y in range(-tile.height, h + tile.height, step_y):
        for x in range(-tile.width, w + tile.width, step_x):
            canvas.alpha_composite(tile, (x, y))


def headline(canvas: Image.Image, title: str, subtitle: str) -> None:
    W, H = canvas.size
    d = ImageDraw.Draw(canvas)
    portrait = H > W
    tf = fit(title, "Bold", scale(78 if portrait else 72, W), int(W * 0.86))
    sf = fit(subtitle, "Regular", scale(46 if portrait else 42, W), int(W * 0.84))
    top = int(H * (0.085 if portrait else 0.09))
    tb = d.textbbox((W // 2, top), ar(title), font=tf, anchor="ma")
    pad_y = scale(26, W)
    scrim_h = (tb[3] - top) + sf.size + scale(96, W) + pad_y * 2
    scrim = Image.new("RGBA", (W, scrim_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for y in range(scrim_h):
        fade = max(0.0, 1.0 - (y / scrim_h) ** 1.6)
        sd.line([(0, y), (W, y)], fill=(12, 12, 12, int(172 * fade)))
    canvas.alpha_composite(scrim, (0, top - pad_y))
    d = ImageDraw.Draw(canvas)
    d.text((W // 2, top), ar(title), font=tf, fill=WHITE, anchor="ma")
    d.text((W // 2, top + tf.size + scale(16, W)), ar(subtitle), font=sf, fill=GOLD, anchor="ma")
    ly = top + tf.size + sf.size + scale(68, W)
    d.line([(W // 2 - scale(70, W), ly), (W // 2 + scale(70, W), ly)], fill=GOLD + (180,), width=max(2, scale(2, W)))


def compose_photo(
    src: Path,
    out: Path,
    title: str,
    subtitle: str,
    size: tuple[int, int] = (1080, 1080),
    centering: tuple[float, float] = (0.5, 0.45),
) -> None:
    W, H = size
    base = Image.open(src).convert("RGB")
    img = ImageOps.fit(base, (W, H), method=Image.LANCZOS, centering=centering).convert("RGBA")

    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    start = int(H * 0.70)
    for y in range(start, H):
        ratio = max(0.0, (y - start) / (H - start))
        sd.line([(0, y), (W, y)], fill=(0, 0, 0, int(120 * ratio ** 1.1)))
    img.alpha_composite(shade)

    gradient_band(img, int(H * 0.36), 208)
    headline(img, title, subtitle)
    watermark(img, angle=32, opacity=46)
    bar_h = int(H * 0.118)
    bottom_bar(img, bar_h)
    stamp(img, bar_h)

    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "JPEG", quality=94, subsampling=0, optimize=True)
    print(f"  {out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB  {W}x{H}")


def text_card(out: Path, title: str, rows: list[tuple[str, str]], footer: str, size: int = 1080) -> None:
    W = H = size
    img = Image.new("RGBA", (W, H), CARD_BG + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, scale(8, W))], fill=GOLD)
    d.rectangle([(0, H - scale(8, W)), (W, H)], fill=GOLD)
    d.rounded_rectangle([(scale(48, W), scale(56, W)), (W - scale(48, W), H - scale(170, W))],
                        radius=scale(8, W), outline=GOLD + (150,), width=max(2, scale(3, W)))

    d.text((W // 2, scale(132, W)), ar(NAME), font=font("Regular", scale(40, W)), fill=GOLD, anchor="ma")
    d.line([(W // 2 - scale(100, W), scale(198, W)), (W // 2 + scale(100, W), scale(198, W))],
           fill=GOLD + (150,), width=max(2, scale(2, W)))
    d.text((W // 2, scale(286, W)), ar(title), font=fit(title, "Bold", scale(92, W), W - scale(160, W)),
           fill=WHITE, anchor="ma")

    n = len(rows)
    # منطقة الصناديق محدودة حتى لا تتداخل مع الختم والنص السفلي
    top = scale(384, W)
    gap = scale(16 if n == 3 else 22, W)
    bottom_limit = scale(772, W)
    box_h = (bottom_limit - top - gap * (n - 1)) // n
    for i, (head, body) in enumerate(rows):
        y = top + i * (box_h + gap)
        d.rounded_rectangle([(scale(92, W), y), (W - scale(92, W), y + box_h)],
                            radius=scale(10, W), outline=GOLD + (120,), width=max(2, scale(2, W)))
        d.text((W - scale(128, W), y + box_h // 2), ar(head),
               font=fit(head, "Bold", scale(46, W), scale(500, W)), fill=GOLD, anchor="rm")
        lines = body.split("\n")
        fnt = fit(lines[0], "Regular", scale(34, W), scale(520, W))
        for j, line in enumerate(lines):
            d.text((scale(150, W), y + box_h // 2 - (len(lines) - 1) * scale(24, W) + j * scale(46, W)),
                   ar(line), font=fnt, fill=CREAM, anchor="lm")

    # السطر السفلي في الجهة المقابلة للختم حتى لا يتداخلا
    ff = fit(footer, "Regular", scale(31, W), scale(600, W))
    d.text((scale(64, W), scale(852, W)), ar(footer), font=ff, fill=MUTED, anchor="lm")
    watermark(img, angle=32, opacity=40)
    bar_h = int(H * 0.118)
    bottom_bar(img, bar_h)
    stamp(img, bar_h)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  {out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB  {W}x{H}")


def main() -> None:
    print("== صور الإعلان 1080x1080 ==")
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [
        ("01-hero.jpg", "01-الغلاف.jpg", "معلم بلك ومباني في الرياض", "يومية أو مقطوعية"),
        ("02-fence.jpg", "02-السور.jpg", "سور يحفظ حوشك", "من أول بلكة لآخر مدماك"),
        ("03-room.jpg", "03-الغرفة.jpg", "غرفة زايدة على مكانك", "تبنيها على كيفك"),
        ("04-wall.jpg", "04-الجدار.jpg", "جدار ما يميل", "تشوفه بعينك قبل ما تتفق"),
        ("05-gate.jpg", "05-البوابة.jpg", "مدخل يهيّب لبيتك", "أعمدة وبوابة على مقاسك"),
        ("06-annex.jpg", "06-الملاحق.jpg", "ملحق أو مخزن على كيفك", "غرفتين في حوشك"),
        ("07-corner.jpg", "07-الزاوية.jpg", "كل مدماك بحساب", "هنا يبان الفرق"),
    ]
    for src, dst, title, sub in jobs:
        compose_photo(RAW / src, OUT / dst, title, sub)

    print("== البطاقات ==")
    text_card(
        OUT / "08-بطاقة-يومية-ومقطوعية.png",
        "يومية أو مقطوعية",
        [
            ("اليومية", "أجرة اليوم على شغلك"),
            ("المقطوعية", "سعر الشغلة كاملة على مكانك\nنتفق من أولها"),
        ],
        "أرسل صورة المكان ونشوف السعر المناسب لشغلك",
    )
    text_card(
        OUT / "09-بطاقة-خطوات-السعر.png",
        "ثلاث خطوات للسعر",
        [
            ("صورة المكان", "أرسلها وأنا أشوف الشغل"),
            ("الطول والارتفاع", "المقاس التقريبي كافي"),
            ("نوع البلك", "10 أو 15 أو 20 حسب شغلك"),
        ],
        "أرسل صورة المكان ونشوف السعر المناسب لشغلك",
    )

    print("== الستوري 1080x1920 ==")
    compose_photo(RAW / "08-story.jpg", OUT / "10-ستوري.jpg",
                  "معلم بلك ومباني في الرياض", "يومية أو مقطوعية", size=(1080, 1920), centering=(0.5, 0.5))
    compose_photo(RAW / "09-story-room.jpg", OUT / "11-ستوري-الغرفة.jpg",
                  "غرفتك تبدأ من هنا", "الشغل على أصول المهنة", size=(1080, 1920), centering=(0.5, 0.5))

    # غلاف المنصة 1500x1500 وصورة الحساب 400x400 لا تُولَّد هنا.
    # مصدرهما أصول صاحب الحساب القديمة عبر: python3 أدوات/تجهيز-أصول-الحساب.py
    print("غلاف 1500 وصورة الحساب 400 يأتيان من تجهيز-أصول-الحساب.py")


if __name__ == "__main__":
    main()
