# This file contain methods that allow the webdriver to click see avaialability buttofrom selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import time

class PageSetting:
    '''
    A class containing methods that control the browser window and switch to different windows.
    Can be used to switch to the main window, or to the detail page back and forth as long the requirements
    '''
    pass


class PropertyDetail:

    '''
    A class containing methods that will allow the webdriver to click availability button.
    and perform actions on the new window to go new window.
    collect necessary information from the new window, close it and return to the main window.  

    '''
    
    def __init__(self, detail_page: WebDriver):
        self.detail_page = detail_page

    def get_availability_button(self, deal_box):

        '''
        This method will click the see availability button.
        The web element is located in the deal_box param.
        '''
        try:
            availability_button = deal_box.find_element(
                By.CSS_SELECTOR, 'div[data-testid="availability-cta"]'
            )

            availability_button.click()

            self.switch_window()
            print('current url is: ', self.detail_page.current_url)
            # time.sleep(5)
            img = self.get_property_gallery()
            description = self.get_property_description()
            self.close_window()
           
        except NoSuchElementException or ElementNotInteractableException or NoSuchAttributeException:
            # prevent browser from crashing and keep it going 
            img = []
            description= ''
            print('Sorry the availability button was not found')
            self.close_window()
        
        return img, description

    def get_window_handle(self) -> list:
        '''
        returns a list window handles of the browser. 
        We try to restrict these handles to maximum of 2 windows. This is achieved by tearing down the current window and switching back to the main window.
        returns a list of window handles.
        '''
        return self.detail_page.window_handles

    def switch_window(self):
        '''
        Method that perform switching mechanism from the main window to the new window created after clicking a button. 
        
        '''
        # First get the window handles.
        handles = self.get_window_handle()
        # Loop through the window handles and switch to the new window if a match is found.
        for index, handle in enumerate(handles):
            if handle != self.detail_page.current_window_handle:
                print('switching to new window:', handle)
                self.detail_page.switch_to.window(handle)
                break

    def switch_to_main_window(self)-> None:
        '''
        Method to take the webdriver back to the main window.
        '''
        handles = self.get_window_handle()
        print('switching back to main window: ', handles[0])
        self.detail_page.switch_to.window(handles[0])

    def tear_down_current_window(self) -> None:

        '''
        This method will close the current window.

        '''
        handles = self.get_window_handle()

        # This hack is needed in order for the function get_availability_button which expected to return a tuple to pull_deal_boxes_attribute in report.py.
        # Once the window is switched to the main window, we have received the data from get_availability_button function, Now we can close the window the new window by going 
        # back to it and tear it down.

        # self.detail_page.switch_to.window(handles[1])
        self.detail_page.close()
        self.switch_to_main_window()

    def close_window(self)-> None:
        '''
        This method will close the current window.
        '''
        # This hack is needed in order for the function get_availability_button which expected to a tuple to pull_deal_boxes_attribute in report.py.
        # Once the window is switched to the main window, we have received the data from get_availability_button function, Now we can close the window the new window by going 
        # back to it and tear it down.
        self.tear_down_current_window()
        # self.switch_to_main_window()
        
    def get_property_gallery(self) -> list:
        '''
        Method to get the property gallery images.
        returns a list of images.
        '''

        try:
            gallery_container = self.detail_page.find_element(
                By.ID,"blockdisplay1")
            hotel_main_content = gallery_container.find_element(By.ID, "hotel_main_content")
            all_img = hotel_main_content.find_element(By.CSS_SELECTOR, 'div[data-component="gallery-side-reviews"]')
            # extra = all_img.find_element(By.CSS_SELECTOR, 'div[class="clearfix bh-photo-grid bh-photo-grid--space-down fix-score-hover-opacity"]')
            property_images_container = all_img.find_elements(By.CSS_SELECTOR, 'div[aria-hidden="true"]')
            
            img_collection = []
            for item in property_images_container:
                a = item.find_element(By.XPATH, '//a[contains(@href, "#")]')
                img = a.find_element(By.XPATH, '//a[contains(@href, "#")]/img')
                print(img.get_attribute('src'))
                img_collection.append(img.get_attribute('src'))

            return img_collection

        except NoSuchAttributeException as e:

            print('No such attribute exception: ', e)
            img_collection = []

            return img_collection
        
    def get_property_description(self) -> str:
        '''
        Method to get the property description in details.
        returns a string.
        '''
    
        try:
            description = ""
            summary = self.detail_page.find_element(By.ID, "summary")
            paragrams  = summary.find_elements(By.TAG_NAME, 'p')
            for item in paragrams:
                # print(item.text)
                description += item.text
            print(description)
            return description

        except NoSuchElementException as e:

            print('description element was not found', str(e))
            return description



        
    

