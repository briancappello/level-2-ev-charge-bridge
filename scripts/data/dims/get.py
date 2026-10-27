#!/home/brian/.venvs/camoufox/bin/python
import sys
from camoufox.sync_api import Camoufox

url, out = sys.argv[1], sys.argv[2]
with Camoufox(headless=True, humanize=False, geoip=False, i_know_what_im_doing=True) as b:
    ctx = b.new_context(accept_downloads=True)
    page = ctx.new_page()
    if out.endswith(".pdf"):
        resp = ctx.request.get(url, timeout=60000)
        open(out, "wb").write(resp.body())
    else:
        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        for _ in range(40):
            page.wait_for_timeout(1000)
            t = page.inner_text("body")
            if "security verification" not in t and "Waiting for" not in t and len(t) > 2000:
                break
        page.wait_for_timeout(3000)
        open(out, "w").write(page.url + "\n" + page.inner_text("body"))
