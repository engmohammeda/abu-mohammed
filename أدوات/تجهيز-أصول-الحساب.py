#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تجهيز أصول الحساب من الصور القديمة المعتمدة.

صورة الحساب والغلاف تُشتق من أصول صاحب الحساب القديمة، لا من صور مولّدة:
    المتجر/صورة-الحساب.png       1000x1000   صورة الحساب القديمة
    المتجر/مرجع-الغلاف.jpg      3136x1344   غلاف الحساب القديم بأعلى دقة

ينتج:
    إعلانات/معلم-بلك-يومية-ومقطوعية/صور/صورة-الحساب-400.png    400x400
    إعلانات/معلم-بلك-يومية-ومقطوعية/صور/غلاف-1500.jpg          1500x1500

طريقة التحويل
    1 تصغير تدريجي على مراحل حتى لا تتفكك الحروف
    2 استعادة حدة خفيفة بعد التصغير
    3 حفظ PNG لصورة الحساب وJPEG بجودة عالية للغلاف

الاستخدام
    python3 أدوات/تجهيز-أصول-الحساب.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "المتجر"
OUT = ROOT / "إعلانات" / "معلم-بلك-يومية-ومقطوعية" / "صور"

PROFILE_SRC = STORE / "صورة-الحساب.png"
COVER_SRC = STORE / "مرجع-الغلاف.jpg"


def premium_resize(img: Image.Image, w: int, h: int) -> Image.Image:
    """تصغير تدريجي على مراحل مع استعادة حدة خفيفة."""
    img = img.convert("RGB")
    cur = img
    while min(cur.size) > max(w, h) * 2:
        cur = cur.resize((max(1, cur.width // 2), max(1, cur.height // 2)),
                         Image.Resampling.LANCZOS)
    cur = cur.resize((w, h), Image.Resampling.LANCZOS)
    return cur.filter(ImageFilter.UnsharpMask(radius=1.1, percent=125, threshold=2))


def square_center(img: Image.Image) -> Image.Image:
    """قص مربع من منتصف الغلاف العريض مع الحفاظ على التصميم كاملاً."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    return img.crop((left, 0, left + side, side))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    print("== صورة الحساب 400x400 من الصورة القديمة ==")
    src = Image.open(PROFILE_SRC)
    print(f"  المصدر: {PROFILE_SRC.name}  {src.size}")
    out = OUT / "صورة-الحساب-400.png"
    premium_resize(src, 400, 400).save(out, "PNG", optimize=True)
    print(f"  {out.name}  (400, 400)  {out.stat().st_size // 1024} KB")

    print("\n== غلاف 1500x1500 من الغلاف القديم ==")
    cov = Image.open(COVER_SRC)
    print(f"  المصدر: {COVER_SRC.name}  {cov.size}")
    sq = square_center(cov)
    print(f"  قص مربع: {sq.size}")
    out = OUT / "غلاف-1500.jpg"
    premium_resize(sq, 1500, 1500).save(out, "JPEG", quality=93, subsampling=0, optimize=True)
    print(f"  {out.name}  (1500, 1500)  {out.stat().st_size // 1024} KB")

    print("\n== اختبار قراءة صورة الحساب دائرية ==")
    from PIL import ImageDraw
    p = Image.open(OUT / "صورة-الحساب-400.png").convert("RGBA")
    mask = Image.new("L", (400, 400), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 399, 399), fill=255)
    bg = Image.new("RGB", (400, 400), (240, 240, 240))
    bg.paste(p, (0, 0), mask)
    bg.resize((600, 600), Image.Resampling.LANCZOS).save(
        "/home/user/raw2/check-old-circle.jpg", "JPEG", quality=94)
    print("  /home/user/raw2/check-old-circle.jpg")


if __name__ == "__main__":
    main()
