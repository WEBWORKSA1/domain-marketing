# Domain Marketing

**Free tools and playbooks for selling domain names.** Nine browser-only tools, twelve sourced
playbooks, a venue and fee table, a daily market wire, a video library, and a plan builder that
doubles as the lead funnel.

Static site for GitHub Pages (`main` branch, repository root). AdSense publisher
`ca-pub-6620975821265271`.

## Structure

| Path | What it is |
|---|---|
| `build/build.py` | Generator. `python3 build/build.py` rewrites every HTML page, `sitemap.xml`, `robots.txt`, `ads.txt`, `feed.xml` and `data/search.json`. Standard library only. |
| `build/layout.py` | Page shell, navigation, footer, lead strip, ad slots. `SITE_URL` and `ADS_SLOTS` live here. |
| `build/content_guides.py` | The twelve playbooks. |
| `build/content_tools.py` | Tool pages: form markup, how-it-works text, FAQs. |
| `build/content_pages.py` | Glossary, daily drills, roles, privacy, terms, disclosure, about. |
| `scripts/update_feeds.py` | Daily refresh of headlines and videos. Fault tolerant; never fails the run. |
| `.github/workflows/auto-refresh.yml` | Runs on push, daily at 06:23 UTC and on demand: refresh, rebuild, commit. Publishing follows the repository's Pages source (branch or GitHub Actions). |
| `data/refresh-log.json` | What each news feed and video channel returned on the last run. Check it when a source goes quiet. |
| `data/venues.json` | Venues and published fees, with sources and the date read. Feeds the calculator, the plan builder and the venue table. |
| `data/stats.json` | Reference numbers shown on the home page and market wire, each with its source. |
| `data/contests.json` | Contest names, briefs, closing dates and prizes. |
| `data/sources.json` | Feed list and video keyword filter for the daily refresh. |
| `data/news.json`, `data/videos.json` | Written by the refresh. Do not edit by hand, except to add a video to `library`. |
| `assets/js/core.js` | Theme, menu, forms, search, consent, video, filters. |
| `assets/js/tools.js` | All tools and the plan builder. |
| `docs/RESEARCH.md` | The 39-site research log. |
| `docs/BUILD-PROMPT.md` | Phase-wise build prompt. |

## Routine edits

- **Change a fee or add a venue:** edit `data/venues.json`, update `read`, rebuild.
- **Change contests or prizes:** edit `data/contests.json`, rebuild.
- **Add a video:** add `{"id": "<11-character id>", "t": "<title>", "c": "<topic>"}` to
  `library` in `data/videos.json`. Topics: basics, pricing, selling, outbound, landers,
  portfolio, expired.
- **Add a news source:** add a feed to `data/sources.json`.
- **Add a playbook:** add an entry to `GUIDES` in `build/content_guides.py`, rebuild.

Pushing to `main` triggers the workflow, which rebuilds and deploys, so a rebuild on your own
machine is optional.

## GitHub Pages

Settings > Pages > Source: **Deploy from a branch**, branch `main`, folder `/ (root)`. GitHub
then publishes `main` after every push, including the daily refresh commit. If the source is
set to "GitHub Actions" instead, the workflow's deploy job publishes the build. The workflow
cannot switch Pages on by itself; that one setting has to be saved in the repository.

## Custom domain

1. Add a `CNAME` file containing the domain.
2. Set `SITE_URL` in `build/layout.py` to `https://<domain>` (no trailing slash).
3. Push. Point the domain's DNS at GitHub Pages and enable HTTPS in the repository's Pages
   settings.

## AdSense

- The AdSense script and the `google-adsense-account` meta tag are in the head of every page.
  `ads.txt` is at the root.
- AdSense reviews sites on a domain you own, so apply after the custom domain is live.
- Until slot ids are set, placement is left to Auto ads (turn them on in the AdSense account).
  To use manual units, put the slot ids in `ADS_SLOTS` in `build/layout.py` and rebuild; the
  reserved positions (top, inline, side, foot) then render.
- For visitors in the EEA, UK and Switzerland, publish a consent message from AdSense's
  "Privacy & messaging" section. The site's own notice handles the non-personalised choice
  elsewhere.

## Forms

All forms post to one inbox through FormSubmit's AJAX endpoint. The inbox address and the
partner contact address are stored encoded in `assets/js/core.js` and assembled in the browser;
they do not appear in clear text anywhere in this repository. FormSubmit may send a one-time
activation email the first time a form is submitted from a new site address; until it is
confirmed, submissions show the "did not send" message. Send one test form after going live.

## Notices

"Domain Marketing" is used descriptively. The site is independent and not affiliated with any
registrar, registry, marketplace, broker or similarly named business. See `disclaimer.html`.
Fonts: Bricolage Grotesque and Instrument Sans, SIL Open Font License (`assets/fonts/LICENSE.txt`).
