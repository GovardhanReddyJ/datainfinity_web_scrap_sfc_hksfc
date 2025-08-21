# Scrape SFC and HK SFC Data

This project contains Python scripts for scraping financial data from:
- **Hong Kong SFC (Securities and Futures Commission)**
- **Public LinkedIn pages**
- **Webb-site SFC licence database**

## 📂 Project Structure
scrape_sfc_and_hksfc/
│── hksfc_scrape.py # Scraper for HK SFC website
│── scrape.py # Scraper for Webb-site SFC licences


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
python scrape.py

# Scrape HK SFC data
python hksfc_scrape.py

scrape.py → Saves results to sfc_licences.xlsx
```
## outputs
scrape.py → Saves results to sfc_licences.xlsx
Contains structured tabular data of SFC licence records.

hksfc_scrape.py → Saves results to hksfc_data.csv (or JSON depending on configuration inside the script)
Contains regulatory filings and notices scraped from the HK SFC website


