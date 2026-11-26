#!/usr/bin/env python3
"""Static generator for Domain Marketing. Standard library only.

    python3 build/build.py

Reads data/*.json and the content modules, writes every HTML page plus
sitemap.xml, robots.txt, ads.txt, feed.xml and data/search.json into the repo root.
"""
import datetime
import json
import os
import sys
from email.utils import format_datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import layout as L  # noqa: E402
from content_guides import GUIDES, REVIEWED  # noqa: E402
from content_tools import TOOLS, HP  # noqa: E402
import content_pages as C  # noqa: E402

esc = L.esc
NOW = datetime.datetime.now(datetime.timezone.utc)
TODAY = NOW.strftime("%Y-%m-%d")
PAGES = []  # (path, title, desc, keywords)


def load(name, default):
    try:
        with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def emit(path, title, desc, body, *, keywords="", index=True, **kw):
    write(path, L.page(path, title, desc, body, **kw))
    if index:
        PAGES.append((path, title, desc, keywords))


def nice_date(iso):
    try:
        d = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return f"{d.strftime('%b')} {d.day}, {d.year}"
    except Exception:
        return ""


def short_date(iso):
    try:
        d = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return f"{d.strftime('%b')} {d.day}"
    except Exception:
        return ""


NEWS = load("news.json", {"items": [], "updated": ""})
VIDEOS = load("videos.json", {"library": [], "latest": [], "updated": ""})
VENUES = load("venues.json", {"venues": [], "read": ""})
STATS = load("stats.json", {"facts": [], "read": ""})
CONTESTS = load("contests.json", {"contests": [], "season_brief": ""})
UPDATED = nice_date(NEWS.get("updated") or NOW.isoformat()) or nice_date(NOW.isoformat())
VENUE_READ = nice_date(VENUES.get("read", "") + "T00:00:00+00:00")

PLAN_TOOL = {"slug": "plan", "title": "Marketing plan builder", "row": "What should I do with this name over the next thirty days?", "time": "1 minute"}


def venues_json(full=False):
    keep = ("id", "name", "modes", "best", "fees") if full else ("id", "name", "modes")
    data = [{k: v.get(k) for k in keep} for v in VENUES.get("venues", [])]
    return '<script type="application/json" id="venues-data">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def tool_rows(p, limit=None):
    rows = [f'<li><a class="row" href="{p}plan.html"><span class="row-t">{PLAN_TOOL["title"]}</span><span class="row-d">{PLAN_TOOL["row"]}</span><span class="row-m">{PLAN_TOOL["time"]}</span></a></li>']
    for t in TOOLS:
        rows.append(f'<li><a class="row" href="{p}tools/{t["slug"]}.html"><span class="row-t">{esc(t["title"])}</span><span class="row-d">{esc(t["row"])}</span><span class="row-m">{esc(t["time"])}</span></a></li>')
    return '<ul class="rows">' + "".join(rows[:limit] if limit else rows) + "</ul>"


def guide_rows(p, guides):
    return '<ul class="rows">' + "".join(
        f'<li><a class="row" href="{p}playbooks/{g["slug"]}.html"><span class="row-t">{esc(g["title"])}</span><span class="row-d">{esc(g["desc"])}</span><span class="row-m">{g["mins"]} min read</span></a></li>'
        for g in guides) + "</ul>"


def news_rows(items, limit=None, attrs=False):
    out = []
    for it in (items[:limit] if limit else items):
        cat = esc(it["s"].lower().replace(" ", "-").replace(".", ""))
        a = f' data-item data-cat="{cat}"' if attrs else ""
        out.append(
            f'<li{a}><a class="row" href="{esc(it["u"])}" target="_blank" rel="noopener nofollow"><span class="row-t">{esc(it["t"])}</span>'
            f'<span class="row-m">{esc(it["s"])}, {short_date(it.get("d", ""))}</span></a></li>')
    return '<ul class="rows news" id="news-list">' + "".join(out) + "</ul>"


def video_card(v, attrs=False):
    a = f' data-item data-cat="{esc(v.get("c", "latest"))}"' if attrs else ""
    meta = " ".join(x for x in [esc(v.get("ch", "")), short_date(v.get("d", ""))] if x)
    meta_html = f"<p>{meta}</p>" if meta else ""
    return (
        f'<article class="vid"{a}><button class="vid-frame" type="button" data-yt="{esc(v["id"])}" aria-label="Play: {esc(v["t"])}">'
        f'<img src="https://i.ytimg.com/vi/{esc(v["id"])}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="play">Play video</span></button>'
        f'<h3>{esc(v["t"])}</h3>{meta_html}</article>')


def faq_block(faq):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return f'<section class="faq"><h2>Questions people ask</h2>{items}</section>', schema


# --------------------------------------------------------------------------- home
def build_home():
    p = ""
    facts = "".join(
        f'<div><dt>{esc(f["k"])}</dt><dd>{esc(f["v"])}</dd><p class="src">{esc(f["x"])} Source: <a href="{esc(f["u"])}" target="_blank" rel="noopener nofollow">{esc(f["s"])}</a>.</p></div>'
        for f in STATS.get("facts", [])[:3])
    vids = "".join(video_card(v) for v in ((VIDEOS.get("latest") or [])[:2] + VIDEOS.get("library", []))[:4])
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>A domain name does not sell itself.</h1>
      <p class="lede">Parking income is gone. What is left is selling, and selling is a skill. Free tools and playbooks for pricing a name, pitching it, and closing safely. Start by scoring one.</p>
      <form id="hero-form" class="addr" autocomplete="off">
        <span class="scheme" aria-hidden="true">https://</span>
        <label class="sr" for="hero-input">Domain name</label>
        <input id="hero-input" type="text" inputmode="url" spellcheck="false" autocapitalize="none" placeholder="yourname.com" data-default="yourname.com">
        <button class="btn" type="submit">Score this name</button>
      </form>
      <div class="chips"><span>Or try:</span>
        <button class="chip" type="button" data-try="quotely.ai">quotely.ai</button>
        <button class="chip" type="button" data-try="solarledger.io">solarledger.io</button>
        <button class="chip" type="button" data-try="get-fresh-meals.com">get-fresh-meals.com</button>
      </div>
    </div>
    <div class="result" id="hero-out" aria-live="polite"><p class="out-empty">Your result appears here.</p></div>
  </div>
</section>

<section class="sec tight">
  <div class="wrap">
    <div class="sec-head"><h2>Nine free tools, one job: get the name sold</h2><p>Everything runs in your browser. Nothing you type is stored or sent unless you choose to send it.</p></div>
    {tool_rows(p)}
  </div>
</section>
{L.ad("top")}
<section class="sec wash">
  <div class="wrap split">
    <div class="daily" data-drills="{esc(json.dumps(C.DRILLS, ensure_ascii=False))}">
      <h2>Today’s ten-minute drill</h2>
      <h3 data-drill-t>{esc(C.DRILLS[0]["t"])}</h3>
      <p data-drill-d>{esc(C.DRILLS[0]["d"])}</p>
      <p><a class="btn sm" data-drill-a href="{C.DRILLS[0]["u"]}">{esc(C.DRILLS[0]["c"])}</a></p>
      <p class="small muted">A new drill every day. Small jobs, done daily, sell names.</p>
    </div>
    <div>
      <h2>The market in three numbers</h2>
      <dl class="facts">{facts}</dl>
      <p class="small"><a href="market.html">More numbers and today’s headlines</a></p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Playbooks</h2><p>Sourced, practical guides. Each one ends with the tool that does the job. <a href="playbooks.html">All {len(GUIDES)} playbooks</a></p></div>
    {guide_rows(p, GUIDES[:6])}
  </div>
</section>

<section class="sec wash" id="free-plan">
  <div class="wrap split wide-left">
    <div>
      <h2>Get a free marketing plan for your name</h2>
      <p class="lede">Answer three questions. The plan builder gives you a price mode and asking band, the venues that fit, what the for-sale page needs, and a thirty-day schedule. It appears on screen at once, and you can send it to us for a second opinion.</p>
      <ul>
        <li>Takes about a minute. No account.</li>
        <li>Uses published venue fees, with sources.</li>
        <li>A person reads every plan that is sent in.</li>
      </ul>
    </div>
    <form class="panel ink" action="plan.html" method="get">
      <div class="field"><label for="home-plan-domain">Which name are you selling?</label>
        <input id="home-plan-domain" name="domain" type="text" inputmode="url" spellcheck="false" autocapitalize="none" placeholder="yourname.com" required></div>
      <button class="btn tagbtn" type="submit">Start my free plan</button>
      <p class="form-note">Buying a name, or holding fifty or more? <a href="plan.html#other">There is a form for that too</a>.</p>
    </form>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div>
      <div class="sec-head"><h2>Market wire</h2><p>Headlines from the trade press, refreshed daily. <a href="market.html">Full wire</a></p></div>
      {news_rows(NEWS.get("items", []), 7)}
    </div>
    <div>
      <div class="sec-head"><h2>Watch and learn</h2><p><a href="videos.html">Whole video library</a></p></div>
      <div class="vgrid" style="grid-template-columns:repeat(auto-fill,minmax(210px,1fr))">{vids}</div>
    </div>
  </div>
</section>
{L.ad("inline")}
<section class="sec wash">
  <div class="wrap trio">
    <div>
      <h3>Contests and prizes</h3>
      <p>Three running contests: the 90-word pitch, the for-sale page of the season, and name-the-startup. Judged on skill, free to enter.</p>
      <p><a class="btn sm" href="contests.html">See the briefs and enter</a></p>
    </div>
    <div>
      <h3>Keep it free</h3>
      <p>Reader contributions pay for running costs, promotion, new writers and contest prizes.</p>
      <p><a class="btn sm ghost" href="support.html">Donate or sponsor</a></p>
    </div>
    <div>
      <h3>Work with us</h3>
      <p>Writers, a fee auditor, a video maker and a front-end developer.</p>
      <p><a class="btn sm ghost" href="careers.html">Open roles</a></p>
    </div>
  </div>
</section>
"""
    schema = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": L.SITE_NAME, "url": L.SITE_URL + "/", "description": L.TAGLINE},
        {"@context": "https://schema.org", "@type": "Organization", "name": L.SITE_NAME, "url": L.SITE_URL + "/", "logo": L.SITE_URL + "/assets/img/favicon.svg"},
    ]
    emit("index.html", "Domain Marketing: free tools and playbooks for selling domain names",
         "Score a domain, compare marketplace fees, build a for-sale page, write the outbound pitch and plan the sale. Free tools and sourced playbooks, refreshed daily.",
         body, schema=schema, scripts=("core", "tools"), updated=UPDATED, keywords="home sell domain tools")


# --------------------------------------------------------------------------- tools
def build_tools():
    body = f"""
<div class="wrap pagehead"><h1>Tools for selling a domain</h1>
<p class="lede">Each tool answers one question a seller actually has. They run in your browser, show their working, and label estimates as estimates.</p></div>
<section class="sec tight"><div class="wrap">{tool_rows("")}</div></section>
{L.ad("inline")}
<section class="sec tight"><div class="wrap prose">
<h2>Which tool first?</h2>
<p>If you have one name to sell, start with the <a href="plan.html">plan builder</a>: it uses the scorecard and the venue table to give you a price mode, a short list of venues and a thirty-day schedule. If you hold a portfolio, start with the <a href="tools/portfolio-math.html">portfolio calculator</a> and find your floor price before you spend time on any single name.</p>
<h2>How the numbers are made</h2>
<p>Fees come from each company’s published pages and carry a read date. Scores and price bands come from fixed rules that are listed on the tool’s own page. Nothing here uses private sales data, and nothing replaces checking real comparable sales before you fix a price.</p>
</div></section>"""
    emit("tools.html", "Free tools for selling domain names",
         "Nine free tools for domain sellers: name scorecard, net proceeds calculator, portfolio calculator, pitch writer, for-sale page builder, payment planner and more.",
         body, crumbs=[("", "Tools")], updated=UPDATED, keywords="calculator generator builder")

    for i, t in enumerate(TOOLS):
        faq_html, faq_schema = faq_block(t["faq"])
        others = [x for x in TOOLS if x["slug"] != t["slug"]]
        nxt = others[i % len(others)], others[(i + 3) % len(others)], others[(i + 5) % len(others)]
        more = "".join(f'<li><a class="row" href="{x["slug"]}.html"><span class="row-t">{esc(x["title"])}</span><span class="row-d">{esc(x["row"])}</span><span class="row-m">{esc(x["time"])}</span></a></li>' for x in nxt)
        needs_venues = t["slug"] == "net-proceeds"
        body = f"""
<div class="wrap pagehead"><h1>{esc(t["h1"])}</h1><p class="lede">{esc(t["lede"])}</p></div>
<section class="sec tight"><div class="wrap">
{t["ui"]}
{venues_json() if needs_venues else ""}
</div></section>
{L.ad("inline")}
<section class="sec tight"><div class="wrap article">
  <div class="prose">{t["how"]}{faq_html}</div>
  <aside><div class="toc"><h3>Next step</h3><p>Turn this result into a full plan: price mode, venues and a thirty-day schedule.</p><p><a class="btn sm" href="../plan.html">Build a marketing plan</a></p></div>{L.ad("side")}</aside>
</div></section>
<section class="sec tight wash"><div class="wrap"><div class="sec-head"><h2>More tools</h2><p><a href="../tools.html">All tools</a></p></div><ul class="rows">{more}</ul></div></section>"""
        app = {"@context": "https://schema.org", "@type": "WebApplication", "name": t["title"], "url": f'{L.SITE_URL}/tools/{t["slug"]}.html',
               "applicationCategory": "BusinessApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": t["desc"]}
        emit(f'tools/{t["slug"]}.html', t["h1"], t["desc"], body, crumbs=[("tools.html", "Tools"), ("", t["title"])],
             schema=[app, faq_schema], scripts=("core", "tools"), keywords=t["title"] + " " + t["row"])


# --------------------------------------------------------------------------- playbooks
def build_playbooks():
    body = f"""
<div class="wrap pagehead"><h1>Playbooks</h1>
<p class="lede">Practical guides to selling, pricing and buying domain names. Claims are sourced, fees are dated, and each guide ends with the tool that does the job.</p></div>
<section class="sec tight"><div class="wrap">{guide_rows("", GUIDES)}</div></section>
{L.ad("inline")}"""
    emit("playbooks.html", "Playbooks for selling domain names",
         "Twelve sourced guides: pricing with comparable sales, where to sell and what it costs, for-sale pages, outbound email, payment plans, escrow, brokers and portfolio math.",
         body, crumbs=[("", "Playbooks")], updated=UPDATED, keywords="guides how to learn")

    import re
    for i, g in enumerate(GUIDES):
        heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', g["body"])
        toc = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in heads)
        srcs = "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener nofollow">{esc(t)}</a></li>' for t, u in g["sources"])
        nxt = [GUIDES[(i + 1) % len(GUIDES)], GUIDES[(i + 2) % len(GUIDES)], GUIDES[(i + 5) % len(GUIDES)]]
        tool_href = "../" + g["tool"][0]
        body = f"""
<div class="wrap pagehead"><h1>{esc(g["title"])}</h1>
<p class="byline">{g["mins"]} minute read. Reviewed {REVIEWED}.</p></div>
<div class="wrap article">
  <article class="prose">
    {g["body"]}
    <div class="note"><p><strong>Do it now.</strong> <a href="{tool_href}">{esc(g["tool"][1])}</a>.</p></div>
    {L.ad("inline")}
    <h2 id="sources">Sources</h2>
    <ul class="sources">{srcs}</ul>
    <p class="small muted">General information for people selling domain names. It is not legal, tax or investment advice.</p>
  </article>
  <aside>
    <nav class="toc" aria-label="On this page"><h3>On this page</h3><ul>{toc}<li><a href="#sources">Sources</a></li></ul>
    <p style="margin-top:1rem"><a class="btn sm" href="{tool_href}">{esc(g["tool"][1])}</a></p></nav>
    {L.ad("side")}
  </aside>
</div>
<section class="sec tight wash" style="margin-top:3rem"><div class="wrap"><div class="sec-head"><h2>Keep reading</h2><p><a href="../playbooks.html">All playbooks</a></p></div>{guide_rows("../", nxt)}</div></section>"""
        art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
               "datePublished": "2026-11-26", "dateModified": "2026-11-26", "author": {"@type": "Organization", "name": L.SITE_NAME},
               "publisher": {"@type": "Organization", "name": L.SITE_NAME}, "mainEntityOfPage": f'{L.SITE_URL}/playbooks/{g["slug"]}.html'}
        emit(f'playbooks/{g["slug"]}.html', g["title"], g["desc"], body, crumbs=[("playbooks.html", "Playbooks"), ("", g["title"])],
             schema=art, keywords="playbook guide " + g["slug"].replace("-", " "))


# --------------------------------------------------------------------------- venues
def build_venues():
    rows = []
    for v in VENUES.get("venues", []):
        url = v["url"]
        link = f'<a href="{esc(url)}">{esc(v["source"])}</a>' if not url.startswith("http") else f'<a href="{esc(url)}" target="_blank" rel="noopener nofollow">{esc(v["source"])}</a>'
        rows.append(f"""<tr data-item><td><strong>{esc(v["name"])}</strong><br><span class="small muted">{esc(v["kind"])}</span></td>
<td>{esc(v["best"])}</td><td>{esc(v["fees"])}</td><td class="small">{link}</td></tr>""")
    body = f"""
<div class="wrap pagehead"><h1>Where to sell a domain</h1>
<p class="lede">{len(VENUES.get("venues", []))} routes to a sale, with what each is best at and the fees each company publishes. Read on {VENUE_READ}. Companies change their terms, so confirm before you list.</p></div>
<section class="sec tight"><div class="wrap">
  <div class="filterbar" data-filter="#venue-body"><label class="sr" for="venue-q">Filter venues</label><input id="venue-q" type="search" placeholder="Filter: broker, 10%, brandable…"><span class="muted small" data-count></span></div>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>Venue</th><th>Best for</th><th>Published fees</th><th>Source</th></tr></thead>
    <tbody id="venue-body">{"".join(rows)}</tbody>
  </table></div>
  <div class="btn-row" style="margin-top:1.5rem"><a class="btn" href="tools/net-proceeds.html">Compare what you keep at each venue</a><a class="btn ghost" href="playbooks/where-to-sell.html">How to choose a route</a></div>
</div></section>
{L.ad("inline")}
<section class="sec tight"><div class="wrap prose">
<h2>How this table is kept honest</h2>
<p>Every fee here was read on the company’s own public page. Where a company did not state a rate on the page we read, the table says so and the calculator leaves that venue out instead of guessing. We do not accept payment for inclusion, position or wording. If you represent a venue and a figure is wrong or out of date, <a href="contact.html">tell us</a> and point us to the page.</p>
<h2>A venue is missing</h2>
<p>The table covers the venues we have reviewed so far. Suggest another through the <a href="contact.html">contact form</a>; we add venues whose terms are public.</p>
</div></section>"""
    emit("venues.html", "Where to sell a domain: venues and fees compared",
         "Domain marketplaces, registrar marketplaces, brokers, escrow and financing compared: what each is best for and the commission each one publishes.",
         body, crumbs=[("", "Where to sell")], updated=UPDATED, keywords="marketplace commission fees sedo afternic broker escrow")


# --------------------------------------------------------------------------- market wire
def build_market():
    items = NEWS.get("items", [])
    sources = []
    for it in items:
        if it["s"] not in sources:
            sources.append(it["s"])
    chips = '<button class="chip" type="button" data-cat="" aria-pressed="true">All sources</button>' + "".join(
        f'<button class="chip" type="button" data-cat="{esc(s.lower().replace(" ", "-").replace(".", ""))}" aria-pressed="false">{esc(s)}</button>' for s in sources)
    facts = "".join(
        f'<div><dt>{esc(f["k"])}</dt><dd>{esc(f["v"])}</dd><p class="src">{esc(f["x"])} Source: <a href="{esc(f["u"])}" target="_blank" rel="noopener nofollow">{esc(f["s"])}</a>.</p></div>'
        for f in STATS.get("facts", []))
    body = f"""
<div class="wrap pagehead"><h1>Market wire</h1>
<p class="lede">Headlines from the domain trade press, gathered from publishers’ own feeds and refreshed every day. Each one opens the original article on the publisher’s site.</p></div>
<section class="sec tight"><div class="wrap split wide-left">
  <div>
    <div class="filterbar" data-filter="#news-list"><label class="sr" for="news-q">Search headlines</label><input id="news-q" type="search" placeholder="Search headlines">{chips}<span class="muted small" data-count></span></div>
    {news_rows(items, None, True) if items else '<p class="muted">The wire is refreshing. Check back shortly.</p>'}
    <p class="small muted" style="margin-top:1rem">Last refreshed {UPDATED}. We list the headline, the publisher and the date, and link to the source. We do not copy article text. <a href="feed.xml">Subscribe by RSS</a>.</p>
  </div>
  <aside>
    <h2>Reference numbers</h2>
    <dl class="facts">{facts}</dl>
    <p class="small muted">Reference numbers are reviewed by hand, not daily. Each shows its source.</p>
    {L.ad("side")}
  </aside>
</div></section>"""
    emit("market.html", "Domain market wire: today’s headlines and key numbers",
         "Daily headlines from the domain name trade press with links to the original articles, plus the reference numbers that matter to sellers.",
         body, crumbs=[("", "Market wire")], updated=UPDATED, keywords="news headlines sales registrations")


# --------------------------------------------------------------------------- videos
def build_videos():
    topics = [("", "All"), ("latest", "Latest"), ("basics", "Basics"), ("pricing", "Pricing"), ("selling", "Selling"), ("outbound", "Outbound"), ("landers", "For-sale pages"), ("portfolio", "Portfolio"), ("expired", "Expired names")]
    latest = [dict(v, c="latest") for v in (VIDEOS.get("latest") or [])]
    if not latest:
        topics = [t for t in topics if t[0] != "latest"]
    chips = "".join(f'<button class="chip" type="button" data-cat="{c}" aria-pressed="{"true" if not c else "false"}">{n}</button>' for c, n in topics)
    cards = "".join(video_card(v, True) for v in latest + VIDEOS.get("library", []))
    body = f"""
<div class="wrap pagehead"><h1>Video library</h1>
<p class="lede">Talks and walkthroughs on pricing, selling and buying domain names, picked from YouTube and sorted by the job they help with. Players load only when you press play.</p></div>
<section class="sec tight"><div class="wrap">
  <div class="filterbar" data-filter="#video-list"><label class="sr" for="video-q">Search videos</label><input id="video-q" type="search" placeholder="Search videos">{chips}<span class="muted small" data-count></span></div>
  <div class="vgrid" id="video-list">{cards}</div>
  <p class="small muted" style="margin-top:1.5rem">Last refreshed {UPDATED}. Videos belong to their creators and play from YouTube. A video being listed is not an endorsement of every claim in it; where a video and a playbook disagree on a fee, trust the dated source.</p>
</div></section>
{L.ad("inline")}"""
    emit("videos.html", "Video library: learn to price and sell domain names",
         "Curated YouTube talks and tutorials on domain pricing, selling, outbound, for-sale pages, portfolios and expired names, refreshed daily.",
         body, crumbs=[("", "Videos")], updated=UPDATED, keywords="youtube watch tutorial")


# --------------------------------------------------------------------------- glossary
def build_glossary():
    items = "".join(f'<div data-item style="padding:.9rem 0;border-bottom:1px solid var(--line)"><dt style="font:700 1.15rem/1.2 var(--display)">{esc(t)}</dt><dd style="margin:.3rem 0 0">{esc(d)}</dd></div>' for t, d in C.GLOSSARY)
    schema = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Domain marketing glossary",
              "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in C.GLOSSARY]}
    body = f"""
<div class="wrap pagehead"><h1>Glossary</h1><p class="lede">{len(C.GLOSSARY)} terms a domain seller meets, in plain words.</p></div>
<section class="sec tight"><div class="wrap prose">
  <div class="filterbar" data-filter="#gloss"><label class="sr" for="gloss-q">Search the glossary</label><input id="gloss-q" type="search" placeholder="Search terms"><span class="muted small" data-count></span></div>
  <dl id="gloss" style="border-top:2.5px solid var(--ink);margin:0">{items}</dl>
</div></section>"""
    emit("glossary.html", "Domain marketing glossary", "Plain-language definitions of the terms used in buying, pricing and selling domain names, from aftermarket to WHOIS.",
         body, crumbs=[("", "Glossary")], schema=schema, keywords="definitions terms meaning " + " ".join(t for t, _ in C.GLOSSARY))


# --------------------------------------------------------------------------- plan (lead funnel)
def build_plan():
    def radios(name, opts, default):
        return '<div class="opts">' + "".join(
            f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == default else ""}> {esc(t)}</label>' for v, t in opts) + "</div>"
    body = f"""
<div class="wrap pagehead"><h1>Build a free marketing plan for your domain</h1>
<p class="lede">Three questions, about a minute. You get a price mode and asking band, the venues that fit, what the for-sale page needs and a thirty-day schedule. Then, if you like, send it to us for a second opinion.</p>
<div class="chips" role="group" aria-label="What describes you">
  <button class="chip" type="button" data-role="seller" aria-pressed="true">I am selling a name</button>
  <button class="chip" type="button" data-role="portfolio" aria-pressed="false">I hold 50 or more names</button>
  <button class="chip" type="button" data-role="buyer" aria-pressed="false">I want to buy a name</button>
  <button class="chip" type="button" data-role="provider" aria-pressed="false">I offer a service to domain owners</button>
</div></div>

<section class="sec tight" data-role-panel="seller"><div class="wrap split wide-left">
  <div>
    <ol class="steps"><li>The name</li><li>Your goal</li><li>Your effort</li></ol>
    <form id="pl-form" class="panel ink" autocomplete="off" novalidate>
      <div data-step>
        <div class="field"><label for="pl-domain">Which domain are you selling?</label>
          <input id="pl-domain" type="text" inputmode="url" spellcheck="false" autocapitalize="none" placeholder="yourname.com">
          <span class="hint">One name. If you have several, start with the best.</span></div>
        <button class="btn" type="button" data-next>Next: your goal</button>
      </div>
      <div data-step hidden>
        <fieldset class="field"><legend>What matters most?</legend>{radios("goal", [("price", "The best price"), ("fast", "A fast sale"), ("lease", "Monthly income"), ("unsure", "Not sure yet")], "price")}</fieldset>
        <fieldset class="field"><legend>By when?</legend>{radios("when", [("30d", "Within 30 days"), ("3m", "About 3 months"), ("12m", "Within a year"), ("none", "No deadline")], "3m")}</fieldset>
        <div class="btn-row"><button class="btn ghost" type="button" data-back>Back</button><button class="btn" type="button" data-next>Next: your effort</button></div>
      </div>
      <div data-step hidden>
        <fieldset class="field"><legend>How much time will you put in?</legend>{radios("effort", [("none", "None. List it and wait"), ("hour", "An hour a week"), ("active", "I will do outreach")], "hour")}</fieldset>
        <div class="field"><label for="pl-floor">Lowest price you would accept (USD)</label><input id="pl-floor" type="number" min="0" step="50" inputmode="decimal" placeholder="Optional"><span class="hint">Stays in your browser unless you send the plan.</span></div>
        <div class="btn-row"><button class="btn ghost" type="button" data-back>Back</button><button class="btn tagbtn" type="submit">Build my plan</button></div>
      </div>
    </form>
    <div class="result" id="pl-out" hidden aria-live="polite"></div>

    <section id="pl-lead" class="panel" style="margin-top:1.5rem" hidden>
      <h2>Want a second opinion on this plan?</h2>
      <p>Send it to us. A person reads it and replies by email with what they would change: the price, the venue, or the first three companies to write to. It is free.</p>
      <form data-dm="Lead: marketing plan review" data-lead="1" novalidate>
        <div class="grid2">
          <div class="field"><label for="pll-name">Your name</label><input id="pll-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="pll-email">Email</label><input id="pll-email" name="email" type="email" autocomplete="email" required></div>
        </div>
        <div class="field"><label for="pll-domain">Domain</label><input id="pll-domain" name="domain" type="text" required></div>
        <div class="field"><label for="pll-q">What is your biggest question about selling it?</label><textarea id="pll-q" name="question" rows="3" placeholder="Optional, but it gets you a better answer"></textarea></div>
        <div class="field"><label for="pll-more">Other names you hold</label><input id="pll-more" name="other_names" type="text" placeholder="Optional: a few names or a rough count"></div>
        <input type="hidden" name="lead_type" value="seller-plan"><input type="hidden" name="plan_summary" value="">
        {HP}
        <button class="btn tagbtn" type="submit">Send my plan for review</button>
        <p class="form-note">We use your details to reply about this name. We never pass them on without asking you first. <a href="privacy.html">Privacy</a></p>
        <div class="form-done" role="status" hidden><strong>Plan sent.</strong> We reply by email. In the meantime, the first job on your list is the for-sale page: <a href="tools/lander-builder.html">build it now</a>.</div>
        <div class="form-fail" role="alert" hidden>That did not send. Check your connection and try again, or use the contact link at the top of this page.</div>
      </form>
    </section>
  </div>
  <aside>
    <div class="toc">
      <h3>What you get</h3>
      <ul>
        <li>A sales-readiness score and an asking band to test</li>
        <li>Fixed price or make-offer, with the reason</li>
        <li>Two or three venues with their published fees</li>
        <li>A for-sale page checklist</li>
        <li>An outreach plan, if you want one</li>
        <li>Four weeks of tasks</li>
      </ul>
      <p class="small muted">The plan is built in your browser from your answers and the structure of the name. It is a planning draft, not an appraisal.</p>
    </div>
    {L.ad("side")}
  </aside>
</div>
{venues_json(True)}
</section>

<section class="sec tight" data-role-panel="portfolio" id="other" hidden><div class="wrap prose">
  <h2>Portfolio review request</h2>
  <p>For holders of fifty or more names. Tell us the size and shape of the list and what you want from it. We reply with where we would start: what to cut, what to price, and which ten names deserve real marketing.</p>
  <form class="panel ink" data-dm="Lead: portfolio review" data-lead="1" novalidate>
    <div class="grid2">
      <div class="field"><label for="pf-name">Your name</label><input id="pf-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="pf-email">Email</label><input id="pf-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="pf-count">Names held</label><select id="pf-count" name="names_held"><option>50 to 200</option><option>200 to 1,000</option><option>1,000 to 5,000</option><option>More than 5,000</option></select></div>
      <div class="field"><label for="pf-goal">Main goal</label><select id="pf-goal" name="goal"><option>Raise sell-through</option><option>Cut renewal cost</option><option>Sell the whole portfolio</option><option>Find a broker or partner</option></select></div>
    </div>
    <div class="field"><label for="pf-best">Your five best names</label><textarea id="pf-best" name="best_names" rows="3" required></textarea></div>
    <div class="field"><label for="pf-note">Anything else we should know</label><textarea id="pf-note" name="note" rows="3"></textarea></div>
    <input type="hidden" name="lead_type" value="portfolio">{HP}
    <button class="btn tagbtn" type="submit">Request my portfolio review</button>
    <p class="form-note">We never pass your details on without asking you first.</p>
    <div class="form-done" role="status" hidden><strong>Request sent.</strong> We reply by email. While you wait, <a href="tools/portfolio-math.html">find your floor price</a>.</div>
    <div class="form-fail" role="alert" hidden>That did not send. Check your connection and try again, or use the contact link at the top of this page.</div>
  </form>
</div></section>

<section class="sec tight" data-role-panel="buyer" hidden><div class="wrap prose">
  <h2>Looking to buy a name</h2>
  <p>Tell us what you are naming and what you can spend. We reply with how we would approach it: whether the name you want is likely to be for sale, a realistic range, and whether a buyer’s broker is worth the fee.</p>
  <form class="panel ink" data-dm="Lead: buyer request" data-lead="1" novalidate>
    <div class="grid2">
      <div class="field"><label for="by-name">Your name</label><input id="by-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="by-email">Email</label><input id="by-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="field"><label for="by-want">The name you want, or the kind of name</label><input id="by-want" name="wanted" type="text" required placeholder="A specific domain, or a description of the business"></div>
    <div class="grid2">
      <div class="field"><label for="by-budget">Budget</label><select id="by-budget" name="budget"><option>Under $1,000</option><option>$1,000 to $5,000</option><option>$5,000 to $25,000</option><option>$25,000 to $100,000</option><option>Over $100,000</option></select></div>
      <div class="field"><label for="by-when">When do you need it?</label><select id="by-when" name="timeline"><option>This month</option><option>Within three months</option><option>No deadline</option></select></div>
    </div>
    <input type="hidden" name="lead_type" value="buyer">{HP}
    <button class="btn tagbtn" type="submit">Send my buying request</button>
    <p class="form-note">We never pass your details on without asking you first.</p>
    <div class="form-done" role="status" hidden><strong>Request sent.</strong> We reply by email. Meanwhile, see <a href="playbooks/price-a-domain.html">how sellers arrive at a price</a>.</div>
    <div class="form-fail" role="alert" hidden>That did not send. Check your connection and try again, or use the contact link at the top of this page.</div>
  </form>
</div></section>

<section class="sec tight" data-role-panel="provider" hidden><div class="wrap prose">
  <h2>Marketplaces, brokers, registrars and tool makers</h2>
  <p>If your service helps people sell or buy domain names, there are three ways to work with this site: sponsor a tool, a playbook or a contest prize; correct or add your published fees in the venue table, which is free; or propose a partnership.</p>
  <div class="btn-row"><a class="btn" data-contact href="#" rel="noopener">Open the partnership contact page</a><a class="btn ghost" href="partners.html">See what sponsorship includes</a></div>
</div></section>
"""
    emit("plan.html", "Free domain marketing plan builder",
         "Answer three questions and get a marketing plan for your domain: price mode, asking band, venues with fees, a for-sale page checklist and a thirty-day schedule.",
         body, crumbs=[("", "Marketing plan")], scripts=("core", "tools"), lead=False, keywords="lead plan sell my domain second opinion buyer portfolio review")


# --------------------------------------------------------------------------- support, contests, careers, partners
def build_support():
    uses = "".join(f"<li><strong>{esc(t)}.</strong> {esc(d)}</li>" for t, d in C.SUPPORT_USES)
    opts = "".join(f"<option>{esc(t)}</option>" for t, _ in C.SUPPORT_USES)
    body = f"""
<div class="wrap pagehead"><h1>Keep the tools free</h1>
<p class="lede">Domain Marketing has no paywall and takes no cut of your sale. Advertising covers part of the cost. Reader contributions and sponsors cover the rest.</p></div>
<section class="sec tight"><div class="wrap split wide-left">
  <div class="prose">
    <h2>Where contributions go</h2>
    <ul>{uses}</ul>
    <h2>How giving works</h2>
    <p>Fill in the pledge form. We email you a secure payment link for the amount you chose, and nothing is charged until you use it. You can direct the money to one of the four uses above or leave the choice to us.</p>
    <div class="note"><p>Domain Marketing is not a registered charity. Contributions are not tax-deductible and are not an investment; they are support for a free resource.</p></div>
    <h2>Other ways to help</h2>
    <ul>
      <li>Send a correction when a fee in the <a href="venues.html">venue table</a> changes.</li>
      <li>Enter a <a href="contests.html">contest</a>, or fund a prize.</li>
      <li>Share a tool with someone selling their first name.</li>
      <li>If you run a business in this industry, <a href="partners.html">sponsor a tool or a playbook</a>.</li>
    </ul>
  </div>
  <form class="panel ink" data-dm="Donation pledge" novalidate>
    <h2>Pledge a contribution</h2>
    <fieldset class="field"><legend>Amount (USD)</legend>
      <div class="opts">
        <label><input type="radio" name="amount" value="10"> $10</label>
        <label><input type="radio" name="amount" value="25" checked> $25</label>
        <label><input type="radio" name="amount" value="50"> $50</label>
        <label><input type="radio" name="amount" value="100"> $100</label>
        <label><input type="radio" name="amount" value="other"> Other</label>
      </div></fieldset>
    <div class="field"><label for="dn-other">Other amount</label><input id="dn-other" name="other_amount" type="number" min="1" step="1" inputmode="decimal" placeholder="Only if you chose Other"></div>
    <fieldset class="field"><legend>How often</legend><div class="opts"><label><input type="radio" name="frequency" value="once" checked> Once</label><label><input type="radio" name="frequency" value="monthly"> Monthly</label></div></fieldset>
    <div class="field"><label for="dn-use">Put it towards</label><select id="dn-use" name="direct_to"><option>Wherever it is needed most</option>{opts}</select></div>
    <div class="grid2">
      <div class="field"><label for="dn-name">Your name</label><input id="dn-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="dn-email">Email for the payment link</label><input id="dn-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="field"><label for="dn-msg">Message</label><textarea id="dn-msg" name="message" rows="2" placeholder="Optional"></textarea></div>
    {HP}
    <button class="btn tagbtn" type="submit">Send my pledge</button>
    <p class="form-note">No payment is taken on this page.</p>
    <div class="form-done" role="status" hidden><strong>Pledge received. Thank you.</strong> We will email you a secure payment link.</div>
    <div class="form-fail" role="alert" hidden>That did not send. Check your connection and try again, or use the contact link at the top of this page.</div>
  </form>
</div></section>"""
    emit("support.html", "Donate or sponsor", "Support a free, independent toolkit for domain sellers. Contributions fund running costs, promotion, new writers and contest prizes.",
         body, crumbs=[("", "Donate or sponsor")], lead=False, keywords="donation support contribute pledge")


def build_contests():
    today = NOW.date().isoformat()
    cards, opts = [], []
    for c in CONTESTS.get("contests", []):
        open_ = c.get("closes", "9999") >= today
        status = f'Entries close {nice_date(c["closes"] + "T00:00:00+00:00")}' if open_ else "Closed. The next round opens soon"
        cards.append(f"""<li><div class="row" style="grid-template-columns:minmax(0,16rem) minmax(0,1fr)"><span class="row-t">{esc(c["name"])}<br><span class="pill" style="margin-top:.5rem">{esc(status)}</span></span>
<span><strong>The brief.</strong> {esc(c["brief"])}<br><strong>Judged on.</strong> {esc(c["judged"])}<br><strong>The prize.</strong> {esc(c["prize"])}</span></div></li>""")
        if open_:
            opts.append(f'<option value="{esc(c["id"])}">{esc(c["name"])}</option>')
    brief = CONTESTS.get("season_brief", "")
    body = f"""
<div class="wrap pagehead"><h1>Contests and prizes</h1>
<p class="lede">Three contests that reward the skills this site teaches. Free to enter, judged on skill, and the best entries are published so everyone learns from them.</p></div>
<section class="sec tight"><div class="wrap"><ul class="rows">{"".join(cards)}</ul>
<div class="note" style="max-width:44rem"><p><strong>This season’s startup to name:</strong> {esc(brief)}</p></div></div></section>
{L.ad("inline")}
<section class="sec tight wash"><div class="wrap split">
  <form class="panel ink" data-dm="Contest entry" novalidate>
    <h2>Enter</h2>
    <div class="field"><label for="ct-which">Contest</label><select id="ct-which" name="contest">{"".join(opts) or "<option>Next round</option>"}</select></div>
    <div class="grid2">
      <div class="field"><label for="ct-name">Name to credit</label><input id="ct-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="ct-email">Email</label><input id="ct-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="field"><label for="ct-entry">Your entry</label><textarea id="ct-entry" name="entry" rows="7" required placeholder="Paste the email, the address of your for-sale page, or the name and your one-sentence reason"></textarea></div>
    <div class="field"><label><input type="checkbox" name="rules" value="accepted" required> I have read the rules and this entry is my own work.</label></div>
    {HP}
    <button class="btn tagbtn" type="submit">Submit my entry</button>
    <div class="form-done" role="status" hidden><strong>Entry received.</strong> Results are published on this page after the closing date, and winners are told by email.</div>
    <div class="form-fail" role="alert" hidden>That did not send. Check your connection and try again, or use the contact link at the top of this page.</div>
  </form>
  <div class="prose">
    <h2>Rules</h2>
    <ol>
      <li>Entry is free. No purchase or contribution is needed, and making one does not improve your chances.</li>
      <li>One entry per person per contest per round. Entries must be your own work.</li>
      <li>These are contests of skill. Entries are judged by the editors against the criteria stated for each contest. The judges’ decision is final.</li>
      <li>Entries that use another party’s trademark, make false claims or contain unlawful content are disqualified.</li>
      <li>You keep ownership of your entry and allow us to publish it on this site with credit.</li>
      <li>Non-cash prizes are as described. A cash prize applies only where one has been announced on this page before the closing date. Winners are responsible for any tax on a prize.</li>
      <li>Open to adults wherever such contests are lawful. Void where prohibited.</li>
      <li>We use your email only to run the contest and contact winners.</li>
    </ol>
    <h2>Fund a prize</h2>
    <p>A sponsor can put a cash prize behind any contest and is named beside it. <a href="partners.html">How sponsorship works</a>.</p>
  </div>
</div></section>"""
    emit("contests.html", "Contests and prizes", "Free, skill-judged contests for domain sellers: the 90-word pitch, the for-sale page of the season and name-the-startup.",
         body, crumbs=[("", "Contests")], lead=False, keywords="contest prize competition win")


def build_careers():
    rows = "".join(f'<li><div class="row" style="grid-template-columns:minmax(0,16rem) minmax(0,1fr)"><span class="row-t">{esc(t)}</span><span class="row-d">{esc(d)}</span></div></li>' for t, d in C.ROLES)
    opts = "".join(f"<option>{esc(t)}</option>" for t, _ in C.ROLES)
    body = f"""
<div class="wrap pagehead"><h1>Work with us</h1>
<p class="lede">Domain Marketing is built by a small team and a circle of contributors. Work is remote and by assignment. Paid assignments open as advertising, sponsorship and contributions fund them, and we tell you which kind an assignment is before you start.</p></div>
<section class="sec tight"><div class="wrap"><ul class="rows">{rows}</ul></div></section>
<section class="sec tight wash"><div class="wrap split">
  <div class="prose">
    <h2>What we look for</h2>
    <ul>
      <li>You check facts and link to the source.</li>
      <li>You write the way you would explain something to a friend who runs a small business.</li>
      <li>You have done the thing you want to write or build about.</li>
    </ul>
    <h2>How it works</h2>
    <ol>
      <li>Send the form with a link to something you have made.</li>
      <li>If there is a fit, we reply with one specific assignment, its scope and its terms.</li>
      <li>Your work is published with your name on it.</li>
    </ol>
  </div>
  <form class="panel ink" data-dm="Careers application" novalidate>
    <h2>Apply</h2>
    <div class="field"><label for="cr-role">Role</label><select id="cr-role" name="role">{opts}<option>Something else</option></select></div>
    <div class="grid2">
      <div class="field"><label for="cr-name">Your name</label><input id="cr-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="cr-email">Email</label><input id="cr-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="field"><label for="cr-link">A link to your work</label><input id="cr-link" name="work_link" type="url" placeholder="https://" required></div>
    <div class="field"><label for="cr-note">Why this role, in a few lines</label><textarea id="cr-note" name="note" rows="4" required></textarea></div>
    {HP}
    <button class="btn tagbtn" type="submit">Send my application</button>
    <div class="form-done" role="status" hidden><strong>Application sent.</strong> We reply by email when there is an assignment that fits.</div>
    <div class="form-fail" role="alert" hidden>That did not send. Check your connection and try again, or use the contact link at the top of this page.</div>
  </form>
</div></section>"""
    emit("careers.html", "Work with us", "Open roles for writers, a fee auditor, a video maker, a front-end developer and a partnerships lead at Domain Marketing. Remote, by assignment.",
         body, crumbs=[("", "Work with us")], lead=False, keywords="jobs careers hiring talent contributor writer")


def build_partners():
    body = f"""
<div class="wrap pagehead"><h1>Advertise, sponsor or partner</h1>
<p class="lede">The people who use this site are in the middle of selling or buying a domain name. If your service helps them do that, here is how to reach them.</p></div>
<section class="sec tight"><div class="wrap split wide-left">
  <div class="prose">
    <h2>What you can sponsor</h2>
    <ul class="rows" style="padding:0">
      <li><div class="row" style="grid-template-columns:minmax(0,14rem) minmax(0,1fr)"><span class="row-t">A tool</span><span class="row-d">Your name beside one calculator or builder, labelled as its sponsor, for a season.</span></div></li>
      <li><div class="row" style="grid-template-columns:minmax(0,14rem) minmax(0,1fr)"><span class="row-t">A playbook</span><span class="row-d">A labelled sponsor line on one guide. You do not see or change the text.</span></div></li>
      <li><div class="row" style="grid-template-columns:minmax(0,14rem) minmax(0,1fr)"><span class="row-t">A contest prize</span><span class="row-d">You fund the cash prize and are named as its sponsor on the contest and the results.</span></div></li>
      <li><div class="row" style="grid-template-columns:minmax(0,14rem) minmax(0,1fr)"><span class="row-t">The market wire</span><span class="row-d">A labelled sponsor line above the daily headlines.</span></div></li>
    </ul>
    <h2>What sponsorship does not buy</h2>
    <p>Inclusion, position or wording in the venue table and the calculator; a say in what a playbook recommends; or readers’ contact details. Those rules are why the audience trusts the site, which is what makes a placement here worth having.</p>
    <h2>Partnerships and acquisitions</h2>
    <p>For partnership proposals, bulk advertising, or interest in acquiring this website or its domain name, use the partnership contact page. It is the same link shown at the top of every page.</p>
    <p><a class="btn" data-contact href="#" rel="noopener">Open the partnership contact page</a></p>
  </div>
  <form class="panel ink" data-dm="Partnership inquiry" novalidate>
    <h2>Or send a short note</h2>
    <div class="grid2">
      <div class="field"><label for="pt-name">Your name</label><input id="pt-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="pt-email">Work email</label><input id="pt-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="field"><label for="pt-co">Company</label><input id="pt-co" name="company" type="text" autocomplete="organization" required></div>
    <div class="field"><label for="pt-kind">I am interested in</label><select id="pt-kind" name="interest"><option>Sponsoring a tool</option><option>Sponsoring a playbook</option><option>Funding a contest prize</option><option>Advertising</option><option>A partnership</option><option>This website or domain name</option></select></div>
    <div class="field"><label for="pt-note">Details</label><textarea id="pt-note" name="details" rows="4" required></textarea></div>
    {HP}
    <button class="btn tagbtn" type="submit">Send my inquiry</button>
    <div class="form-done" role="status" hidden><strong>Inquiry sent.</strong> We reply by email.</div>
    <div class="form-fail" role="alert" hidden>That did not send. Check your connection and try again, or use the contact link at the top of this page.</div>
  </form>
</div></section>"""
    emit("partners.html", "Advertise, sponsor or partner", "Sponsor a tool, a playbook, a contest prize or the market wire on Domain Marketing, or propose a partnership.",
         body, crumbs=[("", "Advertise and partner")], lead=False, keywords="sponsorship advertising partnership advertise")


# --------------------------------------------------------------------------- fixed pages
def build_fixed():
    emit("about.html", "About Domain Marketing", "Who makes Domain Marketing, how the tools and fee tables are built, and how the site is funded.",
         f'<div class="wrap pagehead"><h1>About Domain Marketing</h1><p class="lede">A free, independent toolkit for people selling domain names.</p></div><section class="sec tight"><div class="wrap prose">{C.ABOUT}</div></section>',
         crumbs=[("", "About")], keywords="about who we are method")

    contact = f"""
<div class="wrap pagehead"><h1>Contact</h1><p class="lede">Questions, corrections, and anything about your own names. A person reads every message.</p></div>
<section class="sec tight"><div class="wrap split">
  <form class="panel ink" data-dm="Contact form" novalidate>
    <div class="grid2">
      <div class="field"><label for="cn-name">Your name</label><input id="cn-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="cn-email">Email</label><input id="cn-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="field"><label for="cn-topic">About</label><select id="cn-topic" name="topic"><option>A question about selling a name</option><option>A correction to a fee or a fact</option><option>A venue to add</option><option>A trademark or copyright concern</option><option>A privacy request</option><option>Something else</option></select></div>
    <div class="field"><label for="cn-msg">Message</label><textarea id="cn-msg" name="message" rows="6" required></textarea></div>
    {HP}
    <button class="btn tagbtn" type="submit">Send my message</button>
    <div class="form-done" role="status" hidden><strong>Message sent.</strong> We reply by email.</div>
    <div class="form-fail" role="alert" hidden>That did not send. Check your connection and try again, or use the contact link at the top of this page.</div>
  </form>
  <div class="prose">
    <h2>Sponsorship, advertising, partnership</h2>
    <p>For those, and for interest in this website or its domain name, use the partnership contact page.</p>
    <p><a class="btn ghost" data-contact href="#" rel="noopener">Open the partnership contact page</a></p>
    <h2>Selling a name?</h2>
    <p>You will get a faster and fuller answer from the <a href="plan.html">plan builder</a>, which sends us the details we would otherwise have to ask you for.</p>
  </div>
</div></section>"""
    emit("contact.html", "Contact", "Contact the Domain Marketing team with questions, corrections, venue suggestions or privacy requests.", contact,
         crumbs=[("", "Contact")], lead=False, keywords="contact email message")

    for path, title, desc, text, crumb in [
        ("privacy.html", "Privacy and cookies", "How Domain Marketing handles forms, cookies, Google AdSense advertising and what is stored in your browser.", C.PRIVACY, "Privacy and cookies"),
        ("terms.html", "Terms of use", "The terms for using Domain Marketing’s tools and content, including the limits of estimates and third-party fee information.", C.TERMS, "Terms of use"),
        ("disclaimer.html", "Trademark and copyright disclosure", "Domain Marketing is independent. How the site uses its descriptive name, other companies’ trademarks, headlines and video.", C.DISCLAIMER, "Trademark and copyright disclosure"),
    ]:
        emit(path, title, desc,
             f'<div class="wrap pagehead"><h1>{esc(title)}</h1><p class="byline">Last updated {REVIEWED}.</p></div><section class="sec tight"><div class="wrap prose">{text}</div></section>',
             crumbs=[("", crumb)], lead=False, keywords="legal policy")

    nf = f"""
<div class="wrap pagehead"><h1>That page is not here.</h1><p class="lede">The address may have changed. These will get you back on track.</p>
<div class="btn-row"><a class="btn" href="{L.SITE_URL}/">Go to the home page</a><a class="btn ghost" href="{L.SITE_URL}/tools.html">Browse the tools</a></div></div>"""
    # 404 is served from any depth, so it uses absolute asset URLs.
    html = L.page("404.html", "Page not found", "This page could not be found.", nf, lead=False, noindex=True)
    for a in ('href="assets/', 'src="assets/'):
        html = html.replace(a, a.replace("assets/", L.SITE_URL + "/assets/"))
    html = html.replace('data-root=""', f'data-root="{L.SITE_URL}/"')
    import re
    html = re.sub(r'href="((?!https?:|#|mailto:)[a-z][^"]*\.(?:html|xml))"', lambda m: f'href="{L.SITE_URL}/{m.group(1)}"', html)
    write("404.html", html)


# --------------------------------------------------------------------------- machine files
def build_machine():
    urls = "".join(
        f"<url><loc>{L.SITE_URL}/{'' if p == 'index.html' else p}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>{'daily' if p in ('index.html', 'market.html', 'videos.html') else 'monthly'}</changefreq></url>" for p, *_ in PAGES)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {L.SITE_URL}/sitemap.xml\n")
    write("ads.txt", f"google.com, {L.ADS_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")
    search = [{"t": t, "u": p, "d": d, "k": k} for p, t, d, k in PAGES]
    write("data/search.json", json.dumps(search, ensure_ascii=False))
    items = []
    for it in NEWS.get("items", [])[:40]:
        try:
            d = format_datetime(datetime.datetime.fromisoformat(it["d"].replace("Z", "+00:00")))
        except Exception:
            d = format_datetime(NOW)
        items.append(f"<item><title>{esc(it['t'])}</title><link>{esc(it['u'])}</link><guid isPermaLink=\"true\">{esc(it['u'])}</guid><pubDate>{d}</pubDate><source url=\"{esc(it['u'])}\">{esc(it['s'])}</source></item>")
    write("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{L.SITE_NAME} market wire</title><link>{L.SITE_URL}/market.html</link>'
          f"<description>Daily headlines from the domain name trade press, linked to their sources.</description><lastBuildDate>{format_datetime(NOW)}</lastBuildDate>{''.join(items)}</channel></rss>\n")
    write(".nojekyll", "")
    write("assets/img/favicon.svg", L.LOGO.replace('class="logo-mark" ', 'xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', ""))


def main():
    build_home()
    build_tools()
    build_playbooks()
    build_venues()
    build_market()
    build_videos()
    build_glossary()
    build_plan()
    build_support()
    build_contests()
    build_careers()
    build_partners()
    build_fixed()
    build_machine()
    print(f"Built {len(PAGES)} indexed pages + 404 ({TODAY}). News: {len(NEWS.get('items', []))}, videos: {len(VIDEOS.get('library', [])) + len(VIDEOS.get('latest') or [])}.")


if __name__ == "__main__":
    main()
