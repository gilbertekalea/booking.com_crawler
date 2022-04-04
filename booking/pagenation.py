# This file contain methods that allow the webdriver to perform pagenation functionality.

# Can click next page, or return back to the first page.
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import *
from booking import helpers


class BookingPagenation:

    def __init__(self, next_pager: WebDriver):
        self.next_pager = next_pager

    # Get the property count from the page.
    def get_property_count(self):
        try:
            container_div = self.next_pager.find_element(
                By.CSS_SELECTOR, 'div[data-capla-component="b-search-web-searchresults/PropertiesListDesktop"]'
            )
            propery_found = container_div.find_element(
                By.CSS_SELECTOR, 'div[class="d8f77e681c"]'
            )
            text = propery_found.text
            prop_count = int(helpers.find_number_in_string(text))

        except NoSuchElementException:
            prop_count = 1

        return prop_count

    # This method will return the page pagenation container element.
    def helpers(self):

        try:
            container_div = self.next_pager.find_element(
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

    # This method will return the next page element and clicks next page button.
    def go_next_page(self):

        '''
        This method will return the next page element and clicks next page button.
        '''
        print('go_next_page I hope this works')
        try:
            # container_div = self.next_pager.find_element(
            #     By.CSS_SELECTOR, 'div[class="_b2280f5e6"]'
            # )
            page_div_elem = self.next_pager.find_element(
                By.CSS_SELECTOR, 'div[data-testid="pagination"]'
            )
            page_nav_elem = page_div_elem.find_element(
                By.CSS_SELECTOR, 'nav[class="d493c719bc"]'
            )
            elem_group = page_nav_elem.find_element(By.CSS_SELECTOR, 'div[role="group"]')
            div_elem = elem_group.find_element(By.CSS_SELECTOR, 'div[class="f32a99c8d1 f78c3700d2"]')

            next_button = div_elem.find_element(
                By.CSS_SELECTOR, 'button[aria-label="Next page"]'
            )
            next_button.click()

        except NoSuchElementException:
            
            print('go_next_page NoSuchElementException')

    # This method will return the previous page element and clicks previous page button.
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

