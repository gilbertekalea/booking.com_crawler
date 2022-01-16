# This file includes methods that will parse the specific data we need from each of the deal boxes.
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver


class BookingReport:
    def __init__(self, boxes_section_element: WebDriver):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_element_by_class_name(
            "_814193827"
        ).find_elements_by_css_selector('div[data-testid="property-card"]')

    def pull_deal_box_attributes(self):
        collection = []
        collection_list = []
        for deal_box in self.deal_boxes:
            collection_dict = {}

            hotel_name = (
                deal_box.find_element_by_css_selector('div[data-testid="title"]')
                .get_attribute("innerHTML")
                .strip()
            )

            hotel_price = deal_box.find_element_by_css_selector(
                'span[class="fde444d7ef _e885fdc12"]'
            ).get_attribute("innerHTML")

            try:
                hotel_score = deal_box.find_element_by_css_selector(
                    'div[class="_9c5f726ff bd528f9ea6"]'
                ).get_attribute("innerHTML")

            except NoSuchElementException:

                hotel_score = str(0.0)

            collection.append([hotel_name, hotel_price, hotel_score])
            collection_dict["hotel_name"] = hotel_name
            collection_dict["hotel_price"] = hotel_price
            collection_dict["hotel_score"] = hotel_score
            collection_list.append(collection_dict)

        return collection, collection_list 
