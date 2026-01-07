import time
import pandas as pd
from playwright.sync_api import sync_playwright  #browser automation library

SEARCH_QUERY = "marketing ideas"   # change as needed

def scrape_pinterest(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        page = browser.new_page()

        search_url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
        print("Opening:", search_url)
        
        page.goto(search_url, timeout=60000)
        time.sleep(5)

        # Auto Scroll to load pins
        for _ in range(8):
            page.mouse.wheel(0, 2000)
            time.sleep(1.5)

        print("Extracting pins...")

        pins = page.query_selector_all("a[href*='/pin/']")
        data = []

        # save all pin urls
        for pin in pins:
            href = pin.get_attribute("href")
            if href and "/pin/" in href:
                full_url = "https://www.pinterest.com" + href
                data.append({"pin_url": full_url})

        browser.close()

    return data


# MAIN
pins = scrape_pinterest(SEARCH_QUERY)

df = pd.DataFrame(pins)

# 👉 Save Excel file OUTSIDE src, inside /data
filename = "../../data/pinterest_data.xlsx"
df.to_excel(filename, index=False)

print(f"Scraped {len(df)} pins and saved to {filename}")
