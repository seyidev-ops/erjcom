"use strict";
/* ═══════════════════════════════════════════════════════════════════════
   EVERYTHING REMOTE JOB — INTERACTION LAYER v1  (app.ts)
   Compile: tsc src/app.ts --outFile build/app.js --target es2018 --strict --lib es2018,dom

   ONE script for the whole site. Everything is delegated or observed, so
   markup added later works without re-initialising anything, and nothing
   here throws if its hook is absent on a given page.

   Deliberately NOT included: any library, any per-page script, any inline
   handler. The old site drifted because behaviour lived in six places.
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
    'use strict';
    const $ = (s, r = document) => r.querySelector(s);
    const $$ = (s, r = document) => Array.prototype.slice.call(r.querySelectorAll(s));
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    /* ── 1 · THEME ────────────────────────────────────────────────────
       Applied by an inline snippet in <head> before paint (no flash);
       this only handles the toggle and cross-tab sync. */
    function theme() {
        const KEY = 'erj-theme';
        const root = document.documentElement;
        const apply = (mode) => {
            root.setAttribute('data-theme', mode);
            const meta = $('meta[name="theme-color"]');
            if (meta)
                meta.setAttribute('content', mode === 'day' ? '#FAFAF8' : '#000000');
            $$('[data-theme-toggle]').forEach(b => {
                b.setAttribute('aria-label', mode === 'day' ? 'Switch to dark theme' : 'Switch to light theme');
                b.setAttribute('aria-pressed', String(mode === 'day'));
            });
        };
        $$('[data-theme-toggle]').forEach(btn => {
            btn.addEventListener('click', () => {
                const next = root.getAttribute('data-theme') === 'day' ? 'night' : 'day';
                try {
                    localStorage.setItem(KEY, next);
                }
                catch (e) { /* private mode */ }
                apply(next);
            });
        });
        addEventListener('storage', e => {
            if (e.key === KEY && e.newValue)
                apply(e.newValue);
        });
        apply(root.getAttribute('data-theme') || 'night');
    }
    /* ── 2 · DRAWER ───────────────────────────────────────────────────
       Focus is trapped while open and returned on close; Escape and the
       scrim both close it; body scroll is locked without the layout jump
       that position:fixed causes. */
    function drawer() {
        const panel = $('[data-drawer]');
        const scrim = $('[data-scrim]');
        const btn = $('[data-drawer-open]');
        if (!panel || !scrim || !btn)
            return;
        let last = null;
        const focusables = () => $$('a[href],button:not([disabled])', panel);
        const setOpen = (open) => {
            if (open) {
                last = document.activeElement;
                panel.setAttribute('data-open', '');
                scrim.setAttribute('data-open', '');
                document.body.style.overflow = 'hidden';
                const f = focusables();
                if (f.length)
                    f[0].focus();
            }
            else {
                panel.removeAttribute('data-open');
                scrim.removeAttribute('data-open');
                document.body.style.overflow = '';
                if (last)
                    last.focus();
            }
            btn.setAttribute('aria-expanded', String(open));
            panel.setAttribute('aria-hidden', String(!open));
        };
        btn.addEventListener('click', () => setOpen(!panel.hasAttribute('data-open')));
        scrim.addEventListener('click', () => setOpen(false));
        panel.addEventListener('click', e => {
            if (e.target.closest('a'))
                setOpen(false);
        });
        addEventListener('keydown', e => {
            if (!panel.hasAttribute('data-open'))
                return;
            if (e.key === 'Escape') {
                setOpen(false);
                return;
            }
            if (e.key !== 'Tab')
                return;
            const f = focusables();
            if (!f.length)
                return;
            const first = f[0], lastEl = f[f.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                lastEl.focus();
            }
            else if (!e.shiftKey && document.activeElement === lastEl) {
                e.preventDefault();
                first.focus();
            }
        });
        // a resize past the desktop breakpoint must not leave it stuck open
        const mq = matchMedia('(min-width: 62rem)');
        const onChange = () => { if (mq.matches)
            setOpen(false); };
        mq.addEventListener ? mq.addEventListener('change', onChange)
            : mq.addListener(onChange);
        setOpen(false);
    }
    /* ── 3 · REVEAL ON SCROLL ─────────────────────────────────────────
       IntersectionObserver, not scroll maths — reveal animations change
       element heights, which makes scroll-position arithmetic wrong. */
    function reveal() {
        const targets = $$('[data-reveal],[data-reveal-stagger]');
        if (!targets.length)
            return;
        if (reduced || !('IntersectionObserver' in window)) {
            targets.forEach(t => t.setAttribute('data-shown', ''));
            return;
        }
        const io = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting)
                    return;
                const el = entry.target;
                el.setAttribute('data-shown', '');
                if (el.hasAttribute('data-reveal-stagger')) {
                    $$(':scope > *', el).forEach((child, i) => {
                        child.style.transitionDelay = Math.min(i * 70, 420) + 'ms';
                    });
                }
                io.unobserve(el);
            });
        }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
        targets.forEach(t => io.observe(t));
    }
    /* ── 4 · IMAGES ───────────────────────────────────────────────────
       Fade in on decode. The LQIP sits behind as a CSS background, so a
       slow connection shows the shape and colour rather than a hole —
       and because .media fixes the aspect ratio, nothing ever shifts. */
    function images() {
        $$('.media img').forEach(img => {
            const done = () => img.setAttribute('data-loaded', '');
            if (img.complete && img.naturalWidth) {
                done();
                return;
            }
            img.addEventListener('load', done, { once: true });
            img.addEventListener('error', () => {
                done();
                const holder = img.closest('.media');
                if (holder)
                    holder.style.background = 'var(--surface-2)';
            }, { once: true });
        });
    }
    /* ── 5 · HEADER STATE + READING PROGRESS + BACK TO TOP ────────────
       All three read the same scroll position in one rAF-throttled pass,
       so scrolling costs a single layout read per frame. */
    function scrollUi() {
        const hdr = $('[data-header]');
        const bar = $('[data-progress]');
        const top = $('[data-totop]');
        let ticking = false;
        const run = () => {
            const y = scrollY;
            if (hdr) {
                if (y > 8)
                    hdr.setAttribute('data-stuck', '');
                else
                    hdr.removeAttribute('data-stuck');
            }
            if (bar) {
                const max = document.documentElement.scrollHeight - innerHeight;
                bar.style.width = (max > 0 ? Math.min(100, (y / max) * 100) : 0) + '%';
            }
            if (top) {
                if (y > innerHeight * 0.9)
                    top.setAttribute('data-show', '');
                else
                    top.removeAttribute('data-show');
            }
            ticking = false;
        };
        addEventListener('scroll', () => {
            if (!ticking) {
                ticking = true;
                requestAnimationFrame(run);
            }
        }, { passive: true });
        if (top) {
            top.addEventListener('click', () => scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }));
        }
        run();
    }
    /* ── 6 · SECTION SPY ──────────────────────────────────────────────
       Marks the nav link for whichever section owns the viewport. */
    function spy() {
        const links = $$('[data-spy] a[href^="#"]');
        if (!links.length || !('IntersectionObserver' in window))
            return;
        const map = new Map();
        links.forEach(a => {
            const id = a.getAttribute('href').slice(1);
            if (id)
                map.set(id, a);
        });
        const io = new IntersectionObserver(entries => {
            entries.forEach(e => {
                const a = map.get(e.target.id);
                if (!a)
                    return;
                if (e.isIntersecting) {
                    links.forEach(l => l.removeAttribute('data-active'));
                    a.setAttribute('data-active', '');
                }
            });
        }, { rootMargin: '-45% 0px -50% 0px' });
        map.forEach((_, id) => {
            const sec = document.getElementById(id);
            if (sec)
                io.observe(sec);
        });
    }
    /* ── 7 · COUNT UP ─────────────────────────────────────────────────
       Numbers animate once, when first seen. Honours reduced motion by
       printing the final value immediately. */
    function counters() {
        const nodes = $$('[data-count]');
        if (!nodes.length)
            return;
        const paint = (el, v) => {
            const dp = Number(el.dataset.decimals || 0);
            el.textContent = (el.dataset.prefix || '')
                + v.toFixed(dp).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
                + (el.dataset.suffix || '');
        };
        if (reduced || !('IntersectionObserver' in window)) {
            nodes.forEach(el => paint(el, Number(el.dataset.count)));
            return;
        }
        const io = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (!entry.isIntersecting)
                    return;
                const el = entry.target;
                io.unobserve(el);
                const target = Number(el.dataset.count) || 0;
                const dur = 1100;
                const t0 = performance.now();
                const step = (t) => {
                    const p = Math.min(1, (t - t0) / dur);
                    paint(el, target * (1 - Math.pow(1 - p, 3))); // ease-out cubic
                    if (p < 1)
                        requestAnimationFrame(step);
                };
                requestAnimationFrame(step);
            });
        }, { threshold: 0.4 });
        nodes.forEach(el => { paint(el, 0); io.observe(el); });
    }
    /* ── 8 · COPY TO CLIPBOARD ────────────────────────────────────────── */
    function copy() {
        document.addEventListener('click', async (e) => {
            const btn = e.target.closest('[data-copy]');
            if (!btn)
                return;
            const text = btn.dataset.copy || '';
            try {
                await navigator.clipboard.writeText(text);
            }
            catch (err) {
                const ta = document.createElement('textarea');
                ta.value = text;
                ta.style.position = 'fixed';
                ta.style.opacity = '0';
                document.body.appendChild(ta);
                ta.select();
                try {
                    document.execCommand('copy');
                }
                catch (e2) { /* nothing else to try */ }
                document.body.removeChild(ta);
            }
            const original = btn.textContent;
            btn.textContent = 'Copied';
            setTimeout(() => { btn.textContent = original; }, 1600);
        });
    }
    /* ── 9 · ANCHOR OFFSET ────────────────────────────────────────────
       scroll-padding-top handles this in CSS for real navigation, but a
       hash arriving on first load needs a nudge after layout settles. */
    function hashOnLoad() {
        if (!location.hash)
            return;
        const el = document.getElementById(location.hash.slice(1));
        if (!el)
            return;
        requestAnimationFrame(() => {
            setTimeout(() => el.scrollIntoView({ behavior: 'auto', block: 'start' }), 60);
        });
    }
    /* ── boot ─────────────────────────────────────────────────────────
       Each unit is isolated: one failing must never stop the rest. */
    const units = [
        ['theme', theme], ['drawer', drawer], ['reveal', reveal], ['images', images],
        ['scrollUi', scrollUi], ['spy', spy], ['counters', counters],
        ['copy', copy], ['hashOnLoad', hashOnLoad],
    ];
    function boot() {
        units.forEach(([name, fn]) => {
            try {
                fn();
            }
            catch (err) {
                if (console && console.warn)
                    console.warn('[erj] ' + name + ' failed', err);
            }
        });
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    }
    else {
        boot();
    }
    window.ERJ = { boot: boot };
})();
