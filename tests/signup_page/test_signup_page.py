import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selene import browser, be, have
from config import EMAIL, PASSWORD, USERNAME, BASE_URL
from pages.signup_page import SignupPage
from test_data.signin_signup import *
from tests.utils import generate_email

pytestmark = pytest.mark.signup


# -----------------------
# Successful signup
# -----------------------


def test_sign_up_with_enter_SIGNUP1():
    (SignupPage()
        .open()
        .fill_email(generate_email())
        .fill_password(PASSWORD)
        .submit_with_enter())
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/register-details')
    )


def test_sign_up_with_button_SIGNUP2():
    (SignupPage()
        .open()
        .fill_email(generate_email())
        .fill_password(PASSWORD)
        .submit_with_button())


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
def test_invalid_email_shows_error_SIGNUP3(invalid_email):
    page = SignupPage().open()
    page.fill_email(invalid_email)
    browser.element(SignupPage.EMAIL_ERROR).should(be.visible).should(have.text(ERROR_EMAIL_INVALID))
    browser.element(SignupPage.SUBMIT_BUTTON).should(be.disabled)


def test_hide_validation_error_for_email_SIGNUP4():
    page = SignupPage().open()
    page.fill_email(INVALID_EMAIL_ONLY_LETTERS)
    browser.element(SignupPage.EMAIL_ERROR).should(be.visible)
    page.clear_email().fill_email(VALID_EMAIL)
    browser.element(SignupPage.EMAIL_ERROR).should(be.not_.visible)


# -----------------------
# Password validation
# -----------------------


@pytest.mark.parametrize(
    "invalid_password, expected_error",
    [
        (INVALID_PASSWORD_SHORT, ERROR_PASSWORD_MIN),
        pytest.param(
            INVALID_PASSWORD_LONG,
            ERROR_PASSWORD_MAX,
            marks=pytest.mark.xfail(reason="валидация >64 символов ещё не реализована"),
        ),
    ],
)
def test_invalid_password_shows_error_SIGNUP5(invalid_password, expected_error):
    page = SignupPage().open()
    page.fill_password(invalid_password)
    browser.element(SignupPage.PASSWORD_ERROR).should(be.visible).should(have.text(expected_error))
    browser.element(SignupPage.SUBMIT_BUTTON).should(be.disabled)


def test_hide_validation_error_for_password_SIGNUP6():
    page = SignupPage().open()
    page.fill_password(INVALID_PASSWORD_SHORT)
    browser.element(SignupPage.PASSWORD_ERROR).should(be.visible)
    page.clear_password().fill_password(VALID_PASSWORD)
    browser.element(SignupPage.PASSWORD_ERROR).should(be.not_.visible)


# -----------------------
# Submit button state
# -----------------------


def test_submit_disabled_with_empty_email_SIGNUP7():
    page = SignupPage().open()
    page.fill_password(PASSWORD)
    browser.element(SignupPage.SUBMIT_BUTTON).should(be.disabled)


def test_submit_disabled_with_empty_password_SIGNUP8():
    page = SignupPage().open()
    page.fill_email(EMAIL)
    browser.element(SignupPage.SUBMIT_BUTTON).should(be.disabled)


# -----------------------
# Unexisting credentials
# -----------------------


def test_error_for_taken_email_SIGNUP9():
    page = SignupPage().open()
    page.fill_email(EMAIL).fill_password(VALID_PASSWORD).submit_with_enter()
    browser.element(SignupPage.EMAIL_ERROR).should(be.visible)


# -----------------------
# Password toggle
# -----------------------


def test_password_hidden_when_page_open_SIGNUP10():
    page = SignupPage().open()
    page.click_password_field()
    browser.element('button[aria-label="Show password"] svg').should(be.visible)


def test_hide_show_password_SIGNUP11():
    page = SignupPage().open()
    page.click_password_field()
    page.click_show_password()
    browser.element('button[aria-label="Hide password"] svg').should(be.visible)
    page.click_hide_password()
    browser.element('button[aria-label="Show password"] svg').should(be.visible)


# -----------------------
# Navigation links
# -----------------------


def test_open_log_in_page_SIGNUP12():
    page = SignupPage().open()
    page.click_log_in()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/login')
    )


def test_open_policy_page_SIGNUP13():
    page = SignupPage().open()
    page.click_policy()
    browser.driver.switch_to.window(browser.driver.window_handles[-1])
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f"{BASE_URL}/policy")
    )


@pytest.mark.skip
def test_open_terms_page_SIGNUP14():
    page = SignupPage().open()
    page.click_terms()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/')
    )
