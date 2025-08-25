# Scrape SFC and HK SFC Data

This project contains Python scripts for scraping financial data from:
- **Hong Kong SFC (Securities and Futures Commission)**
- **Public LinkedIn pages**
- **Webb-site SFC licence database**

## 📂 Project Structure
scrape_sfc_and_hksfc/
│── hksfc_scrape.py # Scraper for HK SFC website
│── sfc_website_scrape.py # Scraper for Webb-site SFC licences


## 🚀 Features
- Extract financial regulatory data from HK SFC
- Parse LinkedIn public data for open profiles
- Download & save SFC licence data to Excel

## 🛠 Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

## 📦 Installation
```bash
git clone <repo-url>
cd scrape_sfc_and_hksfc
pip install -r requirements.txt

# Scrape Webb-site SFC licences
python sfc_website_scrape.py

# Scrape HK SFC data
python hksfc_scrape.py

sfc_website_scrape.py → Saves results to sfc_licences.xlsx
```
## outputs
sfc_webisite_scrape.py → Saves results to sfc_licences.xlsx
The extraction process involves scraping publicly available data from the Hong Kong Securities and Futures Commission (SFC) licensee database on Webb-site using the Firecrawl API.
The tool fetches firm and licensee details, including individual names, SFC IDs, roles, license periods, and personal licensee page links,
then follows those links to gather associated organizational roles and activities. The data is cleaned, structured in JSON, and limited to a subset
(e.g., first 2 firms, first 5 licensees, and first 2 organizations) to demonstrate the pipeline's functionality while managing API rate limits and complexity.


hksfc_scrape.py → Saves results to hksfc_data.csv (or JSON depending on configuration inside the script)
Contains regulatory filings and notices scraped from the HK SFC website


