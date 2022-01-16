from booking.booking import Booking

# Context Management: close the browser.
try:
    with Booking() as bot:
        bot.maximize_window()
        bot.implicitly_wait(30)
        bot.land_first_page()
        bot.change_currency(currency="USD")
        bot.select_place_to_go(place_to_go=input("Where do you want to go? : "))
        bot.select_dates(
            checkin=input("check in date YYYY-MM-DD? :"),
            checkout=input("check out dates YYYY-DD-MM? :"),
        )
        bot.select_adult(adult=int(input("How many adults? :")), rooms=6)
        bot.click_search()
        bot.apply_filtration()
        bot.refresh()
        # work around to let the bot grab data properly
        # Gives the bot a second to breath and grans the data the way we want it.

        bot.report_results()

except Exception as e:
    if "in PATH" in str(e):
        print("There is a problem runing this program from a command line")
    else:
        raise SyntaxError
