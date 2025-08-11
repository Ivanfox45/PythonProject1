"""Browser configuration helpers."""
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from fake_useragent import UserAgent


def get_undetected_driver(headless: bool = False):
    """Return an undetected Chrome driver with optional headless mode.

    The driver binary is automatically downloaded and kept up to date via
    ``webdriver_manager``. A random user agent is applied to reduce the
    likelihood of being blocked.
    """
    ua = UserAgent()
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--lang=en-US")
    options.add_argument(f"user-agent={ua.random}")

    if headless:
        options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    return uc.Chrome(service=service, options=options)
