import os
import time
import json
from dotenv import load_dotenv
from firecrawl import Firecrawl
from bs4 import BeautifulSoup
from firecrawl.v2.utils.error_handler import RateLimitError

load_dotenv()
firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

INDEX_URL = "https://webb-site.com/dbpub/SFClicount.asp"

MAX_RETRIES = 5
INITIAL_BACKOFF = 2


def safe_firecrawl_scrape(url, formats=["html"]):
    retry = 0
    backoff = INITIAL_BACKOFF
    while retry < MAX_RETRIES:
        try:
            doc = firecrawl.scrape(url, formats=formats)
            return doc
        except RateLimitError as e:
            wait_time = backoff
            print(f"Rate limit exceeded. Retry {retry + 1} of {MAX_RETRIES} after {wait_time}s...")
            time.sleep(wait_time)
            backoff *= 2
            retry += 1
        except Exception as e:
            print(f"Error during scraping {url}: {e}")
            return None
    print(f"Failed to scrape {url} after {MAX_RETRIES} retries.")
    return None


def get_firm_links():
    print("Scraping firm index page...")
    doc = safe_firecrawl_scrape(INDEX_URL)
    if not doc:
        return []

    html = getattr(doc, "html", "")
    soup = BeautifulSoup(html, "html.parser")

    firms = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) > 1:
            link_tag = tds[1].find("a", href=True)
            if link_tag:
                firm_name = link_tag.text.strip()
                firm_url = link_tag["href"].replace("&amp;", "&")
                if not firm_url.startswith("http"):
                    firm_url = "https://webb-site.com" + firm_url
                firms.append((firm_name, firm_url))
    print(f"Found {len(firms)} firms.")
    return firms


def get_licensees_for_firm(firm_url):
    print(f"Scraping licensees for {firm_url} ...")
    doc = safe_firecrawl_scrape(firm_url)
    if not doc:
        return []

    html = getattr(doc, "html", "")
    soup = BeautifulSoup(html, "html.parser")

    licensees = []
    count = 0
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 7:
            try:
                name_link = tds[1].find("a", href=True)
                if not name_link:
                    continue
                name_text = name_link.text.strip()
                personal_url = name_link["href"].replace("&amp;", "&")
                if not personal_url.startswith("http"):
                    personal_url = "https://webb-site.com" + personal_url

                sfc_id = ""
                if "(" in name_text and ")" in name_text:
                    sfc_id = name_text.split("(")[-1].split(")")[0]
                    name = name_text.split("(")[0].strip()
                else:
                    name = name_text

                role = tds[5].text.strip()
                license_start = tds[6].text.strip()
                license_end = tds[7].text.strip() if len(tds) > 7 else ""

                licensees.append({
                    "name": name,
                    "sfc_id": sfc_id,
                    "role": role,
                    "license_start": license_start,
                    "license_end": license_end,
                    "personal_url": personal_url,
                })
                count += 1
                if count >= 5:
                    break
            except Exception as e:
                print(f"Error parsing licensee row: {e}")
    return licensees


def get_organizations_for_licensee(personal_url):
    print(f"Scraping organizations for licensee at {personal_url} ...")
    doc = safe_firecrawl_scrape(personal_url)
    if not doc:
        return []

    html = getattr(doc, "html", "")
    soup = BeautifulSoup(html, "html.parser")

    organizations = []
    count = 0
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 6:
            try:
                organization = tds[1].text.strip()
                role = tds[3].text.strip()
                activity = tds[4].text.strip()
                from_date = tds[5].text.strip()
                until_date = tds[6].text.strip() if len(tds) > 6 else ""

                organizations.append({
                    "organization": organization,
                    "role": role,
                    "activity": activity,
                    "from": from_date,
                    "until": until_date,
                })
                count += 1
                if count >= 2:
                    break
            except Exception as e:
                print(f"Error parsing organization row: {e}")
    return organizations


def main():
    firms = get_firm_links()
    result = []

    #Process only first 2 firms, remove slice for all
    for firm_name, firm_url in firms[:2]:
        print(f"Processing firm: {firm_name}")
        licensees = get_licensees_for_firm(firm_url)
        for lic in licensees:
            lic["organizations"] = get_organizations_for_licensee(lic["personal_url"])

        result.append({
            "firm_name": firm_name,
            "licensees": licensees
        })

    with open("sfc_licensee_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)



if __name__ == "__main__":
    main()
