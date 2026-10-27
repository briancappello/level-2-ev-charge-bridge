#!/usr/bin/env python3
"""Camoufox CLI for searching the web and fetching pages as text.

  cfx search "query" [-n 10]   DuckDuckGo results: title, URL, snippet
  cfx fetch URL [-c 20000]     page text (PDFs downloaded and run through pdftotext)
"""
import argparse, subprocess, sys, tempfile, urllib.parse
from camoufox.sync_api import Camoufox


def browser():
    return Camoufox(headless=True, humanize=False, geoip=False, i_know_what_im_doing=True)


def search(q, n):
    with browser() as b:
        page = b.new_page()
        page.goto("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q), timeout=45000)
        results = page.eval_on_selector_all(
            ".result",
            """els => els.map(e => ({
                title: e.querySelector('.result__a')?.innerText || '',
                href: e.querySelector('.result__a')?.href || '',
                snippet: e.querySelector('.result__snippet')?.innerText || ''}))""",
        )
    out = []
    for r in results:
        href = r["href"]
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
        if "uddg" in qs:
            href = qs["uddg"][0]
        if not r["title"] or "duckduckgo.com/y.js" in href:
            continue
        out.append((r["title"].strip(), href, r["snippet"].strip()))
    if not out:
        sys.exit("no results (possibly rate-limited); try again shortly")
    for i, (t, h, s) in enumerate(out[:n], 1):
        print(f"{i}. {t}\n   {h}\n   {s}\n")


def fetch(url, cap):
    with browser() as b:
        ctx = b.new_context(accept_downloads=True)
        page = ctx.new_page()
        resp = ctx.request.get(url, timeout=60000)
        if "pdf" in resp.headers.get("content-type", "") or resp.body()[:5] == b"%PDF-":
            with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
                f.write(resp.body()); f.flush()
                text = subprocess.run(["pdftotext", "-layout", f.name, "-"],
                                      capture_output=True, text=True).stdout
        else:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(1500)
            for _ in range(25):  # let Cloudflare-style interstitials clear
                if not any(k in page.title() for k in ("Just a moment", "Attention Required", "Security check")):
                    break
                page.wait_for_timeout(1000)
            text = f"# {page.title()}\n{page.url}\n\n" + page.inner_text("body")
    print(text[:cap])
    if len(text) > cap:
        print(f"\n[truncated at {cap} of {len(text)} chars; use -c to raise]")


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = ap.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("-n", type=int, default=10)
f = sub.add_parser("fetch"); f.add_argument("url"); f.add_argument("-c", type=int, default=20000)
a = ap.parse_args()
search(a.query, a.n) if a.cmd == "search" else fetch(a.url, a.c)
