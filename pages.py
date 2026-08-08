#!/usr/bin/env python3
"""ERJ v1 — page content.

Content is data. Layout, head, nav, footer and SEO live in site.py and are
identical for every page by construction.
"""
from erjsite import (picture, btn, tlink, WA_LINK, CHANNEL, SITE, build)

WA_SCAN = (WA_LINK + "?text=Hello%20ERJ%20%E2%80%94%20I%20just%20took%20the%20free%20"
           "CV%20self-scan%20and%20I%20want%20the%20fix%20list%20for%20my%20score.")
WA_ASK = (WA_LINK + "?text=Hello%20ERJ%20%E2%80%94%20I%20have%20a%20question%20about%20"
          "getting%20a%20remote%20job.")

PLEDGE = "We will not let you go until you&rsquo;re hired."


def hero(kicker, h1, lede, actions, img_key, img_alt, note=None):
    return f'''<section class="section">
  <div class="wrap">
    <div class="split">
      <div data-reveal>
        <p class="kicker">{kicker}</p>
        <h1>{h1}</h1>
        <p class="lede mt-4">{lede}</p>
        <div class="btns mt-5">{actions}</div>
        {f'<p class="mt-4" style="font-size:var(--t-xs);color:var(--ink-faint)">{note}</p>' if note else ''}
      </div>
      <div data-reveal>{picture(img_key, img_alt, eager=True)}</div>
    </div>
  </div>
</section>'''


# ═══ HOME ══════════════════════════════════════════════════════════════
HOME = {
    "key": "home", "file": "index.html", "prio": "1.0", "freq": "weekly",
    "title": "Land a dollar-paying remote job",
    "desc": "The system that gets African professionals hired into USD, EUR and GBP "
            "roles from right where they are. Free CV scan, free diagnostic, free live "
            "masterclass, and three paid routes when you want it carried.",
    "schema": {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "Do I need a degree?",
             "acceptedAnswer": {"@type": "Answer", "text":
              "No. What global employers buy is demonstrable skill and evidence you can "
              "work unsupervised. Several of our students hold an HND or no degree at all."}},
            {"@type": "Question", "name": "How long does it take?",
             "acceptedAnswer": {"@type": "Answer", "text":
              "Most people who do the work land an offer between one and three months. "
              "One published story took fourteen months. We publish the slow ones too."}},
            {"@type": "Question", "name": "Can Nigerian candidates really be paid in dollars?",
             "acceptedAnswer": {"@type": "Answer", "text":
              "Yes, through contractor agreements and employer-of-record services. The skill "
              "is checking which companies already do it before you spend an hour applying."}},
        ],
    },
    "body": hero(
        "The remote job system",
        'Land a <span class="accent">dollar‑paying</span> remote job &mdash; from right where you are.',
        "Your costs stay in naira. Your salary doesn&rsquo;t. We rebuild how you are "
        "represented, aim you at companies that can actually hire you, and stay with you "
        "until an offer letter lands.",
        btn("Find your leak &mdash; free", "diagnose.html")
        + btn("See every option", "register.html", ghost=True),
        "celebrating-offer", "A Nigerian professional celebrating a remote job offer",
        note="90 seconds &middot; no email required &middot; nothing stored",
    ) + f'''

<section class="section">
  <div class="wrap">
    <div class="stats" data-reveal-stagger>
      <div><div class="stat-n" data-count="382" data-suffix="+">0</div><div class="stat-l">Professionals trained</div></div>
      <div><div class="stat-n" data-count="9">0</div><div class="stat-l">Cohorts delivered</div></div>
      <div><div class="stat-n" data-count="30" data-suffix="+">0</div><div class="stat-l">Roles sourced weekly</div></div>
      <div><div class="stat-n" data-count="4">0</div><div class="stat-l">Points a search runs on</div></div>
    </div>
  </div>
</section>

<section class="section section--line" id="model">
  <div class="wrap">
    <p class="kicker" data-reveal>The model</p>
    <h2 data-reveal>Four points. <span class="accent">One leak.</span></h2>
    <p class="lede mt-4" data-reveal>A pipe rarely bursts along its length &mdash; it fails at a
      joint. Every remote job search runs on these same four, in this order, and when it
      produces nothing the fault is almost always at exactly one of them.</p>

    <div class="grid grid-4 mt-6" data-reveal-stagger>
      <div class="card"><div class="card-k">01 Supply</div><h3>They must see it</h3>
        <p>You cannot apply to roles you never find &mdash; or that were closed, fake, or never
        open to applicants from here.</p></div>
      <div class="card"><div class="card-k">02 Representation</div><h3>It must be readable</h3>
        <p>Software reads you before a human does. A CV people call &ldquo;nice&rdquo; can still
        be unreadable to the system screening it.</p></div>
      <div class="card"><div class="card-k">03 Aim</div><h3>It must reach the target</h3>
        <p>A good document sent in the wrong direction produces exactly the same silence
        as a bad one.</p></div>
      <div class="card"><div class="card-k">04 Conversion</div><h3>Interest must become value</h3>
        <p>A CV cannot hire you. It buys twenty minutes. What happens in them is a separate,
        learnable skill.</p></div>
    </div>

    <p class="mt-5" data-reveal><b>Most people patch the wrong one for months.</b>
      {tlink("Four questions tell you which is yours", "diagnose.html")}</p>
  </div>
</section>

<section class="section section--line" id="routes">
  <div class="wrap">
    <p class="kicker" data-reveal>Your starting line</p>
    <h2 data-reveal>One ladder, <span class="accent">three depths.</span></h2>
    <p class="lede mt-4" data-reveal>Nobody needs all three. You need the one that matches
      where you actually are today.</p>

    <div class="rungs mt-6" data-reveal-stagger>
      <div class="rung"><div class="rung-n"></div><div>
        <h3>Remote Job Mastery &mdash; you build it</h3>
        <p>Twenty training days across four stages. You build every career asset yourself and
        keep the skill for the rest of your career.</p>
        <div class="rung-price">&#8358;250,000 &middot; stages from &#8358;70,000</div>
        <p class="mt-4">{tlink("See the four stages", "mastery-training.html")}</p></div></div>

      <div class="rung"><div class="rung-n"></div><div>
        <h3>Get A Remote Job &mdash; done with you</h3>
        <p>We rebuild your four assets, source 30+ verified roles weekly, apply beside you and
        rehearse every interview. Starts any week, no cohort to wait for.</p>
        <div class="rung-price">&#8358;150,000 &middot; until you&rsquo;re hired</div>
        <p class="mt-4">{tlink("See the placement engine", "get-a-remote-job.html")}</p></div></div>

      <div class="rung"><div class="rung-n"></div><div>
        <h3>The Inner Circle &mdash; done beside you</h3>
        <p>A small private residency. Real-time co-applying, private mock panels, direct
        introductions, and negotiation done with you rather than explained to you.</p>
        <div class="rung-price">&#8358;250,000 / year &middot; application-first</div>
        <p class="mt-4">{tlink("See the residency", "inner-circle.html")}</p></div></div>
    </div>
  </div>
</section>

<section class="section section--line" id="free">
  <div class="wrap">
    <div class="split split--flip">
      <div data-reveal>
        <p class="kicker">Free for everyone</p>
        <h2>Start with what costs <span class="accent">nothing.</span></h2>
        <p class="lede mt-4">Four tools, no email address, nothing stored. If you work through
          them properly you will arrive at any paid door already ahead.</p>
        <ul class="ticks mt-5">
          <li><b>Find Your Leak</b> &mdash; four questions, ninety seconds, names your one broken point.</li>
          <li><b>The 10-Point CV Self-Scan</b> &mdash; runs on your own device; your CV never leaves it.</li>
          <li><b>The Global Remote Job Blueprint</b> &mdash; a free live class, one hour, on Zoom.</li>
          <li><b>The free job board</b> &mdash; verified roles on WhatsApp, posted weekly.</li>
        </ul>
        <div class="btns mt-5">{btn("Open the free stack", "free.html")}</div>
      </div>
      {picture("working-remotely", "A woman working remotely at her laptop")}
    </div>
  </div>
</section>

<section class="section section--line" id="proof">
  <div class="wrap">
    <p class="kicker" data-reveal>Documented results</p>
    <h2 data-reveal>Real people. Real offers. <span class="accent">Real dollars.</span></h2>
    <div class="grid grid-3 mt-6" data-reveal-stagger>
      <div class="quote"><div class="delta"><span class="was">&#8358;180,000/mo</span>
        <span class="now">$2,100/mo</span></div>
        <blockquote>&ldquo;Nobody asked about my degree. Every single person asked how I handle
        an angry customer at 11pm, and I had four years of answers.&rdquo;</blockquote>
        <cite>Ngozi &middot; retail supervisor &rarr; remote customer success &middot; 6 weeks</cite></div>
      <div class="quote"><div class="delta"><span class="was">&#8358;7.2M/yr</span>
        <span class="now">$71,000/yr</span></div>
        <blockquote>&ldquo;Being 42 was not the obstacle I thought it was. Eleven years of closing
        books was the entire reason they wanted me.&rdquo;</blockquote>
        <cite>Uche &middot; finance manager &middot; discreet search &middot; 11 weeks</cite></div>
      <div class="quote"><div class="delta"><span class="was">2 finals lost</span>
        <span class="now">$46,800/yr</span></div>
        <blockquote>&ldquo;I rewrote my CV four times for a problem that was never in my CV. The
        thing that was broken took two weeks to fix.&rdquo;</blockquote>
        <cite>Tunde &middot; data analyst &middot; the conversion leak</cite></div>
    </div>
    <p class="mt-5" data-reveal>{tlink("Read all nine journeys, with the numbers", "testimonials.html")}</p>
  </div>
</section>

<section class="section section--line" id="faq">
  <div class="wrap">
    <p class="kicker" data-reveal>Before you decide</p>
    <h2 data-reveal>The questions <span class="accent">everybody asks.</span></h2>
    <div class="acc mt-6" data-reveal>
      <details><summary>Do I need a degree?</summary><div class="acc-body">
        No. What global employers buy is demonstrable skill and evidence you can work
        unsupervised. Several of our students hold an HND, or no degree at all, and are paid
        in hard currency today.</div></details>
      <details><summary>How long does it actually take?</summary><div class="acc-body">
        Most people who do the work land an offer between one and three months. One of our
        published stories took fourteen. We publish the slow ones on purpose, because the
        screenshots everywhere else teach people to quit at week six.</div></details>
      <details><summary>Can Nigerian candidates really be paid in dollars?</summary><div class="acc-body">
        Yes &mdash; through contractor agreements and employer-of-record services. Not every
        company can do it, which is exactly the point: the skill is checking which ones already
        have before you spend an hour applying.</div></details>
      <details><summary>What if I do everything and still don&rsquo;t get hired?</summary><div class="acc-body">
        Then we are still working. {PLEDGE} Two things make that possible: you do the
        assignments, and you apply to what we source. If you cannot give the evenings this
        month, don&rsquo;t pay this month &mdash; tell us and stay on the free stack until the
        season is right.</div></details>
      <details><summary>Is this a scam?</summary><div class="acc-body">
        A fair question, because the space is full of them. Everything we charge for is listed
        with its price in public, the free tools require no email address, and our register page
        includes two honest outcomes that tell you <em>not</em> to buy yet.</div></details>
    </div>
  </div>
</section>

<section class="section section--line">
  <div class="wrap center" data-reveal>
    <h2>The cohort has a date.<br><span class="accent">Your job hunt doesn&rsquo;t.</span></h2>
    <p class="lede mt-4 center">Three doors open the day you walk through them. And if the honest
      answer is &ldquo;not yet&rdquo;, the free stack is genuinely good &mdash; start there.</p>
    <div class="btns mt-5" style="justify-content:center">
      {btn("See every option and price", "register.html")}
      {btn("Talk to a human first", WA_ASK, ghost=True, blank=True)}
    </div>
  </div>
</section>
''',
}


# ═══ DIAGNOSE ══════════════════════════════════════════════════════════
DIAGNOSE = {
    "key": "diagnose", "file": "diagnose.html", "prio": "0.9",
    "title": "Find Your Leak — the four-point diagnostic",
    "desc": "Four questions, ninety seconds. Find out whether your remote job search is "
            "leaking at Supply, Representation, Aim or Conversion — and get the one fix "
            "that matters. Free, no email required, nothing stored.",
    "body": f'''<section class="section">
  <div class="wrap">
    <div style="max-width:var(--measure-text)" data-reveal>
      <p class="kicker">Free &middot; 90 seconds &middot; nothing stored</p>
      <h1>Your job search is leaking at <span class="accent">one</span> of four points.</h1>
      <p class="lede mt-4">Most people patch the wrong one for months &mdash; rewriting a CV when
        the problem was aim, or hunting more job boards when the problem was the document.
        Four questions, and you will know where to spend your next thirty days.</p>
    </div>

    <div class="mt-6" data-reveal>
      <div class="card" id="dx" style="max-width:44rem">
        <div class="card-k">The diagnostic</div>
        <h2 style="font-size:var(--t-xl)">Answer honestly. Nobody is watching.</h2>
        <p class="mt-4">There are no wrong answers and no scoring against anyone else. The
          questions only sort your situation into one of the four points below.</p>
        <div class="btns mt-5">
          {btn("Start the four questions", WA_LINK + "?text=Hello%20ERJ%20%E2%80%94%20I%20want%20to%20find%20my%20leak.%20Please%20send%20me%20the%20four%20questions.", blank=True)}
        </div>
        <p class="mt-4" style="font-size:var(--t-xs);color:var(--ink-faint)">
          We answer personally &mdash; usually within the hour during working hours.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--line" id="four">
  <div class="wrap">
    <p class="kicker" data-reveal>The model</p>
    <h2 data-reveal>Four points. <span class="accent">One leak.</span></h2>
    <div class="grid grid-2 mt-6" data-reveal-stagger>
      <div class="card"><div class="card-k">01 Supply</div>
        <h3>Someone must see the opportunity</h3>
        <p class="mt-2"><b>The leak looks like:</b> you cannot find real openings &mdash; or
        everything you find smells like a scam, is already closed, or was never open to
        applicants from here.</p>
        <p class="mt-4">{tlink("Free verified roles, weekly", CHANNEL, blank=True)}</p></div>
      <div class="card"><div class="card-k">02 Representation</div>
        <h3>Your signal must be understood</h3>
        <p class="mt-2"><b>The leak looks like:</b> you apply and hear nothing at all. Total
        silence usually means you were never actually read.</p>
        <p class="mt-4">{tlink("Score your CV free", "cvscan.html")}</p></div>
      <div class="card"><div class="card-k">03 Aim</div>
        <h3>It must reach the right target</h3>
        <p class="mt-2"><b>The leak looks like:</b> you are applying a lot and getting rejections
        or nothing &mdash; volume without direction.</p>
        <p class="mt-4">{tlink("See the placement engine", "get-a-remote-job.html")}</p></div>
      <div class="card"><div class="card-k">04 Conversion</div>
        <h3>Interest must become value</h3>
        <p class="mt-2"><b>The leak looks like:</b> interviews come, offers do not. Or the offer
        arrives and the money is wrong.</p>
        <p class="mt-4">{tlink("See the Inner Circle", "inner-circle.html")}</p></div>
    </div>
    <p class="lede mt-6" data-reveal><b>Fix one at a time.</b> The most common mistake is trying
      to repair all four at once and finishing none of them.</p>
  </div>
</section>
''',
}


# ═══ FREE ══════════════════════════════════════════════════════════════
def free_block(n, kicker, title, desc, points, cta_label, cta_href, img, alt, flip, blank=False):
    return f'''<div class="split {'split--flip' if flip else ''} mt-6" data-reveal>
  <div>
    <p class="kicker">{n} &middot; {kicker}</p>
    <h2 style="font-size:var(--t-2xl)">{title}</h2>
    <p class="lede mt-4">{desc}</p>
    <ul class="ticks mt-4">{"".join(f"<li>{p}</li>" for p in points)}</ul>
    <div class="btns mt-5">{btn(cta_label, cta_href, blank=blank)}</div>
  </div>
  {picture(img, alt)}
</div>'''


FREE = {
    "key": "free", "file": "free.html", "prio": "0.9",
    "title": "Free For You — four tools, no email",
    "desc": "Four free tools that cost nothing and require no email address: the four-point "
            "diagnostic, the 10-point CV self-scan, a free live masterclass, and a verified "
            "remote job board on WhatsApp.",
    "body": f'''<section class="section">
  <div class="wrap" style="max-width:calc(var(--measure) + 2 * var(--gutter))">
    <div style="max-width:var(--measure-text)" data-reveal>
      <p class="kicker">Free &middot; no email required</p>
      <h1>Four tools that cost nothing and <span class="accent">change everything.</span></h1>
      <p class="lede mt-4">Nothing here is a trial, a teaser, or a form in disguise. Work through
        these properly and you will arrive at any paid door already ahead of where most people
        start.</p>
    </div>

    {free_block("01", "Start here &middot; 90 seconds", "Find Your Leak",
      "Four questions that name which of the four points is actually breaking your search, "
      "so you stop patching the other three.",
      ["Sorts you into Supply, Representation, Aim or Conversion",
       "Gives you three things to do <b>tonight</b>, free, for your point",
       "Tells you which of everything else here to use first"],
      "Find my leak", "diagnose.html", "facilitator-formal",
      "Oluwaseyi Ashiru, who answers every diagnostic personally", False)}

    {free_block("02", "Runs on your device", "The 10-Point CV Self-Scan",
      "Ninety seconds, and you know exactly which of the ten points a recruiter&rsquo;s software "
      "will fail you on. Your CV never leaves your phone.",
      ["Nothing uploads. Nothing is stored. Nothing is logged.",
       "Scores the ten checks that decide whether a human ever sees your file",
       "Send us the score and we reply with the fix list, personally"],
      "Score my CV free", "cvscan.html", "celebrating-offer",
      "A professional celebrating after fixing his CV", True)}

    {free_block("03", "Live on Zoom &middot; 100 seats", "The Global Remote Job Blueprint",
      "A free one-hour class on where remote job searches actually break, taught live, with "
      "your questions answered in the room.",
      ["No prerequisites and no pitch during the teaching",
       "Bring your CV scan score &mdash; we teach to the room&rsquo;s numbers",
       "Recording sent to everyone who reserves a seat"],
      "Reserve a free seat", "masterclass.html", "facilitator-warm",
      "Oluwaseyi Ashiru hosting the live masterclass", False)}

    {free_block("04", "Updated weekly", "The Global Remote Job Board",
      "Verified remote roles open to African applicants, posted free on WhatsApp &mdash; "
      "scam-filtered and checked that the company can actually pay across a border.",
      ["Every listing checked before it is posted",
       "No fees, ever &mdash; the free board stays free",
       "Message us and we&rsquo;ll tell you which roles are worth a real application"],
      "Join the free board", CHANNEL, "paid-in-dollars",
      "A woman celebrating being paid in dollars", True, blank=True)}
  </div>
</section>

<section class="section section--line">
  <div class="wrap center" data-reveal>
    <h2>When free stops being enough</h2>
    <p class="lede mt-4 center">Free is a doorway, not a destination. If you have worked through
      all four and your situation has not moved, the missing ingredient is no longer information
      &mdash; it is a system, a deadline, and somebody who does not let you go quiet.</p>
    <div class="btns mt-5" style="justify-content:center">{btn("See the three routes", "starting-line.html")}</div>
  </div>
</section>
''',
}


# ═══ STARTING LINE ═════════════════════════════════════════════════════
STARTING = {
    "key": "start", "file": "starting-line.html", "prio": "0.9",
    "title": "Your Starting Line",
    "desc": "Three routes to a dollar-paying remote job at three depths: Mastery Training "
            "(you build it), Get A Remote Job (done with you) and the Inner Circle residency "
            "(done beside you, until the offer is signed).",
    "body": f'''<section class="section">
  <div class="wrap">
    <div style="max-width:var(--measure-text)" data-reveal>
      <p class="kicker">Choose your depth</p>
      <h1>Three routes. <span class="accent">Find your rung.</span></h1>
      <p class="lede mt-4">The same work at three depths: <b>you build it</b>, <b>we build it with
        you</b>, or <b>we work it beside you until the offer is signed</b>. Nobody needs all three.</p>
      <p class="mt-4">Not sure where you are? {tlink("Find your leak first", "diagnose.html")}</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split mt-6" data-reveal>
      <div>
        <p class="kicker">Route 01 &middot; You build it</p>
        <h2>Remote Job Mastery</h2>
        <p class="lede mt-4">Twenty training days across four stages. You leave with every asset
          built by your own hands, and the system that produced them.</p>
        <ul class="ticks mt-4">
          <li><b>Stage 1 &middot; Remote Mindset Blueprint</b> &mdash; how global hiring works and who can actually pay you.</li>
          <li><b>Stage 2 &middot; The Digital Toolkit</b> &mdash; the tools distributed teams run on, plus AI fluency.</li>
          <li><b>Stage 3 &middot; Async Communication Mastery</b> &mdash; the skill you are judged on daily.</li>
          <li><b>Stage 4 &middot; Start Your Remote Career</b> &mdash; the Global Ready Package and weekly targeting system.</li>
        </ul>
        <p class="rung-price mt-4">&#8358;250,000 for all four &middot; single stages from &#8358;70,000</p>
        <div class="btns mt-5">{btn("See the four stages", "mastery-training.html")}</div>
      </div>
      {picture("celebrating-offer", "A student celebrating after completing the mastery training")}
    </div>

    <div class="split split--flip mt-6" data-reveal>
      <div>
        <p class="kicker">Route 02 &middot; Done with you</p>
        <h2>Get A Remote Job</h2>
        <p class="lede mt-4">For people whose evenings are already full. We do not hand you a
          better document and wish you luck &mdash; we run the search beside you.</p>
        <ul class="ticks mt-4">
          <li><b>Your four assets rebuilt for you</b> inside seven days.</li>
          <li><b>30+ verified roles sourced weekly</b>, checked for cross-border hiring.</li>
          <li><b>Applications sent alongside you</b>, tailored, while a shortlist still exists.</li>
          <li><b>Interview and salary rehearsal</b> before it matters.</li>
        </ul>
        <p class="rung-price mt-4">&#8358;150,000 once &middot; starts any week</p>
        <div class="btns mt-5">{btn("See the placement engine", "get-a-remote-job.html")}</div>
      </div>
      {picture("hard-currency", "Hard currency earned from a remote role")}
    </div>

    <div class="split mt-6" data-reveal>
      <div>
        <p class="kicker">Route 03 &middot; Done beside you</p>
        <h2>The Inner Circle</h2>
        <p class="lede mt-4">A deliberately small private residency. Not a course &mdash; a room
          that works with you in real time until the offer is signed.</p>
        <ul class="ticks mt-4">
          <li><b>Real-time co-applying</b> rather than homework.</li>
          <li><b>Private mock panels</b> and direct introductions.</li>
          <li><b>Negotiation done with you</b>, not explained to you.</li>
          <li><b>Application-first</b> &mdash; fit is confirmed before any payment.</li>
        </ul>
        <p class="rung-price mt-4">&#8358;250,000 / year &middot; or &#8358;135,000 &times; 2</p>
        <div class="btns mt-5">{btn("See the residency", "inner-circle.html")}</div>
      </div>
      {picture("facilitator-offer", "Oluwaseyi Ashiru, who leads the Inner Circle residency")}
    </div>
  </div>
</section>

<section class="section section--line">
  <div class="wrap center" data-reveal>
    <h2>Still not sure which is yours?</h2>
    <p class="lede mt-4 center">The register page asks three questions &mdash; skill, timeline,
      budget &mdash; and gives you an honest answer, including two outcomes that tell you not to
      pay yet.</p>
    <div class="btns mt-5" style="justify-content:center">{btn("Which door is mine?", "register.html")}</div>
  </div>
</section>
''',
}


# ═══ PRODUCT PAGES ═════════════════════════════════════════════════════
def product(key, file, title, desc, kicker, h1, lede, price, price_note, points,
            img, alt, schema_name, schema_price, extra=""):
    return {
        "key": key, "file": file, "prio": "0.9", "title": title, "desc": desc,
        "schema": {
            "@context": "https://schema.org", "@type": "Course",
            "name": schema_name, "description": desc,
            "provider": {"@type": "Organization", "name": "Everything Remote Job",
                         "sameAs": SITE + "/"},
            "offers": {"@type": "Offer", "price": schema_price, "priceCurrency": "NGN",
                       "availability": "https://schema.org/InStock",
                       "url": f"{SITE}/{file}"},
            "hasCourseInstance": {"@type": "CourseInstance",
                                  "courseMode": "online",
                                  "courseWorkload": "PT20H"},
        },
        "body": hero(kicker, h1, lede,
                     btn("Register now", "register.html")
                     + btn("Ask a question", WA_ASK, ghost=True, blank=True),
                     img, alt, note=PLEDGE)
        + f'''
<section class="section section--line">
  <div class="wrap">
    <div class="split">
      <div data-reveal>
        <p class="kicker">What you get</p>
        <h2>Everything included</h2>
        <ul class="ticks mt-5">{"".join(f"<li>{p}</li>" for p in points)}</ul>
      </div>
      <div class="card" data-reveal>
        <div class="card-k">Your investment</div>
        <div style="font-family:var(--font-display);font-size:var(--t-3xl);font-weight:800;
                    line-height:1;color:var(--ink)">{price}</div>
        <p class="mt-2" style="color:var(--ink-faint);font-size:var(--t-sm)">{price_note}</p>
        <div class="btns mt-5">{btn("Register now", "register.html")}</div>
        <p class="mt-4" style="font-size:var(--t-xs);color:var(--ink-faint)">{PLEDGE}</p>
      </div>
    </div>
  </div>
</section>
{extra}
<section class="section section--line">
  <div class="wrap center" data-reveal>
    <h2>Not sure this is your door?</h2>
    <p class="lede mt-4 center">Four questions name the point that is actually breaking your
      search &mdash; and sometimes the honest answer is that you need a different route, or
      nothing paid at all yet.</p>
    <div class="btns mt-5" style="justify-content:center">
      {btn("Find your leak &mdash; free", "diagnose.html")}
      {btn("Compare all three routes", "starting-line.html", ghost=True)}
    </div>
  </div>
</section>
''',
    }


MASTERY = product(
    "mastery", "mastery-training.html", "Remote Job Mastery Training",
    "Twenty training days across four stages: Remote Mindset Blueprint, The Digital Toolkit, "
    "Async Communication Mastery and Start Your Remote Career. Build every career asset "
    "yourself and keep the skill for life.",
    "You build it &middot; Stages 1&ndash;4",
    'Build every career asset <span class="accent">yourself</span> &mdash; and keep the skill for life.',
    "A rewritten CV fixes this application. The system behind it fixes every application you "
    "will ever send. Twenty training days, four stages, real deliverables every day.",
    "&#8358;250,000", "All four stages &middot; &#8358;370,000 taken separately, so the bundle saves "
    "&#8358;120,000 &middot; single stages from &#8358;70,000",
    ["<b>Stage 1 &middot; Remote Mindset Blueprint</b> &mdash; deep-work blocks, daily KPIs, "
     "end-of-day reporting and a full workspace audit.",
     "<b>Stage 2 &middot; The Digital Toolkit</b> &mdash; Zoom, Asana, cloud collaboration and "
     "AI fluency layered across all of it.",
     "<b>Stage 3 &middot; Async Communication Mastery</b> &mdash; the zero-follow-up email "
     "framework and your own Working With Me manual.",
     "<b>Stage 4 &middot; Start Your Remote Career</b> &mdash; ATS-ready CV, digital portfolio, "
     "optimised LinkedIn and a recorded STAR interview video.",
     "<b>Workbooks, LMS access and recordings</b> for every stage, yours to keep.",
     "<b>Sixty days of the private job board</b> included with enrolment."],
    "celebrating-offer", "A student celebrating a remote job offer",
    "Remote Job Mastery Training", "250000")

GARJ = product(
    "garj", "get-a-remote-job.html", "Get A Remote Job",
    "The done-with-you placement engine: your four career assets rebuilt inside seven days, "
    "30+ verified roles sourced weekly, applications sent alongside you, and interview and "
    "salary rehearsal — until a real offer letter lands.",
    "Done with you &middot; Stage 5",
    'We source the roles, apply <span class="accent">beside you</span>, and prep every interview.',
    "The hardest part of a job hunt is not knowing what to do &mdash; it is doing it in week six. "
    "This is the part that gets carried for you.",
    "&#8358;150,000", "Once &middot; starts the week you join &middot; no cohort to wait for",
    ["<b>Your four assets rebuilt for you</b> &mdash; CV, LinkedIn, portfolio and cover letters, "
     "inside seven days.",
     "<b>30+ verified roles sourced every week</b> &mdash; scam-filtered and checked that the "
     "company can actually pay someone in your country.",
     "<b>Applications sent alongside you</b>, tailored to each advert, in the first week of "
     "posting while a shortlist still exists.",
     "<b>Interview and salary rehearsal</b>, including the two answers that quietly end most "
     "final rounds.",
     "<b>A weekly written report</b> so you always know what moved.",
     "<b>We do not let go until a real offer letter lands.</b>"],
    "hard-currency", "Hard currency earned from a remote role",
    "Get A Remote Job — placement engine", "150000")

INNER = product(
    "inner", "inner-circle.html", "The Inner Circle",
    "A small, application-first private residency: real-time co-applying, private mock panels, "
    "direct introductions and negotiation done with you rather than explained to you.",
    "Private residency &middot; 1:1",
    'A small room, <span class="accent">until the offer is signed.</span>',
    "Not a course. A residency &mdash; deliberately small, because the room works with you in "
    "real time rather than watching a recording.",
    "&#8358;250,000", "Per year &middot; or &#8358;135,000 &times; 2 &middot; application-first, "
    "fit confirmed before any payment",
    ["<b>Real-time co-applying</b> &mdash; we apply together, in the same session.",
     "<b>Private mock panels</b> with honest, specific feedback.",
     "<b>Direct introductions</b> where we genuinely have them.",
     "<b>Negotiation done with you</b> on the live offer, not taught in the abstract.",
     "<b>A deliberately small room</b> &mdash; capacity is people, not a marketing figure.",
     "<b>Application first.</b> An advisor confirms fit before any payment is discussed."],
    "facilitator-offer", "Oluwaseyi Ashiru, who leads the Inner Circle residency",
    "The Inner Circle residency", "250000")


# ═══ REMAINING PAGES ═══════════════════════════════════════════════════
CVSCAN = {
    "key": "cvscan", "file": "cvscan.html", "prio": "0.8",
    "title": "Free 10-Point CV Self-Scan",
    "desc": "Score your CV against the ten points that decide whether a human ever sees it. "
            "Ninety seconds, runs on your own device — nothing uploads, nothing is stored.",
    "body": hero("Free &middot; runs on your device",
                 'Score your CV against <span class="accent">10 points</span> in 90 seconds.',
                 "The first reader of your CV is software. It does not admire your layout &mdash; "
                 "it looks for a title, dates, tools and keywords, and if your design hides them "
                 "it returns almost nothing. That is how &ldquo;my CV is nice&rdquo; and "
                 "&ldquo;nobody replies&rdquo; are both true at once.",
                 btn("Send my CV for scoring", WA_SCAN, blank=True)
                 + btn("Find your leak instead", "diagnose.html", ghost=True),
                 "working-remotely", "A professional reviewing her CV",
                 note="Nothing uploads &middot; nothing is stored &middot; nothing is logged")
    + f'''
<section class="section section--line">
  <div class="wrap">
    <p class="kicker" data-reveal>After the score</p>
    <h2 data-reveal>Knowing where you default is <span class="accent">the easy half</span></h2>
    <p class="lede mt-4" data-reveal>Your score measures ONE of the four points a job search runs
      on &mdash; Representation, whether your signal can be read. A 10/10 CV still gets silence if
      you are aiming at companies that cannot hire you, or if the interview ends without an offer.</p>

    <div class="grid grid-3 mt-6" data-reveal-stagger>
      <div class="card"><div class="card-k">You build it &middot; &#8358;250,000</div>
        <h3>Remote Job Mastery</h3>
        <p class="mt-2">Four stages wide, because the document was never the whole problem:
        how global hiring works, the tools distributed teams run on, the async writing you are
        judged on daily, and the Global Ready Package built by your own hands.</p>
        <p class="mt-4">{tlink("See the four stages", "mastery-training.html")}</p></div>
      <div class="card"><div class="card-k">Done with you &middot; &#8358;150,000</div>
        <h3>Get A Remote Job</h3>
        <p class="mt-2">Your four assets rebuilt to score 9&ndash;10 on the very points you just
        defaulted on, plus 30+ sourced roles weekly, applications sent alongside you, and
        interview rehearsal &mdash; until an offer lands.</p>
        <p class="mt-4">{tlink("See the placement engine", "get-a-remote-job.html")}</p></div>
      <div class="card"><div class="card-k">Free &middot; 90 seconds</div>
        <h3>Check the other three points</h3>
        <p class="mt-2">Scored 8 or higher? Your CV is <em>not</em> why you are not getting
        interviews, and rewriting it a fifth time will change nothing. The leak is further down
        the pipe &mdash; Supply, Aim or Conversion.</p>
        <p class="mt-4">{tlink("Find my leak", "diagnose.html")}</p></div>
    </div>
  </div>
</section>
''',
}

MASTERCLASS = {
    "key": "masterclass", "file": "masterclass.html", "prio": "0.8",
    "title": "The Global Remote Job Blueprint",
    "desc": "A free live one-hour class on where remote job searches actually break — and how "
            "to tell which of the four points is breaking yours. Zoom, 100 seats, no pitch "
            "during the teaching.",
    "schema": {"@context": "https://schema.org", "@type": "EducationEvent",
               "name": "The Global Remote Job Blueprint",
               "description": "Free live class on where remote job searches break.",
               "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
               "eventStatus": "https://schema.org/EventScheduled",
               "location": {"@type": "VirtualLocation", "url": SITE + "/masterclass.html"},
               "organizer": {"@type": "Organization", "name": "Everything Remote Job"},
               "isAccessibleForFree": True},
    "body": hero("Free live class &middot; Zoom",
                 'The Global Remote Job <span class="accent">Blueprint.</span>',
                 "One hour on the four places a remote job hunt actually breaks, and how to tell "
                 "which one is breaking yours. No prerequisites. Bring your questions.",
                 btn("Reserve a free seat", WA_LINK + "?text=Hello%20ERJ%20%E2%80%94%20please%20"
                     "reserve%20me%20a%20seat%20for%20the%20free%20Global%20Remote%20Job%20"
                     "Blueprint%20masterclass.", blank=True)
                 + btn("See the free stack", "free.html", ghost=True),
                 "facilitator-warm", "Oluwaseyi Ashiru hosting the live masterclass",
                 note="Free &middot; 100 seats &middot; recording sent to everyone who reserves")
    + f'''
<section class="section section--line">
  <div class="wrap">
    <p class="kicker" data-reveal>What the hour covers</p>
    <h2 data-reveal>One hour. <span class="accent">Four answers.</span></h2>
    <div class="grid grid-2 mt-6" data-reveal-stagger>
      <div class="card"><h3>Where the roles actually are</h3><p class="mt-2">Which companies can
        legally pay someone across a border, and how to check in two minutes before you spend an
        hour applying.</p></div>
      <div class="card"><h3>Why silence is not feedback</h3><p class="mt-2">What the software
        screening your CV is looking for, and the four checks almost everybody fails.</p></div>
      <div class="card"><h3>Ten aimed beats fifty hopeful</h3><p class="mt-2">Why a big
        application count with no replies is evidence of a problem, not proof of trying.</p></div>
      <div class="card"><h3>The last twenty minutes</h3><p class="mt-2">The question that ends
        most remote interviews, and what to say when they ask your salary expectation.</p></div>
    </div>
    <p class="mt-6" data-reveal><b>The standing rule:</b> we teach for the hour and never sell
      during it. If you want a door afterwards, ask &mdash; and if you don&rsquo;t, the hour was
      still yours.</p>
  </div>
</section>
''',
}

TESTIMONIALS = {
    "key": "stories", "file": "testimonials.html", "prio": "0.8",
    "title": "Success Stories",
    "desc": "Nine documented journeys from ghosted applications to signed offers in USD, EUR "
            "and GBP — with the numbers, the timelines and the exact moves that changed.",
    "body": f'''<section class="section">
  <div class="wrap">
    <div style="max-width:var(--measure-text)" data-reveal>
      <p class="kicker">Documented results</p>
      <h1>Real people. Real offers. <span class="accent">Real dollars.</span></h1>
      <p class="lede mt-4">Nine journeys with the numbers attached. We publish the slow ones too
        &mdash; one of these took fourteen months &mdash; because the screenshots everywhere else
        teach people to quit at week six.</p>
    </div>

    <div class="grid grid-2 mt-6" data-reveal-stagger>
      {"".join(f"""
      <div class="quote">
        <div class="delta"><span class="was">{w}</span><span class="now">{n}</span></div>
        <blockquote>&ldquo;{q}&rdquo;</blockquote>
        <cite>{c}</cite>
      </div>""" for w, n, q, c in [
        ("&#8358;180,000/mo", "$2,100/mo",
         "Nobody asked about my degree. Every single person asked how I handle an angry customer at 11pm, and I had four years of answers.",
         "Ngozi &middot; 26 &middot; retail supervisor &rarr; remote customer success &middot; 6 weeks"),
        ("&#8358;7.2M/yr", "$71,000/yr",
         "Being 42 was not the obstacle I thought it was. Eleven years of closing books across three subsidiaries was the entire reason they wanted me.",
         "Uche &middot; 42 &middot; finance manager &middot; discreet search &middot; 11 weeks"),
        ("2 finals lost", "$46,800/yr",
         "I rewrote my CV four times for a problem that was never in my CV. The thing that was actually broken took two weeks of practice to fix.",
         "Tunde &middot; 30 &middot; data analyst &middot; the conversion leak"),
        ("312 applications", "Hired in 9 weeks",
         "I thought I wasn't good enough. I was applying to companies that had never paid anyone outside their own country, and nobody tells you that.",
         "Blessing &middot; NGO coordinator &rarr; project manager"),
        ("55 apps/month", "10 aimed/week",
         "Fewer applications. More interviews. The only thing that changed was where I was pointing.",
         "Marcus &middot; content strategist &middot; the aim leak"),
        ("14 months", "Offer letter signed",
         "It took longer than anyone promised. It still ended with an offer. I'm glad they published mine.",
         "Kemi &middot; teacher &rarr; technical writer"),
        ("Average interview", "+$14,000",
         "The email took twenty-five minutes. I was the only candidate still visibly thinking about their problem after the call ended.",
         "Taiwo &middot; UX designer &middot; the follow-up that paid"),
        ("&#8358;2.1M/yr", "$38,400/yr",
         "Ninety minutes a night after the children slept. That was the whole secret.",
         "Amara &middot; operations &middot; 27.8&times; on the year"),
        ("Effort, no aim", "Hired",
         "My problem was never effort. I had plenty of effort. I had no target.",
         "Chidi &middot; engineer &middot; the first story we ever published"),
      ])}
    </div>

    <p class="lede mt-6" data-reveal>Names are the students&rsquo; own or their chosen first name,
      published with permission. Figures are what they told us at the time of the offer.</p>
  </div>
</section>

<section class="section section--line">
  <div class="wrap center" data-reveal>
    <h2>Your story is the next one</h2>
    <div class="btns mt-5" style="justify-content:center">
      {btn("Find your leak &mdash; free", "diagnose.html")}
      {btn("See every option", "register.html", ghost=True)}
    </div>
  </div>
</section>
''',
}

BLOG = {
    "key": "blog", "file": "blog.html", "prio": "0.9", "freq": "daily",
    "title": "The Blog — practical remote-job help",
    "desc": "Practical remote-job help in plain English: scam checks, ATS CVs, interviews, "
            "timezones, getting paid across borders, and what the first thirty days of a "
            "remote role actually require.",
    "body": f'''<section class="section">
  <div class="wrap">
    <div style="max-width:var(--measure-text)" data-reveal>
      <p class="kicker">Free &middot; new posts weekly</p>
      <h1>Practical remote-job help, <span class="accent">in plain English.</span></h1>
      <p class="lede mt-4">No abstract essays and no motivation. Each post answers one question a
        real job seeker actually asked us, with something you can do the same evening.</p>
    </div>

    <h2 class="vh">Recent posts</h2>
    <div class="grid grid-3 mt-6" data-reveal-stagger>
      {"".join(f"""
      <article class="card">
        <div class="card-k">{cat}</div>
        <h3>{t}</h3>
        <p class="mt-2">{d}</p>
        <p class="mt-4">{tlink("Read it", WA_ASK, blank=True)}</p>
      </article>""" for cat, t, d in [
        ("Job Search", "Four questions that find your broken point",
         "Most stalled searches are not broken in four places. They are broken in one — and people spend months repairing the other three."),
        ("CV &amp; LinkedIn", "The six-second CV test",
         "Recruiters at remote-first companies do not read CVs. Software does, and it rejects most of them before a human looks."),
        ("Job Search", "The five-second scam check",
         "Five questions to ask any remote listing before you spend an hour on it. Screenshot it — it will save someone a month's salary."),
        ("Interviews", "The question nobody prepares for",
         "It is not technical. It is some version of 'how do you work when nobody is watching?' — and adjectives are the wrong answer."),
        ("Getting Paid", "Contractor, EOR, or neither",
         "The three kinds of company advertising remote roles, and why only one of them can actually hire you."),
        ("First 30 Days", "Getting hired is the first ladder",
         "The first thirty days of a remote role decide the next three years, and they are won by unglamorous things."),
      ])}
    </div>

    <p class="lede mt-6" data-reveal>Want a specific question answered?
      {tlink("Send it to us on WhatsApp", WA_ASK, blank=True)} &mdash; the best ones become posts.</p>
  </div>
</section>
''',
}

REGISTER = {
    "key": "register", "file": "register.html", "prio": "0.9",
    "title": "Register — every option and price",
    "desc": "Every option and price on one page: Mastery Training stages 1–4, Get A Remote Job, "
            "the Inner Circle residency and the private job board — with honest guidance on "
            "which one, or whether to pay at all yet.",
    "body": f'''<section class="section">
  <div class="wrap">
    <div style="max-width:var(--measure-text)" data-reveal>
      <p class="kicker">Start here</p>
      <h1>Which door <span class="accent">is mine?</span></h1>
      <p class="lede mt-4">Every option and every price, in public, on one page. Including the two
        honest answers most schools will not give you: <b>not yet</b>, and <b>not from us</b>.</p>
    </div>

    <h2 class="vh">Before you choose a door</h2>
    <div class="grid grid-2 mt-6" data-reveal-stagger>
      <div class="card"><div class="card-k">If you have no sellable skill yet</div>
        <h3>Don&rsquo;t buy a placement engine</h3>
        <p class="mt-2">A placement engine places a skill. If you do not have one an employer would
        pay for, it will waste your money and our promise. Build the skill first &mdash; we will
        tell you honestly where.</p>
        <p class="mt-4">{tlink("Ask us where to start", WA_ASK, blank=True)}</p></div>
      <div class="card"><div class="card-k">If money is tight this month</div>
        <h3>Don&rsquo;t borrow for this</h3>
        <p class="mt-2">Everything free on this site stays free and is genuinely useful. Work
        through it properly and you will arrive at the next intake ahead of where most people
        start.</p>
        <p class="mt-4">{tlink("Open the free stack", "free.html")}</p></div>
    </div>
  </div>
</section>

<section class="section section--line">
  <div class="wrap">
    <p class="kicker" data-reveal>The full ladder</p>
    <h2 data-reveal>Every price, <span class="accent">in public.</span></h2>

    <div class="rungs mt-6" data-reveal-stagger>
      <div class="rung"><div class="rung-n"></div><div>
        <h3>Single stages</h3>
        <p>Any one stage of the Mastery Training, taken on its own. The smallest honest entry
        point, and what you pay counts toward the bundle later.</p>
        <div class="rung-price">Stage 1 &#8358;70,000 &middot; Stage 2 &#8358;130,000 &middot;
          Stage 3 &#8358;70,000 &middot; Stage 4 &#8358;100,000</div></div></div>

      <div class="rung"><div class="rung-n"></div><div>
        <h3>Remote Job Mastery &mdash; Stages 1&ndash;4</h3>
        <p>All four stages, twenty training days, workbooks, LMS access and sixty days of the
        private job board.</p>
        <div class="rung-price">&#8358;250,000 &middot; saves &#8358;120,000 against
          &#8358;370,000 stage by stage</div>
        <p class="mt-4">{tlink("See the four stages", "mastery-training.html")}</p></div></div>

      <div class="rung"><div class="rung-n"></div><div>
        <h3>Get A Remote Job &mdash; Stage 5</h3>
        <p>The done-with-you placement engine. Starts the week you join, with no cohort to wait
        for, and does not stop until an offer letter lands.</p>
        <div class="rung-price">&#8358;150,000 once</div>
        <p class="mt-4">{tlink("See the placement engine", "get-a-remote-job.html")}</p></div></div>

      <div class="rung"><div class="rung-n"></div><div>
        <h3>Get Your Dream Job Offer &mdash; Stages 1&ndash;5</h3>
        <p>The whole path: every stage built by you, then the placement engine run with you.</p>
        <div class="rung-price">&#8358;500,000 &middot; from &#8358;740,000+ taken separately</div></div></div>

      <div class="rung"><div class="rung-n"></div><div>
        <h3>The Inner Circle</h3>
        <p>Application-first private residency. An advisor confirms fit before any payment is
        discussed.</p>
        <div class="rung-price">&#8358;250,000 / year &middot; or &#8358;135,000 &times; 2</div>
        <p class="mt-4">{tlink("See the residency", "inner-circle.html")}</p></div></div>

      <div class="rung"><div class="rung-n"></div><div>
        <h3>The Private Job Board</h3>
        <p>Sourcing done for you: verified, scam-filtered, cross-border-checked roles from
        platforms most seekers never monitor. Roughly six hours a week of work you stop doing.</p>
        <div class="rung-price">&#8358;50,000 / month &middot; starts the day you join</div></div></div>
    </div>

    <div class="card mt-6" data-reveal style="border-left:3px solid var(--accent)">
      <h3>Ready, or want to talk it through first?</h3>
      <p class="mt-2">Message us with where you are and what you can give this month. We will tell
        you which door fits &mdash; including if the answer is none of them yet.</p>
      <div class="btns mt-5">{btn("Message us on WhatsApp", WA_ASK, blank=True)}
        {btn("Find your leak first", "diagnose.html", ghost=True)}</div>
    </div>
  </div>
</section>
''',
}

NOTFOUND = {
    "key": "404", "file": "404.html", "noindex": True,
    "title": "Page not found — try one of these",
    "desc": "That page has moved on. Everything it used to hold is one link away.",
    "body": f'''<section class="section">
  <div class="wrap">
    <div style="max-width:var(--measure-text)" data-reveal>
      <div style="font-family:var(--font-display);font-size:var(--t-4xl);font-weight:800;
                  color:var(--accent);line-height:.9">404</div>
      <h1 class="mt-4">That page has moved on.<br><span class="accent">You don&rsquo;t have to.</span></h1>
      <p class="lede mt-4">The link you followed points at something we have renamed or retired.
        Nothing is lost &mdash; everything it used to hold is on one of these.</p>
    </div>
    <h2 class="vh">Where to go instead</h2>
    <div class="grid grid-3 mt-6" data-reveal-stagger>
      <a class="card" href="index.html"><h3>Home</h3><p class="mt-2">What we do and who it is for</p></a>
      <a class="card" href="diagnose.html"><h3>Find Your Leak</h3><p class="mt-2">Four questions, ninety seconds, free</p></a>
      <a class="card" href="free.html"><h3>Free For You</h3><p class="mt-2">CV scan, masterclass, blog, job board</p></a>
      <a class="card" href="starting-line.html"><h3>Your Starting Line</h3><p class="mt-2">The three routes, compared</p></a>
      <a class="card" href="register.html"><h3>Register</h3><p class="mt-2">Every option and price on one page</p></a>
      <a class="card" href="blog.html"><h3>The Blog</h3><p class="mt-2">Practical help, published weekly</p></a>
    </div>
    <p class="mt-6" data-reveal>Still stuck? {tlink("Message us and we will send the right link", WA_ASK, blank=True)}</p>
  </div>
</section>
''',
}


PAGES = [HOME, FREE, STARTING, DIAGNOSE, CVSCAN, MASTERY, GARJ, INNER,
         MASTERCLASS, TESTIMONIALS, BLOG, REGISTER, NOTFOUND]

if __name__ == "__main__":
    build(PAGES)
