## Booking.com_crawler

An advanced web scraper for extracting hotel data from *[Booking.com](https://www.booking.com/)*. No sign up or log in required. 
The code is meant to be simple, easy to use and modify. However,there are few configuration and setups that are necessary for the code program to work.

Please read the following the following sections carefully.  

## Summary
Booking.com is an online travel agency for lodging reservations & other travel products. The booking.com_crawler is an web scraping bot that crawls the booking.com website to extract hotel data and stores the scrape data in csv file. 
      
## Scraper Features

 - Apply filters *can be customized*
 - Switch browsers tabs
 - Generate date ranges for checkin and checkout
 - Click and follow the link
 - Perform Pagenation
 - Web automation
 - Data conversion - get in csv format or json format.
 - Proxy - not yet implemented
      
## Data Features 
- city_name 
- property_name 
- property_description
- property_images
- property_url_link
- property_address
- location
- property_price 
- property_type
- property_score
- checkin_date
- checkout_date
- number_of_adults
- number_of_rooms

## Getting Started

### 1. Clone the repository

To clone this repository using Git, use

     git clone https://github.com/gilbertekalea/booking.com_crawler.git

### 2. Installing Dependencies
The official python package manager for installing dependecies is **pip**. 

If you're new to python please checkout this article on [how to install pip](https://stackoverflow.com/questions/4750806/how-can-i-install-pip-on-windows)

### Activate Virtual Environment

To activate virtual environment run the following script in command line. Please refer here [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html) on how to activate venv in your machine.

For windows powershell : 

   my_bot\project_folder_dir> venv\Scripts\activate.ps1 

Now install the dependencies using the requirements.txt file.

            my_bot\project_folder_dir> pip -r requirements.txt

### Selenium

In order for this project to work in your computer; You need to have a selenium and python installed in your computer. 
I assume if you are interested in this project,you already know the basics of python and you have python installed. 

For window users: Open windows terminal and open project directory. 

    pip install selenium

#### **Drivers**
Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin.

Read more about webdrivers here [Selenium Installation](https://pypi.org/project/selenium/) and [Selenium Official documentation](https://www.selenium.dev/documentation/webdriver/)


#### **Downloading WebDriver**
This project uses chromedriver. I understand that you're using a different browser;

Here are download links for most popular browsers. 

[Chrome](https://chromedriver.chromium.org/downloads)

[Firefox](https://github.com/mozilla/geckodriver/releases)

[Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

[Safari](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)

Once you download your prefered driver; You can either save the .exe file in your project folder or you can save it somewhere in the your computer and provide the path. I recommend you save it in a different folder within the project folder or somewhere in your computer and use system path methods to access it. 

## Quick Guide
### client_input folder

 The first thing you would want to do is to set your variables. These will set the foundation on what the bot should do in terms which city to enter in booking.com     search box, generating date ranges etc. Open *client_input/destination_param.csv*  file and fill the data for  the following required variables.
 
      place - Where you want to go, prefered to enter a city name. 
      start_month - lays the foundation on where to start the checkin dates and updates the checkout. 
      start_year - the start year.  
      duration - How long is your stay. The duration helps the bot to generate date ranges starting from next_month and set checkin and checkout dates. 
      adults - Number of adult,
      rooms - number 0f rooms
      
### run the bot

To run the bot you simply type

      python runbot.py
      
 The bot you automatically open your boooking.com in chrome browser window. 
 

                                 
                             
                           
