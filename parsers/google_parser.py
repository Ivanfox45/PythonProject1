from utils.driver_context import create_driver
from utils.file_saver import save_text_file
from utils.logger import log_error
from translators.deepl_translator import translate_text
from datetime import datetime
import os

class google:
    def __init__(self, results_dir):
        self.results_dir = results_dir

    def parse(self):
        try:
            with create_driver("profile1") as driver:
                driver.get("<class 'parsers.google_query_parser.GoogleQueryParser'>")
                self.accept_cookies(driver)
                text = driver.find_element("tag name", "body").text
                translated = translate_text(text)
                today = datetime.now().strftime("%Y-%m-%d")
                filename = f"google_{today}.txt"
                save_text_file("google", today, translated, filename, self.results_dir)
        except Exception as e:
            log_error("google", str(e), self.results_dir)

    def accept_cookies(self, driver):
        try:
            driver.find_element("xpath", '//button[contains(text(),"Accept")]').click()
        except:
            pass
