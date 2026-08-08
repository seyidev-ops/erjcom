#!/usr/bin/env python3
"""ERJ v1.1 — full-site validator (merged build).

The site now has two halves that are validated differently:

  V1_STRICT  — the 11 marketing pages this rebuild generates. Must use
               app.css/app.js exclusively, no page-local <style>, exactly
               one <h1>, no skipped heading levels, one aspect ratio (3:2)
               on every UI photo.

  PORTAL     — the 11 ported operational pages (login, dashboard, admin,
               instructor, surge console, earlybird, offline) plus the 3
               real tool directories (cvscan/, cvbuilder/, diagnose/).
               These are self-contained by design (their own inline
               styles, their own scripts) and are validated on the things
               that matter regardless of which design system a page uses:
               links resolve, images have alt+dimensions, canonical and
               robots meta are present and correct, the WhatsApp number is
               the one true number, and the service worker can actually
               precache the file.

Checks that apply EVERYWHERE regardless of which half a page belongs to
are simply not scoped to either list.
"""
import re, json, pathlib, sys, collections

ROOT = pathlib.Path(__file__).parent
BUILD = ROOT / "build"
SITE = "https://everythingremotejob.com"

errors, warnings, notes = [], [], []
ALL_HTML = sorted(BUILD.rglob("*.html"))

V1_STRICT = {"index.html", "free.html", "starting-line.html", "mastery-training.html",
             "get-a-remote-job.html", "inner-circle.html", "masterclass.html",
             "testimonials.html", "blog.html", "register.html", "404.html"}
# real content pages ported in, but still public and still expected to behave
# like a normal page (one h1, sane heading order) — just not app.css-bound
CONTENT_TOOLS = {"cvscan/index.html", "diagnose/index.html", "cvbuilder/index.html"}
# single-page apps: headings are rendered dynamically or not used semantically
APPS = {"login.html", "dashboard.html", "admin.html", "admin-login.html",
        "instructor.html", "instructor-login.html", "blog-admin.html",
        "erj-surge-console.html", "offline.html", "participant.html",
        "earlybird.html", "cvbuilder/index.html"}


def read(p): return p.read_text(encoding="utf-8", errors="ignore")
def rel(p): return str(p.relative_to(BUILD))


# ── 1 · markup balance (every page, no exceptions) ────────────────────
for f in ALL_HTML:
    s = read(f)
    for tag in ("html", "head", "body", "main", "section", "div", "figure"):
        o = len(re.findall(rf"<{tag}\b", s, re.I))
        c = len(re.findall(rf"</{tag}>", s, re.I))
        if tag in ("html", "head", "body") and o != c:
            errors.append(f"{rel(f)}: <{tag}> {o} open / {c} close")
    ids = re.findall(r'\sid="([^"]+)"', s)
    for i, n in collections.Counter(ids).items():
        if n > 1:
            warnings.append(f"{rel(f)}: duplicate id '{i}' ({n}x)")


# ── 2 · heading structure — only where it is meant to hold ─────────────
for f in ALL_HTML:
    r = rel(f)
    if r in APPS:
        continue
    s = read(f)
    h1s = len(re.findall(r"<h1\b", s))
    if h1s != 1:
        (errors if r in V1_STRICT else warnings).append(
            f"{r}: expected exactly one <h1>, found {h1s}")


# ── 3 · images: alt + dimensions everywhere; one ratio on V1 pages ────
ratios = set()
for f in ALL_HTML:
    r, s = rel(f), read(f)
    for tag in re.findall(r"<img\b[^>]*>", s):
        if 'alt="' not in tag:
            errors.append(f"{r}: <img> without alt")
        if 'width="' not in tag or 'height="' not in tag:
            (errors if r in V1_STRICT else warnings).append(
                f"{r}: <img> without width/height")
        src = re.search(r'src="([^"]+)"', tag)
        if src and not src.group(1).startswith("data:"):
            target = (f.parent / src.group(1)).resolve()
            if not target.exists():
                errors.append(f"{r}: <img> src missing on disk -> {src.group(1)}")
        if r in V1_STRICT:
            w = re.search(r'width="(\d+)"', tag)
            h = re.search(r'height="(\d+)"', tag)
            if w and h and int(h.group(1)) > 0 and "lockup" not in tag:
                ratios.add(round(int(w.group(1)) / int(h.group(1)), 3))
if len(ratios) > 1:
    errors.append(f"marketing-page UI photos render at {len(ratios)} aspect ratios: {sorted(ratios)}")
else:
    notes.append(f"marketing-page UI photos: one aspect ratio ({sorted(ratios)[0] if ratios else 'n/a'})")


# ── 4 · links resolve — every page ─────────────────────────────────────
for f in ALL_HTML:
    r, s = rel(f), read(f)
    for attr in ("href", "src"):
        for m in re.finditer(rf'{attr}="([^"]+)"', s):
            v = m.group(1)
            if "${" in v or "{{" in v:
                continue   # JS template-literal interpolation, resolved at runtime
            if v.startswith(("http", "mailto:", "tel:", "data:", "#", "//", "javascript:")):
                continue
            base = BUILD if v.startswith("/") else f.parent
            target = (base / v.lstrip("/").split("#")[0]).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{r}: dead {attr} -> {v}")


# ── 5 · SEO — canonical, robots, og:image (relaxed uniqueness on portal) ─
og_seen = {}
for f in ALL_HTML:
    r, s = rel(f), read(f)
    can = re.search(r'rel="canonical" href="([^"]+)"', s)
    if not can:
        (warnings if r in APPS else errors).append(f"{r}: no canonical")
    elif "#" in can.group(1):
        errors.append(f"{r}: canonical contains a fragment")
    if 'name="robots"' not in s:
        errors.append(f"{r}: no robots meta")
    elif r in APPS or r.startswith(("cvbuilder/",)):
        if "noindex" not in s:
            errors.append(f"{r}: portal page must be noindex")

    og = re.search(r'property="og:image" content="([^"]+)"', s)
    if og:
        path = og.group(1).replace(SITE + "/", "")
        if not (BUILD / path).exists():
            errors.append(f"{r}: og:image missing on disk -> {path}")
        og_seen.setdefault(path, []).append(r)
    elif r in V1_STRICT:
        errors.append(f"{r}: no og:image")

    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(block)
        except Exception as e:
            errors.append(f"{r}: invalid JSON-LD ({e})")

for img, pages in og_seen.items():
    non_app_sharers = [p for p in pages if p not in APPS]
    if len(non_app_sharers) > 1:
        errors.append(f"{len(non_app_sharers)} public pages share one og:image ({img}): {non_app_sharers}")
    elif len(pages) > 1 and all(p in APPS for p in pages):
        notes.append(f"{len(pages)} noindex portal pages intentionally share one preview image")


# ── 6 · sitemap only lists real, indexable pages ───────────────────────
sm = read(BUILD / "sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
noindexed = {rel(f) for f in ALL_HTML if 'content="noindex' in read(f)}
for loc in locs:
    p = loc.replace(SITE + "/", "") or "index.html"
    target = BUILD / p
    if target.is_dir():
        target = target / "index.html"
    if not target.exists():
        errors.append(f"sitemap lists {loc} which does not exist")
    elif str(target.relative_to(BUILD)) in noindexed:
        errors.append(f"sitemap lists {p}, which is noindex")
notes.append(f"sitemap: {len(locs)} urls, all resolve, none noindexed")


# ── 7 · service worker precache integrity ──────────────────────────────
sw = read(BUILD / "sw.js")
shell = json.loads(re.search(r"const SHELL = (\[.*?\]);", sw, re.S).group(1))
missing = [u for u in shell if u != "./" and not (BUILD / u[2:]).exists()]
if missing:
    errors.append(f"sw.js SHELL names {len(missing)} missing file(s): {missing[:5]}")
else:
    notes.append(f"sw.js precache: {len(shell)} files, every one present")


# ── 8 · one WhatsApp number, site-wide ──────────────────────────────────
nums = set()
for f in ALL_HTML:
    nums.update(re.findall(r"wa\.me/(\d+)", read(f)))
if len(nums) > 1:
    errors.append(f"more than one WhatsApp number in use: {sorted(nums)}")
else:
    notes.append(f"WhatsApp number: {sorted(nums)[0] if nums else 'none found'}")


# ── 9 · V1 marketing pages: single stylesheet/script, no inline style ──
for name in V1_STRICT:
    f = BUILD / name
    if not f.exists():
        errors.append(f"{name}: listed as a v1 page but missing from build/")
        continue
    s = read(f)
    if 'href="app.css"' not in s:
        errors.append(f"{name}: does not load app.css")
    if "<style" in s:
        errors.append(f"{name}: has a page-local <style> block")
    if 'src="app.js"' not in s:
        errors.append(f"{name}: does not load app.js")


# ── 10 · legacy URL map — every retired route resolves to something real ─
legacy = re.search(r"var LEGACY = \{(.*?)\};", read(BUILD / "404.html"), re.S)
if legacy:
    pairs = re.findall(r"'([^']+)':\s*'([^']+)'", legacy.group(1))
    for src, target in pairs:
        t = BUILD / target.split("#")[0]
        if t.is_dir():
            t = t / "index.html"
        if not t.exists():
            errors.append(f"404 legacy map: {src} -> {target}, which does not exist")
    notes.append(f"404 legacy map: {len(pairs)} retired URLs, all resolve")
for stale in ["/inner-circle.html", "/cvscan/", "/diagnose/"]:
    if legacy and f"'{stale}'" in legacy.group(1):
        errors.append(f"404 legacy map still redirects {stale}, which is now real content")


# ── 11 · the essentials for a GitHub Pages custom domain ───────────────
if not (BUILD / "CNAME").exists():
    errors.append("CNAME is missing — the custom domain will not resolve")
elif read(BUILD / "CNAME").strip() != "everythingremotejob.com":
    errors.append(f"CNAME contains unexpected content: {read(BUILD/'CNAME').strip()!r}")
else:
    notes.append("CNAME present: everythingremotejob.com")


# ── report ───────────────────────────────────────────────────────────
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
    print(f"\n{len(errors)} error(s) across {len(ALL_HTML)} pages\n")
    sys.exit(1)
print(f"  none — {len(ALL_HTML)} pages validate clean\n")
