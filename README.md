## BookingBot
Advanced crawler for extracting hotels data from *[Booking.com](https://www.booking.com/)*. 

## Summary
Depending with the start month, the crawler is equiped with functions to generate date range starting from the current month for about 15, months. 
The dates range are then arranged in checkin and checkout format; Where the second checkin date is equivalence of last checkout date. for example:
These dates are automatically generated; All you have to do is provide the following data in *constant.py*

For example, if my first checkin and checkout are the following:

      checkin: 2022-05-01,
      checkout: 2022-06-01

Then the second date range will start from:

    checkin: 2022-06-01,
    checkout: 2022-07-01.

