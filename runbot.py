from booking.booking import Booking
import time
from booking import constant as const
from booking import helpers
try:
    with Booking() as bot:
        # The rate are generated automatically
        GIVEN_DATE = helpers.construct_date(const.START_YEAR, const.START_MONTH, const.DURATION)

        for i, date in enumerate(GIVEN_DATE):
            bot.maximize_window()
            bot.implicitly_wait(30)
            bot.land_first_page()
            bot.change_currency(currency="USD")
            bot.select_place_to_go(
                place_to_go=date["place"]
            )
            if i != 0:
                bot.click_date_box()

            bot.vocation_month(
                month=date["month"]
    
            )

            bot.select_dates(
                checkin=date["checkin"],
                checkout=date["checkout"]
            )
            bot.select_adult(
                adult=date["adult"],
                rooms=date["rooms"]
            )
            bot.click_search()
            bot.apply_filtration()
            bot.refresh()
            # work around to let the bot grab data properly
            bot.report_results()

except Exception as e:
    if "in PATH" in str(e):
        print("There is a problem runing this program from a command line")
    else:
        raise SyntaxError
