# Author: Gilbert Ekaale Amoding
# Github: github.com/gilbekalea
# Email:

from booking import constant as const
from booking.filters import BookingFiltration
from booking.report import BookingReport
from booking import helpers
import os
import datetime
import csv
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *


# This file is responsible for describing the methods that later we are going to call 
# where it will give the bot actions to take.


class Booking(webdriver.Chrome):
    
    # private variables are not accessible outside the class.
    _date_checkin = ""
    _date_checkout= ""
    _adults= 0
    _rooms= 0
    _place= ""

    def __init__(
        self,
        driver_path=r"C:\Users\gilbe\Desktop\workstation\projects\scrape\SeleniumDrivers",
        teardown=True,
    ):
        self.driver_path = driver_path
        self.teardown = teardown

        # Best to put this in the context management code with 'with'
        # self.implicitly_wait(30)
        # self.maximize_window()

        # system level >>>>> operating system path to environment variables.
        os.environ["PATH"] += self.driver_path
        options = webdriver.ChromeOptions()

        # ip_address = '199.195.254.168:8118'
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # options.add_argument(f'proxy-server={ip_address}')
        # Used to instantiate the webdriver.chrome class so that the Booking will inherit all the methods.
        super(Booking, self).__init__(options=options)

        # gives the child a full access to parent class methods.

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.teardown:
            self.quit()

    def set_proxy(self):

        ip_address = "199.195.254.168:8118"

        self.desired_capabilities["proxy"] = {
            "httpProxy": ip_address,
            "ftpProxy": ip_address,
            "sslProxy": ip_address,
            "proxyType": "MANUAL",
        }

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.find_element_by_css_selector(
            'button[data-tooltip-text="Choose your currency"]'
        )
        currency_element.click()

        selected_currency_element = self.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element_by_id("ss")
        search_field.clear()
        search_field.send_keys(place_to_go)
        first_result = self.find_element_by_css_selector('li[data-i="0"]')
        first_result.click()
        Booking.place = place_to_go

    def click_date_box(self):

        """
        clicks the previous month button after the first iteration.
        """

        elem = self.find_element(By.CSS_SELECTOR, 'div[class="xp__dates-inner"]')
        elem.click()
        prev_month_status = True
        while prev_month_status:
            try:
                self.calendar_prev_month_button()

            except ElementNotInteractableException or ElementNotSelectableException or NoSuchElementException:
                prev_month_status = False

        print("click date !!!")

    def vocation_month(self, month: str):
        """_summary_

        :param month: the month you want to go to vacation.
        """
        voc_month = helpers.when_is_vocation(month)
        today_date = datetime.datetime.now()
        year = today_date.year
        start_date = voc_month + " " + str(year)

        # if not current month;
        if today_date.strftime("%B") != month.capitalize():
            status = True
            while status:
                calendar = self.find_element(
                    By.CSS_SELECTOR, 'div[data-bui-ref="calendar-content"]'
                )
                # returns a list
                m = calendar.find_elements(
                    By.CSS_SELECTOR, 'div[data-bui-ref="calendar-month"]'
                )
                ele = m[0].find_element(
                    By.CSS_SELECTOR, 'div[class="bui-calendar__month"]'
                )

                if ele.get_attribute("innerHTML") == start_date:
                    print("this element was found")
                    print("the date", start_date, "was found")
                    status = False
                    break
                else:
                    try:
                        self.calendar_next_month_button()

                    except NoSuchElementException or ElementNotInteractableException:
                        pass
        else:
            pass

    def calendar_next_month_button(self):
        """
        clicks next month icon
        """
        try:
            next_month = self.find_element(
                By.CSS_SELECTOR, 'div[data-bui-ref="calendar-next"]'
            )
            next_month.click()

        except ElementNotInteractableException or NoSuchElementException:
            pass

    def calendar_prev_month_button(self):
        """
        clicks previous month icon
        can be used to go back to previous month,
        """
        prev_month = self.find_element(
            By.CSS_SELECTOR, 'div[data-bui-ref="calendar-prev"]'
        )
        prev_month.click()

    def select_dates(self, checkin: str, checkout: str):
        """_summary_
        Booking.com only allows a maximum of 45 nights; approximately 1.5 months.
        For easy scraping we recommend you keep the date range between one month that is 2022-05-01 - 2022-06-01
        e.i a maximum of 30 days. By default, if the start_month is current_month, the checkin date will start from current_date i.e current month and day.
        This is because, booking.com doesn't allow checkin of past dates.
        Otherwise, if you are planning checkin one month from now, then the checkin start date will always be the first day of
        desired month and checkout will be first day of next month.
        check helpers.py file on `construct_date()` also check `constants.py`

        Args:
            checkin (str): Booking.com checkin date.

            checkout (str): Booking.com checkout date.

        """

        check_in = self.find_element_by_css_selector(f'td[data-date="{checkin}"]')
        check_in.click()

        check_out = self.find_element_by_css_selector(f'td[data-date="{checkout}"]')
        check_out.click()

        Booking.date_checkin = checkin
        Booking.date_checkout = checkout

    # 
    def select_adult(self, adult: int, rooms: int):
        # 
        """
        Selects the number of adults per room.
        Args:
        Adult (int): Number of adults per room.

        """
        selection_element = self.find_element_by_id("xp__guests__toggle")
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element_by_css_selector(
                'button[aria-label="Decrease number of Adults"]'
            )
            decrease_adults_element.click()

            # if the value of adults reaches 1, then we should get out of the loop
            adults_value_element = self.find_element_by_id("group_adults")
            adults_value = adults_value_element.get_attribute("value")

            if int(adults_value) == 1:
                break

        add_adult = self.find_element_by_css_selector(
            'button[aria-label="Increase number of Adults"]'
        )

        for _ in range(adult - 1):
            add_adult.click()

        add_rooms = self.find_element_by_css_selector(
            'button[aria-label="Increase number of Rooms"]'
        )
        for _ in range(rooms - 1):
            add_rooms.click()

        Booking.adults = adult
        Booking.rooms = rooms

    def click_search(self):
        search_element = self.find_element_by_css_selector('button[type="submit"]')
        search_element.click()

    def apply_filtration(self):
        filter = BookingFiltration(driver=self)
        filter.apply_star_rating(3, 4, 5)
        filter.sort_price()

    def report_results(self):
        """ _summary_
        This method will report the results of the search found on the page.
        """
        report = BookingReport(web_driver=self)
        collection, collection_list = report.pull_deal_box_attributes(
            checkin=Booking.date_checkin,
            checkout=Booking.date_checkout,
            adult=Booking.adults,
            rooms=Booking.rooms,
            place=Booking.place,
        )

        # save the collection to a file
        print('saving to csv file')
        Booking.save_results_to_csv(collection_list)
        table = PrettyTable(
            field_names=[
                "City",
                "Hotel Name",
                "location",
                "Hotel Price",
                "Hotel Type",
                "Hotel Score",
                "checkin",
                "checkout",
                "adult",
                "rooms",
            ]
        )
        table.add_rows(collection)
        # print(table)
        # with open(
        #     f"scraped_data\{Booking.place}-booking.csv",
        #     "a",
        #     newline="",
        #     encoding="utf-8",
        # ) as csvfile:
        #     fieldnames = [
        #         "city",
        #         "hotel_name",
        #         "location",
        #         "hotel_price",
        #         "hotel_type",
        #         "hotel_score",
        #         "checkin",
        #         "checkout",
        #         "adult",
        #         "rooms",
        #     ]

        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     # writer.writeheader()
        #     for _, row in enumerate(collection_list):
        #         writer.writerow(row)
        return collection_list

    @staticmethod
    def save_results_to_csv(collection_list):
        print('I just got called')
        with open(
            f"scraped_data\{Booking.place}-booking.csv",
            "a",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            # fieldnames = [
            #     "city",
            #     "hotel_name",
            #     "location",
            #     "hotel_price",
            #     "hotel_type",
            #     "hotel_score",
            #     "checkin",
            #     "checkout",
            #     "adult",
            #     "rooms",
            # ]

            writer = csv.DictWriter(csvfile, fieldnames=collection_list[0].keys())
    
            for _, row in enumerate(collection_list):
                writer.writerow(row)
if __name__ == '__main__':
    pass
