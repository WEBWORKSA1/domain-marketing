/* Domain Marketing — core: theme, menu, protected contact routing, forms, search, consent, video, copy */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem("dm:" + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("dm:" + k, JSON.stringify(v)); } catch (e) {} }
  };
  var ROOT = document.body.getAttribute("data-root") || "";
  var DM = window.DM = { $: $, $$: $$, store: store, root: ROOT };

  /* ---- protected routing: the inbox and the partner contact address are assembled at run time only ---- */
  var un = function (a) { return a.slice().reverse().map(function (n) { return String.fromCharCode(n - 7); }).join(""); };
  var _i = [116, 118, 106, 53, 115, 112, 104, 116, 110, 71, 56, 104, 122, 114, 121, 118, 126, 105, 108, 126];
  var _c = [123, 106, 104, 123, 117, 118, 106, 54, 122, 114, 121, 118, 126, 53, 105, 108, 126, 54, 54, 65, 122, 119, 123, 123, 111];
  var endpoint = function () { return "https://formsubmit.co/ajax/" + un(_i); };
  $$("[data-contact]").forEach(function (a) {
    a.setAttribute("href", un(_c));
    a.setAttribute("target", "_blank");
    a.setAttribute("rel", "noopener");
  });

  /* ---- theme ---- */
  var html = document.documentElement;
  $$("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var dark = html.getAttribute("data-theme") === "dark" ||
        (!html.getAttribute("data-theme") && window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark";
      html.setAttribute("data-theme", next); store.set("theme", next);
    });
  });
  if (!html.getAttribute("data-theme") && window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches) {
    html.setAttribute("data-theme", "dark");
  }

  /* ---- menu ---- */
  var mb = $(".menu-btn"), nav = $("#nav");
  if (mb && nav) mb.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    mb.setAttribute("aria-expanded", open ? "true" : "false");
    mb.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });

  /* ---- year ---- */
  $$("[data-year]").forEach(function (n) { n.textContent = new Date().getFullYear(); });

  /* ---- toast ---- */
  var toastEl;
  DM.toast = function (msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove("show"); }, 2600);
  };

  /* ---- copy buttons ---- */
  DM.copy = function (text, label) {
    var done = function () { DM.toast((label || "Text") + " copied"); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(); });
    } else fallback();
    function fallback() {
      var t = document.createElement("textarea"); t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
      document.body.appendChild(t); t.select();
      try { document.execCommand("copy"); done(); } catch (e) { DM.toast("Copy failed. Select the text and copy it by hand."); }
      document.body.removeChild(t);
    }
  };
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-copy]");
    if (!b) return;
    var src = $(b.getAttribute("data-copy"));
    if (src) DM.copy("value" in src && src.tagName !== "DIV" && src.tagName !== "PRE" ? src.value : src.textContent, b.getAttribute("data-copy-label") || "Text");
  });

  /* ---- forms -> FormSubmit (AJAX) ---- */
  DM.submit = function (subject, data) {
    var body = { _subject: "[Domain Marketing] " + subject, _template: "table", _captcha: "false" };
    Object.keys(data).forEach(function (k) { body[k] = data[k]; });
    body.source_page = location.href;
    body.submitted_at = new Date().toISOString();
    return fetch(endpoint(), {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(body)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok || j.success === "false" || j.success === false) throw new Error((j && j.message) || "Send failed");
        return j;
      });
    });
  };

  function validate(f) {
    var ok = true, first = null;
    $$("input,select,textarea", f).forEach(function (el) {
      if (el.closest(".hp") || el.type === "hidden") return;
      var bad = false;
      if (el.required && !String(el.value).trim()) bad = true;
      if (!bad && el.type === "email" && el.value && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim())) bad = true;
      if (!bad && el.name === "domain" && el.value && !/[a-z0-9-]+\.[a-z]{2,}/i.test(el.value)) bad = true;
      if (el.type === "checkbox" && el.required && !el.checked) bad = true;
      el.setAttribute("aria-invalid", bad ? "true" : "false");
      if (bad) { ok = false; first = first || el; }
    });
    if (first) first.focus();
    return ok;
  }

  function collect(f) {
    var data = {};
    $$("input,select,textarea", f).forEach(function (el) {
      if (!el.name || el.closest(".hp")) return;
      if ((el.type === "radio" || el.type === "checkbox") && !el.checked) return;
      if (el.type === "checkbox" && data[el.name]) data[el.name] += ", " + el.value;
      else data[el.name] = el.value;
    });
    return data;
  }

  $$("form[data-dm]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var hp = $(".hp input", f);
      if (hp && hp.value) return;
      var done = $(".form-done", f), fail = $(".form-fail", f), btn = $("button[type=submit]", f);
      if (fail) fail.hidden = true;
      if (!validate(f)) { DM.toast("Check the highlighted fields"); return; }
      var data = collect(f);
      if (typeof DM.enrich === "function") { try { DM.enrich(f, data); } catch (err) {} }
      var label = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
      DM.submit(f.getAttribute("data-dm"), data).then(function () {
        if (done) { done.hidden = false; done.setAttribute("tabindex", "-1"); done.focus(); }
        $$("input:not([type=hidden]),textarea,select,button[type=submit]", f).forEach(function (el) { if (!el.closest(".form-done")) el.disabled = true; });
        if (btn) btn.textContent = "Sent";
        if (f.hasAttribute("data-lead")) store.set("lead", Date.now());
        f.dispatchEvent(new CustomEvent("dm:sent", { bubbles: true }));
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.textContent = label; }
        if (fail) fail.hidden = false; else DM.toast("That did not send. Try again in a moment.");
      });
    });
  });

  /* ---- prefill from ?domain= or the last name scored ---- */
  var qs = new URLSearchParams(location.search);
  var pre = qs.get("domain") || "";
  if (pre) $$('input[name="domain"],[data-prefill-domain]').forEach(function (i) { if (!i.value) i.value = pre.slice(0, 80); });

  /* ---- search ---- */
  var sb = $("#search"), sq = $("#search-q"), sr = $("#search-res"), idx = null, lastFocus = null;
  function openSearch() {
    if (!sb) return;
    lastFocus = document.activeElement; sb.hidden = false; sq.value = ""; sr.innerHTML = ""; sq.focus();
    if (!idx) fetch(ROOT + "data/search.json").then(function (r) { return r.json(); }).then(function (j) { idx = j; }).catch(function () { idx = []; });
  }
  function closeSearch() { if (sb && !sb.hidden) { sb.hidden = true; if (lastFocus) lastFocus.focus(); } }
  $$("[data-search-open]").forEach(function (b) { b.addEventListener("click", openSearch); });
  $$("[data-search-close]").forEach(function (b) { b.addEventListener("click", closeSearch); });
  if (sb) sb.addEventListener("click", function (e) { if (e.target === sb) closeSearch(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeSearch();
    if (e.key === "/" && !/INPUT|TEXTAREA|SELECT/.test((document.activeElement || {}).tagName || "")) { e.preventDefault(); openSearch(); }
  });
  if (sq) sq.addEventListener("input", function () {
    var q = sq.value.trim().toLowerCase();
    sr.innerHTML = "";
    if (q.length < 2 || !idx) return;
    var terms = q.split(/\s+/);
    var hits = idx.map(function (d) {
      var hay = (d.t + " " + d.d + " " + (d.k || "")).toLowerCase(), s = 0;
      terms.forEach(function (t) { if (d.t.toLowerCase().indexOf(t) > -1) s += 3; else if (hay.indexOf(t) > -1) s += 1; else s -= 5; });
      return { d: d, s: s };
    }).filter(function (h) { return h.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 12);
    if (!hits.length) {
      var li = document.createElement("li"); li.innerHTML = '<a href="' + ROOT + 'tools.html"><b>Nothing matched</b><span>Try a shorter word, or browse all tools.</span></a>'; sr.appendChild(li); return;
    }
    hits.forEach(function (h) {
      var li = document.createElement("li"), a = document.createElement("a"), b = document.createElement("b"), s = document.createElement("span");
      a.href = ROOT + h.d.u; b.textContent = h.d.t; s.textContent = h.d.d; a.appendChild(b); a.appendChild(s); li.appendChild(a); sr.appendChild(li);
    });
  });

  /* ---- consent ---- */
  var ck = $("#cookie");
  if (ck && !store.get("consent", null)) ck.hidden = false;
  $$("[data-consent]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-consent"); store.set("consent", v); if (ck) ck.hidden = true;
      if (v === "essential") { (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1; DM.toast("Saved. Ads will be non-personalised."); }
    });
  });
  $$("[data-consent-reset]").forEach(function (b) { b.addEventListener("click", function () { if (ck) ck.hidden = false; }); });

  /* ---- video: load the player only when asked ---- */
  document.addEventListener("click", function (e) {
    var f = e.target.closest && e.target.closest(".vid-frame[data-yt]");
    if (!f || f.querySelector("iframe")) return;
    var id = f.getAttribute("data-yt");
    if (!/^[\w-]{11}$/.test(id)) return;
    var i = document.createElement("iframe");
    i.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
    i.title = f.getAttribute("aria-label") || "Video";
    i.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    i.allowFullscreen = true; i.loading = "lazy";
    f.innerHTML = ""; f.appendChild(i);
  });

  /* ---- list filters (market wire, videos, glossary) ---- */
  $$("[data-filter]").forEach(function (box) {
    var list = $(box.getAttribute("data-filter")); if (!list) return;
    var q = $("input[type=search]", box), chips = $$(".chip", box), count = $("[data-count]", box), cat = "";
    function run() {
      var t = q ? q.value.trim().toLowerCase() : "", n = 0;
      $$("[data-item]", list).forEach(function (it) {
        var okC = !cat || (" " + (it.getAttribute("data-cat") || "") + " ").indexOf(" " + cat + " ") > -1;
        var okT = !t || it.textContent.toLowerCase().indexOf(t) > -1;
        it.hidden = !(okC && okT); if (okC && okT) n++;
      });
      if (count) count.textContent = n + (n === 1 ? " result" : " results");
    }
    if (q) q.addEventListener("input", run);
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        cat = c.getAttribute("data-cat") || "";
        chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
        run();
      });
    });
  });

  /* ---- today's drill: rotates daily without a rebuild ---- */
  var drill = $("[data-drills]");
  if (drill) {
    try {
      var list = JSON.parse(drill.getAttribute("data-drills"));
      var day = Math.floor(Date.now() / 864e5);
      var d = list[day % list.length];
      $("[data-drill-t]", drill).textContent = d.t;
      $("[data-drill-d]", drill).textContent = d.d;
      var a = $("[data-drill-a]", drill); a.textContent = d.c; a.href = ROOT + d.u;
    } catch (e) {}
  }
})();
