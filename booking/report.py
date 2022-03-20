# This file includes methods that will parse the specific data we need from each of the deal boxes.
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from booking.pagenation import BookingPagenation

import time, math


class BookingReport:
    def __init__(self, boxes_section_element: WebDriver):
        self.boxes_section_element = boxes_section_element
        # self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return (
            self.boxes_section_element.find_element(
                By.CSS_SELECTOR, 'div[data-component="arp-properties-list"]'
            )
            .find_element(By.CSS_SELECTOR, 'div[class="_814193827"]')
            .find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        )

    def pull_deal_box_attributes(self, checkin, checkout, adult, rooms, place):
        next_page = BookingPagenation(page=self.boxes_section_element)
        count = next_page.get_property_count()
        collection = []
        collection_list = []

        # controls the next_page looping:

        for i in range(math.ceil(count / 25)):
            for deal_box in self.pull_deal_boxes():
                print("pull_boxes for", checkin, checkout, adult, rooms, place)
                collection_dict = {}
                hotel_name = (
                    deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]')
                    .get_attribute("innerHTML")
                    .strip()
                )
                location = (
                    deal_box.find_element(
                        By.CSS_SELECTOR, 'div[data-testid="location"]'
                    )
                    .find_element(By.CSS_SELECTOR, 'span[data-testid="address"]')
                    .get_attribute("innerHTML")
                    .strip()
                )
                try:
                    hotel_type = (
                        deal_box.find_element(
                            By.CSS_SELECTOR, 'div[class="_371410fad"]'
                        )
                        .find_element(By.CSS_SELECTOR, 'div[role="link"]')
                        .find_element(By.CSS_SELECTOR, 'span[class="_c5d12bf22"]')
                        .get_attribute("innerHTML")
                    )

                except NoSuchElementException:
                    hotel_type = "None"
                try:
                    hotel_price = deal_box.find_element(
                        By.CSS_SELECTOR, 'span[class="fde444d7ef _e885fdc12"]'
                    ).get_attribute("innerHTML")

                except NoSuchElementException:
                    hotel_price = str(0.0)

                try:
                    hotel_score = deal_box.find_element(
                        By.CSS_SELECTOR, 'div[class="_9c5f726ff bd528f9ea6"]'
                    ).get_attribute("innerHTML")

                except NoSuchElementException:
                    hotel_score = str(0.0)

                collection.append(
                    [place, hotel_name, location, hotel_price, hotel_type, hotel_score, checkin, checkout,adult,rooms]
                )
                collection_dict["city"] = place
                collection_dict["hotel_name"] = hotel_name
                collection_dict["location"] = location
                collection_dict["hotel_price"] = hotel_price
                collection_dict["hotel_type"] = hotel_type
                collection_dict["hotel_score"] = hotel_score
                collection_dict["checkin"] = checkin
                collection_dict["checkout"] = checkout
                collection_dict["adult"] = adult
                collection_dict["rooms"] = rooms
                collection_list.append(collection_dict)

            print("page", i)
            next_page.go_next_page()
            time.sleep(15)
        # next_page.return_first_page
        return collection, collection_list
