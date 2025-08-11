# utils/driver_context.py
import os
from contextlib import contextmanager

import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@contextmanager
def create_driver(profile_name="default"):
    driver = None
    try:
        user_data_path = os.path.abspath("user_data")

        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={user_data_path}")
        options.add_argument(f"--profile-directory={profile_name}")
        options.add_argument("--no-first-run --no-default-browser-check")
        options.add_argument("--start-maximized")

        service = Service(ChromeDriverManager().install())
        driver = uc.Chrome(service=service, options=options)
        yield driver
    finally:
        if driver:
            driver.quit()
