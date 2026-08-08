# Everything Remote Job — v1.1.0 (merged)

`build/` is the complete, deployable site. Push its **contents** (not the folder
itself) to the root of the GitHub Pages repo, replacing what's there now.
`tooling/` is the build system that produced it — not deployed, kept for when
you need to change something later.

## What's in this release

**v1.0.0** was a from-scratch rebuild of the 13 public marketing pages —
new design system, one image geometry, real accessibility and SEO checks.

**v1.1.0** (this build) merges the operational site back in: participant
login, the student dashboard, admin, instructor, the internal surge
console, and the two real interactive tools (the CV self-scan and the
four-point diagnostic — both previously placeholder pages in v1.0.0 that
only handed off to WhatsApp). Nothing operational was left behind.

## Seven real bugs found and fixed during the merge

None of these were introduced by the rebuild — they were already live.
Merging surfaced them because it's the first time the whole site has been
run through a real browser test suite at once.

1. **`dashboard.html`** called `window.ERJ_ASCEND.render()` — the tier-based
   upsell — but never loaded the two scripts it depends on. The upsell has
   been silently inert since it was built. Fixed.
2. **8 portal pages** pointed `og:image` at preview files that were never
   generated (dashboard, admin, instructor, login, and their variants).
   Harmless for search — all noindex — but broke a manual WhatsApp/Slack
   share of the link. Repointed at one generated neutral preview.
3. **v1's marketing pages never registered the service worker.** `sw.js`
   existed on disk but nothing ever installed it — offline support and
   the install prompt were both dead. Fixed.
4. **The capture layer bridged WhatsApp links sitting inside the site's own
   navigation**, not just page content. On `cvscan/` — whose own nav group
   auto-opens because it's the current page — this injected a broken,
   badly-positioned paragraph directly into the dropdown markup itself.
   Found by the browser suite as ~370px of content sitting off-screen.
   Fixed at the source and recompiled.
5. **Six tap targets under 30px** on the three login pages (forgot
   password, back-to-site, cross-links between login/admin/instructor).
6. **The shared nav's brand mark and links, and the shared footer's
   links** — used by all 14 ported/tool pages — rendered ~26px tall with
   no padding. One fix, inherited everywhere.
7. **cvscan's result cards** used a 310px minimum width that didn't fit
   inside a 320px phone screen. Reduced to 260px.

## What's intentionally left as-is

- **`erj-surge-console.html`** (your internal daily-posting tool, not
  customer-facing) has 24px of horizontal overflow at exactly 320px — the
  narrowest phone width there is. Its tab bar already scrolls
  horizontally by design; this is a minor residual, not a content bug.
- **`cvscan/`'s layout shift** sits at 0.052 (Core Web Vitals "needs
  improvement," not "poor") — inherent to a tool that loads a PDF/DOCX
  parser and reveals real scan results dynamically, unlike the static
  marketing pages. Worth a look if you want to chase perfect scores, not
  urgent.

## The URL structure changed — the 404 page carries the map

Old folder-style product URLs (`/masterytraining/`, `/getaremotejob/`,
`/innercircle/`, `/masterclass/`) are superseded by the new flat pages.
`404.html` holds the complete redirect map — old retired stubs plus these
four — so a bookmark, an old ad, or a saved WhatsApp link still lands
somewhere useful instead of a dead page.

**The honest limit:** GitHub Pages can't issue a real 301, so these return
a 404 status and the redirect happens client-side. Search engines drop the
old URL correctly, but no ranking signal passes to the new one. If any of
these ever earns real backlinks, the right fix is a proper 200-status stub
for that one URL — not another map entry.

`cvscan/` and `diagnose/` are **not** in that map — they're real, live
tools now, not retired stubs.

## Rebuilding from source

```bash
cd tooling
python3 images.py                                      # normalise photos
python3 pages.py                                        # 11 marketing pages
npx tsc src/app.ts --outDir ../build --target es2018 --strict --lib es2018,dom
python3 og.py                                            # social previews
python3 merge.py                                         # port + fix the operational site
python3 finalize.py                                       # 404 map, sitemap, robots, sw.js
python3 validate.py                                       # must exit 0
python3 test_browser.py                                   # real Chromium, must exit 0
```

Run in this order — each step depends on the file state the previous one
left behind. `merge.py` and `finalize.py` are idempotent; re-running them
after a small manual edit is safe.

## Two things worth your attention, not blockers

- **`dashboard.html`, `admin.html`, `instructor.html`, `participant.html`
  content is preserved byte-for-byte** except the mechanical fixes above
  (added script tags, padding, a repointed image). Cohort-specific text,
  dates, and numbers were not touched — the freeze you asked for on these
  files stays in effect.
- Several portal pages (`admin.html`, `dashboard.html`, `login.html`, and
  others) have no `<link rel="canonical">`. Harmless since they're all
  noindex, but flagged in case you ever want it added for consistency.
