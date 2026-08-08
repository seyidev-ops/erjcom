#!/usr/bin/env python3
"""One OG preview per page, 1200x630, generated from the page list.

Kickers carry no cohort number and no date: social platforms cache these
for months, so anything time-bound bakes a lie into every future share.
The logo is COMPOSITED from the real lockup, never redrawn.
"""
from PIL import Image, ImageDraw, ImageFont
import pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "build" / "img"
LOCK = ROOT / "build" / "erj-lockup-white.png"
W, H = 1200, 630
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BLACK, WHITE, ORANGE, GREY, DIM = "#000000", "#FFFFFF", "#FF5722", "#9A9A9A", "#3A3A3A"
PAD = 76          # the same generous gutter the site itself uses

F = lambda p, s: ImageFont.truetype(p, s)

CARDS = {
 "home": ("The remote job system", "Land a dollar-paying remote job — from right where you are.",
          ["dollar-paying"], "We will not let you go until you're hired.", "USD · EUR · GBP"),
 "free": ("Free · no email required", "Four tools that cost nothing and change everything.",
          ["nothing"], "Diagnostic, CV scan, live masterclass, job board.", "ALL FREE"),
 "start": ("Choose your depth", "Three routes. Find your rung.",
           ["Three"], "You build it, we build it, or we do it beside you.", "ONE LADDER"),
 "diagnose": ("Free · 90 seconds", "Your job search is leaking at one of four points.",
              ["one"], "Four questions. No email. Nothing stored.", "FIND YOUR LEAK"),
 "cvscan": ("Free · runs on your device", "Score your CV against 10 points in 90 seconds.",
            ["10"], "Nothing uploads. Nothing is stored.", "CV SELF-SCAN"),
 "mastery": ("You build it · Stages 1–4", "Build every career asset yourself.",
             ["yourself."], "Mindset, toolkit, async writing, global-ready assets.", "20 DAYS"),
 "garj": ("Done with you · Stage 5", "We source, apply beside you, and prep every interview.",
          ["beside"], "We will not let you go until you're hired.", "UNTIL HIRED"),
 "inner": ("Private residency · 1:1", "A small room, until the offer is signed.",
           ["signed."], "Application-first. Deliberately small.", "INNER CIRCLE"),
 "masterclass": ("Free live class · Zoom", "The Global Remote Job Blueprint.",
                 ["Blueprint."], "One hour on where job searches actually break.", "LIVE · FREE"),
 "stories": ("Documented results", "Real people. Real offers. Real dollars.",
             ["dollars."], "Nine journeys with the numbers attached.", "SUCCESS STORIES"),
 "blog": ("Free · new posts weekly", "Practical remote-job help, in plain English.",
          ["Practical"], "Scam checks, ATS CVs, interviews, timezones, pay.", "THE BLOG"),
 "register": ("Start here", "Which door is mine? Every price, in public.",
              ["mine?"], "Including the two answers that say don't pay yet.", "REGISTER"),
 "404": ("Page not found", "That page has moved on. You don't have to.",
         ["moved"], "Everything it held is one link away.", "404"),
}

def wrap(d, text, font, mw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= mw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def runs(line, emph):
    out = []
    for w in line.split(" "):
        c = ORANGE if any(w.strip(".,—").lower() == e.strip(".,—").lower() for e in emph) else WHITE
        if out and out[-1][1] == c: out[-1] = (out[-1][0] + " " + w, c)
        else:
            if out: out.append((" ", WHITE))
            out.append((w, c))
    return out

def build(key, kicker, head, emph, sub, tag):
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    for gx in range(40, W, 26):
        for gy in range(40, H, 26): d.point((gx, gy), fill="#141414")

    lock = Image.open(LOCK).convert("RGBA")
    lh = 58; lw = int(lock.width * (lh / lock.height))
    lock = lock.resize((lw, lh), Image.LANCZOS)
    img.paste(lock, (PAD, 48), lock)

    d.line([PAD, 208, PAD + 34, 208], fill=ORANGE, width=3)
    d.text((PAD + 50, 196), kicker.upper(), font=F(BOLD, 21), fill=ORANGE)

    size = 64
    while size > 32:
        f = F(BOLD, size)
        if len(wrap(d, head, f, W - 2 * PAD)) <= 3: break
        size -= 3
    f = F(BOLD, size); y = 258
    for line in wrap(d, head, f, W - 2 * PAD)[:3]:
        x = PAD
        for t, c in runs(line, emph):
            d.text((x, y), t, font=f, fill=c); x += d.textlength(t, font=f)
        y += int(size * 1.32)

    d.line([PAD, 540, W - PAD, 540], fill="#262626", width=1)
    d.text((PAD, 554), sub, font=F(REG, 21), fill=GREY)
    d.text((PAD, 588), "everythingremotejob.com", font=F(REG, 19), fill=DIM)
    tw = d.textlength(tag, font=F(BOLD, 19))
    d.text((W - PAD - tw, 588), tag, font=F(BOLD, 19), fill=ORANGE)

    p = OUT / f"og-{key}.jpg"
    img.save(p, "JPEG", quality=88, optimize=True)
    return p

if __name__ == "__main__":
    for k, args in CARDS.items():
        p = build(k, *args)
        print(f"  {p.name:22s} {p.stat().st_size//1024:>3d} KB")
    print(f"\n  {len(CARDS)} previews · evergreen kickers · real logo composited")
