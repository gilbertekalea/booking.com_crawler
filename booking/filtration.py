from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver

# This file will include a class with instance methods, that will be reposible to interact
# with the website after we have some results, to apply filtrations

class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element_by_css_selector(
            'div[data-filters-group="class"]'
        )
        # Narrow down to children element for star_filtration_box.
        star_child_element = star_filtration_box.find_elements_by_css_selector("*")

        for star_value in star_values:
            for star_element in star_child_element:
                # element = str(star_element.get_attribute('innerHTML')).strip()
                # print(element)
                if (
                    str(star_element.get_attribute("innerHTML")).strip()
                    == f"{star_value} stars"
                ):
                    star_element.click()
                else:
                    continue

    def sort_price(self):
        sort_by_lowest_price = self.driver.find_element_by_css_selector(
            'li[data-id="price"]'
        )
        sort_by_lowest_price.click()

        # show_rooms_more = self.driver.find_element_by_css_selector(
        #     'section[class="_fe1927d9e _0811a1b54 _a8a1be610 _022ee35ec b9c27d6646 fb3c4512b4 f886bb3597"]'
        # )
        
        # try:
        #     if "or more." in show_rooms_more.get_attribute(
        #         "innerHTML"
        #     ):
        #         show_rooms_more.click()
        # except NoSuchElementException:
            
        #     print("Sorry We could find the element, we are continued.....")
