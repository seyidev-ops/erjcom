# Everything Remote Job — v1.0.0

A complete rebuild. Nothing is carried over from the previous codebase except the
photographs, the logo and the copy that was true.

## Build it

```bash
python3 images.py     # normalise every photo to ONE geometry + responsive variants
npx tsc src/app.ts --outDir build --target es2018 --strict --lib es2018,dom
python3 og.py         # one social preview per page
python3 pages.py      # generate every HTML page, sitemap, robots, manifest, sw
python3 validate.py   # 8 static checks — must exit 0
python3 test_browser.py   # 54 assertions in real Chromium — must exit 0
```

`build/` is the deployable site. Nothing outside it ships.

## Why it is built this way

**Pages are generated, not hand-written.** `<head>`, header, nav, footer and every
SEO tag come from one function in `erjsite.py`. A page cannot disagree with the
others because a page does not own any of that. The old site drifted precisely
because each page carried its own copy — that is how it ended up with canonicals
on some pages and not others, an `og:image` pointing at a file that never existed,
and two pages that did not load the stylesheet at all.

**One stylesheet, one script.** No page-local `<style>`, no inline handlers. The
validator fails the build if either appears.

**One image geometry.** Every UI photo is cropped to 3:2 *in the file* by
`images.py`. The markup never needs to know which picture it is holding, so there
is no per-image CSS and no layout shift. Sources ranged from 0.67 to 1.50 — that
mismatch is what made the old cards refuse to line up.

**One gutter token.** `--gutter: clamp(1.25rem, 5vw, 3.25rem)`, with
`env(safe-area-inset-*)` for notches. Containers, the header, the marquee and both
floating controls all obey it, so nothing can crowd the screen edge. A browser test
measures the real distance from every heading, paragraph, card and button to both
edges at 11 widths and fails under 16px.

## Permanent fixes for the bugs that kept coming back

| Old bug | Fix, and why it is permanent |
| --- | --- |
| Horizontal overflow | `overflow-x: clip` (not `hidden`, which kills `position: sticky`). Asserted at 11 widths × 13 pages. |
| Closed drawer widened the page | `visibility: hidden` while closed. A test opens, escapes and re-measures. |
| One missing `sw.js` SHELL path aborted the entire precache | SHELL is **generated from the real file list**, and the worker adds entries individually so one bad asset cannot take the rest down. |
| Replaced an image, users saw the old one | Content-addressed filenames from the pipeline; the service worker versions its cache. |
| Canonical with a `#fragment` (Google discards it) | Emitted centrally, validated. |
| Two pages sharing one `og:image` | One preview per page, uniqueness asserted. |
| Images causing layout shift | Fixed `aspect-ratio` + real `width`/`height`; CLS measured under 0.02. |
| Time-bound social previews | Kickers are evergreen. No cohort number, no date — OG images cache for months. |

## Interaction

`src/app.ts` is the only script. Theme (set before first paint, so no flash),
off-canvas drawer with focus trap and scroll lock, `IntersectionObserver` reveals,
staggered groups, image fade-in over an inlined LQIP, one rAF-throttled scroll pass
driving the sticky header + reading progress + back-to-top, section spy, count-up
statistics, and copy-to-clipboard. Every unit is isolated in a `try` so one failure
cannot stop the rest, and everything collapses gracefully under
`prefers-reduced-motion`.

## Known limits

- **Fonts load from Google Fonts.** The sandbox blocks that host, so the test suite
  ignores font 403s. Self-host if you want zero third-party requests.
- **The diagnostic and CV scan currently hand off to WhatsApp** rather than running
  in-page. The interactive versions can be ported in; the routes and copy are ready.
- **Testimonial figures** are carried over from the previous site and should be
  confirmed against your records before this goes live.
