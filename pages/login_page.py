from selene import browser, be, have, by
from pages.page_with_sidebar import PageWithSidebar

class LoginPage(PageWithSidebar):
    def open(self):
        browser.open('/login')
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

