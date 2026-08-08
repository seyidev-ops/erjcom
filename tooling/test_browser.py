#!/usr/bin/env python3
"""ERJ v1 — real-browser test suite.

Static analysis cannot see a layout. This drives actual Chromium across
the breakpoints that matter and asserts the things that were repeatedly
broken on the old site:

  · no horizontal overflow at any width (the recurring bug)
  · nothing touching the screen edge — a real minimum gutter is measured
  · the closed drawer does not widen the document
  · every photo lands at the same aspect ratio on screen
  · zero cumulative layout shift from images
  · no JavaScript console errors
  · the drawer, theme toggle and reveals actually work
  · tap targets are big enough on a phone
"""
from playwright.sync_api import sync_playwright
import pathlib, sys, json

BUILD = pathlib.Path(__file__).parent / "build"
PAGES = sorted(p.name for p in BUILD.glob("*.html"))
# the merged build also carries the real tools + the operational portal;
# include the two public tools in every full-site sweep, keep the portal
# apps out of checks that assume the v1 marketing design system
TOOL_PAGES = ["cvscan/index.html", "diagnose/index.html"]
PAGES = sorted(set(PAGES) - {"cvscan.html", "diagnose.html"}) + TOOL_PAGES
WIDTHS = [320, 360, 390, 414, 600, 768, 900, 1024, 1280, 1440, 1920]
MIN_GUTTER = 16          # px: nothing may sit closer than this to either edge

passed, failed = 0, 0


def ok(name, cond, extra=""):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"  ✗ {name}" + (f" — {extra}" if extra else ""))


def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        # ── A · overflow + edge safety across every width ──────────────
        print("\nRESPONSIVE — overflow and edge safety")
        for w in WIDTHS:
            page = browser.new_page(viewport={"width": w, "height": 900})
            worst_overflow, worst_gutter, worst_page = 0, 999, ""
            for name in PAGES:
                page.goto((BUILD / name).as_uri())
                page.wait_for_timeout(160)
                m = page.evaluate("""() => {
                  const doc = document.documentElement;
                  const over = doc.scrollWidth - doc.clientWidth;
                  let minL = 9999, minR = 9999;
                  const vw = doc.clientWidth;
                  document.querySelectorAll(
                    'h1,h2,h3,p,li,a.btn,.card,.rung,.stat-n,figure,.wa,.totop,.brand'
                  ).forEach(el => {
                    // a marquee is intentionally wider than its clipping parent
                    if (el.closest('.promise')) return;
                    const r = el.getBoundingClientRect();
                    if (r.width < 2 || r.height < 2) return;
                    minL = Math.min(minL, r.left);
                    minR = Math.min(minR, vw - r.right);
                  });
                  return {over, minL, minR};
                }""")
                if m["over"] > worst_overflow:
                    worst_overflow, worst_page = m["over"], name
                g = min(m["minL"], m["minR"])
                if g < worst_gutter:
                    worst_gutter, worst_page_g = g, name
            ok(f"{w}px · no horizontal overflow", worst_overflow <= 1,
               f"{worst_overflow}px on {worst_page}")
            ok(f"{w}px · nothing within {MIN_GUTTER}px of an edge",
               worst_gutter >= MIN_GUTTER,
               f"{worst_gutter:.0f}px on {worst_page_g}")
            page.close()

        # ── B · drawer must not widen the closed document ──────────────
        print("\nDRAWER")
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto((BUILD / "index.html").as_uri())
        page.wait_for_timeout(200)
        closed = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        ok("closed drawer does not widen the page", closed <= 1, f"{closed}px")
        page.click("[data-drawer-open]")
        page.wait_for_timeout(450)
        ok("drawer opens", page.evaluate(
            "() => document.querySelector('[data-drawer]').hasAttribute('data-open')"))
        ok("body scroll locks while open",
           page.evaluate("() => getComputedStyle(document.body).overflow") == "hidden")
        page.keyboard.press("Escape")
        page.wait_for_timeout(450)
        ok("Escape closes the drawer", not page.evaluate(
            "() => document.querySelector('[data-drawer]').hasAttribute('data-open')"))
        ok("body scroll restored",
           page.evaluate("() => getComputedStyle(document.body).overflow") != "hidden")
        page.close()

        # ── C · images: one geometry on screen, no layout shift ────────
        print("\nIMAGES")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        shifts = []
        for name in PAGES:
            page.goto((BUILD / name).as_uri())
            page.evaluate("""() => { window.__cls = 0;
              new PerformanceObserver(l => l.getEntries().forEach(e => {
                if (!e.hadRecentInput) window.__cls += e.value;
              })).observe({type:'layout-shift', buffered:true}); }""")
            page.wait_for_timeout(700)
            ratios = page.evaluate("""() => Array.from(document.querySelectorAll('.media'))
              .map(m => { const r = m.getBoundingClientRect();
                          return Math.round((r.width / r.height) * 100) / 100; })""")
            if ratios:
                ok(f"{name}: all photos one ratio", len(set(ratios)) == 1, str(set(ratios)))
                ok(f"{name}: photos are 3:2", all(abs(r - 1.5) < 0.02 for r in ratios), str(set(ratios)))
            shifts.append((name, page.evaluate("() => window.__cls || 0")))
        worst = max(shifts, key=lambda x: x[1])
        ok("cumulative layout shift under 0.02 everywhere", worst[1] < 0.02,
           f"{worst[0]} = {worst[1]:.4f}")
        page.close()

        # ── D · no console errors anywhere ─────────────────────────────
        print("\nRUNTIME")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        problems = []
        def note_console(m):
            if m.type == "error" and "403" not in m.text and "font" not in m.text.lower():
                problems.append(m.text)
        page.on("console", note_console)
        page.on("pageerror", lambda e: problems.append(str(e)))
        for name in PAGES:
            page.goto((BUILD / name).as_uri())
            page.wait_for_timeout(320)
            page.evaluate("() => scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(220)
        ok("no JavaScript errors on any page", not problems, "; ".join(problems[:3]))
        page.close()

        # ── E · interactions ───────────────────────────────────────────
        print("\nINTERACTION")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((BUILD / "index.html").as_uri())
        page.wait_for_timeout(400)
        ok("hero reveals on load", page.evaluate(
            "() => !!document.querySelector('[data-reveal][data-shown]')"))
        before = page.evaluate("() => document.documentElement.dataset.theme")
        page.click("[data-theme-toggle]")
        page.wait_for_timeout(200)
        ok("theme toggles", page.evaluate(
            "() => document.documentElement.dataset.theme") != before)
        page.evaluate("() => document.querySelector('.stats').scrollIntoView({block:'center'})")
        page.wait_for_timeout(1500)
        ok("header marks itself stuck", page.evaluate(
            "() => document.querySelector('[data-header]').hasAttribute('data-stuck')"))
        page.evaluate("() => scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(400)
        ok("back-to-top appears once past a screenful", page.evaluate(
            "() => document.querySelector('[data-totop]').hasAttribute('data-show')"))
        ok("progress bar advances", page.evaluate(
            "() => parseFloat(document.querySelector('[data-progress]').style.width) > 0"))
        ok("counters reached their target", page.evaluate(
            '''() => { const el = document.querySelector('[data-count="382"]');
                       return !!el && el.textContent.replace(/[^0-9]/g, '') === '382'; }'''))
        page.close()

        # ── F · tap targets and contrast on a phone ────────────────────
        print("\nACCESSIBILITY")
        page = browser.new_page(viewport={"width": 390, "height": 844})
        small = []
        for name in PAGES:
            page.goto((BUILD / name).as_uri())
            page.wait_for_timeout(200)
            small += page.evaluate("""() => {
              const out = [];
              document.querySelectorAll('a,button').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.width < 2 || r.height < 2) return;
                if (el.classList.contains('skip')) return;
                if (r.height < 30) out.push((el.textContent||el.getAttribute('aria-label')||'?').trim().slice(0,26));
              });
              return out; }""")
        ok("every tap target is at least 30px tall", not small, "; ".join(sorted(set(small))[:4]))

        page.goto((BUILD / "index.html").as_uri())
        ok("page has a skip link", page.evaluate(
            "() => !!document.querySelector('a.skip')"))
        ok("drawer is hidden from AT when closed", page.evaluate(
            "() => document.querySelector('[data-drawer]').getAttribute('aria-hidden')") == "true")
        page.close()

        browser.close()


if __name__ == "__main__":
    run()
    print(f"\n{passed} passed, {failed} failed\n")
    sys.exit(1 if failed else 0)
