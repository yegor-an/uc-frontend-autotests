import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selene import browser, be, have, command
from config import BASE_URL, PASSWORD
from pages.regdet_page import RegdetPage      
from pages.login_page import LoginPage          
from test_data.regdet import *
from tests.utils import *
import logging
logging.basicConfig(level=logging.INFO)

#pytestmark = pytest.mark.regdet

@pytest.fixture
def login_and_regdet():
    email = get_last_email("../emails_without_user_anketa.txt")
    (LoginPage()
        .open()
        .fill_email(email)
        .fill_password(PASSWORD)
        .submit_with_enter()
    )

    return RegdetPage().open()

def test_all_disabled_REGDET1a(login_and_regdet):
    browser.element(login_and_regdet.NAME_INPUT).should(be.blank)
    browser.element(login_and_regdet.LASTNAME_INPUT).should(be.blank)
    browser.element(login_and_regdet.LINKEDIN_INPUT).should(be.blank)
    browser.element(login_and_regdet.RADIO_STARTUP).should(have.attribute("aria-checked", "false"))
    browser.element(login_and_regdet.RADIO_INVESTOR).should(have.attribute("aria-checked", "false"))
    browser.element(login_and_regdet.SUBMIT_BUTTON).should(be.disabled)


def test_success_regdet_REGDET2b(login_and_regdet):
    login_and_regdet.upload_file(JPG_PATH)
    
    browser.execute_script("""
    document.documentElement.style.scrollBehavior = 'auto';
    document.body.style.scrollBehavior = 'auto';
""")
    
    browser.element(login_and_regdet.REMOVE_BUTTON).should(be.visible)

    login_and_regdet.fill_name(NAME)
    login_and_regdet.fill_lastname(LASTNAME)
    login_and_regdet.fill_linkedin(LINKEDIN)
    login_and_regdet.click_startup()

    browser.element(login_and_regdet.SUBMIT_BUTTON).should(be.clickable)

    login_and_regdet.submit()   
    
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/new-startup')
    )
    
    email = get_last_email("../emails_without_user_anketa.txt")
    remove_email("../emails_without_user_anketa.txt", email)
    save_email("../emails_without_profiles.txt", email)
    

@pytest.mark.xfail(reason="Submit активируется при любых непустых данных")
def test_submit_disabled_REGDET3c(login_and_regdet):
    login_and_regdet.fill_name("1")
    login_and_regdet.fill_lastname("q")
    login_and_regdet.click_startup()

    browser.element(login_and_regdet.SUBMIT_BUTTON).should(be.disabled)


def test_name_error_REGDET4d(login_and_regdet):
    login_and_regdet.fill_name("1")
    browser.element(login_and_regdet.NAME_ERROR).should(be.visible)
    login_and_regdet.clear_name().fill_name("John")
    browser.element(login_and_regdet.NAME_ERROR).should(be.not_.visible)


def test_lastname_error_REGDET5e(login_and_regdet):
    login_and_regdet.fill_lastname("1")
    browser.element(login_and_regdet.LASTNAME_ERROR).should(be.visible)
    login_and_regdet.clear_lastname().fill_lastname("Connor")
    browser.element(login_and_regdet.LASTNAME_ERROR).should(be.not_.visible)
    
    
def test_linkedin_error_REGDET6f(login_and_regdet):
    login_and_regdet.fill_linkedin("1")    
    browser.element(login_and_regdet.LINKEDIN_ERROR).should(be.visible)
    login_and_regdet.clear_linkedin().fill_linkedin(LINKEDIN)
    browser.element(login_and_regdet.LINKEDIN_ERROR).should(be.not_.visible)


def test_upload_and_remove_photo_REGDET7g(login_and_regdet):
    login_and_regdet.upload_file(JPG_PATH)
    browser.element(login_and_regdet.IMAGE_ERROR).should(be.not_.visible)    
    browser.element(login_and_regdet.REMOVE_BUTTON).should(be.visible)
    login_and_regdet.click_remove()
    login_and_regdet.upload_file(TXT_PATH)
    browser.element(login_and_regdet.IMAGE_ERROR).should(be.visible)
    login_and_regdet.upload_file(HEAVY_IMAGE_PATH)
    browser.element(login_and_regdet.IMAGE_ERROR).should(be.visible)
    browser.element(login_and_regdet.UPLOAD_BUTTON).should(be.visible)


def test_photo_formats_REGDET8h(login_and_regdet):
    login_and_regdet.upload_file(PNG_PATH)
    browser.element(login_and_regdet.IMAGE_ERROR).should(be.not_.visible)    
    browser.element(login_and_regdet.REMOVE_BUTTON).should(be.visible)
    login_and_regdet.click_remove()
    login_and_regdet.upload_file(WEBP_PATH)
    browser.element(login_and_regdet.IMAGE_ERROR).should(be.not_.visible)    
    browser.element(login_and_regdet.REMOVE_BUTTON).should(be.visible)


def test_radio_REGDET9j(login_and_regdet):
    browser.execute_script("""
    document.documentElement.style.scrollBehavior = 'auto';
    document.body.style.scrollBehavior = 'auto';
""")
    login_and_regdet.click_startup()
    browser.element('#startup-button').should(have.attribute("aria-checked", "true"))
    browser.element('#investor-button').should(have.attribute("aria-checked", "false"))
    login_and_regdet.click_investor()
    browser.element('#investor-button').should(have.attribute("aria-checked", "true"))
    browser.element('#startup-button').should(have.attribute("aria-checked", "false"))


def test_logout_REGDET10k(login_and_regdet):
    login_and_regdet.click_logout()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/')
    )    
