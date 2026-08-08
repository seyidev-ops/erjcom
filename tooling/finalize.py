#!/usr/bin/env python3
"""ERJ v1.1 — final assembly pass.

Runs after pages.py + merge.py. Rebuilds the four files that must describe
the MERGED tree, not just the 11 marketing pages pages.py knows about:
404's legacy-URL map, sitemap.xml, robots.txt, and sw.js's precache list.
"""
import pathlib, re, json

BUILD = pathlib.Path(__file__).parent / "build"
SITE = "https://everythingremotejob.com"


def rd(p): return p.read_text(encoding="utf-8")
def wr(p, s): p.write_text(s, encoding="utf-8")


# ── 1 · 404.html — one legacy map, fully reconciled ────────────────────
p404 = BUILD / "404.html"
if p404.exists():
    s = rd(p404)
    old_script_start = s.index("<script>")
    old_script_end = s.index("</script>", old_script_start) + len("</script>")

    new_script = '''<script>
(function () {
  var LEGACY = {
    '/howtogetaremotejob/':            'get-a-remote-job.html',
    '/job-world-mastery.html':         'mastery-training.html',
    '/jobs.html':                      'testimonials.html#jobboard',
    '/products/remote-job/':           'get-a-remote-job.html',
    '/products/mastery-training/':     'mastery-training.html',
    '/products/inner-circle/':         'inner-circle.html',
    '/masterytraining/':               'mastery-training.html',
    '/getaremotejob/':                 'get-a-remote-job.html',
    '/innercircle/':                   'inner-circle.html',
    '/masterclass/':                   'masterclass.html'
  };

  var path = location.pathname.replace(/\\/index\\.html$/, '/');
  var target = LEGACY[path];

  if (!target) {
    var alt = path.slice(-1) === '/' ? path.slice(0, -1) : path + '/';
    target = LEGACY[alt];
  }

  if (target) {
    var hash = target.indexOf('#') > -1 ? '' : location.hash;
    location.replace('/' + target + hash);
  } else {
    document.documentElement.setAttribute('data-lost', 'true');
  }
})();
</script>'''

    s = s[:old_script_start] + new_script + s[old_script_end:]
    wr(p404, s)
    print("  + 404.html: legacy map reconciled (10 entries, cvscan/ and diagnose/ excluded)")


# ── 2 · sitemap.xml — marketing pages + the two real public tools ──────
MARKETING = ["", "free.html", "starting-line.html", "mastery-training.html",
             "get-a-remote-job.html", "inner-circle.html", "masterclass.html",
             "testimonials.html", "blog.html", "register.html"]
TOOLS = ["cvscan/", "diagnose/"]
PRIO = {"": "1.0", "free.html": "0.9", "starting-line.html": "0.9",
        "register.html": "0.9", "blog.html": "0.9", "cvscan/": "0.8",
        "diagnose/": "0.8"}

urls = MARKETING + TOOLS
body = "\n".join(
    f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-08-08</lastmod>"
    f"<changefreq>{'daily' if u=='blog.html' else 'weekly'}</changefreq>"
    f"<priority>{PRIO.get(u,'0.8')}</priority></url>" for u in urls)
wr(BUILD / "sitemap.xml",
   '<?xml version="1.0" encoding="UTF-8"?>\n'
   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
   + body + '\n</urlset>\n')
print(f"  + sitemap.xml: {len(urls)} urls (marketing/tool pages; portal pages excluded)")


# ── 3 · robots.txt ──────────────────────────────────────────────────────
wr(BUILD / "robots.txt",
   "# Everything Remote Job\n"
   "# Pages that must stay out of the index carry a noindex meta tag and are\n"
   "# deliberately NOT disallowed here: a blocked URL is never crawled, so its\n"
   "# noindex is never read, and an already-indexed page stays indexed.\n"
   "# This covers both the public marketing/tool pages (indexable) and the\n"
   "# participant/admin/instructor portal (noindex,nofollow on every page).\n\n"
   "User-agent: *\nAllow: /\n\n"
   "# Query-string permutations of any reader view\n"
   "Disallow: /*?p=\n\n"
   f"Sitemap: {SITE}/sitemap.xml\n")
print("  + robots.txt: unchanged policy, now covers the full merged tree")


# ── 4 · sw.js — ONE precache list for the ENTIRE merged build ──────────
skip_dirs = {"__pycache__"}
skip_ext = {".py", ".ts", ".md"}
skip_names = {"CNAME"}
shell = []
for f in sorted(BUILD.rglob("*")):
    if f.is_dir():
        continue
    rel = f.relative_to(BUILD)
    if any(part in skip_dirs for part in rel.parts):
        continue
    if f.suffix in skip_ext or f.name in skip_names:
        continue
    shell.append("./" + str(rel).replace("\\", "/"))
shell = ["./"] + sorted(set(shell) - {"./"})

sw = '''/* Everything Remote Job — service worker v1.1 (merged build).
   SHELL is generated from the ACTUAL final file list — marketing pages,
   the real cvscan/ and diagnose/ tools, and the whole participant/admin/
   instructor portal — so it can never name a file that does not exist.
   One missing entry makes addAll() reject and aborts the entire precache;
   entries are added individually here as a second line of defence. */
const VERSION = 'erj-v1-1-0';
const SHELL = ''' + json.dumps(shell, indent=2) + ''';

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const cache = await caches.open(VERSION);
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
wr(BUILD / "sw.js", sw)
print(f"  + sw.js: erj-v1-1-0, {len(shell)} files precached (whole merged tree)")
