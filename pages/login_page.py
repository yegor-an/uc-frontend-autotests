from selene import browser
from config import BASE_URL
from pages.page_with_sidebar import PageWithSidebar


class LoginPage:
    EMAIL_INPUT = '#email'
    PASSWORD_INPUT = '#password'
    SUBMIT_BUTTON = '[type="submit"]'
    RESET_PASSWORD_LINK = '#reset-password-link'
    SIGN_UP_LINK = '#sign-up-link'
    REMEMBER_ME = '[data-checked]'

    def open(self):
        browser.open(f'{BASE_URL}/login')
        return self

    def fill_email(self, email):
        browser.element(self.EMAIL_INPUT).type(email)
        return self

    def fill_password(self, password):
        browser.element(self.PASSWORD_INPUT).type(password)
        return self

    def clear_email(self):
        browser.element(self.EMAIL_INPUT).clear()
        return self

    def clear_password(self):
        browser.element(self.PASSWORD_INPUT).clear()
        return self

    def submit_with_enter(self):
        browser.element(self.PASSWORD_INPUT).press_enter()
        return PageWithSidebar()

    def submit_with_button(self):
        browser.element(self.SUBMIT_BUTTON).click()
        return PageWithSidebar()

    def click_reset_password(self):
        browser.element(self.RESET_PASSWORD_LINK).click()
        return self

    def click_sign_up(self):
        browser.element(self.SIGN_UP_LINK).click()
        return self

    def toggle_remember_me(self):
        browser.element(self.REMEMBER_ME).click()
        return self

    def click_password_field(self):
        browser.element(self.PASSWORD_INPUT).click()
        return self

    def click_show_password(self):
        browser.element('button[aria-label="Show password"] svg').click()
        return self

    def click_hide_password(self):
        browser.element('button[aria-label="Hide password"] svg').click()
        return self
