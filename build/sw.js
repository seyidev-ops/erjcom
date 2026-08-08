/* Everything Remote Job — service worker v1.
   SHELL is emitted by the build from the real file list, so it can never
   name a file that does not exist. One missing entry makes addAll() reject
   and aborts the ENTIRE precache — that bug cost the old site a week. */
const VERSION = 'erj-v1-0-0';
const SHELL = [
  "./",
  "./app.css",
  "./app.js",
  "./manifest.webmanifest",
  "./erj-lockup-white.png",
  "./erj-mark-white.png",
  "./favicon32.png",
  "./index.html",
  "./free.html",
  "./starting-line.html",
  "./diagnose.html",
  "./cvscan.html",
  "./mastery-training.html",
  "./get-a-remote-job.html",
  "./inner-circle.html",
  "./masterclass.html",
  "./testimonials.html",
  "./blog.html",
  "./register.html",
  "./404.html",
  "./img/celebrating-offer-600.webp",
  "./img/hard-currency-600.webp",
  "./img/paid-in-dollars-600.webp",
  "./img/paid-in-dollars-1200.webp",
  "./img/working-remotely-600.webp",
  "./img/working-remotely-1200.webp",
  "./img/out-in-the-world-600.webp",
  "./img/out-in-the-world-1200.webp",
  "./img/facilitator-formal-600.webp",
  "./img/facilitator-formal-1200.webp",
  "./img/facilitator-warm-600.webp",
  "./img/facilitator-note-600.webp",
  "./img/facilitator-note-1200.webp",
  "./img/facilitator-offer-600.webp",
  "./img/facilitator-offer-1200.webp",
  "./img/facilitator-portrait-600.webp",
  "./img/facilitator-portrait-1200.webp"
];

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
