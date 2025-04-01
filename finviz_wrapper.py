# finviz_wrapper.py

import requests
from bs4 import BeautifulSoup
import time
import random

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}

BASE_URL = "https://finviz.com/quote.ashx?t="

# Qidiriladigan ko'rsatkichlar
TARGET_FIELDS = [
    "Market Cap", "P/E", "PEG", "P/S", "P/B", "EPS (ttm)",
    "Insider Own", "Inst Own", "ROA", "ROE", "Debt/Eq",
    "Current Ratio", "Short Float", "Target Price"
]

def get_finviz_data(ticker, delay_range=(1, 3)):
    time.sleep(random.uniform(*delay_range))  # Delay to avoid ban
    url = BASE_URL + ticker
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[X] {ticker} sahifasiga kirishda xatolik: {e}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    try:
        table = soup.find("table", class_="snapshot-table2")
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            for i in range(0, len(cols), 2):
                key = cols[i].get_text(strip=True)
                val = cols[i+1].get_text(strip=True)
                if key in TARGET_FIELDS:
                    data[key] = val
    except Exception as e:
        print(f"[X] {ticker} ma'lumotlarini ajratishda xatolik: {e}")

    return data
