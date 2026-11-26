/* Domain Marketing — tools. Everything runs in the browser; nothing typed here is sent anywhere
   unless the visitor submits a form. All figures are rule-of-thumb planning numbers, not appraisals. */
(function () {
  "use strict";
  var DM = window.DM || (window.DM = {});
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var ROOT = document.body.getAttribute("data-root") || "";

  /* ------------------------------------------------------------------ helpers */
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function num(v, d) { var n = parseFloat(String(v).replace(/[^0-9.\-]/g, "")); return isFinite(n) ? n : (d || 0); }
  function money(n) { var neg = n < 0; n = Math.abs(Math.round(n)); return (neg ? "−$" : "$") + n.toLocaleString("en-US"); }
  function nice(n) {
    if (n < 50) return Math.max(5, Math.round(n / 5) * 5);
    var p = Math.pow(10, Math.floor(Math.log10(n)) - 1);
    return Math.round(n / p) * p;
  }
  function short(n) {
    if (n >= 1e6) return "$" + (n / 1e6).toFixed(n >= 1e7 ? 0 : 1).replace(/\.0$/, "") + "M";
    if (n >= 1e4) return "$" + Math.round(n / 1e3) + "k";
    if (n >= 1e3) return "$" + (n / 1e3).toFixed(1).replace(/\.0$/, "") + "k";
    return "$" + Math.round(n);
  }
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function pick(arr, seed, i) { return arr[(seed + (i || 0) * 7) % arr.length]; }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function fmtDate(d) { return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" }); }
  function jsonFrom(id) { var n = document.getElementById(id); if (!n) return null; try { return JSON.parse(n.textContent); } catch (e) { return null; } }
  function on(el, ev, fn) { if (el) el.addEventListener(ev, fn); }

  function parseDomain(raw) {
    var s = String(raw || "").trim().toLowerCase();
    if (/\s/.test(s)) return { ok: false };
    s = s.replace(/^[a-z]+:\/\//, "").replace(/^www\./, "").split(/[\/?#]/)[0].replace(/\.+$/, "");
    if (!s) return { ok: false };
    if (s.indexOf(".") === -1) s += ".com";
    var parts = s.split(".");
    var sld = parts[0], tld = parts.slice(1).join(".");
    if (!/^[a-z0-9-]{1,63}$/.test(sld) || !/^[a-z0-9.-]{2,24}$/.test(tld) || /^-|-$/.test(sld)) return { ok: false };
    return { ok: true, sld: sld, tld: tld, full: sld + "." + tld };
  }
  DM.parseDomain = parseDomain;

  /* ------------------------------------------------------------------ name scoring */
  var WORDS = ("home house car cars auto loan loans bank pay cash money credit card insurance insure health care med medical doctor dental " +
    "law legal lawyer attorney tax invest fund capital trade trading stock stocks crypto coin token chain block bit ai bot data cloud code dev app apps " +
    "web site net host hosting domain domains name names brand market marketing shop store buy sell sale deal deals best top pro plus hub lab labs base box " +
    "kit tool tools tech soft ware digital online media video music game games play sport sports fit fitness gym yoga food eat cook chef pizza coffee tea " +
    "wine beer bar travel trip tour fly flight hotel stay book books read learn school class course tutor study job jobs work career hire team group club " +
    "social chat talk meet date love pet pets dog cat baby kid kids mom family life live green solar energy power eco earth sun sky star moon sea ocean " +
    "river lake city town local global world north south east west new old big small fast quick easy simple smart safe secure free cheap luxury gold " +
    "silver blue red black white design art studio photo print style fashion beauty hair skin spa real estate property land rent rental lease build builder " +
    "roof plumber electric clean cleaning repair fix service services solutions systems partners agency consult consulting advisor coach expert guide " +
    "review reviews compare find search get my your our the go now today daily time day night one first next future open bright clear pure true good great " +
    "super mega ultra prime elite alpha omega zen nova vista wave flow spark shift sync link loop mint leaf seed root nest hive forge craft works logic " +
    "mind brain think idea vision view voice sound signal pulse wire grid stack node core edge peak summit bridge gate port path way road route map zone " +
    "space place point spot park garden farm fresh organic vegan bio pharma clinic therapy wellness vital senior student wedding event events ticket " +
    "tickets party gift gifts toy toys bike boat truck moving storage ship shipping freight logistics supply factory robot drone laser nano quantum cyber " +
    "security guard shield vault lock key pass wallet ledger mortgage lender broker agent realty homes condo office desk sales lead leads ads seo content " +
    "email mail news press blog wiki forum list index directory pages portal center central station depot outlet mart exchange auction bid offer price " +
    "value save saver discount coupon reward bonus win cedar harbor maple stone iron copper amber coral ivory jade onyx pearl ruby sage willow aspen birch " +
    "atlas beacon compass anchor harvest meadow orchard prairie canyon delta echo ember frost glow halo horizon lumen orbit pixel prism quill ripple summit " +
    "thrive unity valor zenith quote quotes ledger meals meal kitchen table plate rider drive driver fleet cargo parcel courier doctor nurse patient " +
    "tutor mentor founder startup venture equity budget invoice payroll hiring talent resume coding python cloud server cyber pilot rocket planet galaxy").split(/\s+/);
  var DICT = {}; WORDS.forEach(function (w) { DICT[w] = 1; });
  var INTENT = {
    100: "loan loans bank credit insurance insure mortgage lender invest fund capital trade trading tax law legal lawyer attorney pay payroll invoice equity",
    85: "health medical doctor dental clinic therapy pharma realty estate property homes condo ai crypto coin token wallet ledger security cyber cloud data solar energy",
    70: "shop store buy deal deals travel hotel flight trip software app apps hosting marketing seo leads sales jobs career hire course learn school car auto",
  };
  var IW = {}; Object.keys(INTENT).forEach(function (k) { INTENT[k].split(" ").forEach(function (w) { IW[w] = +k; }); });
  var TLD = { com: 100, ai: 78, io: 68, co: 62, org: 62, net: 58, app: 50, dev: 48, me: 42, tv: 42, xyz: 40, info: 30, biz: 28,
    shop: 34, store: 34, online: 34, tech: 36, site: 30, us: 50, uk: 50, "co.uk": 56, ca: 52, de: 56, fr: 50, in: 46, au: 46, "com.au": 54, eu: 44, nl: 50, es: 46, it: 46 };

  function segment(s) {
    var n = s.length, best = new Array(n + 1), i, j;
    best[0] = [];
    for (i = 1; i <= n; i++) {
      for (j = Math.max(0, i - 14); j < i; j++) {
        var w = s.slice(j, i);
        if (best[j] && DICT[w] && (w.length > 1 || w === "a")) {
          var cand = best[j].concat(w);
          if (!best[i] || cand.length < best[i].length) best[i] = cand;
        }
      }
    }
    return best[n] || null;
  }
  function pronounceable(s) {
    if (!/[aeiouy]/.test(s)) return false;
    if (/[^aeiouy]{4,}/.test(s) || /[aeiou]{4,}/.test(s)) return false;
    if (/(.)\1\1/.test(s)) return false;
    var v = (s.match(/[aeiouy]/g) || []).length / s.length;
    return v >= 0.25 && v <= 0.65;
  }

  function score(raw) {
    var d = parseDomain(raw);
    if (!d.ok) return null;
    var sld = d.sld, tld = d.tld, letters = sld.replace(/-/g, ""), L = letters.length;
    var hy = (sld.match(/-/g) || []).length, numeric = /^[0-9]+$/.test(letters), hasDigit = /[0-9]/.test(letters);
    var words = null, kind, clarity;
    if (numeric) { kind = "Numeric name"; clarity = L <= 4 ? 70 : 40; }
    else if (!hasDigit && L <= 3) { kind = L + "-letter name"; clarity = 92; }
    else {
      words = hasDigit ? null : (hy ? (function () { var out = []; var ok = sld.split("-").every(function (p) { var s = DICT[p] ? [p] : segment(p); if (!s) return false; out = out.concat(s); return true; }); return ok ? out : null; })() : (DICT[letters] ? [letters] : segment(letters)));
      if (words && words.length === 1) { kind = "One dictionary word"; clarity = 100; }
      else if (words && words.length === 2) { kind = "Two-word name"; clarity = 66; }
      else if (words && words.length === 3) { kind = "Three-word phrase"; clarity = 42; }
      else if (words && words.length > 3) { kind = "Long phrase"; clarity = 26; }
      else if (hy) { kind = "Hyphenated name"; clarity = 38; words = null; }
      else if (!hasDigit && pronounceable(letters)) { kind = "Coined or uncommon single term"; clarity = L <= 8 ? 60 : 48; words = null; }
      else { kind = "Hard-to-read string"; clarity = 22; words = null; }
    }
    var lenS = L <= 4 ? 100 : L <= 6 ? 88 : L <= 8 ? 74 : L <= 10 ? 62 : L <= 12 ? 50 : L <= 15 ? 36 : 22;
    var ext = TLD[tld] != null ? TLD[tld] : (tld.length === 2 ? 44 : 30);
    var intent = 30;
    if (words) { intent = 40; words.forEach(function (w) { if (IW[w] && IW[w] > intent) intent = IW[w]; }); }
    else if (kind.indexOf("Coined") === 0 || /letter name$/.test(kind)) intent = 40;
    var coined = kind.indexOf("Coined") === 0;
    var clean = numeric ? 100 : Math.max(0, 100 - 30 * hy - (hasDigit ? 22 : 0));
    var total = Math.round(0.25 * lenS + 0.30 * clarity + 0.20 * ext + 0.15 * intent + 0.10 * clean);
    if (kind === "Hard-to-read string") total = Math.min(total, 35);
    if (kind === "Long phrase") total = Math.min(total, 50);
    total = Math.max(1, Math.min(99, total));

    var mid = Math.pow(10, 1.55 + 0.028 * total), isCom = tld === "com";
    if (kind === "One dictionary word") mid *= isCom ? 25 : tld === "ai" ? 6 : ext >= 58 ? 2 : 1;
    else if (/letter name$/.test(kind)) mid *= isCom ? (L === 1 ? 400 : L === 2 ? 60 : 4) : (L <= 2 ? 3 : 1);
    else {
      if (!isCom) mid *= Math.pow(ext / 100, 1.5);
      if (kind === "Two-word name" && isCom && intent >= 85) mid *= 1.6;
      if (kind === "Hard-to-read string") mid *= 0.35;
    }
    if (hy) mid *= 0.45;
    var invLo = nice(mid * 0.05), invHi = nice(mid * 0.12);
    if (invHi <= invLo) invHi = invLo * 2;
    var bands = {
      investor: [invLo, invHi],
      market: [nice(mid * 0.6), nice(mid * 1.4)],
      enduser: [nice(mid * 1.6), nice(mid * 3.2)]
    };

    var notes = [], lifts = [];
    notes.push(kind + ", " + L + " character" + (L === 1 ? "" : "s") + ", on ." + tld + ".");
    if (words && words.length > 1) notes.push("Reads as: " + words.join(" + ") + ".");
    if (hy) lifts.push("The hyphen costs you: people type and say the unhyphenated version. Price at the low end, or go after the clean version.");
    if (hasDigit && !numeric) lifts.push("Mixed letters and digits fail the say-it-out-loud test. Lead with the use case, not the name, in your pitch.");
    if (!isCom) lifts.push("Find out who holds the .com. If a funded company uses it, they are your first outbound email. If it is parked at a high price, sell yours as the affordable alternative and say so on the page.");
    if (kind === "One dictionary word" && isCom) lifts.push("Do not put a low buy-now price on a one-word .com. Use make-offer with a floor, and talk to a broker before you answer the first inquiry.");
    if (kind === "Three-word phrase" || kind === "Long phrase") lifts.push("Long phrases sell on exact meaning. Put the use case in the first line of the for-sale page and target the handful of businesses it describes.");
    if (coined) lifts.push("This is not in our short word list, so it is scored as a coined name. Coined names sell on sound and look: add a simple logo mock and a one-line brand story to the listing.");
    if (kind === "Hyphenated name") lifts.push("Write out what the name means in the first line of the listing, because the words do not read cleanly on their own.");
    if (kind === "Hard-to-read string") lifts.push("If a stranger cannot read this aloud, it will not sell on name quality. Check whether it has traffic or an obvious buyer; if not, it is a drop candidate.");
    if (intent >= 85) lifts.push("The keyword sits in a high-spend category. Outbound to operating businesses in that category is worth the hour.");
    lifts.push("Before you fix a price, pull 10 to 12 comparable sales from a public sales database and see where this band sits against them.");

    return { full: d.full, sld: sld, tld: tld, kind: kind, words: words, score: total,
      parts: { "Length": lenS, "Clarity": clarity, "Extension": ext, "Buyer intent": intent, "Clean typing": clean },
      bands: bands, notes: notes, lifts: lifts };
  }
  DM.score = score;

  function verdict(s) { return s >= 85 ? "Top-shelf. Market it patiently." : s >= 70 ? "Strong. Worth active marketing." : s >= 55 ? "Sellable with the right buyer." : s >= 40 ? "Niche. Price to move or target hard." : "Weak on name quality alone."; }
  function bandText(b) { return short(b[0]) + " to " + short(b[1]); }

  function renderScore(el, r, compact) {
    if (!r) { el.innerHTML = '<p class="out-empty">That does not look like a domain name. Type something like <strong>yourname.com</strong>.</p>'; return; }
    try { sessionStorage.setItem("dm:last", JSON.stringify({ domain: r.full, score: r.score, kind: r.kind, market: bandText(r.bands.market) })); } catch (e) {}
    var q = "?domain=" + encodeURIComponent(r.full);
    var meters = Object.keys(r.parts).map(function (k) {
      return "<span>" + k + '</span><i><u style="width:' + r.parts[k] + '%"></u></i><em>' + r.parts[k] + "</em>";
    }).join("");
    var h = '<p class="result-name">' + esc(r.sld) + '<span class="tld">.' + esc(r.tld) + "</span></p>" +
      '<p class="result-kind">' + esc(r.notes.join(" ")) + "</p>" +
      '<div class="scoreline"><strong>' + r.score + '</strong><span class="muted">out of 100 for sales readiness. ' + verdict(r.score) + "</span></div>";
    if (compact) {
      h += '<div class="tags" style="margin:1rem 0 .2rem"><div class="tag swing"><b>' + bandText(r.bands.market) + "</b><span>marketplace asking band to test</span></div></div>" +
        '<ul class="result-notes"><li>' + esc(r.lifts[0]) + "</li></ul>" +
        '<div class="btn-row" style="margin-top:1rem"><a class="btn sm" href="' + ROOT + "tools/name-score.html" + q + '">See the full scorecard</a>' +
        '<a class="btn sm ghost" href="' + ROOT + "plan.html" + q + '">Build a plan for it</a></div>';
    } else {
      h += '<div class="meter">' + meters + "</div>" +
        '<div class="tags"><div class="tag swing"><b>' + bandText(r.bands.investor) + "</b><span>investor-to-investor band</span></div>" +
        '<div class="tag big swing"><b>' + bandText(r.bands.market) + "</b><span>marketplace asking band to test</span></div>" +
        '<div class="tag swing"><b>' + bandText(r.bands.enduser) + "</b><span>opening ask for a named end user</span></div></div>" +
        '<h3 style="margin-top:1.4rem">What would lift the result</h3><ul class="result-notes">' + r.lifts.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ul>" +
        '<div class="btn-row" style="margin-top:1.1rem"><a class="btn sm" href="' + ROOT + "plan.html" + q + '">Build a marketing plan</a>' +
        '<a class="btn sm ghost" href="' + ROOT + "tools/net-proceeds.html" + q + '">Compare venue fees</a>' +
        '<a class="btn sm ghost" href="' + ROOT + "tools/lander-builder.html" + q + '">Build the for-sale page</a>' +
        '<a class="btn sm ghost" href="' + ROOT + "tools/pitch-writer.html" + q + '">Write the pitch</a></div>';
    }
    h += '<p class="result-foot">A rule-of-thumb band from the structure of the name. It is a starting point for pricing research, not an appraisal, and it cannot see traffic, history or trademarks.</p>';
    el.innerHTML = h;
  }

  function bindScore(formId, inputId, outId, compact) {
    var f = document.getElementById(formId), i = document.getElementById(inputId), o = document.getElementById(outId);
    if (!f || !i || !o) return;
    function run() { if (i.value.trim()) renderScore(o, score(i.value), compact); }
    on(f, "submit", function (e) { e.preventDefault(); run(); });
    $$("[data-try]").forEach(function (c) { on(c, "click", function () { i.value = c.getAttribute("data-try"); run(); }); });
    var pre = new URLSearchParams(location.search).get("domain") || i.getAttribute("data-default") || "";
    if (pre) { i.value = pre.slice(0, 80); run(); }
  }
  bindScore("hero-form", "hero-input", "hero-out", true);
  bindScore("ns-form", "ns-input", "ns-out", false);

  /* ------------------------------------------------------------------ net proceeds */
  (function () {
    var f = $("#np-form"), out = $("#np-out"); if (!f || !out) return;
    var venues = jsonFrom("venues-data") || [];
    function run() {
      var price = num($("#np-price").value), hold = num($("#np-cost").value) + num($("#np-renew").value) * num($("#np-years").value);
      var custom = num($("#np-custom").value, -1);
      if (price <= 0) { out.innerHTML = '<p class="out-empty">Enter a sale price to compare what you keep at each venue.</p>'; return; }
      var rows = [];
      venues.forEach(function (v) {
        (v.modes || []).forEach(function (m) {
          if (m.rate == null) return;
          var fee = Math.max(price * m.rate / 100, m.min || 0);
          rows.push({ name: v.name, mode: m.label, rate: m.rate, fee: fee, net: price - fee, note: m.note || "", cap: m.cap && price > m.cap });
        });
      });
      if (custom >= 0 && $("#np-custom").value !== "") rows.push({ name: "Your own rate", mode: "custom", rate: custom, fee: price * custom / 100, net: price - price * custom / 100, note: "" });
      rows.sort(function (a, b) { return b.net - a.net; });
      var best = rows[0], worst = rows[rows.length - 1];
      var h = '<div class="tags"><div class="tag big swing"><b>' + money(best.net) + "</b><span>most you keep: " + esc(best.name) + ", " + esc(best.mode) + "</span></div>" +
        '<div class="tag swing"><b>' + money(best.net - worst.net) + "</b><span>gap between best and worst route</span></div></div>" +
        '<div class="tbl-wrap"><table class="tbl" style="margin-top:1.1rem"><thead><tr><th>Venue and route</th><th class="n">Rate</th><th class="n">Fee</th><th class="n">You keep</th>' + (hold > 0 ? '<th class="n">After your costs</th>' : "") + "</tr></thead><tbody>";
      rows.forEach(function (r, i) {
        h += "<tr" + (i === 0 ? ' class="best"' : "") + "><td><strong>" + esc(r.name) + "</strong><br><span class=\"small muted\">" + esc(r.mode) + (r.cap ? ". Published rate is lower on deals this size, so treat this fee as a ceiling" : "") + "</span></td>" +
          '<td class="n">' + r.rate + '%</td><td class="n">' + money(r.fee) + '</td><td class="n"><strong>' + money(r.net) + "</strong></td>" +
          (hold > 0 ? '<td class="n">' + money(r.net - hold) + "</td>" : "") + "</tr>";
      });
      h += "</tbody></table></div>" +
        '<p class="small muted" style="margin-top:.8rem">Rates are the published figures we read on each company’s own pages on the date shown in <a href="' + ROOT + 'venues.html">Where to sell</a>. Venues change terms; confirm before you list. A cheaper route is not always the better one: a network that reaches more buyers can out-earn a lower fee.</p>' +
        '<div class="btn-row"><a class="btn sm" href="' + ROOT + 'plan.html">Pick a venue with the plan builder</a></div>';
      out.innerHTML = h;
    }
    on(f, "input", run); on(f, "submit", function (e) { e.preventDefault(); run(); });
    run();
  })();

  /* ------------------------------------------------------------------ portfolio math */
  (function () {
    var f = $("#pm-form"), out = $("#pm-out"); if (!f || !out) return;
    function run() {
      var n = num($("#pm-count").value), renew = num($("#pm-renew").value), str = num($("#pm-str").value) / 100,
        avg = num($("#pm-avg").value), comm = num($("#pm-comm").value) / 100, buys = num($("#pm-buys").value), buyCost = num($("#pm-buycost").value);
      if (n <= 0 || renew <= 0) { out.innerHTML = '<p class="out-empty">Enter how many names you hold and what a renewal costs you.</p>'; return; }
      var carry = n * renew, sales = n * str, gross = sales * avg, net = gross * (1 - comm), spend = carry + buys * buyCost, profit = net - spend;
      var beStr = avg * (1 - comm) > 0 ? spend / (n * avg * (1 - comm)) : 0, bePrice = sales * (1 - comm) > 0 ? spend / (sales * (1 - comm)) : 0;
      var floor = str * (1 - comm) > 0 ? renew / (str * (1 - comm)) : 0;
      var h = '<div class="tags"><div class="tag big swing"><b>' + money(profit) + "</b><span>expected profit per year at these inputs</span></div>" +
        '<div class="tag swing"><b>' + money(floor) + "</b><span>what a name must fetch to pay its own renewal</span></div></div>" +
        '<dl class="facts" style="margin-top:1.2rem">' +
        "<div><dt>Renewals per year</dt><dd>" + money(carry) + "</dd></div>" +
        (buys * buyCost > 0 ? "<div><dt>New purchases per year</dt><dd>" + money(buys * buyCost) + "</dd></div>" : "") +
        "<div><dt>Expected sales per year</dt><dd>" + (Math.round(sales * 10) / 10) + " names</dd></div>" +
        "<div><dt>Gross sales</dt><dd>" + money(gross) + "</dd></div>" +
        "<div><dt>After commission</dt><dd>" + money(net) + "</dd></div>" +
        "<div><dt>Sell-through you need to break even</dt><dd>" + (beStr * 100).toFixed(2) + "%</dd></div>" +
        "<div><dt>Average price you need to break even</dt><dd>" + (bePrice ? money(bePrice) : "n/a") + "</dd></div></dl>";
      var msg;
      if (profit < 0) msg = "At these inputs the portfolio loses money. Three levers, in order of speed: drop the names that cannot clear " + money(floor) + ", raise sell-through with better landers and outbound, then raise average price.";
      else if (beStr > str * 0.7) msg = "You are profitable but thin: break-even sits close to your actual sell-through. One slow year puts you under. Trim the bottom of the list before the next renewal cycle.";
      else msg = "There is room here. The bigger risk is under-marketing the top tenth of the list: those names carry the average price.";
      h += '<div class="note"><p>' + msg + "</p></div>" +
        '<p class="small muted">The drop test: multiply a name’s realistic sale price by your sell-through rate and by what you keep after commission. If that is less than its renewal, it costs more to hold than it is expected to return.</p>';
      out.innerHTML = h;
    }
    on(f, "input", run); on(f, "submit", function (e) { e.preventDefault(); run(); });
    run();
  })();

  /* ------------------------------------------------------------------ pitch writer */
  (function () {
    var f = $("#pw-form"), out = $("#pw-out"); if (!f || !out) return;
    var ANG = {
      upgrade: function (d, cur) { return cur ? "You are on " + cur + " today. " + d + " is the shorter version people already type and say." : d + " is shorter and easier to say than most names in your space."; },
      exact: function (d) { return d + " says what you sell in the words your customers search with."; },
      launch: function (d) { return "If a new product or market is on your roadmap, " + d + " gives it a name that needs no explaining."; },
      category: function (d) { return d + " names the category you compete in. Whoever holds it gets the type-in visits and the first impression."; },
      geo: function (d) { return d + " puts your city and your service in one address, which is how local customers search."; }
    };
    function run() {
      var d = parseDomain($("#pw-domain").value);
      if (!d.ok) { out.innerHTML = '<p class="out-empty">Enter the domain you are selling to draft the emails.</p>'; return; }
      var me = $("#pw-me").value.trim() || "[Your name]", co = $("#pw-co").value.trim(), cur = $("#pw-cur").value.trim(),
        ang = $("#pw-angle").value, tone = $("#pw-tone").value, mode = $("#pw-ask").value, price = num($("#pw-price").value);
      var D = d.sld.charAt(0).toUpperCase() + d.sld.slice(1) + "." + d.tld;
      var hi = tone === "formal" ? "Hello" + (co ? " " + co + " team" : "") + "," : tone === "warm" ? "Hi" + (co ? " " + co + " team" : " there") + "," : "Hi,";
      var why = (ANG[ang] || ANG.exact)(D, cur);
      var ask = mode === "price" && price > 0 ? "The price is " + money(price) + ", paid through a licensed escrow service so neither side carries risk." : "I am open to a sensible offer, with payment through a licensed escrow service so neither side carries risk.";
      var close = tone === "formal" ? "If this is not relevant to you, a one-word reply will make sure I do not write again." : "If it is not for you, reply “no” and I will not write again.";
      var e1 = hi + "\n\nI own the domain name " + D + " and I am offering it to a small number of companies before listing it publicly.\n\n" + why + "\n\n" + ask + "\n\nWould the right person on your side like the details?\n\n" + close + "\n\n" + me + "\nOwner, " + D;
      var e2 = hi + "\n\nA short follow-up on " + D + ". I wrote a few days ago and wanted to make sure it reached whoever looks after your brand or marketing.\n\n" + (mode === "price" && price > 0 ? "It is available at " + money(price) + "." : "It is available, and I am open to an offer.") + " If someone else handles this, I am glad to be pointed to them.\n\n" + me;
      var e3 = hi + "\n\nLast note from me about " + D + ". I am listing it publicly this week, so I will close the loop here.\n\nIf it becomes interesting later, this address reaches me.\n\n" + me;
      var subs = [D + " is available", "The domain " + D, (co ? co + " and " : "Question about ") + D];
      var words = e1.split(/\s+/).length;
      function box(id, title, text) {
        return '<div class="copybox"><h4>' + title + '</h4><button class="btn sm ghost copy" type="button" data-copy="#' + id + '" data-copy-label="Email">Copy</button><pre id="' + id + '">' + esc(text) + "</pre></div>";
      }
      out.innerHTML = '<div class="copybox"><h4>Subject lines to test</h4><pre id="pw-s">' + esc(subs.join("\n")) + '</pre><button class="btn sm ghost copy" type="button" data-copy="#pw-s" data-copy-label="Subject lines">Copy</button></div>' +
        box("pw-1", "First email (" + words + " words)", e1) + box("pw-2", "Follow-up, four working days later", e2) + box("pw-3", "Closing the loop, a week after that", e3) +
        '<div class="note"><p><strong>Before you send:</strong> write to a named person where you can find one, send from an address on a domain you own, include your real name, and stop at three emails. Never write to a company whose trademark matches the name; that is how a sale turns into a dispute.</p></div>';
    }
    on(f, "input", run); on(f, "submit", function (e) { e.preventDefault(); run(); });
    var pre = new URLSearchParams(location.search).get("domain"); if (pre) $("#pw-domain").value = pre.slice(0, 80);
    run();
  })();

  /* ------------------------------------------------------------------ lander builder */
  (function () {
    var f = $("#lb-form"), frame = $("#lb-preview"), code = $("#lb-code"); if (!f || !frame || !code) return;
    var COLORS = { cobalt: ["#2337E8", "#FFFFFF"], forest: ["#0B6B4F", "#FFFFFF"], plum: ["#6B2D7B", "#FFFFFF"], charcoal: ["#22252E", "#FFFFFF"], ember: ["#B6401F", "#FFFFFF"] };
    function build() {
      var d = parseDomain($("#lb-domain").value), name = d.ok ? d.full : "yourname.com";
      var Name = d.ok ? d.sld.charAt(0).toUpperCase() + d.sld.slice(1) + "." + d.tld : "YourName.com";
      var mode = $("#lb-mode").value, price = num($("#lb-price").value), min = num($("#lb-min").value), months = Math.round(num($("#lb-lto").value));
      var tagline = $("#lb-tagline").value.trim() || "This domain name is for sale.";
      var points = $("#lb-points").value.split(/\n+/).map(function (s) { return s.trim(); }).filter(Boolean).slice(0, 4);
      var how = $("#lb-how").value, to = $("#lb-to").value.trim(), col = COLORS[$("#lb-color").value] || COLORS.cobalt;
      var href = "#";
      if (how === "email" && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(to)) href = "mailto:" + to + "?subject=" + encodeURIComponent("Inquiry about " + name);
      else if (how === "url" && /^https?:\/\/\S+$/i.test(to)) href = to;
      var priceLine = "", cta = "Ask about this name";
      if ((mode === "bin" || mode === "both") && price > 0) { priceLine = '<p class="price"><b>' + money(price) + "</b><span>buy it now</span></p>"; cta = mode === "both" ? "Buy now or make an offer" : "Buy this name"; }
      else if (mode === "offer") { priceLine = '<p class="price"><b>Make an offer</b>' + (min > 0 ? "<span>offers from " + money(min) + " are considered</span>" : "<span>serious offers get a reply</span>") + "</p>"; cta = "Make an offer"; }
      else { priceLine = '<p class="price"><b>Price on request</b><span>ask and you will get a number</span></p>'; cta = "Request the price"; }
      var lto = months >= 2 && price > 0 && (mode === "bin" || mode === "both") ? '<p class="plan">Or ' + money(Math.ceil(price / months)) + " a month for " + months + " months. Use the name from the first payment; it becomes yours after the last.</p>" : "";
      var lis = points.map(function (p) { return "<li>" + esc(p) + "</li>"; }).join("");
      var doc = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>" + esc(Name) + " is for sale</title>\n<meta name=\"description\" content=\"" + esc(Name) + " is for sale. " + esc(tagline) + "\">\n<style>\n" +
        "*{box-sizing:border-box}body{margin:0;font:17px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#14172b;background:#f3f4f9}\n" +
        ".top{background:" + col[0] + ";color:" + col[1] + ";padding:9px 16px;text-align:center;font-size:14px;font-weight:600}\n" +
        "main{max-width:760px;margin:0 auto;padding:7vh 22px 48px}\n" +
        "h1{font-size:clamp(34px,9vw,76px);line-height:1;letter-spacing:-.03em;margin:0 0 14px;overflow-wrap:anywhere}\n" +
        ".lead{font-size:20px;color:#454a66;margin:0 0 28px}\n" +
        ".card{background:#fff;border:2px solid #14172b;border-radius:16px;padding:26px}\n" +
        ".price{margin:0 0 6px}.price b{display:block;font-size:clamp(30px,6vw,44px);line-height:1.05;letter-spacing:-.02em}.price span{color:#454a66}\n" +
        ".plan{margin:10px 0 0;color:#454a66}\n" +
        ".btn{display:inline-block;margin-top:20px;background:" + col[0] + ";color:" + col[1] + ";text-decoration:none;font-weight:700;padding:15px 26px;border-radius:999px}\n" +
        ".btn:focus-visible{outline:3px solid #14172b;outline-offset:3px}\n" +
        "ul{padding-left:20px;margin:28px 0 0}li{margin:0 0 8px}\n" +
        ".safe{margin-top:28px;font-size:15px;color:#454a66;border-top:1px solid #d5d8e6;padding-top:16px}\n" +
        "</style>\n</head>\n<body>\n<div class=\"top\">This domain name is for sale</div>\n<main>\n<h1>" + esc(Name) + "</h1>\n<p class=\"lead\">" + esc(tagline) + "</p>\n<div class=\"card\">\n" + priceLine + "\n" + lto + "\n<a class=\"btn\" href=\"" + esc(href) + "\">" + cta + "</a>\n</div>\n" +
        (lis ? "<ul>\n" + lis + "\n</ul>\n" : "") +
        "<p class=\"safe\">Payment goes through a licensed escrow service: you pay the escrow company, the name is transferred to your registrar account, and only then is the seller paid. Most transfers finish within a few working days.</p>\n</main>\n</body>\n</html>\n";
      code.value = doc; frame.srcdoc = doc;
      var warn = $("#lb-warn");
      if (warn) warn.hidden = href !== "#";
      return { doc: doc, name: name };
    }
    var last = build();
    on(f, "input", function () { last = build(); });
    on(f, "submit", function (e) { e.preventDefault(); last = build(); });
    on($("#lb-download"), "click", function () {
      var blob = new Blob([last.doc], { type: "text/html" }), a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = "index.html"; document.body.appendChild(a); a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
      if (DM.toast) DM.toast("Saved as index.html");
    });
    var pre = new URLSearchParams(location.search).get("domain"); if (pre) { $("#lb-domain").value = pre.slice(0, 80); last = build(); }
  })();

  /* ------------------------------------------------------------------ payment plan */
  (function () {
    var f = $("#pp-form"), out = $("#pp-out"); if (!f || !out) return;
    function run() {
      var price = num($("#pp-price").value), type = $("#pp-type").value, m = Math.max(2, Math.min(120, Math.round(num($("#pp-months").value, 12)))),
        prem = num($("#pp-prem").value) / 100, dep = num($("#pp-dep").value) / 100, bal = num($("#pp-bal").value) / 100;
      $("#pp-dep-wrap").hidden = type !== "deposit"; $("#pp-bal-wrap").hidden = type !== "balloon";
      if (price <= 0) { out.innerHTML = '<p class="out-empty">Enter the cash price to see the monthly payment.</p>'; return; }
      var total = price * (1 + prem), first = 0, last = 0, monthly, n = m, desc;
      if (type === "deposit") { first = total * dep; monthly = (total - first) / m; desc = money(first) + " at signing, then " + m + " monthly payments of " + money(monthly); }
      else if (type === "balloon") { last = total * bal; n = m - 1; monthly = (total - last) / n; desc = n + " monthly payments of " + money(monthly) + ", then a final payment of " + money(last); }
      else { monthly = total / m; desc = m + " monthly payments of " + money(monthly); }
      var rows = "", paid = 0, i;
      if (first) { paid += first; rows += "<tr><td>At signing</td><td class=\"n\">" + money(first) + '</td><td class="n">' + money(paid) + "</td></tr>"; }
      for (i = 1; i <= n; i++) { paid += monthly; if (i <= 3 || i > n - 1 || n <= 6) rows += "<tr><td>Month " + i + '</td><td class="n">' + money(monthly) + '</td><td class="n">' + money(paid) + "</td></tr>"; else if (i === 4) rows += '<tr><td colspan="3" class="muted">Months 4 to ' + (n - 1) + ": " + money(monthly) + " each</td></tr>"; }
      if (last) { paid += last; rows += "<tr><td>Final payment (month " + m + ')</td><td class="n">' + money(last) + '</td><td class="n">' + money(paid) + "</td></tr>"; }
      var blurb = "Pay over time: " + desc + ". Total " + money(total) + ". You can use the name from the first payment; ownership transfers after the last one. Payments and the name are held by a licensed escrow service for the length of the plan.";
      out.innerHTML = '<div class="tags"><div class="tag big swing"><b>' + money(monthly) + "</b><span>per month</span></div>" +
        '<div class="tag swing"><b>' + money(total) + "</b><span>total, " + (prem > 0 ? money(total - price) + " over the cash price" : "same as the cash price") + "</span></div></div>" +
        '<div class="tbl-wrap"><table class="tbl" style="margin-top:1.1rem"><thead><tr><th>When</th><th class="n">Payment</th><th class="n">Paid so far</th></tr></thead><tbody>' + rows + "</tbody></table></div>" +
        '<div class="copybox" style="margin-top:1.1rem"><h4>Wording for your listing</h4><button class="btn sm ghost copy" type="button" data-copy="#pp-blurb" data-copy-label="Wording">Copy</button><pre id="pp-blurb">' + esc(blurb) + "</pre></div>";
    }
    on(f, "input", run); on(f, "submit", function (e) { e.preventDefault(); run(); });
    run();
  })();

  /* ------------------------------------------------------------------ expiry timeline */
  (function () {
    var f = $("#et-form"), out = $("#et-out"); if (!f || !out) return;
    var inp = $("#et-date");
    if (inp && !inp.value) { var t = new Date(); t.setDate(t.getDate() + 30); inp.value = t.toISOString().slice(0, 10); }
    function add(d, n) { var x = new Date(d.getTime()); x.setDate(x.getDate() + n); return x; }
    function run() {
      var v = inp.value; if (!v) { out.innerHTML = '<p class="out-empty">Pick the expiry date shown in the public registration record.</p>'; return; }
      var exp = new Date(v + "T12:00:00"), grace = Math.max(0, Math.min(45, Math.round(num($("#et-grace").value, 30))));
      if (isNaN(exp.getTime())) return;
      var gEnd = add(exp, grace), rEnd = add(gEnd, 30), drop = add(rEnd, 5), now = new Date();
      var stages = [
        { d: exp, t: "Registration expires", x: "The site and email usually stop working within days. The owner can still renew at the normal price." },
        { d: gEnd, t: "Registrar grace period ends", x: "Between expiry and this date the registrar decides what happens. Many registrars send unrenewed names to their auction partner inside this window, so a name with bids may never reach the next stages." },
        { d: rEnd, t: "Redemption period ends", x: "For 30 days the previous owner can still get the name back, but only by paying a redemption fee on top of the renewal." },
        { d: drop, t: "Earliest release", x: "After five days of pending delete the registry releases the name. Drop-catching services compete to register it in the first second; a backorder placed before this date is your ticket in." }
      ];
      var state = now < exp ? "still registered" : now < gEnd ? "in the registrar grace period" : now < rEnd ? "in redemption" : now < drop ? "in pending delete" : "past its earliest release date";
      var li = stages.map(function (s) {
        var past = s.d < now;
        return '<li class="' + (past ? "past" : "") + '"><time datetime="' + s.d.toISOString().slice(0, 10) + '">' + fmtDate(s.d) + "</time><strong>" + s.t + "</strong><br><span class=\"small\">" + s.x + "</span></li>";
      }).join("");
      var days = Math.ceil((drop - now) / 864e5);
      out.innerHTML = '<div class="tags"><div class="tag big swing"><b>' + fmtDate(drop) + "</b><span>earliest date the name can be released" + (days > 0 ? ", " + days + " days from today" : "") + "</span></div></div>" +
        '<p style="margin:1rem 0 .4rem">If the dates you entered are right, today the name is <strong>' + state + "</strong>.</p>" +
        '<ol class="timeline">' + li + "</ol>" +
        '<p class="small muted">This follows the standard lifecycle for generic extensions such as .com and .net: a registrar grace period of up to 45 days, 30 days of redemption, then 5 days of pending delete. Each registrar sets its own grace length, and country-code extensions follow their own rules, so treat the dates as a planning guide.</p>';
    }
    on(f, "input", run); on(f, "submit", function (e) { e.preventDefault(); run(); });
    run();
  })();

  /* ------------------------------------------------------------------ listing and social copy */
  (function () {
    var f = $("#lc-form"), out = $("#lc-out"); if (!f || !out) return;
    var OPEN = { trust: ["A name people trust on first read.", "Sounds established from day one.", "Credibility you do not have to explain."],
      modern: ["Short, current and easy to say.", "Built for a product that moves fast.", "A clean name for a modern brand."],
      playful: ["A name that makes people smile, then remember.", "Friendly, quick and hard to forget.", "Easy to say, easier to share."],
      premium: ["A category-level name.", "The kind of address that ends the naming meeting.", "One of very few names this direct."] };
    function run() {
      var d = parseDomain($("#lc-domain").value);
      if (!d.ok) { out.innerHTML = '<p class="out-empty">Enter the domain to draft listing and social copy.</p>'; return; }
      var r = score(d.full), seed = hash(d.full), ind = $("#lc-ind").value, aud = $("#lc-aud").value.trim() || "a growing " + ind + " business", vibe = $("#lc-vibe").value;
      var D = d.sld.charAt(0).toUpperCase() + d.sld.slice(1) + "." + d.tld, L = d.sld.replace(/-/g, "").length;
      var facts = L + " characters" + (r.words && r.words.length <= 3 ? ", " + (r.words.length === 1 ? "one word" : r.words.length + " words") : "") + ", ." + d.tld;
      var open = pick(OPEN[vibe] || OPEN.modern, seed);
      var shortD = (D + ". " + open + " " + cap(facts) + ". Suits " + aud + ".").slice(0, 160);
      var longD = D + " is for sale.\n\n" + open + " It is " + facts + ", easy to spell after hearing it once, and it fits " + aud + ".\n\nGood uses:\n- The main site for a " + ind + " brand\n- A product or campaign address that needs no explanation\n- A defensive purchase for a company already working in " + ind + "\n\nThe sale runs through a licensed escrow service and the name moves to your registrar account before the seller is paid.";
      var tags = [D + ": say it once, they remember it.", "Your " + ind + " brand, in " + L + " characters.", open, "The address your customers already expect.", "Skip the naming meeting. " + D + "."];
      var x = D + " is for sale.\n\n" + cap(facts) + ". " + open + "\n\nFits " + aud + ". Escrow sale, quick transfer.\n\nReplies open.";
      var li = "I am selling the domain name " + D + ".\n\n" + open + " It would suit " + aud + ".\n\nWhy it works:\n• " + cap(facts) + "\n• Easy to say on a call and spell from memory\n• Sale handled through licensed escrow\n\nIf you know a founder or marketing lead in " + ind + " who is naming something, I would be glad of an introduction.";
      var forum = "Domain: " + D + "\nType: " + r.kind + "\nPrice: [BIN price] or best offer\nRegistrar: [registrar]\nExpiry: [date]\nPayment: escrow, buyer pays fee / split\nNotes: " + facts + ". No trademark issues known to seller.";
      function box(id, title, text, label) { return '<div class="copybox"><h4>' + title + '</h4><button class="btn sm ghost copy" type="button" data-copy="#' + id + '" data-copy-label="' + label + '">Copy</button><pre id="' + id + '">' + esc(text) + "</pre></div>"; }
      out.innerHTML = box("lc-1", "Marketplace summary (" + shortD.length + " characters)", shortD, "Summary") + box("lc-2", "Marketplace description", longD, "Description") +
        box("lc-3", "Taglines for the for-sale page", tags.join("\n"), "Taglines") + box("lc-4", "Post for X", x, "Post") + box("lc-5", "Post for LinkedIn", li, "Post") + box("lc-6", "Forum sale listing", forum, "Listing") +
        '<p class="small muted">Drafts are starting points. Read them aloud, cut anything you would not say to a buyer in person, and never claim traffic, revenue or interest you cannot show.</p>';
    }
    on(f, "input", run); on(f, "submit", function (e) { e.preventDefault(); run(); });
    var pre = new URLSearchParams(location.search).get("domain"); if (pre) $("#lc-domain").value = pre.slice(0, 80);
    run();
  })();

  /* ------------------------------------------------------------------ plan builder (lead funnel) */
  (function () {
    var f = $("#pl-form"), out = $("#pl-out"); if (!f || !out) return;
    var venues = jsonFrom("venues-data") || [];
    function v(id) { for (var i = 0; i < venues.length; i++) if (venues[i].id === id) return venues[i]; return null; }
    function vline(id) { var x = v(id); if (!x) return ""; return "<li><strong>" + esc(x.name) + ".</strong> " + esc(x.best) + " <span class=\"muted\">" + esc(x.fees) + "</span></li>"; }
    var steps = $$("[data-step]", f), dots = $$(".steps li"), cur = 0;
    function show(n) {
      cur = n; steps.forEach(function (s, i) { s.hidden = i !== n; });
      dots.forEach(function (d, i) { d.className = i === n ? "on" : i < n ? "done" : ""; });
      var first = $("input,select,textarea", steps[n]); if (first && n > 0) first.focus();
    }
    $$("[data-next]", f).forEach(function (b) { on(b, "click", function () {
      if (cur === 0) { var d = parseDomain($("#pl-domain").value); if (!d.ok) { $("#pl-domain").setAttribute("aria-invalid", "true"); $("#pl-domain").focus(); if (DM.toast) DM.toast("Enter a domain name, like yourname.com"); return; } $("#pl-domain").setAttribute("aria-invalid", "false"); }
      show(Math.min(cur + 1, steps.length - 1));
    }); });
    $$("[data-back]", f).forEach(function (b) { on(b, "click", function () { show(Math.max(cur - 1, 0)); }); });
    function val(name) { var c = $('input[name="' + name + '"]:checked', f); return c ? c.value : ""; }
    on(f, "submit", function (e) {
      e.preventDefault();
      var d = parseDomain($("#pl-domain").value); if (!d.ok) { show(0); return; }
      var r = score(d.full), goal = val("goal") || "price", when = val("when") || "3m", effort = val("effort") || "hour", floor = num($("#pl-floor").value);
      var fast = goal === "fast" || when === "30d", top = r.score >= 85, weak = r.score < 45;
      var band = fast ? [r.bands.market[0], nice((r.bands.market[0] + r.bands.market[1]) / 2)] : r.bands.market;
      var priceMode, priceWhy;
      if (top && !fast) { priceMode = "Make offer, with a private floor"; priceWhy = "Names at this level are priced by the buyer’s budget, not by a list. A public number caps you."; }
      else if (goal === "lease") { priceMode = "Buy-now price with a monthly plan beside it"; priceWhy = "A monthly figure opens the door to buyers who cannot pay cash, and you keep the name if they stop."; }
      else { priceMode = "Fixed buy-now price, offers allowed"; priceWhy = "A visible price removes the first email, which is where most inquiries die. Sedo says its buy-now names sell up to three times faster than negotiated ones."; }
      var vs = top ? ["broker", "afternic", "sedo"] : weak ? ["namecheap", "dynadot", "forum"] : fast ? ["sedo", "afternic", "dynadot"] : ["afternic", "sedo", "own"];
      if (goal === "lease") vs = ["own", "saw", "sedo"];
      var q = "?domain=" + encodeURIComponent(d.full);
      var weeks = [
        "Pull 10 to 12 comparable sales. Fix the price mode and number. Build the for-sale page and point the name at it.",
        "List on " + vs.slice(0, 2).map(function (id) { var x = v(id); return x ? x.name : id; }).join(" and ") + " with the same price everywhere. Write the listing copy once and reuse it.",
        effort === "none" ? "Check that the page loads on a phone and the inquiry route works by sending yourself a test." : "Find " + (effort === "active" ? "25" : "10") + " operating businesses the name fits. Send the first email to a named person at each.",
        effort === "none" ? "Set a calendar reminder 90 days out to review price and inquiries." : "Send the follow-up. Log every reply. Any offer above your floor gets an answer the same day."
      ];
      var h = '<p class="result-name">' + esc(r.sld) + '<span class="tld">.' + esc(r.tld) + "</span></p>" +
        '<p class="result-kind">' + esc(r.kind) + ". Sales-readiness score " + r.score + " of 100. " + verdict(r.score) + "</p>" +
        '<div class="tags"><div class="tag big swing"><b>' + bandText(band) + "</b><span>asking band to test" + (fast ? ", lower half for speed" : "") + "</span></div>" +
        (floor > 0 ? '<div class="tag swing"><b>' + money(floor) + "</b><span>your floor: decline below this without debating it</span></div>" : "") + "</div>" +
        (floor > 0 && floor > band[1] ? '<div class="note"><p>Your floor sits above the band this name’s structure supports. That can be right if you know something the name alone does not show, such as traffic or an obvious buyer. If not, expect a long hold.</p></div>' : "") +
        "<h3 style=\"margin-top:1.5rem\">1. Price</h3><p><strong>" + priceMode + ".</strong> " + priceWhy + "</p>" +
        "<h3>2. Venues</h3><ul>" + vs.map(vline).join("") + "</ul>" +
        "<h3>3. The for-sale page</h3><p>The name itself is your best traffic source: people type it to see what is there. Show the price or the offer route, one sentence on who it suits, and how payment is protected. <a href=\"" + ROOT + "tools/lander-builder.html" + q + "\">Build the page</a>.</p>" +
        (effort === "none" ? "" : "<h3>4. Outreach</h3><p>" + (effort === "active" ? "Twenty-five" : "Ten") + " well-chosen emails beat five hundred sprayed ones. Three touches, then stop. <a href=\"" + ROOT + "tools/pitch-writer.html" + q + "\">Draft the emails</a>.</p>") +
        "<h3>" + (effort === "none" ? "4" : "5") + ". Thirty days</h3><ol>" + weeks.map(function (w, i) { return "<li><strong>Week " + (i + 1) + ".</strong> " + esc(w) + "</li>"; }).join("") + "</ol>" +
        "<h3>" + (effort === "none" ? "5" : "6") + ". What to watch</h3><p>Visits to the for-sale page, inquiries, and offers against your floor. No visits in 90 days means the venue or the name is the problem. Visits without inquiries means the price or the page is.</p>" +
        '<div class="btn-row no-print" style="margin-top:1rem"><button class="btn sm ghost" type="button" id="pl-print">Print or save as PDF</button><button class="btn sm ghost" type="button" id="pl-again">Change my answers</button></div>' +
        '<p class="result-foot">A planning draft built from your answers and the structure of the name. It is not an appraisal or advice on a specific transaction.</p>';
      out.innerHTML = h; out.hidden = false; f.hidden = true;
      var dotsWrap = $(".steps"); if (dotsWrap) dotsWrap.hidden = true;
      var summary = d.full + " | score " + r.score + " | " + r.kind + " | band " + bandText(band) + " | goal " + goal + " | timeline " + when + " | effort " + effort + (floor ? " | floor " + money(floor) : "") + " | price mode: " + priceMode + " | venues: " + vs.join(", ");
      try { sessionStorage.setItem("dm:plan", summary); } catch (err) {}
      var lead = $("#pl-lead"); if (lead) { lead.hidden = false; var di = $('input[name="domain"]', lead); if (di) di.value = d.full; var ps = $('input[name="plan_summary"]', lead); if (ps) ps.value = summary; }
      on($("#pl-print"), "click", function () { window.print(); });
      on($("#pl-again"), "click", function () { out.hidden = true; f.hidden = false; if (dotsWrap) dotsWrap.hidden = false; show(0); });
      out.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    var pre = new URLSearchParams(location.search).get("domain"); if (pre) $("#pl-domain").value = pre.slice(0, 80);
    show(0);
  })();

  /* role switch on the plan page: seller builder or a direct request form */
  (function () {
    var tabs = $$("[data-role]"); if (!tabs.length) return;
    function pickRole(role) {
      tabs.forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-role") === role ? "true" : "false"); });
      $$("[data-role-panel]").forEach(function (p) { p.hidden = p.getAttribute("data-role-panel") !== role; });
    }
    tabs.forEach(function (t) { on(t, "click", function () { pickRole(t.getAttribute("data-role")); }); });
    var want = { "#other": "portfolio", "#portfolio": "portfolio", "#buyer": "buyer", "#provider": "provider" }[location.hash];
    if (want) pickRole(want);
  })();

  /* attach the last scored name and plan to any lead form the visitor sends */
  DM.enrich = function (form, data) {
    if (!form.hasAttribute("data-lead")) return;
    try {
      var last = sessionStorage.getItem("dm:last"), plan = sessionStorage.getItem("dm:plan");
      if (last && !data.last_scored) data.last_scored = last;
      if (plan && !data.plan_summary) data.plan_summary = plan;
    } catch (e) {}
  };
})();
