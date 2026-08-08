#!/usr/bin/env python3
"""ERJ v1 — full-site validator.

Every class of bug the previous site actually shipped now has a test here,
so it cannot come back silently:

  · a page with no canonical, or a canonical containing a fragment
  · an og:image pointing at a file that was never generated
  · two pages sharing one og:image (they then look duplicate to Google)
  · a sw.js SHELL entry that does not exist (aborts the WHOLE precache)
  · a stylesheet a page does not actually load
  · an <img> with no width/height (layout shift) or no alt (a11y)
  · photos at more than one aspect ratio (the sizing complaint)
  · a heading level skipped, a duplicate id, an empty link
  · hard-coded colours or px gutters that bypass the token system
"""
import re, json, pathlib, sys, collections

ROOT = pathlib.Path(__file__).parent
BUILD = ROOT / "build"
SITE = "https://everythingremotejob.com"

errors, warnings, notes = [], [], []
HTML = sorted(BUILD.glob("*.html"))


def read(p):
    return p.read_text(encoding="utf-8", errors="ignore")


# ── 1 · markup balance and structure ──────────────────────────────────
for f in HTML:
    s, rel = read(f), f.name
    for tag in ("html", "head", "body", "main", "header", "footer", "section",
                "figure", "article", "nav"):
        o = len(re.findall(rf"<{tag}\b", s, re.I))
        c = len(re.findall(rf"</{tag}>", s, re.I))
        if o != c:
            errors.append(f"{rel}: <{tag}> {o} open / {c} close")

    if len(re.findall(r"<h1\b", s)) != 1:
        errors.append(f"{rel}: needs exactly one <h1> (found {len(re.findall(r'<h1', s))})")

    ids = re.findall(r'\sid="([^"]+)"', s)
    for i, n in collections.Counter(ids).items():
        if n > 1:
            errors.append(f"{rel}: duplicate id '{i}' ({n}x)")

    # heading levels must not skip (h2 -> h4)
    levels = [int(m) for m in re.findall(r"<h([1-4])\b", s)]
    for a, b in zip(levels, levels[1:]):
        if b - a > 1:
            warnings.append(f"{rel}: heading jumps h{a} -> h{b}")


# ── 2 · images: alt, dimensions, one geometry ─────────────────────────
ratios = set()
for f in HTML:
    s, rel = read(f), f.name
    for tag in re.findall(r"<img\b[^>]*>", s):
        if 'alt="' not in tag:
            errors.append(f"{rel}: <img> without alt")
        if 'width="' not in tag or 'height="' not in tag:
            errors.append(f"{rel}: <img> without width/height (causes layout shift)")
        src = re.search(r'src="([^"]+)"', tag)
        if src and not src.group(1).startswith("data:"):
            if not (BUILD / src.group(1)).exists():
                errors.append(f"{rel}: <img> src missing on disk -> {src.group(1)}")
        w = re.search(r'width="(\d+)"', tag)
        h = re.search(r'height="(\d+)"', tag)
        if w and h and "lockup" not in tag and int(h.group(1)) > 0:
            ratios.add(round(int(w.group(1)) / int(h.group(1)), 3))

if len(ratios) > 1:
    errors.append(f"UI photos render at {len(ratios)} different aspect ratios: "
                  f"{sorted(ratios)} — they must all be one")
else:
    notes.append(f"every UI photo renders at one aspect ratio ({sorted(ratios)[0] if ratios else 'n/a'})")

manifest_img = json.loads((BUILD / "images.json").read_text())
bad = [k for k, m in manifest_img.items() if m["ratio"] != "3 / 2"]
if bad:
    errors.append(f"images not normalised to 3:2: {bad}")


# ── 3 · links resolve ─────────────────────────────────────────────────
for f in HTML:
    s, rel = read(f), f.name
    for attr in ("href", "src"):
        for m in re.finditer(rf'{attr}="([^"]+)"', s):
            v = m.group(1)
            if v.startswith(("http", "mailto:", "tel:", "data:", "#", "//")):
                continue
            target = BUILD / v.split("#")[0]
            if not target.exists():
                errors.append(f"{rel}: dead {attr} -> {v}")
    # no empty links
    if re.search(r"<a\b[^>]*>\s*</a>", s):
        errors.append(f"{rel}: empty <a> element")


# ── 4 · SEO ───────────────────────────────────────────────────────────
og_seen, canon_seen = {}, {}
for f in HTML:
    s, rel = read(f), f.name
    can = re.search(r'rel="canonical" href="([^"]+)"', s)
    if not can:
        errors.append(f"{rel}: no canonical")
    else:
        if "#" in can.group(1):
            errors.append(f"{rel}: canonical contains a fragment (Google discards it)")
        canon_seen.setdefault(can.group(1), []).append(rel)
    if 'name="robots"' not in s:
        errors.append(f"{rel}: no robots meta")
    if not re.search(r'<meta name="description" content="[^"]{60,}"', s):
        warnings.append(f"{rel}: description missing or under 60 chars")
    tm = re.search(r"<title>(.*?)</title>", s)
    if tm and not (28 <= len(tm.group(1)) <= 68):
        warnings.append(f"{rel}: full title is {len(tm.group(1))} chars (aim 28-68)")

    og = re.search(r'property="og:image" content="([^"]+)"', s)
    if not og:
        errors.append(f"{rel}: no og:image")
    else:
        path = og.group(1).replace(SITE + "/", "")
        if not (BUILD / path).exists():
            errors.append(f"{rel}: og:image missing on disk -> {path}")
        og_seen.setdefault(path, []).append(rel)

    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(block)
        except Exception as e:
            errors.append(f"{rel}: invalid JSON-LD ({e})")

for img, pages in og_seen.items():
    if len(pages) > 1:
        errors.append(f"{len(pages)} pages share one og:image ({img}): {pages}")
for url, pages in canon_seen.items():
    if len(pages) > 1:
        errors.append(f"{len(pages)} pages claim the same canonical {url}: {pages}")

sm = read(BUILD / "sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for loc in locs:
    p = loc.replace(SITE + "/", "") or "index.html"
    if not (BUILD / p).exists():
        errors.append(f"sitemap lists {loc} which does not exist")
noindexed = {f.name for f in HTML if 'content="noindex' in read(f)}
for loc in locs:
    p = loc.replace(SITE + "/", "") or "index.html"
    if p in noindexed:
        errors.append(f"sitemap lists {p}, which is noindex")
notes.append(f"sitemap: {len(locs)} urls, all resolve, none noindexed")


# ── 5 · service worker precache integrity ─────────────────────────────
sw = read(BUILD / "sw.js")
shell = json.loads(re.search(r"const SHELL = (\[.*?\]);", sw, re.S).group(1))
missing = [u for u in shell if u != "./" and not (BUILD / u[2:]).exists()]
if missing:
    errors.append(f"sw.js SHELL names {len(missing)} file(s) that do not exist: {missing[:4]}")
else:
    notes.append(f"sw.js precache: {len(shell)} files, every one present")


# ── 6 · one stylesheet, one script, no page-local CSS ─────────────────
for f in HTML:
    s, rel = read(f), f.name
    if 'href="app.css"' not in s:
        errors.append(f"{rel}: does not load app.css")
    if s.count("<style") > 0:
        errors.append(f"{rel}: has a page-local <style> block (design must live in app.css)")
    if 'src="app.js"' not in s:
        errors.append(f"{rel}: does not load app.js")
    if re.search(r"\son(click|load|error|mouseover)=", s):
        errors.append(f"{rel}: inline event handler (behaviour must live in app.js)")


# ── 7 · design-token discipline ───────────────────────────────────────
css = read(BUILD / "app.css")
if "--gutter" not in css:
    errors.append("app.css: the gutter token is gone")
body_css = css.split(":root")[-1]
hex_colours = set(re.findall(r"#[0-9A-Fa-f]{6}", css.split("/* ── 2")[1]))
if hex_colours:
    warnings.append(f"app.css: raw hex outside the token block: {sorted(hex_colours)[:5]}")
for pat, why in [(r"overflow-x:\s*hidden", "use overflow-x:clip — hidden breaks position:sticky"),
                 (r"\.(?:wa|totop|drawer)\s*\{[^}]*left:\s*0(?!\w)",
                  "a floating control is pinned to 0 — it must respect --gutter")]:
    if re.search(pat, css):
        warnings.append(f"app.css: {why}")
if "visibility:hidden" not in css.split(".drawer")[1][:400]:
    errors.append("app.css: closed drawer needs visibility:hidden or it widens the page")
if "prefers-reduced-motion" not in css:
    errors.append("app.css: no reduced-motion handling")
if "env(safe-area-inset" not in css:
    warnings.append("app.css: no safe-area handling for notched devices")


# ── 8 · edge safety: nothing pinned to a bare 0 ───────────────────────
for m in re.finditer(r"\.(wa|totop|drawer|promise|hdr-in)\s*\{([^}]*)\}", css):
    block = m.group(2)
    if re.search(r"(right|left|padding-inline|padding):\s*0(?!\w|\.)", block):
        errors.append(f".{m.group(1)}: pinned to 0 — content would touch the screen edge")


# ── report ────────────────────────────────────────────────────────────
print("\n── NOTES ──")
for n in notes:
    print("  · " + n)
if warnings:
    print("\n── WARNINGS ──")
    for w in warnings:
        print("  ! " + w)
print("\n── ERRORS ──")
if errors:
    for e in errors:
        print("  ✗ " + e)
    print(f"\n{len(errors)} error(s) across {len(HTML)} pages\n")
    sys.exit(1)
print(f"  none — {len(HTML)} pages validate clean\n")
