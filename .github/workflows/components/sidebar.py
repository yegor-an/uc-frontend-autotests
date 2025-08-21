from selene import browser, be, have, by

class Sidebar:
    def should_show_username(self, username):
        browser.element(by.text(username)).should(be.visible).should(have.text(username))
        return self