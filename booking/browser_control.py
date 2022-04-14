
'''
This module contains webbrowser control methods such as switching to a new tab, closing current tab, and switching back to the main tab.
'''
from selenium.webdriver.remote.webdriver import WebDriver


class BrowserWindowControl:

    """
    A class containing methods that control the browser window and switch to different windows.
    Can be used to switch to the main window, or to the detail page back and forth as long the requirements
    """

    def __init__(self, browser: WebDriver):
        self.browser = browser

    def get_window_handle(self) -> list:
        """
        returns a list window handles of the browser.
        We try to restrict these handles to maximum of 2 windows. This is achieved by tearing down the current window and switching back to the main window.
        returns a list of window handles.
        """
        return self.browser.window_handles

    def switch_window(self):
        """
        Method that perform switching mechanism from the main window to the new window created after clicking a button.

        """
        # First get the window handles.
        browser_handles = self.get_window_handle()
        # Loop through the window handles and switch to the new window if a match is found.
      
        if len(browser_handles) > 2:
            # This is a small hack to get the new window handle after clicking the availability button. Turns out that by the time
            # I was writing this program, if you click the availability button the browser misbehaves and opens two windows.
            
            # So this hack take's care of it. Can only handle 2 windows.
            # However, inorder for the program to work, I had to switch to the new window if only we have a maximum of two windows.
            #  
            # time.sleep(2)
            self.browser.switch_to.window(browser_handles[2])
            self.browser.close()
            # time.sleep(2)
            self.browser.switch_to.window(browser_handles[1])

        else:
            for index, handle in enumerate(browser_handles):
                
                if handle != self.browser.current_window_handle:
                    # print('switching to new window:', handle)
                    self.browser.switch_to.window(handle)
                    print("from browser window switch successful")
                    break
                else:
                    continue

    def switch_to_main_window(self) -> None:
        """
        Method to take the webdriver back to the main window.
        """
        handles = self.get_window_handle()
        # print('switching back to main window: ', handles[0])
        self.browser.switch_to.window(handles[0])

    def tear_down_current_window(self) -> None:
        
        """
        This method will close the current window.

        """

        # This hack is needed in order for the function get_availability_button which expected to return a tuple to pull_deal_boxes_attribute in report.py.
        # Once the window is switched to the main window, we have received the data from get_availability_button function, Now we can close the window the new window by going
        # back to it and tear it down.

        self.browser.close()
        self.switch_to_main_window()

    def close_window(self) -> None:
        """
        This method will close the current window.
        """
        # This hack is needed in order for the function get_availability_button which expected to a tuple to pull_deal_boxes_attribute in report.py.
        # Once the window is switched to the main window, we have received the data from get_availability_button function, Now we can close the window the new window by going
        # back to it and tear it down.
        self.tear_down_current_window()
      