/* Everything Remote Job — service worker v1.1 (merged build).
   SHELL is generated from the ACTUAL final file list — marketing pages,
   the real cvscan/ and diagnose/ tools, and the whole participant/admin/
   instructor portal — so it can never name a file that does not exist.
   One missing entry makes addAll() reject and aborts the entire precache;
   entries are added individually here as a second line of defence. */
const VERSION = 'erj-v1-1-0';
const SHELL = [
  "./",
  "./404.html",
  "./admin-login.html",
  "./admin.html",
  "./app.css",
  "./app.js",
  "./appletouchicon.png",
  "./blog-admin.html",
  "./blog.html",
  "./cvbuilder/docx.js",
  "./cvbuilder/engine.js",
  "./cvbuilder/import.js",
  "./cvbuilder/index.html",
  "./cvbuilder/vendor/pdf.min.mjs",
  "./cvbuilder/vendor/pdf.worker.min.mjs",
  "./cvscan/app.js",
  "./cvscan/index.html",
  "./cvscan/scan.css",
  "./cvscan/vendor/jszip.min.js",
  "./cvscan/vendor/pdf.min.js",
  "./cvscan/vendor/pdf.worker.min.js",
  "./dashboard.html",
  "./diagnose/dx.js",
  "./diagnose/index.html",
  "./earlybird.html",
  "./erj-ascend.js",
  "./erj-capture.js",
  "./erj-config.js",
  "./erj-lockup-white.png",
  "./erj-mark-white.png",
  "./erj-nav.js",
  "./erj-passcode.js",
  "./erj-product.js",
  "./erj-schema.js",
  "./erj-surge-console.html",
  "./erj-theme.js",
  "./favicon180.png",
  "./favicon32.png",
  "./founder-oluwaseyi.jpg",
  "./free.html",
  "./get-a-remote-job.html",
  "./icon192.png",
  "./icon192maskable.png",
  "./icon512.png",
  "./icon512maskable.png",
  "./images.json",
  "./img/celebrating-offer-600.webp",
  "./img/facilitator-formal-1200.webp",
  "./img/facilitator-formal-600.webp",
  "./img/facilitator-note-1200.webp",
  "./img/facilitator-note-600.webp",
  "./img/facilitator-offer-1200.webp",
  "./img/facilitator-offer-600.webp",
  "./img/facilitator-portrait-1200.webp",
  "./img/facilitator-portrait-600.webp",
  "./img/facilitator-warm-600.webp",
  "./img/hard-currency-600.webp",
  "./img/og-404.jpg",
  "./img/og-blog.jpg",
  "./img/og-cvscan.jpg",
  "./img/og-diagnose.jpg",
  "./img/og-free.jpg",
  "./img/og-garj.jpg",
  "./img/og-home.jpg",
  "./img/og-inner.jpg",
  "./img/og-masterclass.jpg",
  "./img/og-mastery.jpg",
  "./img/og-portal.jpg",
  "./img/og-register.jpg",
  "./img/og-start.jpg",
  "./img/og-stories.jpg",
  "./img/out-in-the-world-1200.webp",
  "./img/out-in-the-world-600.webp",
  "./img/paid-in-dollars-1200.webp",
  "./img/paid-in-dollars-600.webp",
  "./img/working-remotely-1200.webp",
  "./img/working-remotely-600.webp",
  "./index.html",
  "./inner-circle.html",
  "./instructor-login.html",
  "./instructor.html",
  "./login.html",
  "./logo.png",
  "./manifest.json",
  "./manifest.webmanifest",
  "./masterclass.html",
  "./mastery-training.html",
  "./offline.html",
  "./participant.html",
  "./photo-billboard.webp",
  "./photo-dollars-hand.webp",
  "./photo-dollars-woman.webp",
  "./photo-facilitator-note.webp",
  "./photo-facilitator-offer.webp",
  "./photo-facilitator-smile.webp",
  "./photo-facilitator-suit.webp",
  "./photo-remote-win-v2.webp",
  "./photo-woman-laptop.webp",
  "./preview-blog-v2.jpg",
  "./preview-cvscan-v2.jpg",
  "./preview-diagnose-v2.jpg",
  "./preview-earlybird-v2.jpg",
  "./preview-free-v2.jpg",
  "./preview-getaremotejob-v2.jpg",
  "./preview-index-v2.jpg",
  "./preview-innercircle-v2.jpg",
  "./preview-login-v2.jpg",
  "./preview-masterclass-v2.jpg",
  "./preview-masterytraining-v2.jpg",
  "./preview-portal.jpg",
  "./preview-register-v2.jpg",
  "./preview-starting-line-v2.jpg",
  "./preview-testimonials-v2.jpg",
  "./product.css",
  "./register.html",
  "./robots.txt",
  "./screenshot-mobile-v2.png",
  "./screenshot-wide-v2.png",
  "./sitemap.xml",
  "./starting-line.html",
  "./sw.js",
  "./testimonials.html"
];

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
