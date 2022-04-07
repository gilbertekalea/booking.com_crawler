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
        print('count is: ', count)
        if count == 0:
            count = 1 # This is a hack to prevent an error.

        collection = []
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
        print('property count', count)
        for i in range(math.ceil(count / 25)):

            # This loop will iterate through each deal box and pull the data we need.
            for deal_box in self.pull_deal_boxes():
                print("pull_boxes for", checkin, checkout, adult, rooms, place)
                # This dictionary will contain the data we need from each deal box.
                infor = detail.get_availability_button(deal_box)
                print('image is: ', infor[0])
                print('description is: ', infor[1])
                collection_dict = {}

                # This will contain the name of the hotel.
                try:
                    hotel_name = (
                        deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]')
                        .get_attribute("innerHTML")
                        .strip()
                    )
                except StaleElementReferenceException:
                    hotel_name = deal_box.find_element(
                        By.XPATH, '//a[contains(@data-testid, "title-link")]/div').find_element(
                            By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute(
                                "innerHTML").strip()
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
                    hotel_type = (
                        deal_box.find_element(
                            By.CSS_SELECTOR, 'div[class="_371410fad"]'
                        )
                        .find_element(By.CSS_SELECTOR, 'div[role="link"]')
                        .find_element(By.CSS_SELECTOR, 'span[class="_c5d12bf22"]')
                        .get_attribute("innerHTML")
                    )

                # This will handle the case where the type of the hotel is not available.
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
                    [
                        place,
                        hotel_name,
                        location,
                        hotel_price,
                        hotel_type,
                        hotel_score,
                        checkin,
                        checkout,
                        adult,
                        rooms,
                    ]
                )
                # This will add the data to the collection_dict.
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

                # This will check if the next page button is available.
                # detail.get_availability_button(deal_box)

            print("page", i)
            #
            next_page.go_next_page()
            time.sleep(15)

        return collection, collection_list

    def get_availability_button(self, deal_box):

        try:
            availability_button = deal_box.find_element(
                By.CSS_SELECTOR, 'div[data-testid="availability-cta"]'
            )
            availability_button.click()

        except NoSuchElementException:

            availability_button = None
            print('availability element was not found')