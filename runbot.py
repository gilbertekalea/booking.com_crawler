# Author: Gilbert Ekaale Amoding
# Github: github.com/gilbekalea
# Email: gilbertekalea@gmail.com

########################################################################### `runbot.py` ###########################################################################
# File to run the bot on.

from booking.booking import Booking
import time

from booking import helpers

try:
    with Booking() as bot:

        # loop through each params given by user in csv file then call the get_user_data_from_csv function
        # a wrapper loop will be used to call the get_user_data_from_csv function
        for _, data in enumerate(
            helpers.get_csv_data("./client_input/destination_param.csv")
        ):

            GIVEN_DATE = helpers.construct_date_range(
                start_year=int(data["start_year"]),
                start_month=int(data["start_month"]),
                duration=int(data["duration"]),
                place=data["place"],
                adult=int(data["adult"]),
                rooms=int(data["rooms"]),
            )

            # The date are generated automatically by the function .
            for i, date in enumerate(GIVEN_DATE):
                # bot.set_proxy()
                # print(bot.desired_capabilities['proxy'])
                bot.maximize_window()
                bot.implicitly_wait(30)
                bot.land_first_page()
                bot.change_currency(currency="USD")
                bot.select_place_to_go(place_to_go=date["place"])

                if (_ != 0) or (i != 0):
                    bot.click_date_box()

                bot.vocation_month(month=date["month"])
                bot.select_dates(checkin=date["checkin"], checkout=date["checkout"])
                bot.select_adult(adult=date["adult"], rooms=date["rooms"])
                bot.click_search()
                bot.apply_filtration()
                bot.refresh()
                bot.report_results()

                time.sleep(15)


except Exception as e:

    if "in PATH" in str(e):
        print("There is a problem runing this program from a command line")
    else:
        raise SyntaxError
