# This file contain methods that allow the webdriver to click see avaialability buttofrom selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

class PageSetting:
    '''
    This class contain methods that control the browser window and switch to different windows.
    Can be used to switch to the main window, or to the detail page back and forth as long the requirements
    '''
    pass


class PropertyDetail:

    '''
    A class to containing methods that will allow the webdriver to click the see availability button.
    and perform actions on the new window to go new window.
    collect necessary information from the new window, close it and return to the main window.  

    '''
    
    def __init__(self, detail_page: WebDriver):
        self.detail_page = detail_page
    
    def tear_down_current_window(self):
        '''
        This method will close the current window.

        '''
        self.detail_page.close()

    def get_window_handle(self) -> list:
        '''
        This method will return a list window handles of the browser. 
        We try to restrict these handles to maximum of 2 windows.
        We achieve this by tearing down the current window and switching back to the main window.

        Returns a list of window handles.

        '''
        return self.detail_page.window_handles

    def switch_window(self):
        '''
        This method will switch to from the main window to the new window that contains the property description.

        '''
        # First get the window handles.
        handles = self.get_window_handle()
        # Loop through the window handles and switch to the new window if a match is found.
        for index, handle in enumerate(handles):
            if handle != self.detail_page.current_window_handle:
                print('switching to new window')
                self.detail_page.switch_to.window(handle)
                break

    def switch_to_main_window(self):
        '''
        This method will switch back to the main window.
        '''
        handles = self.get_window_handle()
        print('switching back to main window')
        self.detail_page.switch_to.window(handles[0])

    def close_window(self):
        '''
        This method will close the current window.
        '''
        self.tear_down_current_window()
        self.switch_to_main_window()

    def get_availability_button(self, deal_box) -> None:
        '''
        This method will click the see availability button.
        '''
        try:
            availability_button = deal_box.find_element(
                By.CSS_SELECTOR, 'div[data-testid="availability-cta"]'
            )
            availability_button.click()
            self.switch_window()
            gallery = self.get_property_gallery()
            self.get_property_description()
            self.close_window()
    
        except NoSuchElementException:
            availability_button = None
            print('availability element was not found')
        return gallery

    def get_window_handle(self) -> list:
        '''
        This method will return a list window handles of the browser. 
        We try to restrict these handles to maximum of 2 windows.
        We achieve this by tearing down the current window and switching back to the main window.

        Returns a list of window handles.

        '''
        return self.detail_page.window_handles

    def get_property_gallery(self):
        
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
            
        except NoSuchAttributeException:
            pass
        return img_collection

    def get_property_description(self):
        '''
        This method will return the property description, property_images, property_address.
        '''
        # first switch to the new window.
        # self.switch_window()
        try:
            summary = self.detail_page.find_element(By.ID, "summary")
            paragrams  = summary.find_elements(By.TAG_NAME, 'p')
            for item in paragrams:
                print(item.text)
            
        except NoSuchElementException as e:
            print('summary element was not found', str(e))

        
    

