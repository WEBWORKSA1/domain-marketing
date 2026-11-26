"""Tool pages: form markup (ids match assets/js/tools.js), how-it-works copy and FAQs."""

HP = '<div class="hp" aria-hidden="true"><label>Leave this empty <input name="company_site" tabindex="-1" autocomplete="off"></label></div>'

TOOLS = [
    {
        "slug": "name-score",
        "title": "Name scorecard",
        "h1": "Score a domain name for sales readiness",
        "row": "How sellable is this name, and what asking band should I test?",
        "time": "10 seconds",
        "desc": "Free domain name scorecard: a 0 to 100 sales-readiness score, the five factors behind it, and three rule-of-thumb asking bands to test.",
        "lede": "Type a name. You get a score out of 100, the five factors behind it, and three price bands: what an investor might pay, what to ask on a marketplace, and where to open with a named buyer.",
        "ui": """
<form id="ns-form" class="addr" autocomplete="off">
  <span class="scheme" aria-hidden="true">https://</span>
  <label class="sr" for="ns-input">Domain name</label>
  <input id="ns-input" type="text" inputmode="url" spellcheck="false" autocapitalize="none" placeholder="yourname.com" data-default="yourname.com">
  <button class="btn" type="submit">Score this name</button>
</form>
<div class="chips"><span>Try one:</span>
  <button class="chip" type="button" data-try="quotely.ai">quotely.ai</button>
  <button class="chip" type="button" data-try="solarledger.io">solarledger.io</button>
  <button class="chip" type="button" data-try="get-fresh-meals.com">get-fresh-meals.com</button>
  <button class="chip" type="button" data-try="meadow.com">meadow.com</button>
</div>
<div class="result out" id="ns-out" style="margin-top:1.5rem" aria-live="polite"><p class="out-empty">Your scorecard appears here.</p></div>
""",
        "how": """
<h2>How the score is built</h2>
<p>The scorecard reads the structure of the name and nothing else. Five factors, each scored out of 100, are combined with fixed weights:</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Factor</th><th class="n">Weight</th><th>What it checks</th></tr></thead>
<tbody>
<tr><td>Clarity</td><td class="n">30%</td><td>One dictionary word, two words that read cleanly, a pronounceable coined name, or a string nobody can read aloud</td></tr>
<tr><td>Length</td><td class="n">25%</td><td>Characters before the dot. Shorter scores higher; the fall is steep past ten</td></tr>
<tr><td>Extension</td><td class="n">20%</td><td>.com first, then the extensions with their own demand, then everything else</td></tr>
<tr><td>Buyer intent</td><td class="n">15%</td><td>Whether a word sits in a category where companies spend heavily to win customers</td></tr>
<tr><td>Clean typing</td><td class="n">10%</td><td>Hyphens and mixed digits, which cost visits every time the name is said aloud</td></tr>
</tbody></table></div>
<p>The price bands come from the score and the kind of name, using a fixed curve. The investor band is a small fraction of the marketplace band, because an investor has to leave room to resell. The end-user band is a multiple of it, because a company with a specific use will pay more than a stranger browsing.</p>
<h2>What it cannot see</h2>
<p>Traffic, age, backlinks, past use, live trademarks, and above all real sales of similar names. Those can move a price by ten times in either direction. Treat the band as the first line of your pricing notes, then check it against <a href="../playbooks/price-a-domain.html">comparable sales</a>.</p>
""",
        "faq": [
            ("Is this an appraisal?", "No. It is a rule-of-thumb reading of the name’s structure, meant to give you a band to test and a list of what would lift the result. An appraisal weighs comparable sales and facts this tool cannot see."),
            ("Why does my name score lower than another tool says it is worth?", "Tools differ in method and in what data they hold. This one deliberately uses no sales data, so it is conservative on names whose value comes from an active trend, and generous to none."),
            ("Does the tool store the names I type?", "No. Scoring runs in your browser. A name is only sent anywhere if you choose to submit one of the forms on this site."),
            ("What should I do with a low score?", "Check whether the name has something the score cannot see, such as traffic or an obvious buyer. If it does not, run the drop test in the portfolio calculator before the next renewal."),
        ],
    },
    {
        "slug": "net-proceeds",
        "title": "Net proceeds calculator",
        "h1": "What you keep after fees, venue by venue",
        "row": "Which venue leaves the most in my pocket at this price?",
        "time": "20 seconds",
        "desc": "Compare domain marketplace commissions, broker fees and escrow costs side by side and see what you actually keep at any sale price.",
        "lede": "Enter a sale price. The table ranks each venue and route by what you keep, using the commission rates the companies publish on their own pages.",
        "ui": """
<div class="tool">
  <form id="np-form" class="panel" autocomplete="off">
    <div class="field"><label for="np-price">Sale price (USD)</label><input id="np-price" type="number" min="0" step="50" value="5000" inputmode="decimal"></div>
    <div class="field"><label for="np-cost">What you paid for the name</label><input id="np-cost" type="number" min="0" step="1" value="0" inputmode="decimal"><span class="hint">Optional. Adds an “after your costs” column.</span></div>
    <div class="grid2">
      <div class="field"><label for="np-renew">Yearly renewal</label><input id="np-renew" type="number" min="0" step="0.5" value="12" inputmode="decimal"></div>
      <div class="field"><label for="np-years">Years held</label><input id="np-years" type="number" min="0" step="1" value="0" inputmode="numeric"></div>
    </div>
    <div class="field"><label for="np-custom">Add your own rate (%)</label><input id="np-custom" type="number" min="0" max="100" step="0.5" placeholder="e.g. 20" inputmode="decimal"><span class="hint">For a venue or broker whose rate you know from your own account.</span></div>
  </form>
  <div class="panel ink out" id="np-out" aria-live="polite"></div>
</div>
""",
        "how": """
<h2>Reading the table</h2>
<p>Each row is one route to a sale: a venue, and the way the buyer reached you there. On tiered marketplaces the same name can cost 10%, 15% or 20% depending on whether it was priced, where it pointed and whether the buyer came through a partner. The table shows every published tier, so you can see what the fee would be in the best and worst case before you list.</p>
<p>Two rows are for sales you find yourself and close through an escrow service. On deals above $5,000 the published escrow percentage steps down, so the calculator marks those figures as a ceiling.</p>
<h2>Fee is not the whole decision</h2>
<p>A venue that charges twice as much can still be the better choice if it is the one that finds the buyer. Use the table to understand the cost of each route, then choose on reach. The <a href="../playbooks/where-to-sell.html">where-to-sell playbook</a> matches kinds of name to routes, and <a href="../venues.html">the venue table</a> lists the source for every rate.</p>
""",
        "faq": [
            ("Where do the rates come from?", "From each company’s own published pages, read on the date shown on the Where to sell page. Venues whose rate was not stated on the page we read are left out of the calculator instead of guessed."),
            ("Why is a venue I use missing?", "Either its rate was not published where we could read it, or we have not reviewed it yet. Enter the rate from your own account in the “add your own rate” box to include it."),
            ("Does the buyer or the seller pay escrow?", "Whoever you agree. The calculator assumes the seller pays, which is the conservative case."),
        ],
    },
    {
        "slug": "portfolio-math",
        "title": "Portfolio calculator",
        "h1": "Does your portfolio pay for itself?",
        "row": "Is my portfolio profitable, and which names should I drop?",
        "time": "30 seconds",
        "desc": "Domain portfolio calculator: renewals, sell-through rate, average price and commission in, yearly profit, break-even points and a drop-test floor out.",
        "lede": "Four inputs describe a portfolio. Change any of them and see the yearly result, the sell-through you need to break even, and the price a name has to fetch to earn its renewal.",
        "ui": """
<div class="tool">
  <form id="pm-form" class="panel" autocomplete="off">
    <div class="grid2">
      <div class="field"><label for="pm-count">Names held</label><input id="pm-count" type="number" min="1" step="1" value="400" inputmode="numeric"></div>
      <div class="field"><label for="pm-renew">Average renewal ($)</label><input id="pm-renew" type="number" min="0" step="0.5" value="12" inputmode="decimal"></div>
      <div class="field"><label for="pm-str">Sell-through per year (%)</label><input id="pm-str" type="number" min="0" max="100" step="0.1" value="1.5" inputmode="decimal"></div>
      <div class="field"><label for="pm-avg">Average sale price ($)</label><input id="pm-avg" type="number" min="0" step="50" value="2400" inputmode="decimal"></div>
      <div class="field"><label for="pm-comm">Average commission (%)</label><input id="pm-comm" type="number" min="0" max="100" step="0.5" value="15" inputmode="decimal"></div>
      <div class="field"><label for="pm-buys">New names bought per year</label><input id="pm-buys" type="number" min="0" step="1" value="0" inputmode="numeric"></div>
    </div>
    <div class="field"><label for="pm-buycost">Average cost of a new name ($)</label><input id="pm-buycost" type="number" min="0" step="1" value="0" inputmode="decimal"></div>
    <p class="form-note">Use your real figures from the last twelve months. The defaults are an example, not a benchmark.</p>
  </form>
  <div class="panel ink out" id="pm-out" aria-live="polite"></div>
</div>
""",
        "how": """
<h2>The sums</h2>
<ul>
<li><strong>Carrying cost</strong> = names held × average renewal.</li>
<li><strong>Expected sales</strong> = names held × sell-through rate.</li>
<li><strong>Income kept</strong> = expected sales × average price × (1 − commission).</li>
<li><strong>Profit</strong> = income kept − carrying cost − new purchases.</li>
<li><strong>Floor per name</strong> = renewal ÷ sell-through ÷ (1 − commission). A name that cannot realistically sell for this much is expected to cost more to hold than it returns.</li>
</ul>
<h2>Using the floor</h2>
<p>Sort your list by an honest price estimate and mark everything below the floor. Those names are candidates to drop or to sell wholesale before renewal. The <a href="../playbooks/portfolio-math.html">portfolio math playbook</a> walks through the yearly routine.</p>
""",
        "faq": [
            ("What sell-through rate should I use?", "Your own, measured over at least two years: names sold divided by names held. One good year or one large sale will mislead you if you use a single year."),
            ("Does this include tax?", "No. Tax treatment of domain sales differs by country and by whether you trade as a business. Ask an accountant who knows your situation."),
            ("My result is negative. Now what?", "Cutting names below the floor is the only change that helps at the very next renewal. After that, work on sell-through: prices and for-sale pages on every name, and outreach on the best few."),
        ],
    },
    {
        "slug": "pitch-writer",
        "title": "Outbound pitch writer",
        "h1": "Draft the three emails that sell a domain",
        "row": "What do I actually write to a company that should own this name?",
        "time": "1 minute",
        "desc": "Free outbound email writer for domain sellers: a first email under 90 words, a follow-up and a closing note, with subject lines and a pre-send checklist.",
        "lede": "Fill in what you know. You get a first email, a follow-up and a closing note, written the way one business person writes to another, plus subject lines to test.",
        "ui": """
<div class="tool">
  <form id="pw-form" class="panel" autocomplete="off">
    <div class="field"><label for="pw-domain">Domain you are selling</label><input id="pw-domain" type="text" inputmode="url" spellcheck="false" autocapitalize="none" placeholder="yourname.com" value="yourname.com"></div>
    <div class="field"><label for="pw-me">Your name</label><input id="pw-me" type="text" autocomplete="name" placeholder="Alex Rivera"></div>
    <div class="grid2">
      <div class="field"><label for="pw-co">Their company</label><input id="pw-co" type="text" placeholder="Optional"></div>
      <div class="field"><label for="pw-cur">Their current domain</label><input id="pw-cur" type="text" spellcheck="false" autocapitalize="none" placeholder="Optional"></div>
    </div>
    <div class="field"><label for="pw-angle">Why it fits them</label>
      <select id="pw-angle">
        <option value="upgrade">It is a shorter version of the name they use</option>
        <option value="exact">It says exactly what they sell</option>
        <option value="category">It names the category they compete in</option>
        <option value="launch">It suits a product or market they may launch</option>
        <option value="geo">It pairs their city with their service</option>
      </select></div>
    <div class="grid2">
      <div class="field"><label for="pw-ask">The ask</label>
        <select id="pw-ask"><option value="price">State my price</option><option value="offer">Invite an offer</option></select></div>
      <div class="field"><label for="pw-price">Price (USD)</label><input id="pw-price" type="number" min="0" step="50" value="4800" inputmode="decimal"></div>
    </div>
    <div class="field"><label for="pw-tone">Tone</label>
      <select id="pw-tone"><option value="plain">Plain</option><option value="warm">Warm</option><option value="formal">Formal</option></select></div>
  </form>
  <div class="out" id="pw-out" aria-live="polite"></div>
</div>
""",
        "how": """
<h2>Why the emails look like this</h2>
<p>The first email does four things in under about ninety words: says what you own, gives one specific reason it fits the reader, explains how a purchase would work, and offers an easy way to decline. Nothing in it pretends to urgency, and it mentions escrow early because the reader’s first private question is whether you are real.</p>
<p>The follow-up exists because first emails land on bad days. The third note closes the loop and stops. Three touches is the limit the drafts are built around.</p>
<h2>Before you send anything</h2>
<ul>
<li>Check the company does not hold a trademark that matches the name. If it does, do not write to it.</li>
<li>Find a named person: a founder, or whoever leads marketing or brand.</li>
<li>Add your postal address and a clear way to opt out if the law where your reader lives requires it. In the United States it does.</li>
</ul>
<p>The <a href="../playbooks/outbound.html">outbound playbook</a> covers who to write to and the rules in more detail.</p>
""",
        "faq": [
            ("Is sending these emails legal?", "It depends on where the recipient is and what you include. The United States regulates commercial email, including one-to-one business email, and Canada and European countries have stricter consent rules. The playbook summarises the main points; it is general information, not legal advice."),
            ("How many companies should I write to?", "Ten to twenty-five that you chose by hand. If you cannot say in one sentence why the name helps a company, leave it off the list."),
            ("Should I state the price?", "Usually yes for names in the low thousands, because it saves a round of email and filters out people with no budget. For names where the right buyer could pay far more than you would dare print, invite an offer and keep a private floor."),
        ],
    },
    {
        "slug": "lander-builder",
        "title": "For-sale page builder",
        "h1": "Build a for-sale page for your domain",
        "row": "What should people see when they type my domain?",
        "time": "2 minutes",
        "desc": "Free domain for-sale landing page generator. Set the price or offer route, preview the page live, then copy or download one small HTML file.",
        "lede": "Fill in the form and watch the page take shape. When it looks right, download a single HTML file and upload it to any web host. No account, no code to write.",
        "ui": """
<div class="tool wide">
  <form id="lb-form" class="panel" autocomplete="off">
    <div class="field"><label for="lb-domain">Domain</label><input id="lb-domain" type="text" inputmode="url" spellcheck="false" autocapitalize="none" value="yourname.com"></div>
    <div class="field"><label for="lb-mode">How buyers can act</label>
      <select id="lb-mode"><option value="both">Buy now, offers welcome</option><option value="bin">Buy now only</option><option value="offer">Make an offer</option><option value="request">Price on request</option></select></div>
    <div class="grid2">
      <div class="field"><label for="lb-price">Buy-now price ($)</label><input id="lb-price" type="number" min="0" step="50" value="4800" inputmode="decimal"></div>
      <div class="field"><label for="lb-min">Minimum offer ($)</label><input id="lb-min" type="number" min="0" step="50" value="0" inputmode="decimal"></div>
    </div>
    <div class="field"><label for="lb-lto">Monthly plan, in months</label><input id="lb-lto" type="number" min="0" max="60" step="1" value="12" inputmode="numeric"><span class="hint">0 hides the monthly option.</span></div>
    <div class="field"><label for="lb-tagline">One line on who it suits</label><input id="lb-tagline" type="text" maxlength="120" value="A short, memorable name for a growing brand."></div>
    <div class="field"><label for="lb-points">Selling points, one per line</label><textarea id="lb-points" rows="3">Eight letters, two real words
Easy to say on a call and spell from memory
On .com, the extension buyers expect</textarea></div>
    <div class="field"><label for="lb-how">The button goes to</label><select id="lb-how"><option value="email">My email address</option><option value="url">A web address</option></select></div>
    <div class="field"><label for="lb-to">That email or web address</label><input id="lb-to" type="text" spellcheck="false" autocapitalize="none" placeholder="you@yourdomain.com"></div>
    <div class="field"><label for="lb-color">Accent colour</label>
      <select id="lb-color"><option value="cobalt">Cobalt</option><option value="forest">Forest</option><option value="plum">Plum</option><option value="charcoal">Charcoal</option><option value="ember">Ember</option></select></div>
    <p class="err" id="lb-warn">Add your email or a web address so the button reaches you.</p>
  </form>
  <div>
    <iframe id="lb-preview" class="preview" title="Preview of your for-sale page" sandbox=""></iframe>
    <div class="btn-row" style="margin:1rem 0">
      <button class="btn" type="button" id="lb-download">Download the page</button>
      <button class="btn ghost" type="button" data-copy="#lb-code" data-copy-label="Page code">Copy the code</button>
    </div>
    <label class="sr" for="lb-code">Page code</label>
    <textarea id="lb-code" class="code" readonly spellcheck="false"></textarea>
  </div>
</div>
""",
        "how": """
<h2>Putting the page online</h2>
<ol>
<li>Download the file. It is called <code>index.html</code> and contains everything: no images, fonts or scripts to host.</li>
<li>Upload it to any static host. Most registrars include basic hosting or forwarding, and several free hosts will serve a single page with HTTPS.</li>
<li>Point the domain at that host using the DNS records it gives you.</li>
<li>Open the name on your phone, press the button, and confirm the message reaches you.</li>
</ol>
<h2>What the page includes, and why</h2>
<p>The name as a headline, a single line on who it suits, the price or offer route, one button, up to four selling points and two sentences explaining escrow. That is everything a visitor needs to act and nothing that slows the page down. The reasoning is in the <a href="../playbooks/for-sale-page.html">for-sale page playbook</a>.</p>
<div class="note"><p>If you put an email address on the page, use one you are happy to see in public, since anyone who views the page can read it. A web address for a contact form or a marketplace listing keeps your inbox private.</p></div>
""",
        "faq": [
            ("Do I need an account to use the page?", "No. The file is yours. It contains no tracking and no link back to this site."),
            ("Can I edit the page afterwards?", "Yes. It is plain HTML with the styles inline at the top. Any text editor will open it."),
            ("How do I take payment?", "The page starts the conversation. Close the sale through a licensed escrow service or a marketplace checkout so that neither side has to trust the other with the money."),
        ],
    },
    {
        "slug": "payment-plan",
        "title": "Payment plan planner",
        "h1": "Work out a lease-to-own or payment plan",
        "row": "What monthly figure makes this name affordable without costing me?",
        "time": "20 seconds",
        "desc": "Lease-to-own calculator for domain names: equal payments, deposit plans and balloon plans, with a payment schedule and listing wording.",
        "lede": "Choose a structure, a term and a premium over the cash price. You get the monthly figure, the schedule and a sentence to paste into your listing.",
        "ui": """
<div class="tool">
  <form id="pp-form" class="panel" autocomplete="off">
    <div class="field"><label for="pp-price">Cash price (USD)</label><input id="pp-price" type="number" min="0" step="50" value="8000" inputmode="decimal"></div>
    <div class="field"><label for="pp-type">Structure</label>
      <select id="pp-type"><option value="lto">Lease-to-own: equal monthly payments</option><option value="deposit">Deposit, then equal payments</option><option value="balloon">Lower payments, then a final balloon</option></select></div>
    <div class="grid2">
      <div class="field"><label for="pp-months">Term in months</label><input id="pp-months" type="number" min="2" max="120" step="1" value="24" inputmode="numeric"></div>
      <div class="field"><label for="pp-prem">Premium over cash (%)</label><input id="pp-prem" type="number" min="0" max="100" step="1" value="15" inputmode="decimal"></div>
    </div>
    <div class="field" id="pp-dep-wrap"><label for="pp-dep">Deposit (% of total)</label><input id="pp-dep" type="number" min="0" max="90" step="1" value="20" inputmode="decimal"></div>
    <div class="field" id="pp-bal-wrap"><label for="pp-bal">Final payment (% of total)</label><input id="pp-bal" type="number" min="0" max="90" step="1" value="40" inputmode="decimal"></div>
  </form>
  <div class="panel ink out" id="pp-out" aria-live="polite"></div>
</div>
""",
        "how": """
<h2>The three structures</h2>
<ul>
<li><strong>Lease-to-own</strong> splits the total into equal monthly payments. It is the simplest plan to explain and suits most names.</li>
<li><strong>A deposit plan</strong> takes a larger first payment and spreads the rest. Sellers use it on higher-priced names to see commitment up front.</li>
<li><strong>A balloon plan</strong> keeps the monthly figure low and ends with one large payment. It suits buyers who expect funding or revenue before the term ends.</li>
</ul>
<h2>Setting the premium</h2>
<p>You are waiting for your money and carrying the risk that payments stop, so charging somewhat more than the cash price is reasonable. Show both figures so that paying in full is visibly cheaper. Keep the term short enough that renewals and platform fees do not consume the premium. More in the <a href="../playbooks/payment-plans.html">payment plans playbook</a>.</p>
""",
        "faq": [
            ("Who holds the domain during the plan?", "Not the buyer. Either a platform, an escrow holding service or you, with the name’s settings pointed where the buyer asks. Ownership passes after the final payment."),
            ("What happens if the buyer stops paying?", "Under the usual terms the buyer loses use of the name and the payments already made. Put the grace period and the consequence in writing before the first payment."),
            ("Is this a loan?", "A lease-to-own plan is normally structured as a lease with an option to buy, not as credit. How it is treated legally and for tax depends on where you and the buyer are, so check before you offer plans at scale."),
        ],
    },
    {
        "slug": "expiry-timeline",
        "title": "Expiry timeline",
        "h1": "Map what happens after a domain expires",
        "row": "When could this expiring name actually become available?",
        "time": "10 seconds",
        "desc": "Enter a domain’s expiry date to see the registrar grace period, redemption, pending delete and the earliest date the name can be released.",
        "lede": "Enter the expiry date from the public registration record. The timeline shows each stage, the date it ends, and where the name stands today.",
        "ui": """
<div class="tool">
  <form id="et-form" class="panel" autocomplete="off">
    <div class="field"><label for="et-date">Expiry date</label><input id="et-date" type="date"></div>
    <div class="field"><label for="et-grace">Registrar grace period, in days</label><input id="et-grace" type="number" min="0" max="45" step="1" value="30" inputmode="numeric"><span class="hint">Each registrar sets its own, from 0 to 45. If you do not know it, 30 is a reasonable planning figure.</span></div>
  </form>
  <div class="panel ink out" id="et-out" aria-live="polite"></div>
</div>
""",
        "how": """
<h2>The stages in brief</h2>
<p>After expiry the registrar holds the name for a grace period it sets itself. If the name is not renewed or sold at the registrar’s auction in that time, it enters 30 days of redemption, when only the previous owner can recover it for an extra fee, then 5 days of pending delete, and then it is released.</p>
<p>For any name with obvious value, the important stage is the first one. Most large registrars send unrenewed names to an auction partner during the grace period, and a name that attracts a bid there never reaches release. Find out where the name is registered, then check that registrar’s auction venue.</p>
<h2>Limits</h2>
<p>The dates are a planning guide for generic extensions such as .com and .net. Registrars differ, and country-code extensions follow their own rules. The <a href="../playbooks/expired-domains.html">expired domains playbook</a> explains auctions and backorders.</p>
""",
        "faq": [
            ("Where do I find the expiry date?", "In the public registration record for the name, which any lookup service or registrar search will show. Look for the registry expiry date."),
            ("Can I register the name on the release date myself?", "For a name anyone else wants, almost never. Drop-catching services send registration requests in the instant of release. A backorder with one or more of them is the practical route."),
            ("The owner’s site is still up after the expiry date. Why?", "Some registrars keep services running for part of the grace period, and some owners renew late. An expiry date in the past does not mean the name is available."),
        ],
    },
    {
        "slug": "listing-copy",
        "title": "Listing and social copy writer",
        "h1": "Draft your listing and social posts",
        "row": "How do I describe this name on a marketplace and in a post?",
        "time": "30 seconds",
        "desc": "Generate a marketplace summary and description, taglines, posts for X and LinkedIn, and a forum sale listing for any domain name.",
        "lede": "One form, six drafts: a short marketplace summary, a full description, taglines for the for-sale page, two social posts and a forum listing.",
        "ui": """
<div class="tool">
  <form id="lc-form" class="panel" autocomplete="off">
    <div class="field"><label for="lc-domain">Domain</label><input id="lc-domain" type="text" inputmode="url" spellcheck="false" autocapitalize="none" value="yourname.com"></div>
    <div class="field"><label for="lc-ind">Industry it suits</label>
      <select id="lc-ind">
        <option value="fintech">Fintech and payments</option><option value="software">Software and AI</option><option value="e-commerce">E-commerce and retail</option>
        <option value="health">Health and wellness</option><option value="real estate">Real estate</option><option value="travel">Travel and hospitality</option>
        <option value="education">Education</option><option value="professional services">Professional services</option><option value="food">Food and drink</option><option value="media">Media and entertainment</option>
      </select></div>
    <div class="field"><label for="lc-aud">Who would use it</label><input id="lc-aud" type="text" maxlength="90" placeholder="a growing consumer brand"></div>
    <div class="field"><label for="lc-vibe">How it should sound</label>
      <select id="lc-vibe"><option value="trust">Trustworthy</option><option value="modern">Modern</option><option value="playful">Playful</option><option value="premium">Premium</option></select></div>
  </form>
  <div class="out" id="lc-out" aria-live="polite"></div>
</div>
""",
        "how": """
<h2>Making the drafts yours</h2>
<p>The drafts are deliberately plain: the name, who it suits, three facts and how to buy. Read each one aloud and cut anything you would not say to a buyer in person. Replace the bracketed parts of the forum listing with your real price, registrar and expiry date.</p>
<h2>Where each one goes</h2>
<ul>
<li><strong>Summary and description:</strong> the listing fields on a marketplace.</li>
<li><strong>Taglines:</strong> the one line under the name on your for-sale page.</li>
<li><strong>Social posts:</strong> from an account that says who you are. Lead with the use, not the asset.</li>
<li><strong>Forum listing:</strong> investor communities, at investor prices.</li>
</ul>
<p>The <a href="../playbooks/social-and-community.html">playbook on marketing in public</a> covers which audience pays which price.</p>
""",
        "faq": [
            ("Can I use the text as it is?", "Yes, it is yours to use and change. You will sell better if you edit it into your own voice."),
            ("Why no hashtags or emoji?", "Because the people who buy domains for businesses respond to clear sentences. Add them if your audience expects them."),
            ("Why does it avoid claims about value or traffic?", "Because a claim you cannot support on request costs you the sale and your reputation. State facts about the name and let the buyer judge."),
        ],
    },
]
