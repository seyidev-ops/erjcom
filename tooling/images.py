#!/usr/bin/env python3
"""ERJ v1 — image pipeline.

THE PROBLEM THIS SOLVES
The old site carried photos at aspect ratios from 0.67 to 1.50. Every card,
hero and figure that used them rendered a different shape, so nothing lined
up, and tall portraits towered over their neighbours. Patching that with
per-image CSS is how the old codebase accumulated .fi-art.tall, .hero-photo,
.photo-card and .r-photo — four rules doing one job.

THE RULE HERE
Every UI photo is produced at ONE geometry: 3:2 landscape. The crop happens
once, at build time, in the file itself — so the markup never needs to know
which picture it is holding, and there is no layout shift ever.

Each source yields three widths for srcset (600 / 1200 / 1800) plus a tiny
blurred LQIP used as the CSS background while the real file decodes.

Crop bias: tall sources are cropped toward the upper third, because on this
site every tall source is a person and faces sit high in the frame.
"""
from PIL import Image, ImageFilter
import pathlib, base64, io, json

SRC = pathlib.Path(__file__).parent / "assets" / "img-src"
OUT = pathlib.Path(__file__).parent / "build" / "img"
OUT.mkdir(parents=True, exist_ok=True)

RATIO = 3 / 2               # every UI photo, without exception
WIDTHS = [600, 1200, 1800]

# source -> (public name, vertical crop bias 0=top .5=centre 1=bottom)
PHOTOS = {
    "photo-remote-win-v2.webp":     ("celebrating-offer",   0.50),
    "photo-dollars-hand.webp":      ("hard-currency",       0.45),
    "photo-dollars-woman.webp":     ("paid-in-dollars",     0.40),
    "photo-woman-laptop.webp":      ("working-remotely",    0.42),
    "photo-billboard.webp":         ("out-in-the-world",    0.45),
    "photo-facilitator-suit.webp":  ("facilitator-formal",  0.22),
    "photo-facilitator-smile.webp": ("facilitator-warm",    0.30),
    "photo-facilitator-note.webp":  ("facilitator-note",    0.28),
    "photo-facilitator-offer.webp": ("facilitator-offer",   0.24),
    "founder-oluwaseyi.jpg":        ("facilitator-portrait", 0.20),
}


def crop_to_ratio(im, bias):
    """Cover-crop to RATIO, keeping the interesting band."""
    w, h = im.size
    if w / h > RATIO:                     # too wide: trim the sides evenly
        new_w = int(h * RATIO)
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:                                 # too tall: trim using the bias
        new_h = int(w / RATIO)
        top = int((h - new_h) * bias)
        top = max(0, min(top, h - new_h))
        box = (0, top, w, top + new_h)
    return im.crop(box)


def lqip(im):
    """A 24px blurred placeholder, inlined as a data URI."""
    tiny = im.resize((24, 16), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
    buf = io.BytesIO()
    tiny.save(buf, "JPEG", quality=42)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    manifest = {}
    for src_name, (public, bias) in PHOTOS.items():
        src = SRC / src_name
        if not src.exists():
            print(f"  !! missing source: {src_name}")
            continue

        im = Image.open(src).convert("RGB")
        base = crop_to_ratio(im, bias)

        sizes = []
        for w in WIDTHS:
            h = round(w / RATIO)
            # 1200 is the canonical display asset and must always exist, so a
            # mild upscale is accepted; beyond ~1.7x it only adds bytes.
            if w > WIDTHS[1] and w > base.width * 1.05:
                continue
            if w == WIDTHS[1] and w > base.width * 1.7:
                continue
            variant = base.resize((w, h), Image.LANCZOS)
            fn = f"{public}-{w}.webp"
            variant.save(OUT / fn, "WEBP", quality=82, method=6)
            sizes.append({"w": w, "file": fn,
                          "kb": round((OUT / fn).stat().st_size / 1024)})

        manifest[public] = {
            "sizes": sizes,
            "lqip": lqip(base),
            "ratio": "3 / 2",
            "width": WIDTHS[1],
            "height": round(WIDTHS[1] / RATIO),
        }
        widths = "/".join(str(s["w"]) for s in sizes)
        print(f"  {public:22s} {src_name:30s} -> 3:2 @ {widths}")

    (pathlib.Path(__file__).parent / "build" / "images.json").write_text(
        json.dumps(manifest, indent=1), encoding="utf-8")

    # brand artwork passes through untouched — never resample a logo
    for f in ["erj-lockup-white.png", "erj-mark-white.png", "favicon32.png",
              "favicon180.png", "appletouchicon.png", "icon192.png",
              "icon512.png", "icon192maskable.png", "icon512maskable.png"]:
        s = SRC / f
        if s.exists():
            (OUT.parent / f).write_bytes(s.read_bytes())

    total = sum(s["kb"] for m in manifest.values() for s in m["sizes"])
    print(f"\n  {len(manifest)} photos, one geometry (3:2), {total} KB total")


if __name__ == "__main__":
    main()
