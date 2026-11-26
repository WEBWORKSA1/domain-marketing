"""Shared page shell for Domain Marketing: head, ribbon, header, footer, lead strip, ad slots.

Every page is written relative-path safe, so the site works both at
https://<user>.github.io/<repo>/ and at the root of a custom domain.
"""
import html
import json

SITE_NAME = "Domain Marketing"
# When the custom domain is attached: add a CNAME file, change SITE_URL, rebuild, push.
SITE_URL = "https://webworksa1.github.io/domain-marketing"
TAGLINE = "Free tools and playbooks for selling domain names"
ADS_CLIENT = "ca-pub-6620975821265271"
# Optional manual ad units. Leave a slot empty to rely on AdSense Auto ads for that position.
ADS_SLOTS = {"top": "", "inline": "", "side": "", "foot": ""}

NAV = [
    ("tools.html", "Tools"),
    ("playbooks.html", "Playbooks"),
    ("venues.html", "Where to sell"),
    ("market.html", "Market wire"),
    ("videos.html", "Videos"),
]

FOOT = [
    ("Sell a name", [
        ("plan.html", "Build a marketing plan"),
        ("tools/name-score.html", "Score a name"),
        ("tools/net-proceeds.html", "Compare venue fees"),
        ("tools/lander-builder.html", "Build a for-sale page"),
        ("tools/pitch-writer.html", "Write an outbound pitch"),
        ("venues.html", "Where to sell"),
    ]),
    ("Learn", [
        ("playbooks.html", "Playbooks"),
        ("glossary.html", "Glossary"),
        ("videos.html", "Video library"),
        ("market.html", "Market wire"),
        ("tools.html", "All tools"),
    ]),
    ("Take part", [
        ("contests.html", "Contests and prizes"),
        ("support.html", "Donate or sponsor"),
        ("careers.html", "Work with us"),
        ("partners.html", "Advertise and partner"),
    ]),
    ("Site", [
        ("about.html", "About"),
        ("contact.html", "Contact"),
        ("privacy.html", "Privacy and cookies"),
        ("terms.html", "Terms of use"),
        ("disclaimer.html", "Trademark and copyright disclosure"),
    ]),
]


def esc(s):
    return html.escape(str(s), quote=True)


def prefix_for(path):
    depth = path.count("/")
    return "../" * depth


def ad(position):
    """Manual ad unit, rendered only when a slot id is configured (otherwise Auto ads decide)."""
    slot = ADS_SLOTS.get(position, "")
    if not slot:
        return ""
    return (
        '<aside class="ad" aria-label="Advertisement"><span class="ad-l">Advertisement</span>'
        f'<ins class="adsbygoogle" style="display:block" data-ad-client="{ADS_CLIENT}" data-ad-slot="{slot}" '
        'data-ad-format="auto" data-full-width-responsive="true"></ins>'
        "<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></aside>"
    )


LOGO = (
    '<svg class="logo-mark" viewBox="0 0 44 44" aria-hidden="true">'
    '<path d="M13 6h25a4 4 0 0 1 4 4v24a4 4 0 0 1-4 4H13L2 22z" fill="#FFCF24"/>'
    '<circle cx="12.5" cy="22" r="3.4" fill="#0E1230"/>'
    '<circle cx="24" cy="27.5" r="2.6" fill="#2337E8"/>'
    '<path d="M29 16.5v11M34 20v7.5" stroke="#0E1230" stroke-width="3.2" stroke-linecap="round"/></svg>'
)


def lead_strip(prefix, context="page"):
    return f"""
<section class="leadstrip" aria-labelledby="ls-h">
  <div class="wrap leadstrip-in">
    <div>
      <h2 id="ls-h">Selling a name? Get a second opinion on price and venue.</h2>
      <p>Send the domain and where you want it to end up. It is free, and a person reads every request.</p>
    </div>
    <form class="quick" data-dm="Lead: quick second opinion" data-lead="1" novalidate>
      <label class="sr" for="ls-domain">Domain name</label>
      <input id="ls-domain" name="domain" type="text" inputmode="url" autocomplete="off" placeholder="yourname.com" required>
      <label class="sr" for="ls-email">Your email</label>
      <input id="ls-email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required>
      <input type="hidden" name="lead_type" value="seller-quick">
      <input type="hidden" name="context" value="{esc(context)}">
      <div class="hp" aria-hidden="true"><label>Leave this empty <input name="company_site" tabindex="-1" autocomplete="off"></label></div>
      <button class="btn tagbtn" type="submit">Request my second opinion</button>
      <p class="form-note">No spam, no list rental. <a href="{prefix}plan.html">Add details with the plan builder</a> if you want a fuller answer.</p>
      <div class="form-done" role="status" hidden>
        <strong>Request sent.</strong> We reply by email. Want an instant draft while you wait? <a href="{prefix}plan.html">Build your plan now</a>.
      </div>
      <div class="form-fail" role="alert" hidden>That did not send. Check your connection and try again, or use the contact link at the top of this page.</div>
    </form>
  </div>
</section>"""


def page(path, title, desc, body, *, crumbs=None, schema=None, scripts=("core",), lead=True,
         updated="", noindex=False, body_class=""):
    p = prefix_for(path)
    canonical = SITE_URL + "/" + ("" if path == "index.html" else path)
    full_title = title if path == "index.html" else f"{title} | {SITE_NAME}"
    nav_parts = []
    for href, label in NAV:
        here = path == href or path.startswith(href.split(".")[0] + "/")
        cur = ' aria-current="page"' if here else ""
        nav_parts.append(f'<a href="{p}{href}"{cur}>{label}</a>')
    nav = "".join(nav_parts)
    foot_cols = "".join(
        "<div><h3>" + esc(h) + "</h3><ul>" + "".join(f'<li><a href="{p}{u}">{esc(t)}</a></li>' for u, t in links) + "</ul></div>"
        for h, links in FOOT
    )
    crumb_html = ""
    ld = []
    if crumbs:
        parts = [f'<a href="{p}index.html">Home</a>']
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
        for i, (u, t) in enumerate(crumbs, start=2):
            if u:
                parts.append(f'<a href="{p}{u}">{esc(t)}</a>')
                items.append({"@type": "ListItem", "position": i, "name": t, "item": SITE_URL + "/" + u})
            else:
                parts.append(f'<span aria-current="page">{esc(t)}</span>')
                items.append({"@type": "ListItem", "position": i, "name": t, "item": canonical})
        crumb_html = '<nav class="crumbs wrap" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">/</span>'.join(parts) + "</nav>"
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if schema:
        ld.extend(schema if isinstance(schema, list) else [schema])
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    script_html = "".join(f'<script src="{p}assets/js/{s}.js" defer></script>' for s in scripts)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    stamp = f'<p class="stamp">Content refreshed {esc(updated)}.</p>' if updated else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2337E8">
<meta name="google-adsense-account" content="{ADS_CLIENT}">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{p}assets/fonts/bricolage-grotesque-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/instrument-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/site.css">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME} market wire" href="{p}feed.xml">
<script>(function(){{try{{var t=localStorage.getItem("dm:theme");if(t)document.documentElement.setAttribute("data-theme",JSON.parse(t));var c=localStorage.getItem("dm:consent");if(c&&JSON.parse(c)==="essential"){{(window.adsbygoogle=window.adsbygoogle||[]).requestNonPersonalizedAds=1;}}}}catch(e){{}}}})();</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS_CLIENT}" crossorigin="anonymous"></script>
{ld_html}
</head>
<body class="{esc(body_class)}" data-root="{p}">
<a class="skip" href="#main">Skip to content</a>
<div class="ribbon"><a data-contact href="#" rel="noopener">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership</a></div>
<header class="hdr">
  <div class="wrap hdr-in">
    <a class="logo" href="{p}index.html" aria-label="{SITE_NAME} home">{LOGO}<span>Domain Marketing</span></a>
    <nav class="nav" id="nav" aria-label="Main">{nav}</nav>
    <div class="hdr-act">
      <button class="icon-btn" type="button" data-search-open aria-label="Search the site"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg></button>
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch between light and dark"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.6 6.6 0 0 0 9.8 9.8z"/></svg></button>
      <a class="btn sm hdr-cta" href="{p}plan.html">Get a free plan</a>
      <button class="icon-btn menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
</header>
{crumb_html}
<main id="main">
{body}
</main>
{lead_strip(p, path) if lead else ""}
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-top">
      <div class="ftr-brand">
        <a class="logo" href="{p}index.html">{LOGO}<span>Domain Marketing</span></a>
        <p>{TAGLINE}. Independent, reader-supported, and free to use.</p>
        <p><a class="btn sm ghost" data-contact href="#" rel="noopener">Contact the team</a></p>
      </div>
      <div class="ftr-cols">{foot_cols}</div>
    </div>
    <div class="ftr-legal">
      <p><strong>Disclosure.</strong> “Domain Marketing” is used here as a plain descriptive phrase for the practice of marketing domain names. This site is independent and is not affiliated with, endorsed by or sponsored by any registrar, registry, marketplace, broker or similarly named business. Company and product names are the trademarks of their owners and appear only to identify the services discussed. <a href="{p}disclaimer.html">Full trademark and copyright disclosure</a>.</p>
      <p>Tools give rule-of-thumb estimates for planning. They are not appraisals, and nothing here is legal, tax or investment advice. This site shows ads from Google AdSense. <a href="{p}privacy.html#cookies">How ads and cookies work here</a>.</p>
      {stamp}
      <p>© <span data-year>2026</span> Domain Marketing. Original text may be quoted with a link back.</p>
    </div>
  </div>
</footer>
<div class="search" id="search" role="dialog" aria-modal="true" aria-label="Search" hidden>
  <div class="search-box">
    <label class="sr" for="search-q">Search tools, playbooks and pages</label>
    <input id="search-q" type="search" placeholder="Search tools, playbooks and pages" autocomplete="off">
    <button class="icon-btn" type="button" data-search-close aria-label="Close search">✕</button>
    <ul class="search-res" id="search-res"></ul>
  </div>
</div>
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie choices" hidden>
  <p><strong>Cookies and ads.</strong> This site uses cookies for basic functions and for Google AdSense, which may personalise ads. Choose “Essential only” for non-personalised ads. <a href="{p}privacy.html#cookies">Details</a></p>
  <div class="cookie-act"><button class="btn sm" type="button" data-consent="all">Accept all</button><button class="btn sm ghost" type="button" data-consent="essential">Essential only</button></div>
</div>
{script_html}
</body>
</html>
"""
