# Domain Marketing: phase-wise build prompt

Use this prompt, one phase at a time, to rebuild or extend the site. Each phase ends with a
check that must pass before the next one starts. Fixed inputs that apply to every phase are in
the first section.

---

## Fixed inputs (apply to every phase)

- **Name and concept.** "Domain Marketing": a free toolkit and playbook site for people selling
  domain names. Thesis: parking income is gone, so a spare domain earns money only by being
  sold well. The site teaches and equips the selling.
- **Audience.** Domain investors holding 10 to 5,000 names, business owners selling one spare
  name, and founders buying one.
- **Revenue.** Google AdSense (publisher `ca-pub-6620975821265271`), sponsorship, reader
  contributions, and qualified leads from the plan builder.
- **Hosting.** Static files on GitHub Pages, free plan, `main` branch, repository
  `domain-marketing`. No server, no database, no build step that needs paid services.
- **Contact rules.**
  - The first element on every page is a ribbon reading: "Contact, if you are interested in
    this website/domain name/Sponsorship/Advertisement/Partnership". It links to the owner's
    partner contact page.
  - Every form on the site delivers to one inbox and no other.
  - Neither that inbox address nor the partner contact address may appear as readable text
    anywhere: not on a page, not in page source, not in the repository. Store both encoded and
    assemble them in the browser at run time.
- **Legal rules.** Use "Domain Marketing" only as a descriptive phrase. No logos of other
  companies. Name other companies only to identify their services. Publish a trademark and
  copyright disclosure and link it from every footer. State that the site is not affiliated
  with any similarly named business.
- **Honesty rules.** Every fee attributed to another company comes from that company's own
  page, with the date read and a link. If a rate is not published, say so; never estimate it.
  Label estimates as estimates. No invented urgency, counters or testimonials.

---

## Phase 1: Research

Open and read at least 38 sites in the domain industry: marketplaces, registrar marketplaces,
brokers, escrow and financing services, portfolio platforms, trade news, forums and courses.
For each one record, from the page itself: what it does, navigation, tools, forms and calls to
action, fees, how it makes money, and layout. Do not record anything from memory.

Write `docs/RESEARCH.md`: one row per site with what it does and what the build takes from it,
a list of features carried forward, and a list of things deliberately not copied.

**Check:** 38 or more rows, each tied to a page actually opened. Pages that failed to load are
listed as failures, not counted.

## Phase 2: Concept and information architecture

From the research, confirm the gap and fix the structure:

- Home
- Tools (index + one page per tool)
- Plan builder (the lead funnel)
- Playbooks (index + one page per guide)
- Where to sell (venue and fee table)
- Market wire (daily headlines + reference numbers)
- Video library
- Glossary
- Contests, Donate or sponsor, Work with us, Advertise and partner
- About, Contact, Privacy and cookies, Terms, Trademark and copyright disclosure, 404

All internal links are relative so the site works both under `/<repo>/` and at a domain root.

**Check:** every page has one job and one primary action; nothing on the list duplicates
another page.

## Phase 3: Design system

Build one stylesheet and one page shell.

- **Idea.** The domain name is the hero, set large inside an address-field shape. A yellow
  price tag marks every number the reader can act on, and nothing else is yellow. Listings are
  rows, like a portfolio table, not cards.
- **Colour.** White paper, deep indigo ink, cobalt for actions, tag yellow for results, a pale
  blue-grey wash for alternate bands. A dark theme using the same roles.
- **Type.** Bricolage Grotesque for display, Instrument Sans for text, both self-hosted under
  the Open Font License. Body lines under 80 characters.
- **Motion.** One: the tag swings in when a result appears. Respect reduced-motion.
- **Floor.** Responsive to 360 px, visible keyboard focus, labelled inputs, one `h1` per page,
  skip link, colour contrast that passes AA.

**Check:** home, a tool page, a playbook and the plan page render correctly at 390 px and
1280 px in light and dark.

## Phase 4: Tools (browser-only)

Build each as its own page with the form, the result, a "how it works" section and an FAQ.
Nothing typed is sent anywhere unless the visitor submits a form.

1. **Name scorecard.** Score 0 to 100 from five published factors (clarity 30%, length 25%,
   extension 20%, buyer intent 15%, clean typing 10%), plus three rule-of-thumb bands:
   investor, marketplace, end user. List what would lift the result.
2. **Net proceeds calculator.** Sale price in; every venue and route ranked by what the seller
   keeps, from `data/venues.json`. Minimum fees applied. Optional cost column. Custom rate.
3. **Portfolio calculator.** Names, renewal, sell-through, average price, commission in; yearly
   profit, break-even points and a floor price per name out.
4. **Outbound pitch writer.** First email under about 90 words, follow-up, closing note,
   subject lines, pre-send checklist. No invented urgency. Never an angle that targets a
   trademark owner.
5. **For-sale page builder.** Live preview; exports one self-contained HTML file. All input
   HTML-escaped; only `mailto:` and `http(s)` links accepted.
6. **Payment plan planner.** Lease-to-own, deposit and balloon structures; schedule and
   listing wording.
7. **Expiry timeline.** Expiry date in; grace, redemption, pending delete and earliest release
   dates out, with today's stage.
8. **Listing and social copy writer.** Marketplace summary and description, taglines, two
   social posts, a forum listing.

**Check:** automated tests load every tool, confirm output with no `NaN` or `undefined`, check
the arithmetic on one known case per calculator, and confirm hostile input is escaped.

## Phase 5: Lead generation

The plan builder is the dedicated lead section.

- Three steps: the name, the goal and deadline, the effort and floor price.
- It produces the plan on screen immediately: price mode with the reason, asking band, two or
  three venues with published fees, for-sale page checklist, outreach plan, four weeks of tasks.
- Only then does it offer: "Want a second opinion on this plan?" with name, email, the domain
  pre-filled, and the plan summary attached automatically.
- Role tabs open separate request forms for portfolio holders (50+ names), buyers and service
  providers.
- A two-field quick form (domain + email) closes every other page.
- Every tool result links to the plan builder with the name carried in the address.
- Forms: client-side validation, a honeypot field, a clear success state that names the next
  step, and a failure state that says what to do. Say plainly that details are never passed on
  without asking.

**Check:** a test submits each form against a mocked endpoint and confirms the subject, the
fields, the attached plan summary, and that a filled honeypot blocks the send.

## Phase 6: Content

- **Twelve playbooks**, 500 to 900 words each, original, practical, sourced: parking is over;
  pricing with three numbers; where to sell; the for-sale page; outbound; payment plans;
  expired names; closing safely; portfolio math; marketing in public; working with a broker;
  what makes a name sell. Paraphrase sources, link them at the foot, and end each guide with
  the matching tool.
- **Where to sell.** One row per venue: best for, published fees, source link, read date.
- **Glossary.** 40 or more plain-language terms.
- **About, privacy, terms, disclosure**, written for this site, not boilerplate.

**Check:** no claim about another company without a source link; no copied passages; every
guide passes a read-aloud test.

## Phase 7: Monetisation and AdSense readiness

- AdSense script and `google-adsense-account` meta tag in the head of every page.
- `ads.txt` at the root.
- Manual ad positions exist in the layout but render only when a slot id is configured;
  otherwise Auto ads decide.
- Cookie notice with "Accept all" and "Essential only"; the second requests non-personalised
  ads. Privacy page explains Google's use of cookies and how to opt out.
- Substantial original text on every indexed page; clear navigation; about, contact, privacy
  and terms pages; no deceptive layout; ads never placed to be mistaken for navigation.
- Sponsorship offer on the partners page, with what it does not buy stated.

**Check:** each indexed page has a unique title and description, one `h1`, a canonical URL,
structured data where it fits, and is listed in `sitemap.xml`.

## Phase 8: Community and funding

- **Donate or sponsor.** A pledge form (amount, frequency, where to direct it) for running
  costs, promotion and marketing, hiring talent, and contests and prizes. No payment is taken
  on the page. State that contributions are not tax-deductible.
- **Contests.** Three skill contests defined in `data/contests.json`, an entry form, and
  published rules: free entry, judged on stated criteria, void where prohibited.
- **Work with us.** Roles, how assignments work, and an application form.

**Check:** nothing on these pages promises money or work that is not funded.

## Phase 9: Automation

- `scripts/update_feeds.py` (standard library only): pulls headline, link, source and date
  from trade-press feeds; checks each curated video still plays and learns its channel; lists
  recent domain-related uploads from those channels. A failing source is skipped, earlier data
  is kept, and the script never fails the run.
- `build/build.py` regenerates every page, the sitemap, the RSS feed and the search index.
- `.github/workflows/auto-refresh.yml` runs on push, daily and on demand: refresh, rebuild,
  commit, deploy to Pages.
- A daily drill on the home page rotates by date in the browser, with no rebuild needed.

**Check:** the updater runs offline without error and leaves data intact; with mocked feeds it
filters bad links, undated items and off-topic videos.

## Phase 10: Quality gate

- Link check across all pages, including anchors.
- Every input has a label; one `h1` per page.
- Search the whole repository for the inbox address and the partner contact address in clear
  text. Zero matches allowed.
- Screenshots at phone and desktop widths, light and dark.
- All functional tests pass.

## Phase 11: Publish

- Push to `main`. Confirm the workflow completed, the bot's refresh commit landed, and the
  live address returns the home page.
- When the custom domain is ready: add a `CNAME` file, set `SITE_URL` in `build/layout.py`,
  rebuild and push. Then submit the domain in AdSense and turn on Auto ads.
- Review `data/venues.json` and `data/stats.json` each quarter.
