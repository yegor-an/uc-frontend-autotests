from selene import browser, be
from components.sidebar import Sidebar

class PageWithSidebar:
    def __init__(self):
        self.sidebar = Sidebar()

    def should_be_loaded(self):
        browser.element('#sidebar-team-switch').should(be.visible)
        return self
