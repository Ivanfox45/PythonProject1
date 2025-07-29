# utils/driver_context.py
import undetected_chromedriver as uc
from contextlib import contextmanager
import os

@contextmanager
def create_driver(profile_name="default"):
    driver = None
    try:
        user_data_path = os.path.abspath("user_data")
        profile_path = os.path.join(user_data_path, profile_name)

        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={user_data_path}")
        options.add_argument(f"--profile-directory={profile_name}")
        options.add_argument("--no-first-run --no-default-browser-check")
        options.add_argument("--start-maximized")

        driver = uc.Chrome(options=options)
        yield driver
    finally:
        if driver:
            driver.quit()
