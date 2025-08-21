import csv
import time
import json
import requests
from datetime import datetime
from urllib.parse import urlencode


COOKIE_STR = (
    "JSESSIONID=88177DCB3BB3EE1DF14BA277DF02F91D; TS0173272d=01ee71089814529aeeffe9217b13704027718c03dead8527977e9d97e3282d963824e50ccf2eb8056aa0446eda729f63ebd4436661; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=en; abb0e204f3eee1c5a6ef12a16ed04d43=292af034523e0a7b21df33fe07cd8ffb; _gid=GA1.2.266702140.1755774450; LICDETAIL_TYPE=all; TS019a838e=01ee710898cc0a05783a772c9cab2df097d0da76d768bb8ea23dcd7c155a0c87fb6876fbeec8c6e6e84183d7c2f41d95629fae0c47; _gat=1; BIGipServerPOOL_SFCAPPS_HTTPS=%00%FFb%80%C7%A9%CD%EE%AA%AD%7D%FD%DD%E7%BF%E7%8A%B8%7D)9%AD%AD%81%02%99%1E%E2%92%15%5C%8F%F6%AA%E8%C0%84wA%FC%B8%14%8A%AF%B6%E7zY%08%BCr%F3%CE%B9h%0E%80%B9%99%00%00%00%01; _ga=GA1.1.177061960.1755774450; _ga_PSYEMG5425=GS2.1.s1755774450$o1$g1$t1755775030$j18$l0$h0"
)


SEARCH_PREFIXES = list("abcdefghijklmnopqrstuvwxyz")

PAGE_LIMIT = 100

OUTPUT_CSV = "sfc_corporations.csv"




def cookie_str_to_dict(cookie_str: str) -> dict:
    cookies = {}
    for part in cookie_str.split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            cookies[k.strip()] = v.strip()
    return cookies


def build_headers() -> dict:
    return {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apps.sfc.hk",
        "Referer": "https://apps.sfc.hk/publicregWeb/searchByName?locale=en",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        ),
    }


def fetch_page(session: requests.Session, searchtext, start, limit):
    """Fetch one page for a given search text. Returns a list of rows (dicts)."""
    # _dc is cache-busting; use current ms
    dc = int(time.time() * 1000)
    url = f"https://apps.sfc.hk/publicregWeb/searchByNameJson?_dc={dc}"

    payload = {
        "licstatus": "active",
        "lictype": "all",
        "searchbyoption": "byname",
        "searchlang": "en",
        "entityType": "corporation",
        "searchtext": searchtext,
        "page": 1,
        "start": start,
        "limit": limit,
        "sort": '[{"property":"ceref","direction":"ASC"}]',
    }

    resp = session.post(url, data=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()


    rows = None
    for key in ("data", "rows", "list", "result", "results", "items"):
        if isinstance(data, dict) and key in data and isinstance(data[key], list):
            rows = data[key]
            break
    if rows is None:

        if isinstance(data, list):
            rows = data
        else:

            print("Unexpected JSON shape. Top-level keys:", list(data.keys()) if isinstance(data, dict) else type(data))
            rows = []

    return rows


def scrape_prefix(session: requests.Session, prefix):
    """Page through all results for a given search prefix."""
    all_rows = []
    start = 0
    while True:
        rows = fetch_page(session, prefix, start=start, limit=PAGE_LIMIT)
        if not rows:
            break
        all_rows.extend(rows)

        if len(rows) < PAGE_LIMIT:
            break
        start += PAGE_LIMIT

        time.sleep(0.5)
    print(f"[{prefix}] collected {len(all_rows)} rows")
    return all_rows


def write_csv(filename: str, records):
    if not records:
        print("No records to write.")
        return
    # Union of keys across all rows
    fieldnames = set()
    for r in records:
        if isinstance(r, dict):
            fieldnames.update(r.keys())
    fieldnames = sorted(fieldnames)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            if isinstance(r, dict):
                writer.writerow({k: r.get(k, "") for k in fieldnames})


def main():
    cookies = cookie_str_to_dict(COOKIE_STR)
    if not cookies or "JSESSIONID" not in cookies:
        print("ERROR: Please paste a valid COOKIE_STR with at least JSESSIONID.")
        return

    session = requests.Session()
    session.headers.update(build_headers())
    session.cookies.update(cookies)

    all_records: list[dict] = []
    for prefix in SEARCH_PREFIXES:
        try:
            rows = scrape_prefix(session, prefix)
            all_records.extend(rows)
        except requests.HTTPError as e:
            print(f"[{prefix}] HTTP error:", e)
        except Exception as e:
            print(f"[{prefix}] Error:", e)
        # short delay between prefixes
        time.sleep(0.5)

    write_csv(OUTPUT_CSV, all_records)
    print(f"Done. Wrote {len(all_records)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

