from datetime import datetime
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator
from utils.driver_context import create_driver
from utils.logger import log_error

QUERIES = {
    "dengue06": '"dengue" "cases" OR "outbreak" after:2025-05-01 before:2025-06-01',
    "cholera07": '"cholera" "cases" OR "outbreak" after:2025-06-01 before:2025-07-01',
    "anthrax07": '"anthrax" "outbreak" after:2025-06-01 before:2025-07-01',
    "measles07": '"measles" "outbreak" after:2025-06-01 before:2025-07-01',
    "avianflu07": '"avian influenza" "outbreak" after:2025-06-01 before:2025-07-01'
}

class GoogleQueryParser:
    def __init__(self, results_dir):
        self.results_dir = results_dir
        self.google_dir = os.path.join(self.results_dir, "google")

    def translate(self, text):
        try:
            return GoogleTranslator(source="auto", target="ru").translate(text)
        except:
            return "[ошибка перевода]"

    def search_one(self, query_key, query_text):
        try:
            with create_driver() as driver:
                url = f"https://www.google.com/search?q={query_text.replace(' ', '+')}"
                driver.get(url)
                time.sleep(2)

                # Клик по cookies
                try:
                    driver.find_element("xpath", '//button[contains(text(),"Accept")]').click()
                    time.sleep(1)
                except:
                    pass

                # Сбор ссылок и заголовков
                link_elements = driver.find_elements("xpath", '//div[@class="yuRUbf"]/a')
                links = [a.get_attribute("href") for a in link_elements if a.get_attribute("href")]

                title_elements = driver.find_elements("xpath", '//h3')
                titles = [el.text for el in title_elements if el.text.strip()]

                # Сохраняем
                today = datetime.now().strftime("%Y-%m-%d")
                filename = f"{query_key}_{today}.txt"
                file_path = os.path.join(self.google_dir, filename)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"Query: {query_text}\nDate: {today}\n\n")
                    for title, link in zip(titles, links):
                        translated = self.translate(title)
                        f.write(f"Original: {title}\n")
                        f.write(f"Translated: {translated}\n")
                        f.write(f"{link}\n\n")

                print(f"[✓] Google {query_key} — {len(links)} links saved")

        except Exception as e:
            log_error(f"google:{query_key}", str(e), self.results_dir)

    def parse(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.search_one, key, query)
                for key, query in QUERIES.items()
            ]
            for future in as_completed(futures):
                pass
