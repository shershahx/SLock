"""
generate_icons.py
Generates the full set of Android launcher icon assets from app_logo.png.

Outputs:
  Legacy mipmap PNGs (ic_launcher.png + ic_launcher_round.png) for all 5 densities.
  Adaptive foreground PNG (432x432, 108dp @ 4x) placed in mipmap-xxxhdpi.
  Adaptive icon XMLs in mipmap-anydpi-v26.
  Solid colour XML for the adaptive background.
"""

import os
import math
from pathlib import Path
from PIL import Image, ImageDraw

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
SRC  = ROOT / "app_logo.png"
RES  = ROOT / "app" / "src" / "main" / "res"
DRW  = RES / "drawable"

# ─────────────────────────────────────────────────────────────────────────────
# Android launcher icon sizes (px) per density bucket
# ─────────────────────────────────────────────────────────────────────────────
DENSITIES = {
    "mdpi":    48,
    "hdpi":    72,
    "xhdpi":   96,
    "xxhdpi":  144,
    "xxxhdpi": 192,
}

# Adaptive foreground canvas: 108dp rendered at each density
# The safe zone (guaranteed-visible area) is the central 72dp
ADAPTIVE_FG_SIZES = {
    "mdpi":    108,   # 108dp × 1.0
    "hdpi":    162,   # 108dp × 1.5
    "xhdpi":   216,   # 108dp × 2.0
    "xxhdpi":  324,   # 108dp × 3.0
    "xxxhdpi": 432,   # 108dp × 4.0
}


def make_dirs():
    for density in DENSITIES:
        (RES / f"mipmap-{density}").mkdir(parents=True, exist_ok=True)
    (RES / "mipmap-anydpi-v26").mkdir(parents=True, exist_ok=True)
    DRW.mkdir(parents=True, exist_ok=True)
    print("[dirs] All mipmap directories created.")


# ─────────────────────────────────────────────────────────────────────────────
# Legacy square icon: resize source to NxN, no rounding
# ─────────────────────────────────────────────────────────────────────────────
def make_legacy_icons(src: Image.Image):
    for density, size in DENSITIES.items():
        out_dir = RES / f"mipmap-{density}"

        # Square (standard)
        img = src.resize((size, size), Image.LANCZOS)
        img.save(out_dir / "ic_launcher.png", "PNG", optimize=True)

        # Round – clip to circle on a transparent background
        img_round = src.resize((size, size), Image.LANCZOS).convert("RGBA")
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size - 1, size - 1), fill=255)
        result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        result.paste(img_round, mask=mask)
        result.save(out_dir / "ic_launcher_round.png", "PNG", optimize=True)

        print(f"[legacy] mipmap-{density}: {size}px square + round")


# ─────────────────────────────────────────────────────────────────────────────
# Adaptive foreground PNGs
# 108dp canvas; logo fills the central 72dp safe zone (2/3 of canvas).
# The outer 18dp on each side is the bleed zone (may be cropped by launcher).
# ─────────────────────────────────────────────────────────────────────────────
def make_adaptive_foreground(src: Image.Image):
    """
    Renders the logo centred within the 108dp adaptive foreground canvas.
    The logo is scaled to occupy the 72dp safe zone (66.7% of canvas).
    Background is fully transparent — the adaptive background layer provides colour.
    """
    for density, canvas_px in ADAPTIVE_FG_SIZES.items():
        out_dir = RES / f"mipmap-{density}"
        out_dir.mkdir(parents=True, exist_ok=True)

        # Safe zone = central 72/108 = 2/3 of canvas
        safe_px = int(canvas_px * 72 / 108)

        canvas = Image.new("RGBA", (canvas_px, canvas_px), (0, 0, 0, 0))
        logo   = src.convert("RGBA").resize((safe_px, safe_px), Image.LANCZOS)
        offset = (canvas_px - safe_px) // 2
        canvas.paste(logo, (offset, offset), logo)
        canvas.save(out_dir / "ic_launcher_foreground.png", "PNG", optimize=True)
        print(f"[fg]     mipmap-{density}: {canvas_px}px canvas, {safe_px}px logo")


# ─────────────────────────────────────────────────────────────────────────────
# Adaptive background colour XML  (matches logo's navy background #0F1E3C)
# ─────────────────────────────────────────────────────────────────────────────
def make_background_xml():
    xml = """\
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <solid android:color="#0F1E3C" />
</shape>
"""
    path = DRW / "ic_launcher_background.xml"
    path.write_text(xml, encoding="utf-8")
    print("[xml]  drawable/ic_launcher_background.xml written.")


# ─────────────────────────────────────────────────────────────────────────────
# Adaptive icon XMLs  (mipmap-anydpi-v26)
# ─────────────────────────────────────────────────────────────────────────────
def make_adaptive_xmls():
    anydpi = RES / "mipmap-anydpi-v26"

    template = """\
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
</adaptive-icon>
"""
    (anydpi / "ic_launcher.xml").write_text(template, encoding="utf-8")
    (anydpi / "ic_launcher_round.xml").write_text(template, encoding="utf-8")
    print("[xml]  mipmap-anydpi-v26/ic_launcher.xml written.")
    print("[xml]  mipmap-anydpi-v26/ic_launcher_round.xml written.")


# ─────────────────────────────────────────────────────────────────────────────
# Verify every expected file exists
# ─────────────────────────────────────────────────────────────────────────────
def verify():
    expected = []
    for density in DENSITIES:
        d = RES / f"mipmap-{density}"
        expected += [
            d / "ic_launcher.png",
            d / "ic_launcher_round.png",
            d / "ic_launcher_foreground.png",
        ]
    expected += [
        RES / "mipmap-anydpi-v26" / "ic_launcher.xml",
        RES / "mipmap-anydpi-v26" / "ic_launcher_round.xml",
        DRW / "ic_launcher_background.xml",
    ]

    all_ok = True
    print("\n── Verification ─────────────────────────────────────────────────")
    for p in expected:
        exists = p.exists()
        size   = p.stat().st_size if exists else 0
        status = "✓" if exists else "✗ MISSING"
        print(f"  {status}  {p.relative_to(ROOT)}  ({size} bytes)")
        if not exists:
            all_ok = False

    print("─────────────────────────────────────────────────────────────────")
    if all_ok:
        print("All assets generated successfully.\n")
    else:
        print("ERROR: Some assets are missing!\n")
        raise SystemExit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print(f"Source: {SRC} ({SRC.stat().st_size:,} bytes)\n")
    src = Image.open(SRC).convert("RGBA")
    print(f"Source dimensions: {src.width}x{src.height}px\n")

    make_dirs()
    make_legacy_icons(src)
    make_adaptive_foreground(src)
    make_background_xml()
    make_adaptive_xmls()
    verify()


if __name__ == "__main__":
    main()
