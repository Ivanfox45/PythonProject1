from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

def get_undetected_driver(headless=False):
    ua = UserAgent()
    options = uc.ChromeOptions()
    #options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--lang=en-US")
    options.add_argument("user-agent=Mozilla/5.0 ...")  # можно использовать fake_useragent
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument(f'user-agent={ua.random}')

    if headless:
        options.add_argument("--headless=new")

    driver = uc.Chrome(options=options)
    return driver
