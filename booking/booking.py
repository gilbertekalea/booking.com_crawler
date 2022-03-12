import booking.constant as const
from booking.filtration import BookingFiltration
from booking.report import BookingReport
from booking import helpers
import os
import datetime
import csv
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.by import By

# This file is responsible for describing the methods that later we are going to call
# where it will give the bot actions to take.

# Todo
#   Automate clicking the currency - in this case clicking on USD.
#   send some text to search text element
# Click on two dates, first one represents checkin and check out.
#  Choose how number of people : adult, children, and rooms.


class Booking(webdriver.Chrome):
    def __init__(
        self,
        driver_path=r"C:\Users\gilbe\Desktop\workstation\projects\scrape\SeleniumDrivers",
        teardown=False,
    ):
        self.driver_path = driver_path
        self.teardown = teardown
        # Best to put this in the context management code with 'with'
        # self.implicitly_wait(30)
        # self.maximize_window()

        # system level >>>>> operating system path to environment variables.
        os.environ["PATH"] += self.driver_path
        options = webdriver.ChromeOptions()

        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Used to instantiate the webdriver.chrome class so that the Booking will inherit all the methods.
        super(Booking, self).__init__(options=options)

        # gives the child a full access to parent class methods.

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.teardown:
            self.quit()

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

    def vocation_month(self, month):
        voc_month = helpers.when_is_vocation(month)
        today_date = datetime.datetime.now()
        year = today_date.year
        start_date = voc_month + str(year)

        if today_date.strftime("%B") != month:
            self.calendar_month_next()
            calendar = self.find_element(
                By.CSS_SELECTOR, 'div[data-bui-ref="calendar-content"]'
            )
            m = calendar.find_elements(
                By.CSS_SELECTOR, 'div[data-bui-ref="calendar-month"]'
            )
            for i, item in enumerate(m):
                if i == 0:
                    ele = item.find_element(
                        By.CSS_SELECTOR, 'div[class="bui-calendar__month"]'
                    )
                    if ele.text == start_date:
                        print("Match found")
                    else:
                        self.calendar_month_next()
        else:
            pass

    def select_dates(self, checkin, duration: int, checkout):
        check_in = self.find_element_by_css_selector(f'td[data-date="{checkin}"]')
        check_in.click()

        # Booking.com only allows a maximum of  45 nights; approximately 1.5 months.

        stay_length = self.find_element(
            By.CSS_SELECTOR, 'div[data-bui-ref="calendar-next"]'
        )

        for _ in range(duration):
            stay_length.click()

        check_out = self.find_element_by_css_selector(f'td[data-date="{checkout}"]')
        check_out.click()

    def select_adult(self, adult, rooms):
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

    def calendar_month_next(self):
        click_next = self.find_element(
            By.CSS_SELECTOR, 'div[data-bui-ref="calendar-next"]'
        )
        click_next.click()

    def click_search(self):
        search_element = self.find_element_by_css_selector('button[type="submit"]')
        search_element.click()

    def apply_filtration(self):
        filter = BookingFiltration(driver=self)
        filter.apply_star_rating(3, 4, 5)
        filter.sort_price()

    def report_results(self):
        report = BookingReport(boxes_section_element=self)

        collection, collection_list = report.pull_deal_box_attributes()

        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Type", "Hotel Score"]
        )
        table.add_rows(collection)
        print(table)

        with open(r"data\booking.csv", "w", newline="") as csvfile:
            fieldnames = ["hotel_name", "hotel_price", "hotel_type", "hotel_score"]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for _, row in enumerate(collection_list):
                writer.writerow(row)
