import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selene import browser, be, have
from config import EMAIL, PASSWORD, USERNAME, BASE_URL
from pages.login_page import LoginPage
from test_data.signin_signup import (
    INVALID_EMAIL_ONLY_LETTERS,
    INVALID_EMAIL_NO_AT,
    INVALID_EMAIL_NO_DOT,
    VALID_EMAIL,
    INVALID_PASSWORD_SHORT,
    INVALID_PASSWORD_LONG,
    VALID_PASSWORD,
    UNEXISTING_EMAIL,
    UNMATCHING_PASSWORD,
    ERROR_EMAIL_INVALID,
    ERROR_PASSWORD_MIN,
    ERROR_PASSWORD_MAX,
)

# -----------------------
# Позитивные сценарии
# -----------------------

@pytest.mark.c1
@pytest.mark.qase(id=1)
def test_log_in_with_enter():
    (LoginPage()
        .open()
        .fill_email(EMAIL)
        .fill_password(PASSWORD)
        .submit_with_enter()
        .should_be_loaded()
        .sidebar.should_show_username(USERNAME))


@pytest.mark.c2
@pytest.mark.qase(id=2)
def test_log_in_with_button():
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

@pytest.mark.c3
@pytest.mark.qase(id=3)
@pytest.mark.parametrize(
    "invalid_email",
    [INVALID_EMAIL_ONLY_LETTERS, INVALID_EMAIL_NO_AT, INVALID_EMAIL_NO_DOT],
)
def test_invalid_email_shows_error(invalid_email):
    page = LoginPage().open()
    page.fill_email(invalid_email)
    browser.element(LoginPage.EMAIL_ERROR).should(be.visible).should(have.text(ERROR_EMAIL_INVALID))
    browser.element(LoginPage.SUBMIT_BUTTON).should(be.disabled)


@pytest.mark.c4
@pytest.mark.qase(id=4)
def test_hide_validation_error_for_email():
    page = LoginPage().open()
    page.fill_email(INVALID_EMAIL_ONLY_LETTERS)
    browser.element(LoginPage.EMAIL_ERROR).should(be.visible)
    page.clear_email().fill_email(VALID_EMAIL)
    browser.element(LoginPage.EMAIL_ERROR).should(be.not_.visible)

# -----------------------
# Password validation
# -----------------------

@pytest.mark.c5
@pytest.mark.qase(id=5)
@pytest.mark.parametrize(
    "invalid_password, expected_error",
    [
        (INVALID_PASSWORD_SHORT, ERROR_PASSWORD_MIN),
        (INVALID_PASSWORD_LONG, ERROR_PASSWORD_MAX),
    ],
)
def test_invalid_password_shows_error(invalid_password, expected_error):
    page = LoginPage().open()
    page.fill_password(invalid_password)
    browser.element(LoginPage.PASSWORD_ERROR).should(be.visible).should(have.text(expected_error))
    browser.element(LoginPage.SUBMIT_BUTTON).should(be.disabled)


@pytest.mark.c6
@pytest.mark.qase(id=6)
def test_hide_validation_error_for_password():
    page = LoginPage().open()
    page.fill_password(INVALID_PASSWORD_SHORT)
    browser.element(LoginPage.PASSWORD_ERROR).should(be.visible)
    page.clear_password().fill_password(VALID_PASSWORD)
    browser.element(LoginPage.PASSWORD_ERROR).should(be.not_.visible)

# -----------------------
# Submit button state
# -----------------------

@pytest.mark.c7
@pytest.mark.qase(id=7)
def test_submit_disabled_with_empty_email():
    page = LoginPage().open()
    page.fill_password(PASSWORD)
    browser.element(LoginPage.SUBMIT_BUTTON).should(be.disabled)


@pytest.mark.c8
@pytest.mark.qase(id=8)
def test_submit_disabled_with_empty_password():
    page = LoginPage().open()
    page.fill_email(EMAIL)
    browser.element(LoginPage.SUBMIT_BUTTON).should(be.disabled)

# -----------------------
# Unexisting credentials
# -----------------------

@pytest.mark.c9
@pytest.mark.qase(id=9)
def test_error_for_unexisting_email():
    page = LoginPage().open()
    page.fill_email(UNEXISTING_EMAIL).fill_password(VALID_PASSWORD).submit_with_enter()
    browser.element('#error-message #top-reset-password-link').should(be.visible)

@pytest.mark.c10
@pytest.mark.qase(id=10)
def test_error_for_unmatching_password():
    page = LoginPage().open()
    page.fill_email(EMAIL).fill_password(UNMATCHING_PASSWORD).submit_with_enter()
    browser.element('#error-message #top-reset-password-link').should(be.visible)

# -----------------------
# Password toggle
# -----------------------

@pytest.mark.c11
@pytest.mark.qase(id=11)
def test_hide_show_password():
    page = LoginPage().open()
    page.click_password_field()
    page.click_show_password()
    browser.element('button[aria-label="Hide password"] svg').should(be.visible)
    page.click_hide_password()
    browser.element('button[aria-label="Show password"] svg').should(be.visible)

# -----------------------
# Navigation links
# -----------------------

@pytest.mark.c12
@pytest.mark.qase(id=12)
def test_open_reset_password_page():
    page = LoginPage().open()
    page.click_reset_password()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/forgot-password')
    )

@pytest.mark.c13
@pytest.mark.qase(id=13)
def test_open_sign_up_page():
    page = LoginPage().open()
    page.click_sign_up()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/register')
    )

# -----------------------
# Remember me
# -----------------------

@pytest.mark.c14
@pytest.mark.qase(id=14)
def test_show_checked_remember_me():
    LoginPage().open()
    browser.element(LoginPage.REMEMBER_ME).should(have.attribute("data-checked", "true"))


@pytest.mark.c15
@pytest.mark.qase(id=15)
def test_uncheck_remember_me():
    page = LoginPage().open()
    page.toggle_remember_me()
    browser.element(LoginPage.REMEMBER_ME).should(have.attribute("data-checked", "false"))
