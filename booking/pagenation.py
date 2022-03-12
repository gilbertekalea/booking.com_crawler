from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from booking import helpers


class BookingPagenation:
    def __init__(self, page: WebDriver):
        self.page = page

    def get_property_count(self):
        container_div = self.page.find_element(
            By.CSS_SELECTOR, 'div[class="_b2280f5e6"]'
        )
        city_div = container_div.find_element(
            By.CSS_SELECTOR, 'div[class="_111b4b398"]'
        )
        text = city_div.text
        prop_count = int(helpers.find_number_in_string(text))
        return prop_count

    def go_next_page(self):
        container_div = self.page.find_element(
            By.CSS_SELECTOR, 'div[class="_b2280f5e6"]'
        )
        page_div_elem = container_div.find_element(
            By.CSS_SELECTOR, 'div[data-testid="pagination"]'
        )
        page_nav_elem = page_div_elem.find_element(
            By.CSS_SELECTOR, 'nav[class="_09161c483"]'
        )

        next_button = page_nav_elem.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Next page"]'
        )
        next_button.click()
