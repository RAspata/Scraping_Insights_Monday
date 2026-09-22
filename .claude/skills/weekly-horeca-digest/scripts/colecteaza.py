#!/usr/bin/env python3
"""Colecteaza stirile din feed-urile RSS listate in surse-horeca-retail.md.

Utilizare (din radacina repo-ului):
  python .claude/skills/weekly-horeca-digest/scripts/colecteaza.py
      -> afiseaza fereastra de timp, starea fiecarei surse si articolele noi
  python .claude/skills/weekly-horeca-digest/scripts/colecteaza.py --since 2026-09-14
      -> forteaza inceputul ferestrei
  python .claude/skills/weekly-horeca-digest/scripts/colecteaza.py --mark rapoarte/digest-2026-09-28.md
      -> adauga linkurile stirilor din raport in rapoarte/linkuri-procesate.txt

Doar biblioteca standard + curl (curl foloseste proxy-ul si certificatele mediului).
"""
import argparse
import html
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[4]
SOURCES = ROOT / "surse-horeca-retail.md"
REPORTS = ROOT / "rapoarte"
LEDGER = REPORTS / "linkuri-procesate.txt"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"
MAX_PAGES = 30
MAX_WINDOW_DAYS = 21

# Pentru feed-urile marcate "(filtrat)": pastram doar titlurile/categoriile care
# se potrivesc cu unul dintre aceste tipare (text fara diacritice, lowercase).
# Tiparele sunt ancorate la inceput de cuvant; cele scurte si la final (ex. "bere").
KEYWORDS = re.compile(r"\b(" + "|".join([
    r"horeca", r"restaurant", r"cafenea", r"cafenel", r"cafea", r"coffee", r"bistro",
    r"bar\b", r"baruri", r"terasa", r"terase", r"fast[- ]?food", r"food", r"mancare",
    r"gastronom", r"culinar", r"bucatar", r"chef\b", r"meniu", r"livrar", r"delivery",
    r"glovo", r"wolt", r"tazz", r"bolt food", r"catering", r"patiser", r"brutar",
    r"cofetar", r"pizz", r"burger", r"kebab", r"shaorm", r"mcdonald", r"kfc",
    r"starbucks", r"popeyes", r"spartan", r"franciz", r"ospitalitat", r"alimentar",
    r"bere\b", r"berari", r"vinuri", r"crama", r"ghost kitchen", r"food hall",
    r"ospatar", r"bacsis",
]) + r")")

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Europe/Bucharest")
except Exception:  # fara tzdata (ex. Windows) -> aproximare
    TZ = timezone(timedelta(hours=3))


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def normalize_url(u):
    p = urlsplit(u.strip())
    q = [(k, v) for k, v in parse_qsl(p.query) if not k.lower().startswith(("utm_", "fbclid", "gclid"))]
    path = p.path.rstrip("/") or "/"
    return urlunsplit((p.scheme.lower(), p.netloc.lower().removeprefix("www."), path, urlencode(q), ""))


def parse_sources():
    sources, cur = [], None
    for line in SOURCES.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- \[(.+?)\]\((\S+?)\)", line)
        if m:
            cur = {"name": m.group(1), "home": m.group(2), "feeds": [], "pages": []}
            sources.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^\s+- Feed(?: \((filtrat)\))?: (\S+)", line)
        if m:
            cur["feeds"].append((m.group(2), bool(m.group(1))))
            continue
        m = re.match(r"^\s+- Pagină HoReCa/food: (\S+)", line)
        if m:
            cur["pages"].append(m.group(1))
    return sources


def fetch(url):
    """Returneaza (status, body). status: 'ok', 'blocat', 'eroare HTTP xxx', 'eroare'."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30", "-w", "\n__HTTP__%{http_code}", url],
            capture_output=True, timeout=60,
        )
    except Exception as e:
        return f"eroare ({e.__class__.__name__})", ""
    out = r.stdout.decode("utf-8", errors="replace")
    body, _, code = out.rpartition("\n__HTTP__")
    err = r.stderr.decode("utf-8", errors="replace")
    if r.returncode == 56 or "CONNECT tunnel failed" in err or "403" in err and code == "000":
        return "blocat (proxy de retea)", ""
    if r.returncode != 0:
        return f"eroare curl {r.returncode}", ""
    if code != "200":
        return f"eroare HTTP {code}", ""
    return "ok", body


def text_of(block, tag):
    m = re.search(rf"<{tag}\b[^>]*>(.*?)</{tag}>", block, re.S)
    if not m:
        return ""
    v = m.group(1).strip()
    v = re.sub(r"^<!\[CDATA\[(.*)\]\]>$", r"\1", v, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", v)).strip()


def parse_items(xml):
    items = []
    for block in re.findall(r"<item\b.*?</item>", xml, re.S):
        link = text_of(block, "link") or text_of(block, "guid")
        date_s = text_of(block, "pubDate") or text_of(block, "dc:date")
        try:
            dt = parsedate_to_datetime(date_s)
        except Exception:
            try:
                dt = datetime.fromisoformat(date_s.replace("Z", "+00:00"))
            except Exception:
                dt = None
        if dt is not None and dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        cats = [html.unescape(c) for c in re.findall(r"<category[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</category>", block, re.S)]
        items.append({"title": text_of(block, "title"), "link": link, "date": dt, "cats": cats})
    return items


def page_url(feed, n):
    if n == 1:
        return feed
    return feed + ("&" if "?" in feed else "?") + f"paged={n}"


def collect_feed(feed, since):
    """Parcurge paginile feed-ului pana trece de `since`. Returneaza (status, items, acoperit)."""
    all_items, seen_first = [], set()
    for n in range(1, MAX_PAGES + 1):
        status, body = fetch(page_url(feed, n))
        if status != "ok":
            return (status if n == 1 else "ok"), all_items, False
        items = parse_items(body)
        if not items:
            return ("feed gol" if n == 1 else "ok"), all_items, n > 1
        first = items[0]["link"]
        if first in seen_first:  # feed-ul ignora paginarea
            return "ok", all_items, False
        seen_first.add(first)
        all_items.extend(items)
        dated = [i["date"] for i in items if i["date"]]
        if dated and min(dated) < since:
            return "ok", all_items, True
    return "ok", all_items, False


def load_ledger():
    if not LEDGER.exists():
        return set()
    urls = set()
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            urls.add(normalize_url(parts[1]))
    return urls


def default_since(now):
    today = now.astimezone(TZ).date()
    dates = []
    for p in REPORTS.glob("digest-*.md"):
        m = re.match(r"digest-(\d{4}-\d{2}-\d{2})\.md$", p.name)
        if m:
            d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            if d < today:
                dates.append(d)
    start = max(dates) if dates else today - timedelta(days=7)
    start = max(start, today - timedelta(days=MAX_WINDOW_DAYS))
    return datetime(start.year, start.month, start.day, tzinfo=TZ)


def cmd_collect(args):
    now = datetime.now(timezone.utc)
    since = (datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=TZ) if args.since else default_since(now))
    ledger = load_ledger()
    print(f"# Fereastra: {since.astimezone(TZ):%Y-%m-%d %H:%M} -> {now.astimezone(TZ):%Y-%m-%d %H:%M} (Europe/Bucharest)")
    print(f"# Linkuri deja publicate in rapoarte anterioare: {len(ledger)}\n")

    status_rows, sections = [], []
    for src in parse_sources():
        if not src["feeds"]:
            status_rows.append((src["name"], "fara feed", 0, 0, "verifica paginile/homepage"))
            continue
        kept, dropped, statuses, covered_all = [], 0, [], True
        seen = set()
        for feed, filtered in src["feeds"]:
            status, items, covered = collect_feed(feed, since)
            statuses.append(status)
            if status != "ok":
                covered_all = False
                continue
            covered_all &= covered
            for it in items:
                if not it["date"] or it["date"] < since or not it["link"]:
                    continue
                key = normalize_url(it["link"])
                if key in seen:
                    continue
                seen.add(key)
                if key in ledger:
                    dropped += 1
                    continue
                if filtered and not KEYWORDS.search(fold(it["title"] + " " + " ".join(it["cats"]))):
                    continue
                kept.append(it)
        st = "ok" if all(s == "ok" for s in statuses) else "; ".join(statuses)
        note = "feed complet pe fereastra" if covered_all and st == "ok" else "feed INCOMPLET -> verifica si paginile HoReCa/food"
        status_rows.append((src["name"], st, len(kept), dropped, note))
        if kept:
            kept.sort(key=lambda i: i["date"], reverse=True)
            sections.append((src, kept))

    print("## Stare surse\n")
    print("| Sursa | Stare | Articole noi | Deja publicate | Observatie |")
    print("|---|---|---|---|---|")
    for r in status_rows:
        print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")
    with_feed = [r for r in status_rows if r[1] != "fara feed"]
    if with_feed and all(r[1].startswith("blocat") for r in with_feed):
        print("\n!! TOATE feed-urile sunt blocate de reteaua mediului. NU scrie si NU publica"
              " niciun raport; opreste-te si raporteaza problema (vezi SKILL.md, pasul 1).")
        sys.exit(3)
    print("\n## Articole din feed-uri (in fereastra, nepublicate inca)\n")
    for src, items in sections:
        print(f"### {src['name']}")
        if src["pages"]:
            print("Pagini HoReCa/food: " + ", ".join(src["pages"]))
        for it in items:
            cats = f" [{', '.join(it['cats'][:4])}]" if it["cats"] else ""
            print(f"- {it['date'].astimezone(TZ):%Y-%m-%d %H:%M} | {it['title']}{cats} | {it['link']}")
        print()


def cmd_mark(report):
    text = Path(report).read_text(encoding="utf-8")
    m = re.search(r"^## Toate [sșş]tirile.*?$(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        sys.exit("Nu gasesc sectiunea '## Toate stirile' in raport.")
    day = re.search(r"(\d{4}-\d{2}-\d{2})", Path(report).name)
    day = day.group(1) if day else datetime.now(TZ).strftime("%Y-%m-%d")
    existing = load_ledger()
    new, title = [], ""
    for line in m.group(1).splitlines():
        h = re.match(r"^###\s+(?:\d+/10\s+[—-]\s+)?(.*)$", line)
        if h:
            title = h.group(1).strip()
            continue
        for u in re.findall(r"https?://[^\s)>\]]+", line):
            key = normalize_url(u)
            if key not in existing:
                existing.add(key)
                new.append(f"{day}\t{u}\t{title}")
    if new:
        REPORTS.mkdir(exist_ok=True)
        with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(new) + "\n")
    print(f"Adaugate {len(new)} linkuri in {LEDGER.relative_to(ROOT)}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD, inceputul ferestrei (implicit: data ultimului raport)")
    ap.add_argument("--mark", metavar="RAPORT", help="adauga linkurile din raport in registrul de linkuri publicate")
    args = ap.parse_args()
    if args.mark:
        cmd_mark(args.mark)
    else:
        cmd_collect(args)


if __name__ == "__main__":
    main()
