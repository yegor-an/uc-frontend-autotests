import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selene import browser, be, have
from config import EMAIL, PASSWORD, USERNAME, BASE_URL
from pages.login_page import LoginPage
from pages.page_with_sidebar import PageWithSidebar
from test_data.signin_signup import *

pytestmark = pytest.mark.login

# -----------------------
# Successful login
# -----------------------


def test_log_in_with_enter_LOGIN1a():
    (LoginPage()
        .open()
        .fill_email(EMAIL)
        .fill_password(PASSWORD)
        .submit_with_enter()
        .should_be_loaded()
        .sidebar.should_show_username(USERNAME))


def test_log_in_with_button_LOGIN2b():
    (LoginPage()
        .open()
        .fill_email(EMAIL)
        .fill_password(PASSWORD)
        .submit_with_button()
        .should_be_loaded()
        .sidebar.should_show_username(USERNAME))


# -----------------------
# Email validation
# -----------------------


@pytest.mark.parametrize(
    "invalid_email",
    [
        INVALID_EMAIL_ONLY_LETTERS,
        INVALID_EMAIL_NO_AT,
        INVALID_EMAIL_NO_DOT,
        pytest.param(INVALID_EMAIL_WITH_SPACES, marks=pytest.mark.xfail(reason="нужна реализация")),
        INVALID_EMAIL_DOUBLE_AT,
        pytest.param(INVALID_EMAIL_DOUBLE_DOT, marks=pytest.mark.xfail(reason="нужна реализация")),
    ],
)
def test_invalid_email_shows_error_LOGIN3c(invalid_email):
    page = LoginPage().open()
    page.fill_email(invalid_email)
    browser.element(LoginPage.EMAIL_ERROR).should(be.visible).should(have.text(ERROR_EMAIL_INVALID))
    browser.element(LoginPage.SUBMIT_BUTTON).should(be.disabled)


def test_hide_validation_error_for_email_LOGIN4d():
    page = LoginPage().open()
    page.fill_email(INVALID_EMAIL_ONLY_LETTERS)
    browser.element(LoginPage.EMAIL_ERROR).should(be.visible)
    page.clear_email().fill_email(VALID_EMAIL)
    browser.element(LoginPage.EMAIL_ERROR).should(be.not_.visible)


# -----------------------
# Password validation
# -----------------------


def test_invalid_password_shows_error_LOGIN5e():
    page = LoginPage().open()
    page.fill_password(INVALID_PASSWORD_SHORT)
    browser.element(LoginPage.PASSWORD_ERROR).should(be.visible).should(have.text(ERROR_PASSWORD_MIN))
    browser.element(LoginPage.SUBMIT_BUTTON).should(be.disabled)


def test_hide_validation_error_for_password_LOGIN6f():
    page = LoginPage().open()
    page.fill_password(INVALID_PASSWORD_SHORT)
    browser.element(LoginPage.PASSWORD_ERROR).should(be.visible)
    page.clear_password().fill_password(VALID_PASSWORD)
    browser.element(LoginPage.PASSWORD_ERROR).should(be.not_.visible)


# -----------------------
# Submit button state
# -----------------------


def test_submit_disabled_when_page_open_LOGIN7g():
    page = LoginPage().open()
    browser.element(LoginPage.SUBMIT_BUTTON).should(be.disabled)


def test_submit_disabled_with_empty_email_LOGIN8h():
    page = LoginPage().open()
    page.fill_password(PASSWORD)
    browser.element(LoginPage.SUBMIT_BUTTON).should(be.disabled)


def test_submit_disabled_with_empty_password_LOGIN9i():
    page = LoginPage().open()
    page.fill_email(EMAIL)
    browser.element(LoginPage.SUBMIT_BUTTON).should(be.disabled)


# -----------------------
# Unexisting credentials
# -----------------------


def test_error_for_unexisting_email_LOGIN10j():
    page = LoginPage().open()
    page.fill_email(UNEXISTING_EMAIL).fill_password(VALID_PASSWORD).submit_with_enter()
    browser.element('#error-message #top-reset-password-link').should(be.visible)


def test_error_for_unmatching_password_LOGIN11k():
    page = LoginPage().open()
    page.fill_email(EMAIL).fill_password(UNMATCHING_PASSWORD).submit_with_enter()
    browser.element('#error-message #top-reset-password-link').should(be.visible)


# -----------------------
# Password toggle
# -----------------------


def test_password_hidden_when_page_open_LOGIN12l():
    page = LoginPage().open()
    page.click_password_field()
    browser.element('button[aria-label="Show password"] svg').should(be.visible)


def test_hide_show_password_LOGIN13m():
    page = LoginPage().open()
    page.click_password_field()
    page.click_show_password()
    browser.element('button[aria-label="Hide password"] svg').should(be.visible)
    page.click_hide_password()
    browser.element('button[aria-label="Show password"] svg').should(be.visible)


# -----------------------
# Navigation links
# -----------------------


def test_open_reset_password_page_LOGIN14n():
    page = LoginPage().open()
    page.click_reset_password()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/forgot-password')
    )


def test_open_sign_up_page_LOGIN15o():
    page = LoginPage().open()
    page.click_sign_up()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/register')
    )

# -----------------------
# Remember me
# -----------------------


def test_show_checked_remember_me_LOGIN16p():
    LoginPage().open()
    browser.element(LoginPage.REMEMBER_ME).should(have.attribute("data-checked", "true"))


def test_uncheck_remember_me_LOGIN17q():
    page = LoginPage().open()
    page.toggle_remember_me()
    browser.element(LoginPage.REMEMBER_ME).should(have.attribute("data-checked", "false"))
