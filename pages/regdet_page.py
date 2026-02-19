from selene import browser, command
from config import BASE_URL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time


class RegdetPage:
    LOGOUT_BUTTON = '#logout-button'
    AVATAR = '#avatar'
    UPLOAD_BUTTON = '[alt="upload"]'
    REMOVE_BUTTON = '#photo-remove-button'
    NAME_INPUT = '#name'
    LASTNAME_INPUT = '#lastName'
    LINKEDIN_INPUT = '#linkedin'
    RADIO_STARTUP = '#startup-button'
    RADIO_INVESTOR = '#investor-button'    
    SUBMIT_BUTTON = '[type="submit"]'
    IMAGE_ERROR = '#format-size-error'
    NAME_ERROR = '#name-error'
    LASTNAME_ERROR = '#lastName-error'
    LINKEDIN_ERROR = '#linkedin-error'
    
    
    def open(self):
        browser.open(f'{BASE_URL}/register-details')
        return self

    def fill_name(self, name):
        browser.element(self.NAME_INPUT).type(name)
        return self

    def fill_lastname(self, lastname):
        browser.element(self.LASTNAME_INPUT).type(lastname)
        return self

    def fill_linkedin(self, linkedin):
        browser.element(self.LINKEDIN_INPUT).perform(command.js.scroll_into_view)
        browser.element(self.LINKEDIN_INPUT).type(linkedin)
        browser.element("body").click()
        return self
        
    def clear_name(self):
        el = browser.element(self.NAME_INPUT)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.BACKSPACE)
        return self

    def clear_lastname(self):
        el = browser.element(self.LASTNAME_INPUT)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.BACKSPACE)
        return self

    def clear_linkedin(self):
        el = browser.element(self.LINKEDIN_INPUT)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.BACKSPACE)
        return self

    def submit(self):
        browser.element(self.SUBMIT_BUTTON).perform(command.js.scroll_into_view)
        browser.element(self.SUBMIT_BUTTON).click()
        return self

    def click_logout(self):
        browser.element(self.LOGOUT_BUTTON).perform(command.js.scroll_into_view)
        browser.element(self.LOGOUT_BUTTON).click()
        return self

    def upload_file(self, file_path: str):
        browser.element('#photo').set_value(file_path)
        return self
        
    def click_remove(self):
        browser.element(self.REMOVE_BUTTON).click()
        return self

    def click_startup(self):
        browser.element(self.RADIO_STARTUP).perform(command.js.scroll_into_view)
        browser.element(self.RADIO_STARTUP).click()
        return self       

    def click_investor(self):
        browser.element(self.RADIO_INVESTOR).click()
        return self                