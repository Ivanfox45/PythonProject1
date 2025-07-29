from utils.browser_config import get_undetected_driver
import time

class GoogleSearch:
    def __init__(self, query):
        self.query = query
        self.url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        self.driver = get_undetected_driver()

    def search(self):
        try:
            self.driver.get(self.url)
            self.accept_cookies()
            time.sleep(2)
            links = []
            results = self.driver.find_elements("xpath", '//div[@class="yuRUbf"]/a')
            for r in results[:10]:
                links.append(r.get_attribute("href"))
            return links
        finally:
            self.driver.quit()

    def accept_cookies(self):
        try:
            self.driver.find_element("xpath", '//button[contains(text(),"Accept all")]').click()
        except:
            pass
