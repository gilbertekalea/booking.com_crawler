import datetime


def when_is_vocation(month):
    """
    return month in capitalized format
    """
    months_lower = month.lower()
    return months_lower.capitalize()


def find_number_in_string(string) -> str:
    """
    Given a string, loop through a string and return a int type occurance.
    """
    store = []
    for i, item in enumerate(string):
        try:
            if type(int(item)) == int:
                store.append(item)
        except ValueError:
            continue

    # concetenating
    prop_count = ""
    for i in store:
        prop_count = prop_count + i
    return prop_count
