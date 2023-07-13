import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


class Parser:
    def __init__(self, url: str, items: list, count: int=3, version_main=114):
        self.url = url
        self.items = items
        self.count = count
        self.version_main = version_main
        self.data = []

    def set_up(self):
        self.driver = uc.Chrome(version_main=self.version_main)

    def get_url(self):
        self.driver.get(self.url)

    def paginator(self):
        while self.driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]') and self.count > 0:
            self.parse_page()
            self.driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]').click()
            self.count -= 1

    def parse_page(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
        for item in items:
            # name = item.find_element(By.CSS_SELECTOR, '[ itemprop="name" ]').text
            try:
                description = item.find_element(By.CSS_SELECTOR, '[ class*="item-description" ]').text
            except BaseException:
                description = "0"
            link = item.find_element(By.CSS_SELECTOR, '[ data-marker="item-title" ]').get_attribute("href")
            price = item.find_element(By.CSS_SELECTOR, '[ itemprop="price" ]').get_attribute("content")
            # price_per_sq_m = title.find_element(By.CSS_SELECTOR, '[
            text = item.text.split('\n')[:3]
            name, price, price_per_sq_m = text
            print(name, description, link, price, price_per_sq_m)

    def safe_data(self):
        with open("items.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def parse(self):
        self.set_up()
        self.get_url()
        self.paginator()


if __name__ == "__main__":
    Parser(url='https://www.avito.ru/novorossiysk/kvartiry/prodam/do-3500000-rubley-ASgBAgECAUSSA8YQAUXGmgwXeyJmcm9tIjowLCJ0byI6MzUwMDAwMH0?f=ASgBAQECAUSSA8YQAUDKCDT~WIBZglkCRYQJFXsiZnJvbSI6MjIsInRvIjpudWxsfcaaDBd7ImZyb20iOjAsInRvIjozNTAwMDAwfQ&s=1',
           count=1, items=[116]).parse()
