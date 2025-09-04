from selene import browser
from pages.page_with_sidebar import PageWithSidebar
from config import BASE_URL


class LoginPage(PageWithSidebar):
    EMAIL_INPUT = '#email'
    PASSWORD_INPUT = '#password'
    SUBMIT_BUTTON = '[type="submit"]'
    RESET_PASSWORD_LINK = '#reset-password-link'
    LOG_IN_LINK = '#log-in-link'
    PRIVACY_POLICY_LINK = '#privacy-policy-link'
    TERMS_OF_SERVICE_LINK = '#terms-of-service-link'
    
    def open(self):
        browser.open(f'{BASE_URL}/register')
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
        return self

    def submit_with_button(self):
        browser.element(self.SUBMIT_BUTTON).click()
        return self

    def click_login(self):
        browser.element(self.LOG_IN_LINK).click()
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

    def click_privacy_policy(self):
        browser.element(self.PRIVACY_POLICY_LINK).click()
        return self
        
    def click_terms_of_service(self):
        browser.element(self.TERMS_OF_SERVICE_LINK).click()
        return self