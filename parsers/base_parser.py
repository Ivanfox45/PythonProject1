from utils.browser_config import get_undetected_driver
from utils.file_saver import save_text_file
from utils.logger import log_error, log_success
from translators.deepl_translator import translate_text
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os


class BaseParser:
    SOURCE = "base"
    URL = None
    HEADLESS = True
    TIMEOUT = 10

    def __init__(self, results_dir="results"):
        self.results_dir = results_dir
        self.driver = get_undetected_driver(headless=self.HEADLESS)
        os.makedirs(os.path.join(self.results_dir, "html"), exist_ok=True)

    def set_results_dir(self, results_dir):
        """Allow setting results directory after initialization."""
        self.results_dir = results_dir
        os.makedirs(os.path.join(self.results_dir, "html"), exist_ok=True)

    def parse(self):
        try:
            if not self.URL:
                raise ValueError("URL is not set in parser.")
            self.driver.get(self.URL)
            self.accept_cookies()

            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            text = self.extract_text()
            if not text:
                raise Exception("Empty text extracted.")

            cleaned = self.clean_text(text)
            translated = translate_text(cleaned)
            self.save_text(translated)
            log_success(self.SOURCE, "Успешно сохранено")

        except Exception as e:
            log_error(self.SOURCE, str(e))
            self.save_html_debug()
        finally:
            try:
                self.driver.quit()
            except Exception:
                pass

    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(text(),"Accept")]')
                )
            ).click()
        except Exception:
            pass

    def extract_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def clean_text(self, text):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    def save_text(self, translated_text):
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{self.SOURCE}_{today}.txt"
        save_text_file(
            self.SOURCE,
            today,
            translated_text,
            filename,
            self.results_dir,
        )

    def save_html_debug(self):
        try:
            html = self.driver.page_source
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = os.path.join(
                self.results_dir,
                "html",
                f"{self.SOURCE}_{timestamp}.html",
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
        except Exception:
            pass
