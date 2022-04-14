from gettext import find
from importlib.machinery import BYTECODE_SUFFIXES
from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from booking.pagenation import BookingPagenation
from booking.property_detail import PropertyDetail

import time, math

# This file contains methods that will parse the specific data we need from each of the deal boxes.
class BookingReport:
    def __init__(self, report_driver: WebDriver):
        self.report_driver = report_driver

    # This method will return a list of WebElements that are the deal boxes.
    def pull_deal_boxes(self):
        return (
            self.report_driver.find_element(
                By.CSS_SELECTOR, 'div[data-component="arp-properties-list"]'
            )
            .find_element(By.CSS_SELECTOR, 'div[class="d4924c9e74"]')
            .find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        )

    # This method will return a list of dictionaries that contain the data we need from each deal box.
    def pull_deal_box_attributes(self, checkin, checkout, adult, rooms, place):
        next_page = BookingPagenation(next_pager=self.report_driver)
        detail = PropertyDetail(detail_page=self.report_driver)
        count = next_page.get_property_count()
        print("count is: ", count)
        if count == 0:
            count = 1  # This is a hack to prevent an error.

      
        collection_list = []

        # This was testing loop. It was used to test the pagenation.
        # for i in range(12):
        #     print('page', i)
        #     next_page.go_next_page()
        #     if i == 3:
        #         break

        # This loop will iterate through each deal box for given duration based on the number of properties on the page.
        # The loop will continue until the next page method returns False.

        # The third event loop is for parsing the data from each deal box and following the next page link.
        # The range is determined by calculating the number of properties found divide by number of properties per page.
        print("property count", count)
        for i in range(math.ceil(count / 25)):

            # This loop will iterate through each deal box and pull the data we need.
            for deal_box in self.pull_deal_boxes():
                print("pull_boxes for", checkin, checkout, adult, rooms, place)

                # This dictionary will contain the data we need from each deal box.
                
                img, description, property_url, property_address = detail.get_availability_button(deal_box)
            
                collection_dict = {}

                # This will contain the name of the hotel.
                try:
                    property_name = (
                        deal_box.find_element(
                            By.CSS_SELECTOR, 'div[data-testid="title"]'
                        )
                        .get_attribute("innerHTML")
                        .strip()
                    )
                except StaleElementReferenceException:
                    property_name = (
                        deal_box.find_element(
                            By.XPATH, '//a[contains(@data-testid, "title-link")]/div'
                        )
                        .find_element(By.CSS_SELECTOR, 'div[data-testid="title"]')
                        .get_attribute("innerHTML")
                        .strip()
                    )
                # This will contain the location of the hotel.
                location = (
                    deal_box.find_element(
                        By.CSS_SELECTOR, 'div[data-testid="location"]'
                    )
                    .find_element(By.CSS_SELECTOR, 'span[data-testid="address"]')
                    .get_attribute("innerHTML")
                    .strip()
                )

                try:
                    # This will contain the type of the hotel.
                    property_type = (
                        deal_box.find_element(
                            By.CSS_SELECTOR, 'div[class="_371410fad"]'
                        )
                        .find_element(By.CSS_SELECTOR, 'div[role="link"]')
                        .find_element(By.CSS_SELECTOR, 'span[class="_c5d12bf22"]')
                        .get_attribute("innerHTML")
                    )

                # This will handle the case where the type of the hotel is not available.
                except NoSuchElementException:
                    property_type = "None"

                try:
                    property_price = (
                        deal_box.find_element(
                            By.CSS_SELECTOR,
                            'div[data-testid="price-and-discounted-price"]',
                        )
                        .find_element(By.TAG_NAME, "span")
                        .get_attribute("innerHTML")
                    )
                    print("price is: ", property_price)

                except NoSuchElementException:
                    print("no price")
                    property_price = str(0.0)

                try:
                    property_score = (
                        deal_box.find_element(
                            By.CSS_SELECTOR, 'div[data-testid="review-score"]'
                        )
                        .find_element(
                            By.XPATH,
                            '//a[contains(@data-testid, "review-score-link")]/span',
                        )
                        .find_element(
                            By.CSS_SELECTOR, 'div[data-testid="review-score"]'
                        )
                        .find_element(
                            By.CSS_SELECTOR, 'div[class="b5cd09854e d10a6220b4"]'
                        )
                        .get_attribute("innerHTML")
                    )

                    print("score is: ", property_score)
                except NoSuchElementException:
                    print("no score")
                    property_score = str(0.0)

            
                # This will add the data to the collection_dict.
                collection_dict["city_name"] = place
                collection_dict["property_name"] = property_name
                collection_dict["property_description"] = description
                collection_dict["property_image"] = img
                collection_dict["property_url"] = property_url
                collection_dict["property_address"] = property_address
                collection_dict["location"] = location
                collection_dict["property_price"] = property_price
                collection_dict["property_type"] = property_type
                collection_dict["property_score"] = property_score
                collection_dict["checkin_date"] = checkin
                collection_dict["checkout_date"] = checkout
                collection_dict["number_of_adults"] = adult
                collection_dict["number_of_rooms"] = rooms
                collection_list.append(collection_dict)

            print("page", i)
            #
            next_page.go_next_page()
            time.sleep(15)

        return collection_list
