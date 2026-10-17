"""Verify the deployed public GitHub Pages site after publishing.

Usage: python analytics/verify_live.py https://natinaelaberashi.github.io/cloud-desk-it-support/
Checks HTTP responses, expected dashboard DOM, current JavaScript and 600-row CSV.
"""
import csv
import io
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

def get(base, path):
    url = urljoin(base.rstrip("/") + "/", path)
    request = Request(url, headers={"User-Agent": "service-desk-deployment-check/1.0", "Cache-Control": "no-cache"})
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"{url}: HTTP {response.status}")
        return response.read().decode("utf-8-sig")

def verify(base, expected_sha=None):
    if expected_sha:
        deployed_sha = get(base, "deployment-version.txt").strip()
        if deployed_sha != expected_sha:
            raise AssertionError(f"Published commit {deployed_sha} does not match expected {expected_sha}")
    html = get(base, "index.html")
    for marker in ('id="trends"', 'id="teams"', 'id="load-status"', 'id="resetBtn"'):
        if marker not in html:
            raise AssertionError(f"Published HTML missing {marker}")
    js = get(base, "app.js")
    if 'data/incidents_extended.csv' not in js or 'status==="Resolved"' not in js:
        raise AssertionError("Published JS is not the analytics dashboard")
    rows = list(csv.DictReader(io.StringIO(get(base, "data/incidents_extended.csv"))))
    if len(rows) != 600 or len({row["id"] for row in rows}) != 600:
        raise AssertionError("Published CSV must have 600 unique incidents")
    print(f"PASS: live HTML, JavaScript and {len(rows)} CSV incidents at {base}")

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "https://natinaelaberashi.github.io/cloud-desk-it-support/"
    expected_sha = sys.argv[2] if len(sys.argv) > 2 else None
    for attempt in range(1, 13):
        try:
            verify(base, expected_sha)
            return
        except (AssertionError, RuntimeError, HTTPError, URLError, TimeoutError) as exc:
            print(f"Attempt {attempt}/12: {exc}", flush=True)
            if attempt == 12:
                raise
            time.sleep(10)

if __name__ == "__main__":
    main()
