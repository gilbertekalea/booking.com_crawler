import datetime
from booking import constant as const

def when_is_vocation(month) -> datetime:
    """_summary_
        return month in capitalized format.

    Args:
        month (_type_): _description_

    Returns:
        datetime: _description_
    """
    months_lower = month.lower()
    return months_lower.capitalize()

def find_number_in_string(string) -> str:
    
    """_summary_
        Given a string, find ans return a int type occurrance.
        if no string found return a string 1.
    Args:
        string (_type_): _description_

    Returns:
        str: _description_
    """
    store = []
    for i, item in enumerate(string):
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
    if prop_count == "":
        prop_count = prop_count + "1"

    return prop_count


# print(find_number_in_string("gilber777tekale2678282"))

# Helper function
# This function works only if the start_month and start_year is the current calendar year/month: for example today is 2022-03-17
# and is being called from `constuct_date function.`


def generate_date_range_current_month(
    start_year: int, start_month: int, duration: int, place: str, adult: int, rooms: int
) -> dict:
    """_summary_
        generate date range starting today i.e current month,date and year.
        The date range will always be generated starting with the current day and month.
    Args:
        start_year (int): _description_
        start_month (int): _description_
        duration (int): _description_
        place (str): _description_
        adult (int): _description_
        rooms (int): _description_

    Returns:
        dict: _description_
    """
    today_dates = datetime.datetime.now()
    date_range_list = []

    for i in range(abs(start_month - duration) + 1):
        date_range_dict = {}
        # date formating -> for From january to september. Add a prefix zero.
        if int(today_dates.strftime("%m")) + i <= 9:
            # formating month after september; do not add prefix zero.
            if (int(today_dates.strftime("%m")) + i + 1) <= 9:
                date_range = f'{start_year}-0{str(int(today_dates.strftime("%m"))+i)}-{today_dates.strftime("%d")}'
                date_range_dict["checkin"] = date_range
                date_range_dict[
                    "checkout"
                ] = f'{start_year}-0{str(int(today_dates.strftime("%m"))+i+1)}-{today_dates.strftime("%d")}'

                month_num = str(int(today_dates.strftime("%m")) + i)

                datetime_object = datetime.datetime.strptime(month_num, "%m")

                full_month_name = datetime_object.strftime("%B")
                date_range_dict["month"] = full_month_name
                date_range_dict['place'] = place
                date_range_dict['adult']= adult
                date_range_dict['rooms']=rooms
            else:
                date_range = f'{start_year}-0{str(int(today_dates.strftime("%m"))+i)}-{today_dates.strftime("%d")}'
                date_range_dict["checkin"] = date_range
                date_range_dict[
                    "checkout"
                ] = f'{start_year}-{str(int(today_dates.strftime("%m"))+i+1)}-{today_dates.strftime("%d")}'

                month_num = str(int(today_dates.strftime("%m")) + i)

                datetime_object = datetime.datetime.strptime(month_num, "%m")

                full_month_name = datetime_object.strftime("%B")

                date_range_dict["month"] = full_month_name
                date_range_dict['place'] = place
                date_range_dict['adult']= adult
                date_range_dict['rooms']=rooms

        # Date formatting from october to december.
        elif int(today_dates.strftime("%m")) + i > 9:
            if (int(today_dates.strftime("%m")) + i + 1) > 12:
                # avoid 00 2023-00-01 date like
                if int(today_dates.strftime("%m")) + i - 12 == 0:
                    date_range = f'{start_year}-{str(int(today_dates.strftime("%m"))+i)}-{today_dates.strftime("%d")}'
                    date_range_dict["checkin"] = date_range
                    date_range_dict[
                        "checkout"
                    ] = f'{start_year+1}-0{str((int(today_dates.strftime("%m"))+i+1)-12)}-{today_dates.strftime("%d")}'
                    month_num = str(int(today_dates.strftime("%m")) + i)
                    datetime_object = datetime.datetime.strptime(month_num, "%m")
                    full_month_name = datetime_object.strftime("%B")
                    date_range_dict["month"] = full_month_name
                    date_range_dict['place'] = place
                    date_range_dict['adult']= adult
                    date_range_dict['rooms']=rooms
                else:
                    date_range = f'{start_year+1}-0{str(int(today_dates.strftime("%m"))+i-12)}-{today_dates.strftime("%d")}'
                    date_range_dict["checkin"] = date_range
                    date_range_dict[
                        "checkout"
                    ] = f'{start_year+1}-0{str((int(today_dates.strftime("%m"))+i+1)-12)}-{today_dates.strftime("%d")}'

                    # getting string format of the month.
                    month_num = str(int(today_dates.strftime("%m")) + i - 12)

                    # creating datetime object
                    datetime_object = datetime.datetime.strptime(month_num, "%m")

                    full_month_name = datetime_object.strftime("%B")
                    date_range_dict["month"] = full_month_name
                    date_range_dict['place'] = place
                    date_range_dict['adult']= adult
                    date_range_dict['rooms']=rooms
            else:
                date_range = f'{start_year}-{str((int(today_dates.strftime("%m"))+i))}-{today_dates.strftime("%d")}'
                date_range_dict["checkin"] = date_range
                date_range_dict[
                    "checkout"
                ] = f'{start_year}-{str(int(today_dates.strftime("%m"))+i+1)}-{today_dates.strftime("%d")}'

                month_num = str(int(today_dates.strftime("%m")) + i)
                datetime_object = datetime.datetime.strptime(month_num, "%m")
                full_month_name = datetime_object.strftime("%B")
                date_range_dict["month"] = full_month_name
                date_range_dict['place'] = place
                date_range_dict['adult']= adult
                date_range_dict['rooms']=rooms
            
        else:
            pass
        date_range_list.append(date_range_dict)

    return date_range_list


def generate_date_range_not_current_month(start_year: int, start_month: int, duration: int, place: str, adult: int, rooms: int) -> dict:
    """_summary_
    Generate date ranges if start_month is not current month(given datetime)

    Args:
        start_year (int): _description_
        start_month (int): _description_
        duration (int): _description_
        place (str): _description_
        adult (int): _description_
        rooms (int): _description_

    Returns:
        dict: _description_
    """
    today_dates = datetime.datetime.now()
    date_range_wrapper = []
    for i in range(abs(start_month - duration)+1):
        date_range_dict = {}
        # date formating -> for From january to september. Add a prefix zero.
        if int(start_month) + i <= 9:
                # formating month after september; do not add prefix zero.
            if int(start_month) + i + 1 <= 9:
                date_range = f'{start_year}-0{str(int(start_month+i))}-01'
                date_range_dict["checkin"] = date_range
                date_range_dict[
                    "checkout"
                ] = f'{start_year}-0{str(int(start_month) + i +1)}-01'

                month_num = str(int(start_month) + i)
                
                datetime_object = datetime.datetime.strptime(month_num, "%m")

                full_month_name = datetime_object.strftime("%B")
                date_range_dict["month"] = full_month_name
                date_range_dict['place'] = place
                date_range_dict['adult']= adult
                date_range_dict['rooms']=rooms

            else:
                date_range = f'{start_year}-0{str(int(start_month) + i)}-01'
                date_range_dict["checkin"] = date_range
                date_range_dict[
                    "checkout"
                ] = f'{start_year}-{str(int(start_month)+i+1)}-01'

                month_num = str(int(start_month) + i)

                datetime_object = datetime.datetime.strptime(month_num, "%m")

                full_month_name = datetime_object.strftime("%B")

                date_range_dict["month"] = full_month_name
                date_range_dict['place'] = place
                date_range_dict['adult']= adult
                date_range_dict['rooms']=rooms


         # Date formatting from october to december.
        elif int(start_month) + i > 9:
            if (int(start_month) + i + 1) > 12:
                # avoid 00 2023-00-01 date like
                if int(start_month) + i - 12 == 0:
                    date_range = f'{start_year}-{str(int(start_month)+i)}-01'
                    date_range_dict["checkin"] = date_range
                    date_range_dict[
                        "checkout"
                    ] = f'{start_year+1}-0{str((int(start_month)+i+1)-12)}-01'

                    month_num = str(int(start_month) + i)
                    datetime_object = datetime.datetime.strptime(month_num, "%m")
                    full_month_name = datetime_object.strftime("%B")
                    date_range_dict["month"] = full_month_name
                    date_range_dict['place'] = place
                    date_range_dict['adult']= adult
                    date_range_dict['rooms']=rooms
                else:
                    date_range = f'{start_year+1}-0{str(int(start_month)+i-12)}-01'
                    date_range_dict["checkin"] = date_range
                    date_range_dict[
                        "checkout"
                    ] = f'{start_year+1}-0{str((int(start_month)+i+1)-12)}-01'

                    # getting string format of the month.
                    month_num = str(int(start_month) + i - 12)

                    # creating datetime object
                    datetime_object = datetime.datetime.strptime(month_num, "%m")

                    full_month_name = datetime_object.strftime("%B")
                    date_range_dict["month"] = full_month_name
                    date_range_dict['place'] = place
                    date_range_dict['adult']= adult
                    date_range_dict['rooms']=rooms
            else:
                date_range = f'{start_year}-{str((int(start_month)+i))}-01'
                date_range_dict["checkin"] = date_range
                date_range_dict[
                    "checkout"
                ] = f'{start_year}-{str(int(start_month)+i+1)}-01'

                month_num = str(int(start_month) + i)

                datetime_object = datetime.datetime.strptime(month_num, "%m")

                full_month_name = datetime_object.strftime("%B")
                date_range_dict["month"] = full_month_name
                date_range_dict['place'] = place
                date_range_dict['adult']= adult
                date_range_dict['rooms']=rooms
        else:
            pass
        date_range_wrapper.append(date_range_dict)

    return date_range_wrapper

def construct_date(start_year: int, start_month: int, duration: int) -> dict:
    """_summary_
    date format: YYYY-MM-DD
    Generate a date range of 30 days if the start month is current calendar month or
    31 days depending with the calendar:

    Args:
        start_year (int): _description_
        start_month (int): _description_
        duration (int): _description_

    Returns:
        dict: _description_
    """
    today_dates = datetime.datetime.now()
    current_year = today_dates.year
    current_month = today_dates.strftime("%m")

    # if the start month is the current calendar month or past months and the year is current year.
    if (
        start_month == int(current_month)
        or start_month < int(current_month)
        and start_year == int(current_year)
    ):

        return generate_date_range_current_month(
            start_year,
            start_month,
            duration,
            place=const.PLACE,
            adult=const.ADULT,
            rooms=const.ROOMS,
        )

    else:
        # use numerical representation of months to compare which month is greater or less than current month.
        # The logic is that we assume if a month has high numerical representation compared to current month, it signifies future date.
        # For example: March > February: 3 > 2 or March < April, May, june... 3 < 4,5,6.... respectively.
            return generate_date_range_not_current_month(
                start_year,
                start_month,
                duration,
                place=const.PLACE,
                adult=const.ADULT,
                rooms=const.ROOMS,
            )
            
# print(construct_date(const.START_YEAR, 5, const.DURATION))
