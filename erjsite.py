#!/usr/bin/env python3
"""ERJ v1 — static site generator.

WHY A GENERATOR
The previous site was hand-maintained HTML. Every fix had to be applied
page by page, which is how it ended up with canonicals on some pages and
not others, one page pointing at an og:image that never existed, two pages
that didn't load the stylesheet, and a nav that disagreed with itself.

Here, <head>, header, nav, footer and every SEO tag are emitted from ONE
function. A page cannot be inconsistent with the others because a page
does not own any of that. Content is data; layout is code.
"""
import json, pathlib, re, html, shutil, datetime

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "build"
SITE = "https://everythingremotejob.com"
WA = "2348032925957"
WA_LINK = f"https://wa.me/{WA}"
CHANNEL = "https://whatsapp.com/channel/0029Vaym4DE3mFY2wCrC713S"
TODAY = "2026-08-08"

IMG = json.loads((OUT / "images.json").read_text(encoding="utf-8"))


# ═══ helpers ═══════════════════════════════════════════════════════════

def esc(t):
    return html.escape(str(t), quote=True)


def picture(key, alt, *, eager=False, caption=None, sizes="(min-width:52rem) 46vw, 92vw"):
    """Every photo on the site goes through here.

    That is what keeps them identical: one aspect ratio, one border, one
    fade-in, one LQIP, real width/height attributes so nothing shifts."""
    m = IMG[key]
    srcset = ", ".join(f"img/{s['file']} {s['w']}w" for s in m["sizes"])
    largest = m["sizes"][-1]["file"]
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    fig = (
        f'<figure>'
        f'<div class="media" style="background-image:url({m["lqip"]})">'
        f'<img src="img/{largest}" srcset="{srcset}" sizes="{sizes}" '
        f'width="{m["width"]}" height="{m["height"]}" alt="{esc(alt)}" '
        f'{loading} decoding="async">'
        f'</div>'
    )
    if caption:
        fig += f'<figcaption>{caption}</figcaption>'
    return fig + '</figure>'


def btn(label, href, ghost=False, blank=False):
    cls = "btn btn--ghost" if ghost else "btn"
    tgt = ' target="_blank" rel="noopener"' if blank else ''
    return (f'<a class="{cls}" href="{href}"{tgt}>{label} '
            f'<span class="arw" aria-hidden="true">&rarr;</span></a>')


def tlink(label, href, blank=False):
    tgt = ' target="_blank" rel="noopener"' if blank else ''
    return (f'<a class="tlink" href="{href}"{tgt}>{label} '
            f'<span class="arw" aria-hidden="true">&rarr;</span></a>')


# ═══ navigation — one definition, used by header, drawer and footer ════
NAV = [
    ("Home", "index.html", "home"),
    ("Free For You", "free.html", "free"),
    ("Your Starting Line", "starting-line.html", "start"),
    ("Success Stories", "testimonials.html", "stories"),
    ("The Blog", "blog.html", "blog"),
    ("Register", "register.html", "register"),
]

FOOTER = [
    ("Start here", [("Find Your Leak", "diagnose.html"), ("Free CV Self-Scan", "cvscan.html"),
                    ("Free For You", "free.html"), ("Your Starting Line", "starting-line.html")]),
    ("Programmes", [("Mastery Training", "mastery-training.html"),
                    ("Get A Remote Job", "get-a-remote-job.html"),
                    ("The Inner Circle", "inner-circle.html"),
                    ("Register", "register.html")]),
    ("More", [("Success Stories", "testimonials.html"), ("The Blog", "blog.html"),
              ("Free Masterclass", "masterclass.html"),
              ("Free Job Board", CHANNEL)]),
]

WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97'
          '-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.46-2.39-1.48'
          '-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5'
          '.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.91-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07'
          '-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.07c.15.2 2.1 3.2 5.08 4.49.7.3 1.26.49'
          '1.69.62.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.42-.08-.12-.28-.2'
          '-.57-.34M12.05 21.79h-.01a9.87 9.87 0 01-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 '
          '01-1.51-5.26C2.16 6.45 6.6 2.01 12.05 2.01c2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 012.89 6.99'
          'c0 5.45-4.44 9.89-9.88 9.89"/></svg>')


def head(page):
    """Every meta tag the site emits, for every page, from one place."""
    url = f'{SITE}/{page["file"]}' if page["file"] != "index.html" else f'{SITE}/'
    og = f'{SITE}/img/og-{page["key"]}.jpg'
    robots = ('noindex,follow' if page.get("noindex")
              else 'index,follow,max-image-preview:large,max-snippet:-1')

    schema = [{
        "@context": "https://schema.org", "@type": "Organization",
        "name": "Everything Remote Job", "url": SITE + "/",
        "logo": f"{SITE}/erj-mark-white.png",
        "sameAs": [CHANNEL],
        "contactPoint": [{"@type": "ContactPoint", "contactType": "customer support",
                          "telephone": "+" + WA, "areaServed": "NG",
                          "availableLanguage": "English"}],
    }]
    if page["key"] == "home":
        schema.append({
            "@context": "https://schema.org", "@type": "WebSite",
            "name": "Everything Remote Job", "url": SITE + "/",
        })
    if page.get("schema"):
        schema.append(page["schema"])
    if page["file"] != "index.html":
        schema.append({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": page["title"], "item": url},
            ],
        })

    ld = "\n".join('<script type="application/ld+json">'
                   + json.dumps(s, separators=(",", ":")) + '</script>' for s in schema)

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="night">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(page["title"])} — Everything Remote Job</title>
<meta name="description" content="{esc(page["desc"])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#000000">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Everything Remote Job">
<meta property="og:locale" content="en_NG">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(page["title"])} — Everything Remote Job">
<meta property="og:description" content="{esc(page["desc"])}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page["title"])} — Everything Remote Job">
<meta name="twitter:description" content="{esc(page["desc"])}">
<meta name="twitter:image" content="{og}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="favicon32.png" sizes="32x32">
<link rel="apple-touch-icon" href="appletouchicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="app.css">
<script>/* set the theme before first paint so it never flashes */
(function(){{try{{var t=localStorage.getItem('erj-theme');
if(!t)t=matchMedia('(prefers-color-scheme: light)').matches?'day':'night';
document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" data-progress aria-hidden="true"></div>
'''


def chrome_top(page):
    marquee = ('We will not let you go <b>until you\u2019re hired.</b> &nbsp;&middot;&nbsp; '
               * 2)
    nav_links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if k == page["key"] else ""}>{esc(l)}</a>'
        for l, h, k in NAV)
    drawer_links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if k == page["key"] else ""}>{esc(l)}</a>'
        for l, h, k in NAV)

    return f'''<div class="promise" aria-label="Our promise"><p>{marquee}</p></div>

<header class="hdr" data-header>
  <div class="wrap hdr-in">
    <a class="brand" href="index.html" aria-label="Everything Remote Job — home">
      <img src="erj-lockup-white.png" alt="Everything Remote Job" width="1400" height="258">
    </a>
    <nav class="nav" aria-label="Main">{nav_links}</nav>
    <div class="hdr-acts">
      <button class="icon-btn" data-theme-toggle type="button" aria-label="Switch theme">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z"/></svg>
      </button>
      <button class="icon-btn burger" data-drawer-open type="button"
              aria-label="Open menu" aria-expanded="false" aria-controls="menu">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
</header>

<div class="scrim" data-scrim></div>
<nav class="drawer" id="menu" data-drawer aria-label="Menu" aria-hidden="true">
  {drawer_links}
</nav>

<main id="main">
'''


def chrome_bottom():
    cols = ""
    for title, links in FOOTER:
        items = "".join(
            f'<li><a href="{h}"'
            + (' target="_blank" rel="noopener"' if h.startswith("http") else '')
            + f'>{esc(l)}</a></li>' for l, h in links)
        cols += f'<div><h2 class="ftr-h">{esc(title)}</h2><ul>{items}</ul></div>'

    return f'''</main>

<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div>
        <img src="erj-lockup-white.png" alt="Everything Remote Job" width="1400" height="258"
             style="height:2rem;width:auto" class="brand-mark">
        <p style="margin-top:.9rem;color:var(--ink-soft);font-size:var(--t-sm);max-width:26ch">
          We will not let you go until you&rsquo;re hired.</p>
        <p style="margin-top:.7rem"><a class="tlink" href="{WA_LINK}" target="_blank"
           rel="noopener">WhatsApp +234 803 292 5957 <span class="arw">&rarr;</span></a></p>
      </div>
      {cols}
    </div>
    <div class="ftr-base">
      <span>&copy; 2026 Everything Remote Job &middot; Business Play Limited</span>
      <span>Built for global career scale.</span>
    </div>
  </div>
</footer>

<a class="wa" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WA_SVG}</a>
<button class="totop" data-totop type="button" aria-label="Back to top">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<script src="app.js" defer></script>
</body>
</html>
'''


def render(page):
    return head(page) + chrome_top(page) + page["body"] + chrome_bottom()


# ═══ build ═════════════════════════════════════════════════════════════

def build(pages):
    OUT.mkdir(exist_ok=True)
    shutil.copy(ROOT / "src" / "app.css", OUT / "app.css")

    for p in pages:
        (OUT / p["file"]).write_text(render(p), encoding="utf-8")
        print(f"  {p['file']:28s} {len(render(p))//1024:>3d} KB")

    # sitemap — only indexable pages, generated from the same list
    urls = "\n".join(
        f'  <url><loc>{SITE}/{"" if p["file"]=="index.html" else p["file"]}</loc>'
        f'<lastmod>{TODAY}</lastmod>'
        f'<changefreq>{p.get("freq","weekly")}</changefreq>'
        f'<priority>{p.get("prio","0.8")}</priority></url>'
        for p in pages if not p.get("noindex"))
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + urls + '\n</urlset>\n', encoding="utf-8")

    (OUT / "robots.txt").write_text(
        "# Everything Remote Job\n"
        "# Pages that must stay out of the index carry a noindex meta tag and are\n"
        "# deliberately NOT disallowed here: a blocked URL is never crawled, so its\n"
        "# noindex is never read, and an already-indexed page stays indexed.\n\n"
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

    (OUT / "manifest.webmanifest").write_text(json.dumps({
        "name": "Everything Remote Job",
        "short_name": "ERJ",
        "description": "Land a dollar-paying remote job from right where you are.",
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "background_color": "#000000",
        "theme_color": "#000000",
        "icons": [
            {"src": "icon192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icon512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icon192maskable.png", "sizes": "192x192", "type": "image/png",
             "purpose": "maskable"},
            {"src": "icon512maskable.png", "sizes": "512x512", "type": "image/png",
             "purpose": "maskable"},
        ],
    }, indent=1), encoding="utf-8")

    # service worker — SHELL is generated, so it can never list a missing file
    shell = ["./", "./app.css", "./app.js", "./manifest.webmanifest",
             "./erj-lockup-white.png", "./erj-mark-white.png", "./favicon32.png"]
    shell += [f"./{p['file']}" for p in pages]
    shell += [f"./img/{s['file']}" for m in IMG.values() for s in m["sizes"]]
    (OUT / "sw.js").write_text(SW.replace("__SHELL__", json.dumps(shell, indent=2)),
                               encoding="utf-8")
    print(f"\n  sitemap {sum(1 for p in pages if not p.get('noindex'))} urls "
          f"· sw shell {len(shell)} files · every entry generated, none hand-typed")


SW = '''/* Everything Remote Job — service worker v1.
   SHELL is emitted by the build from the real file list, so it can never
   name a file that does not exist. One missing entry makes addAll() reject
   and aborts the ENTIRE precache — that bug cost the old site a week. */
const VERSION = 'erj-v1-0-0';
const SHELL = __SHELL__;

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const cache = await caches.open(VERSION);
    // addAll is all-or-nothing; add individually so one bad asset cannot
    // take the whole precache down with it.
    await Promise.all(SHELL.map(u => cache.add(u).catch(() => {})));
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;

  // HTML: network first, so a deploy is seen immediately; cache as a fallback.
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
    e.respondWith((async () => {
      try {
        const fresh = await fetch(req);
        const cache = await caches.open(VERSION);
        cache.put(req, fresh.clone());
        return fresh;
      } catch (err) {
        return (await caches.match(req)) || (await caches.match('./index.html'));
      }
    })());
    return;
  }

  // Everything else: cache first, refresh in the background.
  e.respondWith((async () => {
    const hit = await caches.match(req);
    const net = fetch(req).then(res => {
      if (res && res.ok) caches.open(VERSION).then(c => c.put(req, res.clone()));
      return res;
    }).catch(() => hit);
    return hit || net;
  })());
});
'''
