import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.browser_config import get_undetected_driver
from utils.logger import log_error
from datetime import datetime
from deep_translator import GoogleTranslator

QUERIES = {
    "dengue06": '"dengue" "cases" OR "outbreak" after:2025-05-01 before:2025-06-01',
    "cholera07": '"cholera" "cases" OR "outbreak" after:2025-06-01 before:2025-07-01',
    "anthrax07": '"anthrax" "outbreak" after:2025-06-01 before:2025-07-01',
    "measles07": '"measles" "outbreak" after:2025-06-01 before:2025-07-01',
    "avianflu07": '"avian influenza" "outbreak" after:2025-06-01 before:2025-07-01'
}

os.makedirs("results/google", exist_ok=True)

def translate(text):
    try:
        return GoogleTranslator(source="auto", target="ru").translate(text)
    except:
        return "[ошибка перевода]"

def google_search(query_key, query_text):
    try:
        driver = get_undetected_driver()
        url = f"https://www.google.com/search?q={query_text.replace(' ', '+')}"
        driver.get(url)
        time.sleep(2)

        # Клик по cookies
        try:
            driver.find_element("xpath", '//button[contains(text(),"Accept")]').click()
            time.sleep(1)
        except:
            pass

        time.sleep(1)
        link_elements = driver.find_elements("xpath", '//div[@class="yuRUbf"]/a')
        links = [a.get_attribute("href") for a in link_elements if a.get_attribute("href")]

        title_elements = driver.find_elements("xpath", '//h3')
        titles = [el.text for el in title_elements if el.text.strip()]

        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"results/google/{query_key}_{today}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Query: {query_text}\nDate: {today}\n\n")
            for title, link in zip(titles, links):
                translation = translate(title)
                f.write(f"Original: {title}\n")
                f.write(f"Translated: {translation}\n")
                f.write(f"{link}\n\n")

        print(f"[✓] {query_key} — {len(links)} links saved")

    except Exception as e:
        log_error(query_key, str(e))
        print(f"[X] {query_key} — ошибка")
    finally:
        try:
            driver.quit()
        except:
            pass

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(google_search, key, query)
            for key, query in QUERIES.items()
        ]
        for future in as_completed(futures):
            pass

if __name__ == "__main__":
    main()
