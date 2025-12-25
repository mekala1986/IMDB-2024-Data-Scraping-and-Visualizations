import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def scrape_imdb_2024():
    print("🚀 Starting Robust Scraper...")
    options = Options()
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(30)

    try:
        url = "https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31"
        driver.get(url)
        time.sleep(10) 

        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(3)

        movies_data = []
        items = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
        print(f"🔍 Found {len(items)} movie containers...")

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text.split(". ", 1)[-1]
                try:
                    genre = item.find_element(By.CSS_SELECTOR, ".dli-genre").text
                except:
                    genre = "Drama" 

                meta_items = item.find_elements(By.CSS_SELECTOR, ".dli-title-metadata-item")
                duration = meta_items[1].text if len(meta_items) > 1 else "N/A"
                rating = item.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
                votes = item.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text.strip("()")

                movies_data.append({
                    "Movie Name": title,
                    "Genre": genre,
                    "Ratings": rating,
                    "Voting Counts": votes,
                    "Duration": duration
                })
            except:
                continue

        df = pd.DataFrame(movies_data)
        df.to_csv("imdb_2024_raw.csv", index=False)
        print(f"✅ Success! Captured {len(df)} movies.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_imdb_2024()