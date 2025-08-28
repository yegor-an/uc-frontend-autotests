from selene import browser, be, have, by
from pages.page_with_sidebar import PageWithSidebar
from config import BASE_URL

class LoginPage(PageWithSidebar):
    def open(self):
        browser.open(f'{BASE_URL}/login')
        return self

    def login_with_enter(self, email, password):
        browser.element('#email').type(email)
        browser.element('#password').type(password).press_enter()
        return self

    def login_with_button(self, email, password):
        browser.element('#email').type(email)
        browser.element('#password').type(password)
        browser.element('[type="submit"]').click()
        return self

    def email_validation_error(self):
        browser.element('#email').type('la')
        browser.element('#email-error').should(be.visible) 
        browser.element('#email-error').should(have.text('Email not valid'))  
        browser.element('[type="submit"]').should(be.disabled)
        
    def password_validation_error(self):
        browser.element('#password').type('la')
        browser.element('#password-error').should(be.visible) 
        browser.element('#password-error').should(have.text('Min. 8 characters')) 
        browser.element('[type="submit"]').should(be.disabled)