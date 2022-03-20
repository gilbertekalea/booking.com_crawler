from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import *
from booking import helpers


class BookingPagenation:
    def __init__(self, page: WebDriver):
        self.page = page

    def get_property_count(self):
        try:
            container_div = self.page.find_element(
                By.CSS_SELECTOR, 'div[class="_b2280f5e6"]'
            )
            city_div = container_div.find_element(
                By.CSS_SELECTOR, 'div[class="_111b4b398"]'
            )
            text = city_div.text
            prop_count = int(helpers.find_number_in_string(text))

        except NoSuchElementException:
            prop_count = 1
        return prop_count

    def helpers(self):
        try:
            container_div = self.page.find_element(
                By.CSS_SELECTOR, 'div[class="_b2280f5e6"]'
            )
            page_div_elem = container_div.find_element(
                By.CSS_SELECTOR, 'div[data-testid="pagination"]'
            )
            page_nav_elem = page_div_elem.find_element(
                By.CSS_SELECTOR, 'nav[class="_09161c483"]'
            )
        except NoSuchElementException:
            pass

        return page_nav_elem

    def go_next_page(self):
        try:
            page_nav_elem = self.helpers()
            next_button = page_nav_elem.find_element(
                By.CSS_SELECTOR, 'button[aria-label="Next page"]'
            )
            next_button.click()

        except NoSuchElementException: 
            pass

    def return_first_page(self):
        elem = self.helpers()
        ol_elem = elem.find_element(By.CSS_SELECTOR, 'ol[class="_5312cbccb"]')
        li_elem = ol_elem.find_elements(By.CSS_SELECTOR, 'li[class="ce83a38554"]')

        for item in li_elem:
            if (
                item.find_element(By.TAG_NAME, "button").get_attribute("innerHTML")
                == "1"
            ):
                item.click()
