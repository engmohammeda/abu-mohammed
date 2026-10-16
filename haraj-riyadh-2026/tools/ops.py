#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""أدوات تشغيل ح package حراج — فحص، تركيب، تدقيق صور، قالب تقرير."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = json.loads((ROOT / "tools" / "image-spec.json").read_text(encoding="utf-8"))

def cmd_check(_):
    subprocess.run([sys.executable, str(ROOT / "tools" / "check-banned.py")], check=False)

def cmd_render(args):
    targets = ["--all"] if args.all else (args.names or [])
    cmd = [sys.executable, str(ROOT / "tools" / "render.py")] + targets
    subprocess.run(cmd, check=False)

def cmd_audit(_):
    missing, bad = [], []
    for name, spec in SPEC["images"].items():
        p = ROOT / spec["file"]
        if not p.exists():
            missing.append(name); continue
        try:
            from PIL import Image
            im = Image.open(p)
            if tuple(im.size) != tuple(spec["size"]):
                bad.append((name, im.size, spec["size"]))
        except Exception as e:
            bad.append((name, str(e), spec["size"]))
    print(f"إجمالي الصور في المواصفة: {len(SPEC['images'])}")
    print(f"مفقودة: {len(missing)}")
    for m in missing: print("  -", m)
    print(f"مقاس خاطئ: {len(bad)}")
    for b in bad: print("  -", b)

def cmd_report(_):
    out = ROOT / "تقرير-الأسبوع.md"
    if out.exists():
        print("الملف موجود بالفعل:", out)
        return
    out.write_text("""# تقرير الأسبوع — مشبات وأفران (الرياض)

**الفترة:** 23–29 سبتمبر 2026

## 1) الرسائل الواردة
| التاريخ | القناة | السؤال | الصورة أُرسلت؟ | السعر أُرسل؟ | النتيجة |
|---|---|---|---|---|---|

## 2) مصادر الرسائل
- حراج:
- واتساب:
- قروبات:
- شركاء:
- لافتة الموقع:

## 3) الصور التي جلبت السؤال
- 

## 4) ما نُفِّذ
- 

## 5) ما لا يُكرر
- 

## 6) قرار الأسبوع القادم
- 
""", encoding="utf-8")
    print("أُنشئ:", out)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").set_defaults(func=cmd_check)
    r = sub.add_parser("render"); r.add_argument("--all", action="store_true"); r.add_argument("names", nargs="*"); r.set_defaults(func=cmd_render)
    sub.add_parser("audit").set_defaults(func=cmd_audit)
    sub.add_parser("report").set_defaults(func=cmd_report)
    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
