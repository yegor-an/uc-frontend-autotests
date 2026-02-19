from selene import browser
from .visual_utils import assert_screenshot
from config import BASE_URL

def test_login_page_visual():
    browser.config.window_width = 1517
    browser.config.window_height = 841

    browser.open(f"{BASE_URL}/login")
    assert_screenshot(browser.driver, "login_page.png", threshold=1)
