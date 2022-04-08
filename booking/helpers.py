# Author: Gilbert Ekaale Amoding
# Github: github.com/gilbekalea
# Email:
# Date:
# Description:

########################################################################################################################

# This file contains the logic for generating date range for current month, not current month, and other helper functions.

import datetime
import csv

from booking import constant as const

# import constant as const


def get_csv_data(file_name: str) -> list:
    """_summary_
    Get user data from csv file and return a list of dictionaries.

    Args:
        file_name (str): _description_

    Returns:
        list: _description_
            List of dictionaries contain the user data. The list is empty if the file is empty. The list is not empty if the file is not empty.

    """
    with open(file_name, "r") as f:
        # read the csv file
        reader = csv.DictReader(f)
        # store the data in a list of dictionaries
        user_data = []
        for item in reader:
            user_data.append(item)

    # return the list of dictionaries
    return user_data


def when_is_vocation(month: str) -> str:
    """_summary_
    Takes a string of month and returns the vocation month first letter capitalized.

    Args:
        month (str): _description_
        A month a after or after the current month.

    Returns:
        str : _description_
    """
    months_lower = month.lower()
    return months_lower.capitalize()


def find_number_in_string(string: str) -> str:

    """_summary_
    A helper function to find the number in a string. No formatting is applied.
    for example: "1gilbert2hajajsjs3" will return 123.

    Args:
        string (str): _description_

    Returns:
        str: _description_
    """
    store = []
    # find all numbers in the string
    for i, item in enumerate(string):
        # if the item is a number
        try:
            if type(int(item)) == int:
                store.append(item)

        except ValueError:
            continue

    # propery counts
    prop_count = ""
    for i in store:
        prop_count = prop_count + i

    # checks if prop count is empty string. Avoid returning empty string.
    # if prop_count == "":
    #     prop_count = prop_count + "1"

    return prop_count


# Generate if the start_year is not current year and start_month is not current month.
def generate_date_range(
    start_year: int, start_month: int, duration: int, place: str, adult: int, rooms: int
) -> list:
    """_summary_
    generate if the start_year is not current year and start_month is not current month.


    Args:
        start_year (int): Year to start date range.
        start_month (int): Month to start date range
        duration (int): The duration of the stay from start_month, the maximum is 22. If the duration is greater than 22, the function will set duration to 22.
                        The duration is the number of months to stay and is used to generate the date range of one-month-long stay.
        place (str): The place to stay. The destination you would like to visit.
        adult (int): the number of adults
        rooms (int): the number of rooms

    Returns:
        list: _description_
            a list of dicts, each dict contains the date range of one-month-long stay with desireable parameters such as checkin, checkout, month, place, adult, rooms.
            data obtained from csv file using get_csv_data() function.

    """

    today_dates = datetime.datetime.now()
    current_month = today_dates.strftime("%m")

    # if the start_month is the past month, the start_Month is set to the current month.
    # Note: This is only applicable if you are using the date for booking.com website, otherwise, you can ignore this.
    # Calculate the difference between the current month and start_month to determine how much additional months to add to start_month.
    if start_month < int(current_month) or start_month == int(current_month):
        start_month = start_month + abs(int(current_month) - start_month) + 1
        print("start_month: ", start_month)
    # duration is greater than 22, set duration to 22.
    if duration > 22:
        duration = 22
    date_range_wrapper = []
    for i in range(duration):
        date_range_dict = {}
        # date formating -> for From january to september. Add a prefix zero.

        if int(start_month) + i <= 9:
            # formating month after september; do not add prefix zero.
            if int(start_month) + i + 1 <= 9:
                date_range = f"{start_year}-0{str(int(start_month+i))}-01"
                date_range_dict["checkin"] = date_range
                date_range_dict[
                    "checkout"
                ] = f"{start_year}-0{str(int(start_month) + i +1)}-01"

                month_num = str(int(start_month) + i)

                datetime_object = datetime.datetime.strptime(month_num, "%m")
                full_month_name = datetime_object.strftime("%B")
                date_range_dict["month"] = full_month_name
                date_range_dict["place"] = place
                date_range_dict["adult"] = adult
                date_range_dict["rooms"] = rooms

            else:
                date_range = f"{start_year}-0{str(int(start_month) + i)}-01"
                date_range_dict["checkin"] = date_range
                date_range_dict[
                    "checkout"
                ] = f"{start_year}-{str(int(start_month)+i+1)}-01"

                month_num = str(int(start_month) + i)

                datetime_object = datetime.datetime.strptime(month_num, "%m")

                full_month_name = datetime_object.strftime("%B")

                date_range_dict["month"] = full_month_name
                date_range_dict["place"] = place
                date_range_dict["adult"] = adult
                date_range_dict["rooms"] = rooms

        # Date formatting from october to december.
        elif int(start_month) + i > 9:

            if (int(start_month) + i + 1) > 12:
                # avoid 00 2023-00-01 date like
                if int(start_month) + i - 12 == 0:
                    date_range = f"{start_year}-{str(int(start_month)+i)}-01"
                    date_range_dict["checkin"] = date_range
                    date_range_dict[
                        "checkout"
                    ] = f"{start_year+1}-0{str((int(start_month)+i+1)-12)}-01"

                    month_num = str(int(start_month) + i)
                    datetime_object = datetime.datetime.strptime(month_num, "%m")
                    full_month_name = datetime_object.strftime("%B")
                    date_range_dict["month"] = full_month_name
                    date_range_dict["place"] = place
                    date_range_dict["adult"] = adult
                    date_range_dict["rooms"] = rooms

                elif int(start_month) + i - 12 <= 9:

                    date_range = f"{start_year+1}-0{str((start_month + i) - 12)}-01"
                    date_range_dict["checkin"] = date_range

                    if (int(start_month) + i + 1) - 12 > 9:
                        date_range_dict[
                            "checkout"
                        ] = f"{start_year+1}-{str((int(start_month)+i+1)-12)}-01"
                    else:
                        date_range_dict[
                            "checkout"
                        ] = f"{start_year+1}-0{str((int(start_month)+i+1)-12)}-01"
                    # getting string format of the month.
                    month_num = str(int(start_month) + i - 12)

                    # creating datetime object
                    datetime_object = datetime.datetime.strptime(month_num, "%m")

                    full_month_name = datetime_object.strftime("%B")
                    date_range_dict["month"] = full_month_name
                    date_range_dict["place"] = place
                    date_range_dict["adult"] = adult
                    date_range_dict["rooms"] = rooms

                else:
                    # if the condition above doesn't certify, do the normal date generation.
                    if (int(start_month) + i + 1) - 12 > 12:
                        if int(start_month) + i + 1 - 24 <= 9:
                            date_range = (
                                f"{start_year+2}-0{str(int(start_month)+i+1-24)}-01"
                            )
                            date_range_dict["checkin"] = date_range

                            date_range_dict[
                                "checkout"
                            ] = f"{start_year+2}-0{str(int(start_month)+i+2-24)}-01"

                    else:
                        date_range = f"{start_year+1}-{str(int(start_month)+i-12)}-01"
                        date_range_dict["checkin"] = date_range
                        date_range_dict[
                            "checkout"
                        ] = f"{start_year+1}-{str((int(start_month)+i+1)-12)}-01"

                    # getting string format of the month.
                    month_num = str(int(today_dates.strftime("%m")) + i - 12)

                    # creating datetime object
                    datetime_object = datetime.datetime.strptime(month_num, "%m")

                    full_month_name = datetime_object.strftime("%B")
                    date_range_dict["month"] = full_month_name
                    date_range_dict["place"] = place
                    date_range_dict["adult"] = adult
                    date_range_dict["rooms"] = rooms

            # if (int(start_month) + i + 1) > 12 fails, do the normal date generation.
            else:
                date_range = f"{start_year}-{str((int(start_month)+i))}-01"
                date_range_dict["checkin"] = date_range
                date_range_dict[
                    "checkout"
                ] = f"{start_year}-{str(int(start_month)+i+1)}-01"

                month_num = str(int(start_month) + i)

                datetime_object = datetime.datetime.strptime(month_num, "%m")

                full_month_name = datetime_object.strftime("%B")
                date_range_dict["month"] = full_month_name
                date_range_dict["place"] = place
                date_range_dict["adult"] = adult
                date_range_dict["rooms"] = rooms
        else:
            pass
        date_range_wrapper.append(date_range_dict)

    return date_range_wrapper


def construct_date_range(
    start_year: int, start_month: int, duration: int, place: str, adult: int, rooms: int
) -> dict:
    """_summary_
    date format: YYYY-MM-DD
    Generate a date range of 30 days if the start month is current calendar month or
    31 days depending with the calendar:

    Args:
        start_year (int): Year to start date range.
        start_month (int): Month to start date range
        duration (int): The period you would like to generate date expressed in months.

    Returns:
        dict: Returns a list of dictinaries containing date range.
    """

    # use numerical representation of months to compare which month is greater or less than current month.
    # The logic is that we assume if a month has high numerical representation compared to current month, it signifies future date.
    # For example: March > February: 3 > 2 or March < April, May, june... 3 < 4,5,6.... respectively.
    return generate_date_range(start_year, start_month, duration, place, adult, rooms)


if __name__ == "__main__":
    print(find_number_in_string("gilber777tekale2678282"))
    obj = construct_date_range(
        start_year=2022, start_month=4, duration=12, place="Montreal", adult=2, rooms=2
    )
    print(get_csv_data("../user_param/city_param.csv"))
    for item in obj:
        print(item["checkin"], item["checkout"], item["month"])
