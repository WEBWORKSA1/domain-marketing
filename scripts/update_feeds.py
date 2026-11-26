#!/usr/bin/env python3
"""Daily auto-refresh for Domain Marketing. Standard library only.

  news   : pulls headline, link, source and date from the trade-press feeds in data/sources.json
  videos : checks every curated video is still playable (YouTube oEmbed), learns its channel,
           then lists recent domain-related uploads from those same channels (public RSS)

Fault tolerant by design: a failing source is logged and skipped, earlier data is kept,
and the script always exits 0 so a bad day upstream never breaks the site.
"""
import datetime
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
UA = "Mozilla/5.0 (compatible; DomainMarketingRefresh/1.0; daily headline refresh)"
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "dc": "http://purl.org/dc/elements/1.1/"}
MAX_BYTES = 3_000_000
NOW = datetime.datetime.now(datetime.timezone.utc)


def fetch(url, timeout=25, accept="application/rss+xml, application/atom+xml, application/xml, text/xml, */*"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept, "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(MAX_BYTES)


def clean(s, n=180):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(html.unescape(s))
    s = re.sub(r"\s+", " ", s).strip()
    return (s[: n - 1].rstrip() + "…") if len(s) > n else s


def iso(s):
    s = (s or "").strip()
    if not s:
        return ""
    for parse in (parsedate_to_datetime, lambda x: datetime.datetime.fromisoformat(x.replace("Z", "+00:00"))):
        try:
            d = parse(s)
            if d.tzinfo is None:
                d = d.replace(tzinfo=datetime.timezone.utc)
            return d.astimezone(datetime.timezone.utc).isoformat(timespec="seconds")
        except Exception:
            continue
    return ""


def load(name, default):
    try:
        with open(os.path.join(DATA, name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save(name, obj):
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def ok_url(u):
    return isinstance(u, str) and re.match(r"^https?://[^\s<>\"']+$", u) is not None


# ----------------------------------------------------------------------------- news
def parse_feed(raw):
    raw = raw.lstrip(b"\xef\xbb\xbf \t\r\n")  # some feeds ship blank lines or a BOM before the XML declaration
    if not raw.startswith(b"<"):
        cut = min([i for i in (raw.find(b"<?xml"), raw.find(b"<rss"), raw.find(b"<feed")) if i >= 0] or [0])
        raw = raw[cut:]
    root = ET.fromstring(raw)
    out = []
    for e in root.iter("item"):
        out.append((e.findtext("title", ""), (e.findtext("link", "") or "").strip(),
                    e.findtext("pubDate", "") or e.findtext("dc:date", "", NS)))
    if not out:
        for e in root.findall("a:entry", NS):
            link = ""
            for l in e.findall("a:link", NS):
                if l.get("rel", "alternate") == "alternate":
                    link = l.get("href", "")
                    break
            out.append((e.findtext("a:title", "", NS), link, e.findtext("a:published", "", NS) or e.findtext("a:updated", "", NS)))
    return out


def refresh_news(src, old):
    per = int(src.get("per_feed", 8))
    keep = int(src.get("keep", 80))
    cutoff = NOW - datetime.timedelta(days=int(src.get("max_age_days", 75)))
    fresh, failed, log = [], set(), []
    for fd in src.get("feeds", []):
        try:
            got = 0
            for title, link, date in parse_feed(fetch(fd["url"])):
                t, d = clean(title), iso(date)
                if not t or not ok_url(link) or not d:
                    continue
                must = fd.get("must")
                if must and not any(m in t.lower() for m in must):
                    continue
                fresh.append({"t": t, "u": link, "s": fd["name"], "d": d})
                got += 1
                if got >= per:
                    break
            log.append(f"OK   {fd['name']}: {got}")
            if got == 0:
                failed.add(fd["name"])
        except Exception as ex:
            failed.add(fd["name"])
            log.append(f"FAIL {fd['name']}: {type(ex).__name__}: {ex}")
    names = {fd["name"] for fd in src.get("feeds", [])}
    merged, seen = [], set()
    # keep earlier items so a quiet or failing source does not vanish from the wire
    for it in fresh + [o for o in old.get("items", []) if o.get("s") in names or o.get("s") in failed]:
        key = it["u"].split("?")[0].rstrip("/")
        if key in seen or not ok_url(it.get("u")):
            continue
        seen.add(key)
        merged.append(it)
    merged.sort(key=lambda x: x.get("d", ""), reverse=True)
    recent = [m for m in merged if m.get("d", "") >= cutoff.isoformat(timespec="seconds")]
    items = (recent if len(recent) >= 12 else merged[:12])[:keep]
    return items, log, bool(fresh)


# ----------------------------------------------------------------------------- videos
def oembed(video_id):
    """Returns (status, author_name, author_url). status: ok | gone | unknown."""
    q = urllib.parse.urlencode({"url": f"https://www.youtube.com/watch?v={video_id}", "format": "json"})
    try:
        j = json.loads(fetch("https://www.youtube.com/oembed?" + q, accept="application/json"))
        return "ok", clean(j.get("author_name", ""), 60), j.get("author_url", "")
    except urllib.error.HTTPError as ex:
        return ("gone" if ex.code in (400, 401, 403, 404) else "unknown"), "", ""
    except Exception:
        return "unknown", "", ""


def channel_id_for(author_url):
    if not ok_url(author_url) or "youtube.com" not in author_url:
        return ""
    m = re.search(r"/channel/(UC[\w-]{22})", author_url)
    if m:
        return m.group(1)
    try:
        page = fetch(author_url, accept="text/html").decode("utf-8", "replace")
    except Exception:
        return ""
    for pat in (r'"channelId":"(UC[\w-]{22})"', r'"externalId":"(UC[\w-]{22})"', r"youtube\.com/channel/(UC[\w-]{22})"):
        m = re.search(pat, page)
        if m:
            return m.group(1)
    return ""


def refresh_videos(src, old):
    log, library, channels = [], [], load("channels.json", {})
    for v in old.get("library", []):
        if not re.match(r"^[\w-]{11}$", v.get("id", "")):
            continue
        status, name, url = oembed(v["id"])
        if status == "ok":
            v["ch"], v["au"], v["f"] = name or v.get("ch", ""), url or v.get("au", ""), 0
        elif status == "gone":  # removed, private or not embeddable: retire it
            log.append(f"GONE {v['id']} {v.get('t', '')[:50]}")
            continue
        library.append(v)
    log.append(f"OK   library: {len(library)} of {len(old.get('library', []))} playable")

    want = re.compile(src.get("video_include", r"\bdomain(s|ing|er|ers)?\b"), re.I)
    skip = re.compile(src.get("video_exclude", r"(?!x)x"), re.I)
    oldest = (NOW - datetime.timedelta(days=int(src.get("video_max_age_days", 300)))).isoformat(timespec="seconds")
    lib_ids = {v["id"] for v in library}
    latest, seen_ch = [], set()
    for v in library:
        au = v.get("au", "")
        if not au or au in seen_ch:
            continue
        seen_ch.add(au)
        cid = (channels.get(au) or {}).get("id") or channel_id_for(au)
        if not cid:
            log.append(f"SKIP channel {v.get('ch') or au}: id not resolved")
            continue
        channels[au] = {"id": cid, "name": v.get("ch", "")}
        try:
            root = ET.fromstring(fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
            n = 0
            for e in root.findall("a:entry", NS):
                vid = e.findtext("yt:videoId", "", NS)
                title = clean(e.findtext("a:title", "", NS), 140)
                link = e.find("a:link", NS)
                href = link.get("href", "") if link is not None else ""
                low = title.lower()
                if not re.match(r"^[\w-]{11}$", vid) or vid in lib_ids or "/shorts/" in href or "#shorts" in low:
                    continue
                when = iso(e.findtext("a:published", "", NS))
                if not want.search(title) or skip.search(title) or (when and when < oldest):
                    continue
                latest.append({"id": vid, "t": title, "ch": v.get("ch", ""), "d": when})
                n += 1
                if n >= 3:
                    break
            log.append(f"OK   channel {v.get('ch')}: {n}")
        except Exception as ex:
            log.append(f"FAIL channel {v.get('ch')}: {type(ex).__name__}: {ex}")
    if not latest and not any(l.startswith("OK   channel") for l in log):
        latest = old.get("latest", [])  # every channel failed: keep yesterday's list
    dedup, ids = [], set()
    for v in sorted(latest, key=lambda x: x.get("d", ""), reverse=True):
        if v["id"] not in ids:
            ids.add(v["id"])
            dedup.append(v)
    save("channels.json", channels)
    return library, dedup[: int(src.get("video_latest_keep", 24))], log


def main():
    src = load("sources.json", {})
    stamp = NOW.isoformat(timespec="seconds")
    report = {"at": stamp, "news": [], "videos": []}
    try:
        old_news = load("news.json", {"items": []})
        items, log, got = refresh_news(src, old_news)
        print("\n".join(["NEWS"] + log))
        report["news"] = log
        if items:
            save("news.json", {"updated": stamp if got else old_news.get("updated", stamp), "items": items})
    except Exception as ex:  # never fail the workflow
        print("NEWS step failed:", ex)
    try:
        old_v = load("videos.json", {"library": [], "latest": []})
        library, latest, log = refresh_videos(src, old_v)
        print("\n".join(["VIDEOS"] + log))
        report["videos"] = log
        if library:
            save("videos.json", {"updated": stamp, "library": library, "latest": latest})
    except Exception as ex:
        print("VIDEOS step failed:", ex)
    try:
        save("refresh-log.json", report)  # what each source did on the last run
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
