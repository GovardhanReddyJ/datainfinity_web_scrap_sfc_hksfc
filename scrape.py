
import sys
import json
import time
from typing import Dict, List, Tuple
import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://webb-site.com/dbpub/SFClicount.asp"
OUTFILE = "sfc_licences.xlsx"


def make_session() -> requests.Session:
    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; SFC-scraper/1.0; +https://example.com)",
        "Referer": BASE_URL,
    })
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s

def discover_form_fields(html: str) -> List[Tuple[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    form = soup.find("form")
    if not form:
        return []
    fields = []
    for inp in form.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        value = inp.get("value", "")
        fields.append((name, value))
    for sel in form.find_all("select"):
        name = sel.get("name")
        if not name:
            continue
        # pick selected option or first
        opt = sel.find("option", selected=True) or sel.find("option")
        value = opt.get("value", "") if opt else ""
        fields.append((name, value))
    return fields


def fetch_html(session: requests.Session, method: str = "GET", params: Dict = None) -> str:
    params = params or {}
    if method.upper() == "POST":
        resp = session.post(BASE_URL, data=params, timeout=30)
    else:
        resp = session.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_tables(html: str) -> List[pd.DataFrame]:

    try:
        tables = pd.read_html(html)
    except ValueError:
        tables = []
    return tables

def save_to_excel(tables: List[pd.DataFrame], path: str) -> None:
    if not tables:
        print("[!] No tables found; nothing to save.")
        return

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for i, df in enumerate(tables, start=1):

            df.columns = [str(c).replace("Unnamed: 0", "").strip() for c in df.columns]
            sheet = f"Table{i}"
            df.to_excel(writer, sheet_name=sheet, index=False)
    print(f"[+] Saved {len(tables)} table(s) → {path}")

def main():

    method = "GET"
    params = {}
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--method" and i + 1 < len(args):
            method = args[i + 1].upper()
        if a == "--params" and i + 1 < len(args):
            try:
                params = json.loads(args[i + 1])
            except json.JSONDecodeError:
                print("[!] Could not parse --params JSON. Example: --params '{\"key\":\"value\"}'")
                return

    session = make_session()


    print(f"[*] Requesting {BASE_URL} ({method}) with params: {params or '(none)'}")
    html = fetch_html(session, method=method, params=params)


    tables = parse_tables(html)
    if tables:
        print(f"[+] Found {len(tables)} table(s).")
        save_to_excel(tables, OUTFILE)
        return

    print("[!] No tables parsed. Dumping form field hints so you can set correct names/values...")
    fields = discover_form_fields(html)
    if not fields:
        print("    (No <form> found on the page.)")
        return

    seen = {}
    for name, value in fields:
        seen.setdefault(name, set()).add(value)
    print("    Candidate form fields and example values:")
    for name, values in seen.items():
        example = next(iter(values)) if values else ""
        print(f"    - {name}: e.g. '{example}'")


if __name__ == "__main__":
    main()
