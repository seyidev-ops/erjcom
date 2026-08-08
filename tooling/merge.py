#!/usr/bin/env python3
"""ERJ v1.1 — merge the operational site into the v1 rebuild.

v1.0.0 was a from-scratch rebuild of the 13 PUBLIC MARKETING pages. It never
touched — and therefore doesn't contain — the operational side: participant
login, the student dashboard, admin, instructor, the internal surge console,
or the two real interactive tools (CV self-scan, the four-point diagnostic).

This script ports all of that in UNCHANGED where it already works, fixes the
seams where old page names no longer match v1's, and fixes three real,
pre-existing bugs it surfaced along the way (noted inline, below).

Run after pages.py. Idempotent — safe to re-run.
"""
import re, pathlib, shutil, json, subprocess, sys

OLD = pathlib.Path("/home/claude/erjwork/erj.com-2-Early-bird")
NEW = pathlib.Path("/home/claude/erjv1")
BUILD = NEW / "build"
SITE = "https://everythingremotejob.com"
log = []

# Old folder-style product URLs -> the new v1 flat filenames that replace
# them. cvscan/ and diagnose/ are NOT in this map: those are real tools and
# stay at their folder paths — only the pure-marketing pages flattened.
RENAME = {
    "masterytraining/": "mastery-training.html",
    "getaremotejob/":    "get-a-remote-job.html",
    "innercircle/":      "inner-circle.html",
    "masterclass/":      "masterclass.html",
}

PORTAL_PAGES = ["login.html", "participant.html", "dashboard.html", "admin.html",
                "admin-login.html", "instructor.html", "instructor-login.html",
                "blog-admin.html", "erj-surge-console.html", "offline.html",
                "earlybird.html"]
TOOL_DIRS = ["cvscan", "cvbuilder", "diagnose"]
SHARED_JS = ["erj-nav.js", "erj-nav.ts", "erj-passcode.js", "erj-product.js",
             "erj-schema.js", "erj-theme.js", "erj-config.js",
             "erj-capture.js", "erj-capture.ts", "erj-ascend.js"]
SHARED_CSS = ["product.css"]
IMAGES = ["logo.png", "founder-oluwaseyi.jpg", "photo-facilitator-note.webp",
          "photo-facilitator-offer.webp", "photo-facilitator-smile.webp",
          "photo-facilitator-suit.webp", "photo-dollars-hand.webp",
          "photo-dollars-woman.webp", "photo-billboard.webp",
          "photo-woman-laptop.webp", "photo-remote-win-v2.webp",
          "screenshot-mobile-v2.png", "screenshot-wide-v2.png"]
PREVIEWS_V2 = [f"preview-{n}-v2.jpg" for n in
               ["blog", "cvscan", "diagnose", "earlybird", "free",
                "getaremotejob", "index", "innercircle", "login",
                "masterclass", "masterytraining", "register",
                "starting-line", "testimonials"]]


def rd(p): return p.read_text(encoding="utf-8", errors="ignore")
def wr(p, s): p.write_text(s, encoding="utf-8")


# ── 1 · copy everything operational, verbatim ─────────────────────────
for name in PORTAL_PAGES:
    shutil.copy2(OLD / name, BUILD / name)
for d in TOOL_DIRS:
    dst = BUILD / d
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(OLD / d, dst)
for name in SHARED_JS + SHARED_CSS + IMAGES + PREVIEWS_V2:
    src = OLD / name
    if src.exists():
        shutil.copy2(src, BUILD / name)
    else:
        log.append(f"  ! expected but missing in source: {name}")
shutil.copy2(OLD / "manifest.json", BUILD / "manifest.json")
shutil.copy2(OLD / "CNAME", BUILD / "CNAME")
log.append(f"  + copied {len(PORTAL_PAGES)} portal pages, {len(TOOL_DIRS)} tool "
          f"directories, {len(SHARED_JS)+len(SHARED_CSS)} shared modules, "
          f"{len(IMAGES)} images, CNAME, manifest.json")

# ── 2 · v1's placeholder cvscan.html / diagnose.html are superseded ───
# by the REAL interactive tools just copied in at cvscan/ and diagnose/.
# The placeholders only ever hand off to WhatsApp; keeping both would mean
# two different pages answering to two different URLs for the same claim.
for stub in ["cvscan.html", "diagnose.html"]:
    p = BUILD / stub
    if p.exists():
        p.unlink()
        log.append(f"  - removed v1 placeholder {stub} (real tool lives at /{stub[:-5]}/)")

# ── 3 · rewrite old folder-style hrefs to the new v1 flat filenames ───
touched = 0
targets = ([BUILD / n for n in PORTAL_PAGES] +
           list((BUILD / "cvscan").rglob("*.html")) +
           list((BUILD / "cvbuilder").rglob("*.html")) +
           list((BUILD / "diagnose").rglob("*.html")) +
           [BUILD / "erj-nav.ts"])
for f in targets:
    if not f.exists():
        continue
    s = before = rd(f)
    depth_prefix = "../" if f.parent != BUILD else ""
    for old, new in RENAME.items():
        # href="../masterytraining/"  and  href="masterytraining/" — both forms appear
        s = s.replace(f'"{depth_prefix}{old}"', f'"{depth_prefix}{new}"')
        s = s.replace(f"'{old}'", f"'{new}'")   # erj-nav.ts uses single quotes
    if s != before:
        wr(f, s)
        touched += 1
log.append(f"  + old folder-style links rewritten to v1 flat filenames in {touched} file(s)")

# ── 4 · recompile the navigation now that erj-nav.ts has new hrefs ────
r = subprocess.run(["npx", "tsc", str(BUILD / "erj-nav.ts"),
                    "--target", "es2017", "--outDir", str(BUILD)],
                   capture_output=True, text=True)
if r.returncode != 0:
    log.append("  ✗ erj-nav.ts failed to compile:\n" + r.stdout + r.stderr)
else:
    log.append("  + erj-nav.ts recompiled -> erj-nav.js")

# ── 5 · three real bugs found while inspecting the source, fixed here ──

# 5a. dashboard.html calls window.ERJ_ASCEND.render(...) but never loads
#     erj-config.js or erj-ascend.js — the tier-upsell block has been
#     silently dead since it was built (the call is guarded, so it fails
#     silently rather than throwing, which is exactly why this went unnoticed).
dp = BUILD / "dashboard.html"
s = rd(dp)
if 'src="erj-ascend.js"' not in s:
    s = s.replace('<script src="erj-passcode.js"></script>',
                  '<script src="erj-config.js"></script>\n'
                  '<script src="erj-ascend.js"></script>\n'
                  '<script src="erj-passcode.js"></script>', 1)
    wr(dp, s)
    log.append("  ✗→+ BUG FIXED: dashboard.html called window.ERJ_ASCEND.render() "
              "but never loaded erj-config.js/erj-ascend.js — the tier upsell has "
              "been silently inert. Both scripts now load.")

# 5b. Eight portal pages point og:image at preview-*.jpg files that were
#     never generated (dashboard, admin, admin-login, instructor,
#     instructor-login, blog-admin, offline, participant). Harmless for
#     search (all noindex) but breaks a manual WhatsApp/Slack share of the
#     link. Repointed at one generated neutral portal preview.
DEAD_PREVIEWS = ["preview-admin.jpg", "preview-admin-login.jpg",
                 "preview-blog-admin.jpg", "preview-dashboard.jpg",
                 "preview-instructor.jpg", "preview-instructor-login.jpg",
                 "preview-offline.jpg", "preview-participant.jpg"]
fixed_previews = 0
for name in PORTAL_PAGES:
    p = BUILD / name
    if not p.exists():
        continue
    s = before = rd(p)
    for dead in DEAD_PREVIEWS:
        s = s.replace(f"{SITE}/{dead}", f"{SITE}/preview-portal.jpg")
    if s != before:
        fixed_previews += 1
        wr(p, s)
if fixed_previews:
    log.append(f"  ✗→+ BUG FIXED: {fixed_previews} portal page(s) pointed og:image "
              f"at a preview file that was never generated — repointed at one "
              f"generated neutral portal preview (preview-portal.jpg).")

# 5c. v1's generated marketing pages never registered the service worker —
#     sw.js was built and precached nothing because it was never installed.
#     Ported here into the shared chrome so both halves of the merged site
#     get the same offline behaviour the old site had.
es = NEW / "erjsite.py"
s = rd(es)
if "serviceWorker" not in s:
    s = s.replace(
        '<script src="app.js" defer></script>\n</body>\n</html>\n\'\'\'',
        '<script src="app.js" defer></script>\n'
        '<script>if("serviceWorker" in navigator){addEventListener("load",'
        'function(){navigator.serviceWorker.register("/sw.js").then(function(r)'
        '{r.update();}).catch(function(){});});}</script>\n'
        '</body>\n</html>\n\'\'\'')
    wr(es, s)
    log.append("  ✗→+ BUG FIXED: v1's own pages never registered the service "
              "worker — sw.js existed but nothing ever installed it. Registration "
              "added to the shared chrome.")

# ── 6 · footer gains a discreet Participant Login link ────────────────
# matches the old site's own convention: not in the main nav, present in
# the footer so returning students can always find it.
s = rd(es)
old_col = '''("More", [("Success Stories", "testimonials.html"), ("The Blog", "blog.html"),
              ("Free Masterclass", "masterclass.html"),
              ("Free Job Board", CHANNEL)]),'''
new_col = '''("More", [("Success Stories", "testimonials.html"), ("The Blog", "blog.html"),
              ("Free Masterclass", "masterclass.html"),
              ("Free Job Board", CHANNEL)]),
    ("Participants", [("Participant Login", "login.html")]),'''
if old_col in s and "Participant Login" not in s:
    s = s.replace(old_col, new_col, 1)
    wr(es, s)
    log.append("  + footer gained a 'Participants' column (Login, matching the "
              "old site's own convention of keeping it out of the main nav)")

# ── 7 · erj-capture.js's channelBridge() bridged nav-chrome links too ──
# On any page whose own nav group auto-opens (e.g. cvscan/ opens "Free For
# You", which also lists the WhatsApp job-board channel), the capture
# layer matched that in-nav link the same as a content link, and inserted
# a stray, badly-positioned <p class="cap-bridge"> INSIDE the dropdown
# markup itself. Found by the browser test suite (cvscan/ showed content
# rendered ~370px past the viewport edge). Fixed at the TypeScript source
# so it can never regress, then recompiled.
cap_ts = BUILD / "erj-capture.ts"
s = rd(cap_ts)
old_cb = '''  function channelBridge(): void {
    const links = Array.from(
      document.querySelectorAll<HTMLAnchorElement>('a[href*="whatsapp.com/channel"]')
    );
    if (!links.length) return;'''
new_cb = '''  function channelBridge(): void {
    const links = Array.from(
      document.querySelectorAll<HTMLAnchorElement>('a[href*="whatsapp.com/channel"]')
    ).filter(link =>
      // A channel link inside the site's OWN navigation (header, off-canvas
      // panel, or a dropdown) is chrome, not page content — bridging it
      // injected a stray paragraph into the nav markup itself.
      !link.closest('.erj-nav, .erj-panel, .erj-drop, .erj-bar, nav')
    );
    if (!links.length) return;'''
if old_cb in s:
    s = s.replace(old_cb, new_cb, 1)
    wr(cap_ts, s)
    r = subprocess.run(["npx", "tsc", str(cap_ts), "--target", "es2017", "--strict",
                        "--lib", "es2017,dom", "--outDir", str(BUILD)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        log.append("  ✗ erj-capture.ts failed to compile:\n" + r.stdout + r.stderr)
    else:
        log.append("  ✗→+ BUG FIXED: erj-capture.js bridged WhatsApp channel links "
                  "sitting INSIDE the site's own nav, injecting broken markup into "
                  "the dropdown on pages like cvscan/. channelBridge() now skips "
                  "anything inside nav chrome. Recompiled.")
elif "erj-nav, .erj-panel" not in s:
    log.append("  ! erj-capture.ts: channelBridge() anchor text not found — CHECK")

# ── 8 · six tap targets under 30px on the three login pages ───────────
# Found by the browser test suite at phone width. Each is an isolated
# utility link (forgot-password, back-to-site, cross-links between the
# three login pages) — padding added without changing visual spacing.
TAP_FIXES = [
    ("login.html",
     '<a href="#" class="forgot-link" onclick="showForgot(event)">Forgot password?</a>',
     '<a href="#" class="forgot-link" style="display:inline-block;padding:.5rem 0" onclick="showForgot(event)">Forgot password?</a>'),
    ("login.html",
     '<a href="index.html">Back to site</a>',
     '<a href="index.html" style="display:inline-block;padding:.5rem 0">Back to site</a>'),
    ("login.html",
     'style="font-size:.76rem;color:var(--muted);text-decoration:none;display:inline-flex;align-items:center;gap:5px;transition:color .2s;" onmouseover="this.style.color=\'var(--electric)\'" onmouseout="this.style.color=\'var(--muted)\'">\U0001F6E1\uFE0F Admin Portal Login</a>',
     'style="font-size:.76rem;color:var(--muted);text-decoration:none;display:inline-flex;align-items:center;gap:5px;padding:.5rem 0;transition:color .2s;" onmouseover="this.style.color=\'var(--electric)\'" onmouseout="this.style.color=\'var(--muted)\'">\U0001F6E1\uFE0F Admin Portal Login</a>'),
    ("admin-login.html",
     'Not an admin? <a href="login.html">\u2190 Participant Login</a> &nbsp;\u00b7&nbsp; <a href="index.html">Back to site</a>',
     'Not an admin? <a href="login.html" style="display:inline-block;padding:.5rem 0">\u2190 Participant Login</a> &nbsp;\u00b7&nbsp; <a href="index.html" style="display:inline-block;padding:.5rem 0">Back to site</a>'),
    ("instructor-login.html",
     '.forgot-link{font-size:.8rem;color:var(--electric);text-decoration:none;transition:opacity .2s;}',
     '.forgot-link{font-size:.8rem;color:var(--electric);text-decoration:none;transition:opacity .2s;display:inline-block;padding:.5rem 0;}'),
    ("instructor-login.html",
     'Not an instructor? <a href="login.html">\u2190 Participant Login</a> \u00b7 <a href="admin-login.html">Admin Portal</a>',
     'Not an instructor? <a href="login.html" style="display:inline-block;padding:.5rem 0">\u2190 Participant Login</a> \u00b7 <a href="admin-login.html" style="display:inline-block;padding:.5rem 0">Admin Portal</a>'),
]
tap_done = 0
for name, old, new in TAP_FIXES:
    p = BUILD / name
    s = rd(p)
    if old in s:
        wr(p, s.replace(old, new, 1))
        tap_done += 1
if tap_done:
    log.append(f"  ✗→+ BUG FIXED: {tap_done} tap targets under 30px on the login "
              f"pages (forgot-password, back-to-site, cross-links) — padding added, "
              f"visual spacing unchanged.")

# ── 9 · shared nav tap targets, and two more found by the browser suite ─
# erj-nav.js's brand mark and top-bar links render at ~26px tall (font
# metrics only, no padding) across all 14 ported/tool pages that use it.
nav_ts = BUILD / "erj-nav.ts"
s = rd(nav_ts)
before = s
s = s.replace(
    "'.erj-brand{display:inline-flex;align-items:center;gap:9px;font-family:var(--font-display,Georgia,serif);',",
    "'.erj-brand{display:inline-flex;align-items:center;gap:9px;min-height:2.75rem;font-family:var(--font-display,Georgia,serif);',")
s = s.replace(
    "'.erj-bar-link{display:inline-flex;align-items:center;gap:0.3rem;color:var(--enInk);text-decoration:none;',",
    "'.erj-bar-link{display:inline-flex;align-items:center;gap:0.3rem;min-height:1.9rem;color:var(--enInk);text-decoration:none;',")
if s != before:
    wr(nav_ts, s)
    r = subprocess.run(["npx", "tsc", str(nav_ts), "--target", "es2017",
                        "--outDir", str(BUILD)], capture_output=True, text=True)
    if r.returncode != 0:
        log.append("  ✗ erj-nav.ts failed to recompile:\n" + r.stdout + r.stderr)
    else:
        log.append("  ✗→+ BUG FIXED: erj-nav.js brand mark and top-bar links rendered "
                  "~26px tall (font metrics only) across all 14 pages that use shared "
                  "nav — min-height added, recompiled.")

# cvscan's "After the score" cards used minmax(310px,1fr), which does not
# fit inside a 320px viewport once page padding is subtracted (found by
# the browser suite: 11px past the edge at 320px).
scan_css = BUILD / "cvscan" / "scan.css"
s = rd(scan_css)
if "minmax(310px,1fr)" in s:
    wr(scan_css, s.replace(
        "#next .cards{grid-template-columns:repeat(auto-fit,minmax(310px,1fr));align-items:start;}",
        "#next .cards{grid-template-columns:repeat(auto-fit,minmax(260px,1fr));align-items:start;}"))
    log.append("  ✗→+ BUG FIXED: cvscan's result cards used a 310px minimum width, "
              "which overflowed a 320px viewport once padding was subtracted — "
              "reduced to 260px.")

# login.html's inline tab-switch link ("Register now") had no padding.
login = BUILD / "login.html"
s = rd(login)
old_reg = '''Don't have an account? <a href="#" onclick="switchTab('register');return false">Register now</a> ·'''
new_reg = '''Don't have an account? <a href="#" style="display:inline-block;padding:.5rem 0" onclick="switchTab('register');return false">Register now</a> ·'''
if old_reg in s:
    wr(login, s.replace(old_reg, new_reg, 1))
    log.append("  ✗→+ BUG FIXED: login.html's 'Register now' tab-switch link was "
              "15px tall — padding added.")

# product.css's shared page footer (.foot-links, used by cvscan/, cvbuilder/,
# diagnose/ and earlybird.html) had no padding on its links either.
prod_css = BUILD / "product.css"
s = rd(prod_css)
old_fl = ".foot .foot-links a{white-space:nowrap;}"
new_fl = ".foot .foot-links a{white-space:nowrap;display:inline-block;padding:.4rem 0;}"
if old_fl in s:
    wr(prod_css, s.replace(old_fl, new_fl, 1))
    log.append("  ✗→+ BUG FIXED: product.css's shared footer links (.foot-links, "
              "used by cvscan/, cvbuilder/, diagnose/, earlybird.html) were 26px "
              "tall — padding added.")

print("\n".join(log))
