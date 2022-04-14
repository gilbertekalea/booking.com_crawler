# This file contain methods that allow the webdriver to click see avaialability buttofrom selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from booking.browser_control import BrowserWindowControl
import time
class PropertyDetail:

    """
    A class containing methods that will allow the webdriver to click availability button.
    and perform actions on the new window to go new window.
    collect necessary information from the new window, close it and return to the main window.

    """

    def __init__(self, detail_page: WebDriver):
        self.detail_page = detail_page

    def get_availability_button(self, deal_box):
       
        """
        This method will click the see availability button.
        The web element is located in the deal_box param.
        """
        browser = BrowserWindowControl(browser=self.detail_page)
        time.sleep(3)
        availability_button = deal_box.find_element(
            By.CSS_SELECTOR, 'div[data-testid="availability-cta"]'
        )

        availability_button.click()
        
        browser.switch_window()

        property_url = self.detail_page.current_url
        property_address = self.get_property_address()
        # print("property address is: ", property_address)
        img = self.get_property_gallery()

        description = self.get_property_description()

        browser.close_window()

        # except NoSuchElementException or ElementNotInteractableException or NoSuchAttributeException:
        #     # prevent browser from crashing and keep it going
        #     img = []
        #     description= ''
        #     print('Sorry the availability button was not found')
        #     self.close_window()

        return img, description, property_url, property_address

    def get_property_address(self):

        """
        This method will return the property address.
        """
        
        property_address = (
            self.detail_page.find_element(By.ID, "showMap2")
            .find_element(By.CSS_SELECTOR, 'span[data-source="top_link"]')
            .text
        )

        return property_address

    def get_property_gallery(self) -> list:
        """
        Method to get the property gallery images.
        returns a list of images.
        """

        try:
            try:
                gallery_container = self.detail_page.find_element(
                    By.ID, "blockdisplay1"
                )
                hotel_main_content = gallery_container.find_element(
                    By.ID, "hotel_main_content"
                )
                all_img = hotel_main_content.find_element(
                    By.CSS_SELECTOR, 'div[data-component="gallery-side-reviews"]'
                )

            except NoSuchElementException:
                gallery_container = self.detail_page.find_element(
                    By.ID, "blockdisplay1"
                )
                hotel_main_content = gallery_container.find_element(
                    By.ID, "hotel_main_content"
                )
                all_img = hotel_main_content.find_element(
                    By.CSS_SELECTOR,
                    'div[class="clearfix bh-photo-grid fix-score-hover-opacity"]',
                )

            property_images_container = all_img.find_elements(
                By.CSS_SELECTOR, 'div[aria-hidden="true"]'
            )

            img_collection = []
            for item in property_images_container:
                a = item.find_element(By.XPATH, '//a[contains(@href, "#")]')
                img = a.find_element(By.XPATH, '//a[contains(@href, "#")]/img')
                # print(img.get_attribute('src'))
                img_collection.append(img.get_attribute("src"))

            return img_collection

        except NoSuchAttributeException:

            print("gallery element was not found")
            img_collection = []

            return img_collection

    def get_property_description(self) -> str:
        """
        Method to get the property description in details.
        returns a string.
        """

        try:

            print("working on description")
            description = ""
            summary = self.detail_page.find_element(By.ID, "summary")
            paragrams = summary.find_elements(By.TAG_NAME, "p")
            for item in paragrams:
                description += item.text
            print(description)
            return description

        except NoSuchElementException or NoSuchAttributeException or ElementNotInteractableException:
            description = ""
            show_more = self.detail_page.find_element(
                By.XPATH,
                '//div[@class="hp-description__show_more hp-description__show_more--visible"]/a',
            )

            print("show more: ", show_more.text)
            if show_more.text == "Show me more":
                print("click show more")
                show_more.click()

            print("working on description")
            description = ""
            summary = self.detail_page.find_element(By.ID, "summary")
            paragrams = summary.find_elements(By.TAG_NAME, "p")
            for item in paragrams:
                description += item.text
            print(description)
            print("description element was not found")
            return description
