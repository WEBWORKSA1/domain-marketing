"""Playbooks: original long-form guides. Facts from other sites are paraphrased, attributed and linked."""

REVIEWED = "November 26, 2026"

GUIDES = [
    {
        "slug": "parking-is-over",
        "title": "Parking is over. Selling is the business now.",
        "desc": "Pay-per-click parking stopped covering renewals in 2025 and 2026. Here is what changed, what it means for a portfolio, and what to do this quarter.",
        "mins": 6,
        "tool": ("tools/portfolio-math.html", "Run your portfolio numbers"),
        "body": """
<p class="lede">For twenty years the default answer to “what do I do with an unused domain?” was to park it and collect ad clicks. That answer no longer works for most names, and the consequence is simple: a domain you are not using earns money one way, by being sold.</p>

<h2 id="what-changed">What changed</h2>
<p>Search consultant Bill Hartzer pulled the numbers together in an August 2026 analysis. In his account, Google stepped back from advertising on parked domains in stages through 2025, one long-running parking company announced its shutdown in January 2026, and the listed companies that run the remaining parking platforms reported steep falls in that line of revenue. His conclusion for a typical portfolio is blunt: list the names for sale or let them go.</p>
<p>You do not have to take one analyst’s word for the direction. IONOS, a large registrar, now tells its own customers that monetisation is no longer the default use of parking and should not be treated as a dependable core strategy. Parking products still exist. GoDaddy sells CashParking plans, for example, with an 80% revenue share on its paid tier. But a share of a shrinking number is still a shrinking number.</p>

<h2 id="the-cost-side">The cost side moved the other way</h2>
<p>While ad income fell, the cost of holding a name rose. Hartzer notes that the wholesale price registrars pay for a .com goes to $10.97 from November 1, 2026, with a small ICANN fee on top. Your registrar adds its own margin. Every name in the portfolio now has to justify roughly a dozen dollars a year with something other than clicks.</p>
<div class="note"><p><strong>The drop test.</strong> Take a name’s realistic sale price, multiply by the share of your names that sell in a year, then by what you keep after commission. If the answer is below the renewal fee, the name is expected to cost more than it returns. The <a href="../tools/portfolio-math.html">portfolio calculator</a> does this for the whole list.</p></div>

<h2 id="what-replaces-it">What replaces parking income</h2>
<p>Nothing replaces it passively. What replaces it is marketing, which is to say doing the things that make a sale more likely:</p>
<ul>
<li><strong>A price.</strong> A visible buy-now price, or a clear offer route, on every name you would sell.</li>
<li><strong>A page.</strong> The name itself is a traffic source: people type it to see what is there. A for-sale page turns that visit into an inquiry. A blank page or an error wastes it.</li>
<li><strong>Distribution.</strong> A listing on at least one marketplace network, so the name shows up when someone searches a registrar for something similar.</li>
<li><strong>Outreach</strong> for the handful of names where you can name the buyer.</li>
<li><strong>A smaller list.</strong> Dropping the names that fail the test above is a marketing decision too. It frees renewal money and attention for the names that can sell.</li>
</ul>

<h2 id="this-quarter">A plan for this quarter</h2>
<ol>
<li>Export your list with renewal dates. Sort by the next 90 days.</li>
<li>Score each name and write down a realistic marketplace price. Be honest about the bottom third.</li>
<li>Run the drop test. Let the failures expire, or sell them to other investors at wholesale for whatever they fetch.</li>
<li>Put a price and a for-sale page on everything that survives.</li>
<li>Pick the ten names with an obvious buyer and send thirty good emails in total.</li>
</ol>
<p>None of this is glamorous. It is the difference between a portfolio that costs money every November and one that pays for itself.</p>
""",
        "sources": [
            ("Bill Hartzer, “Domain Parking Is Finished: What the 2025 Numbers Show” (August 2026)", "https://www.billhartzer.com/?p=18461"),
            ("IONOS Digital Guide, “What is domain parking?”", "https://www.ionos.com/digitalguide/domains/domain-administration/domain-parking-earning-money-with-domains/"),
            ("GoDaddy CashParking plans", "https://www.godaddy.com/domains/cashparking"),
        ],
    },
    {
        "slug": "price-a-domain",
        "title": "How to price a domain: three numbers, not one",
        "desc": "A domain has an investor price, a marketplace price and an end-user price. How to find each with comparable sales, and when to show a number at all.",
        "mins": 7,
        "tool": ("tools/name-score.html", "Score a name and see its bands"),
        "body": """
<p class="lede">Ask five tools what a domain is worth and you get five answers. They are not all wrong. They are answering different questions, and the first job in pricing is to decide which question you are asking.</p>

<h2 id="three-prices">The three prices</h2>
<p>Instant Domain Search’s appraisal tool lays this out more clearly than most: it reports an auction price, a marketplace price and a brokerage price for the same name. The idea is worth borrowing whatever tool you use.</p>
<ul>
<li><strong>The investor price</strong> is what another domain investor would pay this week. It is the floor, and it is usually a small fraction of the retail figure, because the buyer needs room to resell.</li>
<li><strong>The marketplace price</strong> is the buy-now number you would list at and reasonably expect to get from a business that finds the name on its own, some time in the next few years.</li>
<li><strong>The end-user price</strong> is the opening ask to a specific company that has a clear reason to want this exact name. It is the ceiling, and it only exists when such a company does.</li>
</ul>
<p>Most pricing arguments are two people quoting different rows of that list at each other.</p>

<h2 id="comps">Finding the marketplace price with comparable sales</h2>
<p>The method is the one estate agents use. MediaOptions, a brokerage, describes it well: gather verified past sales, keep only those that match on length, keyword type, extension and industry, adjust for how long ago they happened, and narrow to a range.</p>
<ol>
<li><strong>Collect.</strong> Search a public sales database for your keyword and extension. Aim for ten to twelve sales, with at least four or five that bracket your likely price from above and below.</li>
<li><strong>Filter hard.</strong> A two-word .com is not a comparable for a one-word .com. A .net is not a comparable for a .com. Drop anything that differs on more than one dimension.</li>
<li><strong>Weight recent sales.</strong> Sort by date. Demand for a keyword moves with technology and fashion, so a 2019 sale tells you less than one from this year.</li>
<li><strong>Read the venue.</strong> A sale at an expired-name auction is an investor price. A sale through a broker is closer to an end-user price. Do not average the two.</li>
</ol>
<p>The method has a known blind spot: many of the largest sales are private and never reach a database. For ordinary names that matters little. For one-word .coms it means the public record understates the market.</p>

<h2 id="automated">Where automated appraisals fit</h2>
<p>Automated tools are fast and consistent, which makes them good for sorting a long list and bad as a final answer. GoDaddy’s tool returns an estimated value, a suggested list price and a probability of sale, and says plainly that it looks only at the name, not at any website on it. Dynadot’s own advice is to run several tools, discard the highest and lowest, and treat the rest as a baseline. The scorecard on this site belongs in the same category: a band to test, not a verdict.</p>
<div class="note"><p><strong>One warning.</strong> If a “buyer” asks you to pay for an appraisal from a particular service before they will make an offer, stop replying. It is a long-running scam and the buyer does not exist.</p></div>

<h2 id="show-the-number">Buy-now, make-offer, or both</h2>
<p>Sedo says names with a buy-now price sell up to three times faster than names that require negotiation. The reason is friction: a priced name can be bought at midnight by someone with a company card, and an unpriced one needs an email, a reply and a week.</p>
<ul>
<li><strong>Use a fixed price</strong> for the bulk of a portfolio: names in the hundreds to low thousands, where speed and volume matter more than the last 20%.</li>
<li><strong>Use make-offer with a private floor</strong> for names where the right buyer’s budget could be many multiples of any number you would dare to print.</li>
<li><strong>Use both</strong>, a buy-now price with offers allowed, when you want the anchor and the conversation.</li>
</ul>

<h2 id="using-comps-in-negotiation">Using comps when the offer is low</h2>
<p>Comparable sales also do a job after the inquiry arrives. A buyer who has never bought a domain often opens at a few hundred dollars because that is what registration costs suggest. Sending three or four recent, truly comparable sales reframes the conversation without an argument. Investor Elliot Silver makes the necessary caveat: only cite sales that are really comparable. Quoting a seven-figure outlier against a mid-range name makes you look unserious and can end the conversation.</p>
""",
        "sources": [
            ("Instant Domain Search, free domain appraisal (three prices and scoring factors)", "https://instantdomainsearch.com/domain-appraisal"),
            ("MediaOptions, “Valuing Domains Using Comparable Sales”", "https://mediaoptions.com/blog/valuing-domains-using-comparable-sales/"),
            ("ICANNWiki, “DN Sale Price” (ten to twelve comparables)", "https://icannwiki.com/DN_Sale_Price"),
            ("GoDaddy domain value appraisal", "https://www.godaddy.com/domain-value-appraisal"),
            ("Dynadot, domain appraisal FAQs", "https://www.dynadot.com/blog/domain-appraisal-faqs"),
            ("Sedo, sell domains (buy-now names sell faster)", "https://sedo.com/uk/sell-domains/"),
            ("DomainInvesting.com, “Don’t scare a prospect away”", "https://domaininvesting.com/dont-scare-a-prospect-away/"),
        ],
    },
    {
        "slug": "where-to-sell",
        "title": "Where to sell a domain, and what each route costs",
        "desc": "Marketplace networks, registrar marketplaces, brokers and your own page compared on fees, reach and the kind of name each one suits.",
        "mins": 6,
        "tool": ("tools/net-proceeds.html", "Compare what you keep at each venue"),
        "body": """
<p class="lede">The cheapest venue is rarely the right question. A 5% route that nobody visits earns less than a 20% route that puts the name in front of a buyer mid-search. Choose on reach first, then on fee.</p>

<h2 id="four-routes">The four routes</h2>
<h3>1. Marketplace networks</h3>
<p>Networks syndicate your priced listing into the search results of many registrars. Someone looking for a name at their registrar sees yours as a premium option and can buy it in the same checkout. This is the nearest thing to passive selling that still works, and it is why most investors list their priced names on at least one network.</p>
<p>The price of that reach is the top of the fee scale. Sedo publishes its structure clearly: 10% when a priced name is parked with Sedo or uses its sales page and sells directly, 15% for make-offer and auction sales, and 20% whenever the buyer arrives through the partner network.</p>

<h3>2. Registrar marketplaces</h3>
<p>Several registrars run their own marketplaces for names held in your account. Listing takes a minute and fees sit around 10%: Namecheap charges a flat 10%, and Dynadot charges 10% on listings and auctions, dropping to 5% when you bring the buyer yourself through a payment link. Reach is narrower than a network, so these suit lower-priced names and quick sales.</p>

<h3>3. Brokers</h3>
<p>A broker goes out and finds the buyer. DomainInvesting.com’s guide puts typical commissions at 10% to 20% and notes that nearly every broker will ask for an exclusivity period. That is a fair price when the name is worth six figures and the buyer has to be found and persuaded. It is poor value on a $2,000 name, and most brokers will decline it anyway.</p>

<h3>4. Your own page plus escrow</h3>
<p>Point the name at a for-sale page you control and close through an escrow service. There is no commission, only the escrow fee: Escrow.com starts at 2.6% with a $50 minimum on deals up to $5,000, and the percentage falls as the price rises. You keep the buyer’s details and the whole negotiation. You also do all the marketing.</p>

<h2 id="match">Matching the name to the route</h2>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>If the name is…</th><th>Start with</th><th>Why</th></tr></thead>
<tbody>
<tr><td>A solid two-word .com priced under $5,000</td><td>A marketplace network at a fixed price</td><td>Volume and impulse purchases; the network does the finding</td></tr>
<tr><td>A coined, brandable name</td><td>A curated brandable marketplace</td><td>Buyers there are shopping for a brand, with logos and payment plans on show</td></tr>
<tr><td>A one-word .com or a short acronym</td><td>A broker, or make-offer on your own page</td><td>The buyer’s budget sets the price; a public number caps it</td></tr>
<tr><td>A name with an old site, links or traffic</td><td>A marketplace that sells websites as well as names</td><td>Buyers there value the history</td></tr>
<tr><td>A name you want gone this month</td><td>An investor community or a registrar auction</td><td>Wholesale price, same-week sale</td></tr>
</tbody></table></div>

<h2 id="rules">Three rules that save money</h2>
<ul>
<li><strong>One price everywhere.</strong> If a buyer finds the name cheaper on a second venue, you have negotiated against yourself.</li>
<li><strong>Know which fee applies before the sale.</strong> On tiered venues the rate depends on how the buyer arrived, not on what you hoped.</li>
<li><strong>Read the exclusivity clause.</strong> Some venues and nearly all brokers restrict where else you may sell. Check before you sign, not after an offer arrives elsewhere.</li>
</ul>
<p>The full table of venues, with the published fees we read and links to each company’s own page, is in <a href="../venues.html">Where to sell</a>.</p>
""",
        "sources": [
            ("Sedo, “Buy, Park, Sell”", "https://sedo.com/us/what-we-offer/buy-park-sell"),
            ("DomainGang, “Sedo: Complete breakdown of its marketplace fees”", "https://domaingang.com/domain-news/sedo-complete-breakdown-of-its-marketplace-fees"),
            ("Namecheap, “How do I list a domain for sale?”", "https://www.namecheap.com/support/knowledgebase/article.aspx/359/15/how-do-i-sell-my-domain-on-namecheap-market/"),
            ("Dynadot domain market", "https://www.dynadot.com/market"),
            ("DomainInvesting.com, guide to domain brokers", "https://domaininvesting.com/guide/list-of-domain-brokers/"),
            ("Escrow.com, domain and website escrow", "https://www.escrow.com/domains"),
        ],
    },
    {
        "slug": "for-sale-page",
        "title": "The for-sale page: what belongs on it",
        "desc": "People type your domain to see what is there. A good for-sale page turns that visit into an inquiry. What to show, what to leave out, and how to test it.",
        "mins": 6,
        "tool": ("tools/lander-builder.html", "Build a for-sale page"),
        "body": """
<p class="lede">The best traffic a domain for sale will ever get is someone typing the name itself to see whether it is taken. That person is already interested. The for-sale page has one job: let them act before they close the tab.</p>

<h2 id="five-things">Five things the page must do</h2>
<ol>
<li><strong>Say it is for sale, in the first line.</strong> Not “coming soon”, not a logo. The words “this domain is for sale”.</li>
<li><strong>Show the name large.</strong> Seeing a name set as a headline is how a buyer pictures it on a sign or a slide.</li>
<li><strong>Give a price or a clear route to one.</strong> A buy-now figure, a make-offer button with a stated minimum, or “price on request” with a promise of a number.</li>
<li><strong>Offer one obvious next step.</strong> One button. Buy, offer or ask.</li>
<li><strong>Explain how payment is protected.</strong> Two sentences on escrow remove the biggest fear a first-time buyer has: paying a stranger for something invisible.</li>
</ol>

<h2 id="price-display">Exact price, range or nothing</h2>
<p>An exact price converts best on names up to the low thousands, because a buyer can decide alone. A stated minimum offer filters out the $50 messages without capping the top. Showing nothing only makes sense for names where you truly want every inquiry, and you are willing to answer each one fast.</p>
<p>If you offer monthly payments, put the monthly figure beside the full price. Large portfolio sellers such as HugeDomains show a payment plan on their own for-sale pages, and investor Elliot Silver has pointed out that buyers who meet those pages first may come to expect the option everywhere. The <a href="../tools/payment-plan.html">payment plan tool</a> gives you the figure and the wording.</p>

<h2 id="trust">Trust is technical too</h2>
<ul>
<li><strong>HTTPS.</strong> A browser warning on a page asking for money ends the sale. Any modern static host gives you a certificate for free.</li>
<li><strong>Speed.</strong> The page should be one small file. No frameworks, no tracking pile-up, no slideshow.</li>
<li><strong>Works on a phone.</strong> A large share of type-in visits come from phones. Check yours on one.</li>
<li><strong>A real route to a person.</strong> A form or address that reaches you, tested this month.</li>
</ul>

<h2 id="chat">Chat widgets and other extras</h2>
<p>Live chat helps if you will actually be there to answer within minutes. Some marketplaces build chat into their own pages for this reason. If you cannot staff it, an unanswered chat box is worse than none. The same goes for visitor counters, “3 people are looking at this name” banners and countdown timers: if they are not true, they are a lie, and if they are true, they rarely help.</p>

<h2 id="copy">What to write</h2>
<p>One sentence on who the name suits is enough. “A short name for a payments product” does more than a paragraph about brand equity. Three plain selling points at most: length, how easily it is said aloud, the extension. Never claim traffic, revenue or interest you cannot prove on request.</p>

<h2 id="test">Test it like a buyer</h2>
<p>Open the name in a private window on your phone. Time how long it takes to understand that it is for sale and what to do next. Press the button and confirm the message arrives. Then ask someone outside the business to do the same while you watch. Fix whatever made them hesitate.</p>
""",
        "sources": [
            ("DN.org, domain landing pages (pricing display, minimum offers, chat, SSL)", "https://dn.org/category/domain-landing-pages"),
            ("DomainInvesting.com, “Offer an installment plan”", "https://domaininvesting.com/offer-an-installment-plan"),
            ("Saw.com, seller page (for-sale pages, chat, lease-to-own)", "https://saw.com/sell"),
            ("Efty Investor (landing pages and storefront)", "https://www.efty.com/products/efty_investor/"),
        ],
    },
    {
        "slug": "outbound",
        "title": "Outbound that gets replies instead of blocks",
        "desc": "How to find the few companies a name really fits, write a 90-word email that respects them, follow up twice, and stay clear of spam and trademark trouble.",
        "mins": 7,
        "tool": ("tools/pitch-writer.html", "Draft the three emails"),
        "body": """
<p class="lede">Outbound has a bad name because most of it is bad: hundreds of identical emails to scraped addresses. Done properly it is the opposite. It is ten or twenty messages to companies for whom the name is plainly useful, written as one business person to another.</p>

<h2 id="who">Finding the right ten</h2>
<p>Good prospects share one trait: you can finish the sentence “this name helps them because…” with something specific.</p>
<ul>
<li><strong>The upgrade.</strong> A company operating on a longer or clumsier version of the same name: a prefix like “get” or “try”, a hyphen, a lesser extension.</li>
<li><strong>The exact match.</strong> Businesses whose main product is the phrase in the name.</li>
<li><strong>The advertiser.</strong> Companies already paying for search ads on the keyword. They have told you what the phrase is worth to them.</li>
<li><strong>The local operator.</strong> For city-plus-service names, the established firms in that city.</li>
</ul>
<p>Then find a person. Founder, head of marketing or brand lead. An email to “info@” is a coin toss; an email to the person whose job the name affects is a conversation.</p>

<h2 id="email">The email</h2>
<p>Keep the first message under about 90 words and give it four parts: what you own, why it fits them in one sentence, how a purchase would work, and an easy way to say no.</p>
<ul>
<li>Use a plain subject: the domain name itself works.</li>
<li>State the price, or say you are open to an offer. Hiding both wastes a round trip.</li>
<li>Mention escrow. It answers the question “how do I know this is real?” before it is asked.</li>
<li>No urgency you invented. No “other buyers are circling” unless they are.</li>
</ul>

<h2 id="follow-up">Follow up twice, then stop</h2>
<p>Most replies come from the follow-up, because the first email arrived on a bad day. Send a short second note after about four working days and a closing note a week later. Three touches is persistent. Five is a nuisance, and it trains spam filters to treat your address as one.</p>

<h2 id="rules">The rules you have to follow</h2>
<p>This is general information, not legal advice, and the rules differ by country.</p>
<ul>
<li><strong>United States.</strong> The CAN-SPAM Act applies to commercial email, including one-to-one business email. Use accurate sender details and subject lines, include a valid postal address, and honour any request to stop.</li>
<li><strong>Canada.</strong> The anti-spam law there is consent-based. Implied consent can cover a business address that was conspicuously published without a no-solicitation notice, when your message relates to the recipient’s business role. You must still identify yourself and include a working unsubscribe mechanism. The conditions are narrow, so read the regulator’s guidance before you write to Canadian companies.</li>
<li><strong>Europe and the United Kingdom.</strong> Data protection and e-privacy rules apply to named individuals’ addresses, and member states treat business email differently. When in doubt, use the company’s published contact form.</li>
</ul>

<h2 id="trademarks">The line you must not cross</h2>
<p>Never offer a name to the owner of a matching trademark. Under the dispute policy that governs most extensions, registering or holding a name mainly to sell it to the trademark owner is listed as evidence of bad faith. An outbound email to that owner hands them the evidence. If a name only makes sense because of someone else’s brand, the right move is to let it expire, not to pitch it.</p>
<p>Generic words and phrases are different. Offering a dictionary-word name to companies in the industry it describes is ordinary commerce. The test is whether the value comes from the language or from a specific company’s reputation.</p>

<h2 id="track">Keep score</h2>
<p>A simple sheet: company, person, date sent, follow-ups, reply, outcome. After fifty emails you will know your reply rate and which angle earns it. That is worth more than any template.</p>
""",
        "sources": [
            ("GoDaddy, “Everything you need to know about working with a domain broker” (identifying likely buyers)", "https://www.godaddy.com/resources/skills/how-to-work-with-domain-broker"),
            ("U.S. Federal Trade Commission, CAN-SPAM Act compliance guide", "https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business"),
            ("CRTC, frequently asked questions about Canada’s anti-spam legislation", "https://crtc.gc.ca/eng/com500/faq500.htm"),
            ("WIPO, guide to the Uniform Domain Name Dispute Resolution Policy (paragraph 4(b), evidence of bad faith)", "https://www.wipo.int/en/web/amc/domain-name-disputes/guide/index"),
        ],
    },
    {
        "slug": "payment-plans",
        "title": "Lease-to-own and payment plans",
        "desc": "Monthly payments let more buyers say yes. The three common structures, how to price the premium, and what protects you if the buyer stops paying.",
        "mins": 5,
        "tool": ("tools/payment-plan.html", "Work out the monthly figure"),
        "body": """
<p class="lede">A small company that cannot find $8,000 this month can often find $400 a month for two years. Offering that option does not lower your price. It widens the group of people who can pay it.</p>

<h2 id="structures">Three structures</h2>
<p>DomainEasy, a financing service, publishes the three shapes most plans take, along with the price ranges each tends to suit:</p>
<ul>
<li><strong>Lease-to-own.</strong> Equal monthly payments for a fixed term. The simplest form, used mostly for names from about $1,000 to $50,000.</li>
<li><strong>Deposit plan.</strong> A larger first payment, then equal instalments on the balance. Common from about $50,000 to $500,000, where the seller wants real commitment up front.</li>
<li><strong>Balloon plan.</strong> Lower monthly payments with a large final payment. Used at the top of the market, where the buyer expects funding or revenue to arrive before the end of the term.</li>
</ul>
<p>In all three the buyer normally gets use of the name from the first payment, and ownership passes only after the last.</p>

<h2 id="premium">Should a plan cost more than cash?</h2>
<p>Usually yes, modestly. You are carrying risk and waiting for your money. A premium of 10% to 25% over the cash price across a one-to-three-year term is easy to explain and easy to accept. Show both numbers, so the saving for paying in full is visible. Some sellers charge no premium at all and treat the plan purely as a way to close more sales. That is a legitimate choice on lower-priced names.</p>

<h2 id="protection">What protects the seller</h2>
<ul>
<li><strong>The name stays out of the buyer’s control until it is paid for.</strong> Either it remains in an account you or the platform controls with the nameservers pointed where the buyer asks, or it sits with an escrow holding service.</li>
<li><strong>A written default clause.</strong> If payments stop, use of the name ends and payments made are not refunded. State the grace period in days.</li>
<li><strong>No transfer mid-plan.</strong> Portfolio sellers who offer plans say the same in their own terms: the name cannot move to another registrar until every payment has cleared.</li>
</ul>
<p>Escrow.com’s domain holding service is one way to arrange this at arm’s length. Its published terms run from a minimum of three months to a maximum of five years, and it charges for changes to the schedule or to the name’s technical settings during the term, so agree the schedule properly at the start.</p>

<h2 id="buyer-side">What the buyer should understand</h2>
<p>Put these in plain words on the listing, because a buyer who misunderstands will resent you later:</p>
<ul>
<li>They are building on a name they do not yet own. If they stop paying, the site and email on it stop too.</li>
<li>They can usually pay the balance early.</li>
<li>They can usually walk away; they simply lose what they have paid.</li>
</ul>

<h2 id="when-not">When not to offer a plan</h2>
<p>Skip it on names under a few hundred dollars, where the administration costs more than the benefit. Be careful with buyers you cannot identify. And do not agree a term so long that renewals, platform fees and your own attention eat the premium.</p>
""",
        "sources": [
            ("DomainEasy, domain financing (plan types and price ranges)", "https://domaineasy.com/financing"),
            ("Escrow.com, secure domain name holding", "https://www.escrow.com/domain-name-holding"),
            ("Identity Digital, premium catalog FAQ (financing and leasing terms)", "https://identity.digital/premium-catalog"),
            ("Domain Lions, comparison of premium-domain sellers (payment-plan transfer terms)", "https://www.domainlions.com/compare/best-places-to-buy-premium-domains"),
        ],
    },
    {
        "slug": "expired-domains",
        "title": "What happens when a domain expires",
        "desc": "The stages between an expiry date and a name becoming available again, where auctions fit in, and how backorders work.",
        "mins": 5,
        "tool": ("tools/expiry-timeline.html", "Map the dates for a name"),
        "body": """
<p class="lede">An expired domain does not become available the next morning. It passes through a sequence that can last more than two months, and for any name worth having it is usually sold at auction before the sequence ends.</p>

<h2 id="stages">The stages</h2>
<ol>
<li><strong>Expiry.</strong> The registration lapses. The website and email normally stop within days. The owner can still renew at the usual price.</li>
<li><strong>Registrar grace period.</strong> The registrar holds the name for a period it sets itself, anywhere from zero to 45 days. This is the important window, because most large registrars now send unrenewed names to an auction partner during it. As DomainSherpa’s long-running guide explains, each registrar is tied to one auction service, so where a name is registered decides where it will be sold.</li>
<li><strong>Redemption.</strong> If nobody bought the name, it enters a 30-day period in which only the previous owner can recover it, by paying a redemption fee on top of the renewal.</li>
<li><strong>Pending delete.</strong> Five days in which nothing can be done.</li>
<li><strong>Release.</strong> The registry frees the name. Drop-catching services fire registration requests the instant it happens.</li>
</ol>
<p>That is the standard pattern for generic extensions such as .com and .net. Country-code extensions set their own rules, and some skip stages entirely.</p>

<h2 id="auctions">Expired-name auctions</h2>
<p>If a name you want is registered at a registrar with an auction partner, the auction is your route. The name never reaches release if someone bids. Formats vary: Dynadot, for example, describes seven-day auctions that extend by five minutes when a late bid arrives. Create the account, add the name to a watch list and decide your maximum before the last hour, not during it.</p>

<h2 id="backorders">Backorders and drop-catching</h2>
<p>For names that go all the way to release, you need a backorder: an instruction to a drop-catching service to try to register the name the moment it frees up. You normally pay only if the service succeeds.</p>
<p>Two practical points, both from Domain Name Wire’s comparisons of the main platforms. First, services differ in who may bid once a name is caught: on some, only people who placed a backorder take part in the auction; on at least one large service the auction is open to every customer, so your research can be rewarded with a bidding war. Second, no service wins every name, so serious buyers place the same backorder at more than one.</p>

<h2 id="evaluate">Is the name worth chasing?</h2>
<ul>
<li><strong>Why did it expire?</strong> A business that closed is neutral. A name abandoned after a dispute or a penalty is not.</li>
<li><strong>What was on it?</strong> Look at archived copies of the old site. Spam, counterfeit goods or adult content leave a mark that can take years to fade.</li>
<li><strong>Is it somebody’s brand?</strong> An expired name that matches a live trademark is a liability, not an asset.</li>
<li><strong>Would you register it fresh at ten times the fee?</strong> If not, the excitement is about the auction, not the name.</li>
</ul>

<h2 id="own-names">If it is your name that is expiring</h2>
<p>Turn on auto-renew for anything you would be sorry to lose and keep the payment card current. If you mean to let a name go, decide on purpose: list it at wholesale a month before expiry and see whether another investor wants it.</p>
""",
        "sources": [
            ("DomainSherpa, “How to Grab an Expiring Domain Name”", "https://domainsherpa.com/how-to-grab-an-expiring-domain-name/"),
            ("InterNetX Snapshot, “What is the domain aftermarket?”", "https://snapshot.internetx.com/en/what-is-the-domain-aftermarket/"),
            ("Dynadot domain market (auction rules)", "https://www.dynadot.com/market"),
            ("Domain Name Wire, “Comparing expired domain name platforms”", "https://domainnamewire.com/2021/03/18/comparing-expired-domain-name-platforms/"),
        ],
    },
    {
        "slug": "closing-safely",
        "title": "Closing the sale safely: escrow, transfer and scams",
        "desc": "How a domain sale actually completes, what escrow costs, how the name moves between accounts, and the scams aimed at sellers.",
        "mins": 5,
        "tool": ("tools/net-proceeds.html", "See escrow fees against commissions"),
        "body": """
<p class="lede">Agreeing a price is the middle of a sale, not the end. Money has to move one way and a domain the other, between two parties who have usually never met. Escrow exists to make that safe for both.</p>

<h2 id="how-escrow-works">How escrow works</h2>
<p>Escrow.com, the service most domain sales use, describes the sequence on its domains page. In short:</p>
<ol>
<li>Buyer and seller agree the terms inside the escrow service.</li>
<li>The buyer pays the escrow company, which holds the money in a trust account.</li>
<li>The seller transfers the domain to the buyer.</li>
<li>The escrow company checks the public registration record to confirm the buyer now holds the name.</li>
<li>Only then is the seller paid.</li>
</ol>
<p>The seller never sends a domain to someone who has not paid, and the buyer never pays for a domain that does not arrive.</p>

<h2 id="cost">What it costs and who pays</h2>
<p>The published fee starts at 2.6% with a $50 minimum for domains up to $5,000 and falls in steps as the price rises. A concierge option, where the escrow company holds the name in its own registrar account during the handover, starts at 5.2%. Who pays is negotiable: the buyer, the seller or a split. Settle it before you agree the price, because on a small sale the fee is a real share of the money.</p>
<p>Marketplaces generally bundle payment handling into their commission, so you do not pay escrow on top.</p>

<h2 id="transfer">Moving the name</h2>
<ul>
<li><strong>Account push.</strong> If buyer and seller use the same registrar, the name moves between accounts in minutes. This is the fastest and least error-prone method, and it is worth asking the buyer to open a free account at your registrar to use it.</li>
<li><strong>Registrar transfer.</strong> Unlock the name, give the buyer the authorisation code, and they start a transfer at their registrar. Allow five to seven days.</li>
</ul>
<p>Two things delay transfers: a name registered or transferred very recently may be locked for a period, and a transfer usually adds a year of registration that somebody has to pay for. Check both before promising a date.</p>

<h2 id="scams">Scams aimed at sellers</h2>
<ul>
<li><strong>The paid appraisal.</strong> A buyer offers a generous price but insists on a valuation from a named service first, at your cost. There is no buyer. The appraisal fee is the scam.</li>
<li><strong>The fake escrow site.</strong> The buyer proposes an escrow company you have not heard of, with a convincing website. Type the address of a licensed service yourself; never follow a link from the other party.</li>
<li><strong>The overpayment.</strong> A payment arrives for more than the price with a request to refund the difference. The original payment later reverses.</li>
<li><strong>The reversible payment.</strong> Card and wallet payments can be disputed for months. For anything above pocket money, use escrow or a marketplace checkout.</li>
<li><strong>The verification code.</strong> Someone asks you to read back a code sent to your phone or email “to confirm ownership”. It is the reset code for your registrar account.</li>
</ul>

<h2 id="checklist">A closing checklist</h2>
<ol>
<li>Price, currency, who pays the fee and the transfer method agreed in writing.</li>
<li>Transaction opened at the escrow service by you, or checked by you at an address you typed.</li>
<li>Payment confirmed as received by the escrow service, in its dashboard, before you move anything.</li>
<li>Name transferred; buyer confirms; funds released.</li>
<li>Remove the listing everywhere else the same day.</li>
</ol>
""",
        "sources": [
            ("Escrow.com, domain and website escrow (process and fees)", "https://www.escrow.com/domains"),
            ("Escrow.com, domain concierge service", "https://escrow.com/domain-concierge"),
            ("Instant Domain Search, appraisal FAQ (paid-appraisal warning)", "https://instantdomainsearch.com/domain-appraisal"),
        ],
    },
    {
        "slug": "portfolio-math",
        "title": "Portfolio math: sell-through, renewals and the drop list",
        "desc": "The four numbers that decide whether a domain portfolio makes money, and a yearly routine for cutting the names that cannot pay their way.",
        "mins": 5,
        "tool": ("tools/portfolio-math.html", "Open the portfolio calculator"),
        "body": """
<p class="lede">A domain portfolio is a small business with one kind of cost and one kind of income. Four numbers describe it completely, and most owners know only one of them.</p>

<h2 id="four-numbers">The four numbers</h2>
<ul>
<li><strong>Names held.</strong> The count you renew each year.</li>
<li><strong>Carrying cost.</strong> Names held multiplied by your average renewal fee. This is due whether or not anything sells.</li>
<li><strong>Sell-through rate.</strong> The share of your names that sell in a year. One sale from a hundred names is 1%.</li>
<li><strong>Average net price.</strong> What you actually keep per sale after commission.</li>
</ul>
<p>Profit is sales income minus carrying cost minus whatever you spent on new names. Everything else is detail.</p>

<h2 id="worked">A worked example</h2>
<p>Take 400 names at $12 a year to renew. Carrying cost is $4,800. Suppose 1.5% sell, so six names a year, at an average of $2,400 before a 15% commission. That is $14,400 gross and $12,240 kept, for a profit of $7,440 before any new purchases.</p>
<p>Now change one input. If sell-through is 0.5% instead, two names sell, you keep $4,080, and the portfolio loses $720 a year. Nothing else moved. This is why sell-through, not the size of the list, is the number to watch.</p>

<h2 id="floor">The floor price for a name</h2>
<p>Each name has to earn its own renewal. Divide the renewal fee by your sell-through rate and by the share you keep after commission. In the example above: $12 ÷ 1.5% ÷ 85% ≈ $940. A name that could not realistically sell for about $940 is, on average, costing you money to hold. At 0.5% sell-through the same sum gives about $2,820.</p>
<p>Bill Hartzer’s 2026 analysis of holding costs reached a similar order of magnitude for a hand-registered .com, which is a useful sanity check on your own figure.</p>

<h2 id="levers">Three levers, in order of speed</h2>
<ol>
<li><strong>Cut.</strong> Dropping names below the floor improves the result at the next renewal date. It is the only lever that works immediately.</li>
<li><strong>Raise sell-through.</strong> Prices on every name, working for-sale pages, a network listing, and outreach on the best ten. These take a few months to show.</li>
<li><strong>Raise average price.</strong> Better buying, and firmer negotiation on the top tenth of the list. This takes years, because it depends on what you acquire.</li>
</ol>

<h2 id="routine">A yearly routine</h2>
<ol>
<li>Once a year, export the list and record the four numbers. Use real figures from the past twelve months, not hopes.</li>
<li>Rank names by your honest price estimate. Mark everything under the floor.</li>
<li>For each marked name ask one question: is there a specific reason it is worth more than it looks? Traffic, an inquiry on file, a buyer you can name. If not, let it go.</li>
<li>Before a marked name expires, offer it to other investors at wholesale. Small money is better than none.</li>
<li>Put the renewal money you saved into marketing the top of the list, not into more names.</li>
</ol>

<h2 id="honesty">Being honest with the inputs</h2>
<p>The calculator is only as good as what you type into it. Two habits keep it honest. Measure sell-through over at least two years, because one good sale distorts a single year. And count every cost: renewals, marketplace subscriptions, tools, and the names you bought and later dropped.</p>
""",
        "sources": [
            ("Domain Details, portfolio manager (sell-through and commission tracking)", "https://portfolio.domaindetails.com/"),
            ("Bill Hartzer, “Domain Parking Is Finished: What the 2025 Numbers Show”", "https://www.billhartzer.com/?p=18461"),
        ],
    },
    {
        "slug": "social-and-community",
        "title": "Marketing a domain in public: social posts and communities",
        "desc": "Where posting a name for sale helps, where it only reaches other sellers, and how to write a listing people read.",
        "mins": 5,
        "tool": ("tools/listing-copy.html", "Draft listing and social copy"),
        "body": """
<p class="lede">Posting “great domain for sale!” to an audience of other people selling domains is the most common wasted hour in this business. Public marketing works when the post reaches people who build things, and when it gives them a reason to care.</p>

<h2 id="two-audiences">Two audiences, two prices</h2>
<p>Investor communities are full of knowledgeable buyers who pay investor prices. That is useful when you want to turn names into cash this week, and useless when you are hoping for a retail sale. Founder and industry audiences are the reverse: fewer buyers, slower, and far better prices. Decide which sale you are after before choosing where to post.</p>

<h2 id="investor-communities">Selling in investor communities</h2>
<p>The large forums run structured marketplaces. NamePros, for example, publishes standard sale templates, including a reverse auction that starts at a buy-now price and falls until someone takes it, and it expects members to leave trader ratings after each deal.</p>
<ul>
<li><strong>Use the template.</strong> Price, registrar, expiry date and payment method, every time. Missing details read as inexperience.</li>
<li><strong>Price for investors.</strong> If your number assumes an end user, it is the wrong venue.</li>
<li><strong>Build a record.</strong> A handful of clean small deals makes the larger ones possible.</li>
<li><strong>Read the rules.</strong> Each marketplace section has its own, and moderators enforce them.</li>
</ul>

<h2 id="founder-audiences">Reaching founders and marketers</h2>
<p>On general platforms, a domain post competes with everything else in the feed. Three things help:</p>
<ul>
<li><strong>Lead with the use, not the asset.</strong> “A short name for a logistics startup” gives the right reader something to recognise. “Premium domain” gives nobody anything.</li>
<li><strong>Show it.</strong> The name set large, as it would look on a homepage. A single clean image beats a paragraph.</li>
<li><strong>Ask for introductions.</strong> “If you know someone naming a product in this space” is easier to act on than “buy this”.</li>
</ul>
<p>Post from an account that says who you are. Anonymous accounts selling domains look like every scam the reader has already blocked.</p>

<h2 id="write-the-listing">Writing a listing people finish</h2>
<ol>
<li><strong>First line:</strong> the name and that it is for sale.</li>
<li><strong>Second line:</strong> who it suits, concretely.</li>
<li><strong>Three facts:</strong> length, extension, how it sounds aloud.</li>
<li><strong>How to buy:</strong> price or offer route, and escrow.</li>
</ol>
<p>Stop there. Leave out superlatives, estimated “values” from tools, and anything you could not back up if asked.</p>

<h2 id="newsletters">Newsletters and sponsorships</h2>
<p>The trade publications in this industry are funded by sponsors, and several sell newsletter or banner placements. One of the better-known reports its banner positions as sold out, which tells you both that the audience is real and that it is an audience of the industry itself. That fits a portfolio, a new marketplace or a service. It rarely fits a single mid-priced name.</p>

<h2 id="etiquette">Etiquette that keeps accounts alive</h2>
<ul>
<li>Do not reply to strangers’ posts with your name for sale.</li>
<li>Do not tag companies you hope will buy.</li>
<li>Post a given name once per venue, then leave it. Repetition gets muted.</li>
<li>Answer every serious question, in public where possible. Other readers are watching how you deal.</li>
</ul>
""",
        "sources": [
            ("NamePros, domain auctions guide (templates and trader ratings)", "https://www.namepros.com/threads/domain-auctions-guide.861616/"),
            ("DomainInvesting.com (advertising positions)", "https://domaininvesting.com/guide/list-of-domain-brokers/"),
            ("Domain Name Wire (newsletter and podcast)", "https://domainnamewire.com/"),
        ],
    },
    {
        "slug": "working-with-a-broker",
        "title": "Working with a domain broker",
        "desc": "What a broker does for the commission, when one is worth it, what the agreement should say, and how to brief them.",
        "mins": 5,
        "tool": ("plan.html", "Check whether your name needs a broker"),
        "body": """
<p class="lede">A broker is worth the fee when the hard part of the sale is finding one particular buyer and getting them to a number. For most names that is not the hard part, and a marketplace listing does the job for less.</p>

<h2 id="what-they-do">What a broker actually does</h2>
<p>Bill Sweetman’s guide for GoDaddy describes the work plainly. A broker sets a realistic price expectation, tracks down likely buyers or a hidden owner, runs the negotiation, and oversees the payment and transfer. On the selling side, the part that matters most is proactive: building a list of the most probable buyers and contacting them, instead of waiting for someone to stumble on the name.</p>
<p>Brokers work for one side. A seller’s broker is paid to get you the highest price. A buyer’s broker is paid to acquire a name, often anonymously, for the least. Know which you are talking to.</p>

<h2 id="cost">What it costs</h2>
<p>DomainInvesting.com’s directory of brokers puts typical commission at 10% to 20% of the sale price. Published examples sit inside that range: Saw.com lists full-service brokerage at 15%, and Dynadot charges 15% for outbound brokerage, which it reserves for names it judges to be worth roughly $200,000 or more.</p>
<p>That threshold is the useful signal. Outbound work is expensive in hours. A broker takes it on when the commission can repay those hours, which generally means five figures at the least.</p>

<h2 id="when">When a broker makes sense</h2>
<ul>
<li>The name is a one-word .com, a short acronym or a category-defining phrase.</li>
<li>The plausible buyers are large companies you cannot reach yourself.</li>
<li>You have had serious inquiries and suspect you are leaving money on the table.</li>
<li>You do not want your identity known in the negotiation.</li>
</ul>
<p>It does not make sense for a name priced in the low thousands, for a name with no identifiable buyer, or as a way to avoid setting a price.</p>

<h2 id="agreement">What the agreement should say</h2>
<ul>
<li><strong>Exclusivity and its length.</strong> Nearly every broker requires it. Ninety days is common; a year is long. Ask what happens to buyers the broker contacted if they come back after the term.</li>
<li><strong>Commission and what it is charged on.</strong> The full sale price, or the price net of escrow fees.</li>
<li><strong>Your reserve.</strong> The price below which the broker will not bring you offers, and whether it can be revised.</li>
<li><strong>Escrow.</strong> The guide above recommends a licensed escrow service even where a brokerage offers its own.</li>
<li><strong>Confidentiality.</strong> Whether the price may be reported publicly after the sale. Reported sales help the broker; they may or may not help you.</li>
</ul>

<h2 id="choose">Choosing one</h2>
<p>Ask for sales of similar names at similar prices, not their biggest deal. Ask who will do the work, since at larger firms it may not be the person you spoke to first. The Internet Commerce Association publishes best practices for brokers, and a broker who has never heard of them is telling you something.</p>

<h2 id="brief">Briefing them well</h2>
<p>Give the broker every past inquiry, with dates and amounts. Tell them your real floor. Share anything that affects value: traffic, old trademarks, previous use. Then answer their messages quickly. Deals at this level die of delay more often than of price.</p>
""",
        "sources": [
            ("GoDaddy, “Everything you need to know about working with a domain broker” by Bill Sweetman", "https://www.godaddy.com/resources/skills/how-to-work-with-domain-broker"),
            ("DomainInvesting.com, “Domain Brokers: How to Hire One to Buy or Sell a Domain”", "https://domaininvesting.com/guide/list-of-domain-brokers/"),
            ("Saw.com, brokerage service options", "https://saw.com/sell"),
            ("Dynadot, brokerage service help article", "https://www.dynadot.com/help/question/sell-domain-broker-service"),
            ("Afternic, domain brokerage", "https://www.afternic.com/domain-broker"),
        ],
    },
    {
        "slug": "what-makes-a-name-sell",
        "title": "What makes a domain name sell",
        "desc": "The handful of traits buyers pay for, the ones that quietly kill a sale, and how the 2026 sales record backs them up.",
        "mins": 5,
        "tool": ("tools/name-score.html", "Score a name on these traits"),
        "body": """
<p class="lede">Buyers do not pay for domains. They pay for what a name does: it gets remembered, typed correctly, trusted on sight. Every trait that raises a price is a version of one of those three.</p>

<h2 id="traits">The traits that raise a price</h2>
<ul>
<li><strong>Short.</strong> Fewer characters mean fewer mistakes and more room on a sign. Value falls off quickly past about ten characters.</li>
<li><strong>Real words.</strong> One dictionary word is the top of the market. Two words that belong together come next. Three need a reason.</li>
<li><strong>Passes the phone test.</strong> Say it once to someone and ask them to type it. If they get it wrong, so will customers.</li>
<li><strong>The right extension.</strong> .com remains the default that needs no explanation. A few others carry weight in particular fields.</li>
<li><strong>Commercial meaning.</strong> A word tied to a category where companies spend heavily to win customers is worth more than an equally nice word that is not.</li>
</ul>
<p>The public appraisal tools weigh the same things. GoDaddy lists memorability, word count and how common the phrase is. Instant Domain Search scores length, word type, familiarity, brandability and extension, and gives brandability the heaviest weight.</p>

<h2 id="penalties">The traits that lower it</h2>
<ul>
<li><strong>Hyphens.</strong> People leave them out when typing, which sends visitors to whoever owns the unhyphenated version.</li>
<li><strong>Digits mixed with letters.</strong> “4” or “for”? Every ambiguity is a lost visit.</li>
<li><strong>Filler prefixes.</strong> “Get”, “my”, “the” and “try” mark a name as the second choice. The scoring tools penalise them for that reason.</li>
<li><strong>Awkward letter joins.</strong> Where one word ends with the letter the next begins with, readers stumble.</li>
<li><strong>Someone else’s brand.</strong> Not a discount but a disqualification. A name that trades on a trademark is a legal problem, not a product.</li>
</ul>

<h2 id="record">What the 2026 record shows</h2>
<p>DNJournal’s year-to-date chart of the largest publicly reported sales, through mid-November 2026, is led by Shop.com at $99 million and AI.com at $70 million, with Club.com, Green.com and Tokens.com rounding out the top five. Every one is a single short dictionary word or a two-letter term on .com.</p>
<p>Lower down the same chart, .ai names appear repeatedly at six and seven figures. That is the “right extension” rule at work: an extension that happens to spell the name of a fast-growing industry is carrying real weight in that industry and almost none outside it.</p>
<p>The market underneath is still growing. The latest Domain Name Industry Brief counted 411.6 million registrations across all extensions at the end of the third quarter of 2026, up 8.7% on a year earlier. More registered names means fewer good ones left to hand-register, which is the basic reason an aftermarket exists.</p>

<h2 id="brandables">Coined names</h2>
<p>Invented names follow different rules, because there is no dictionary meaning to lean on. They sell on sound and look: five to eight letters, alternating consonants and vowels, one obvious pronunciation, no accidental meaning in another major language. Curated marketplaces for these names present each with a logo for a reason. A coined name is easier to value once you can see it as a brand.</p>

<h2 id="buying-rule">A rule for buying</h2>
<p>Before registering or bidding, name three kinds of business that could use the name as their main address, and say the name aloud to someone who has not seen it written. If you cannot do the first, or they cannot spell the second, keep your money.</p>
""",
        "sources": [
            ("DNJournal, 2026 year-to-date top 100 domain sales chart", "https://dnjournal.com/ytd-sales-charts.htm"),
            ("Verisign blog, Domain Name Industry Brief quarterly report (Q3 2026)", "https://blog.verisign.com/"),
            ("GoDaddy domain value appraisal (value factors)", "https://www.godaddy.com/domain-value-appraisal"),
            ("Instant Domain Search, free domain appraisal (scoring factors and penalties)", "https://instantdomainsearch.com/domain-appraisal"),
            ("BrandBucket (brandable names presented with logos)", "https://www.brandbucket.com/"),
        ],
    },
]
