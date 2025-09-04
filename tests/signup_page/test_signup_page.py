import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selene import browser, be, have
from config import EMAIL, PASSWORD, USERNAME, BASE_URL
from pages.signup_page import SignupPage
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
# Successful signup
# -----------------------


@pytest.mark.signup1
def test_sign_up_with_enter():
    (SignupPage()
        .open()
        .fill_email(EMAIL)
        .fill_password(PASSWORD)
        .submit_with_enter()
        .should_be_loaded()
        .sidebar.should_show_username(USERNAME))


@pytest.mark.signup2
def test_sign_up_with_button():
    (SignupPage()
        .open()
        .fill_email(EMAIL)
        .fill_password(PASSWORD)
        .submit_with_button()
        .should_be_loaded()
        .sidebar.should_show_username(USERNAME))


# -----------------------
# Email validation
# -----------------------


@pytest.mark.signup3
@pytest.mark.parametrize(
    "invalid_email",
    [INVALID_EMAIL_ONLY_LETTERS, INVALID_EMAIL_NO_AT, INVALID_EMAIL_NO_DOT],
)
def test_invalid_email_shows_error(invalid_email):
    page = SignupPage().open()
    page.fill_email(invalid_email)
    browser.element(SignupPage.EMAIL_ERROR).should(be.visible).should(have.text(ERROR_EMAIL_INVALID))
    browser.element(SignupPage.SUBMIT_BUTTON).should(be.disabled)


@pytest.mark.signup4
def test_hide_validation_error_for_email():
    page = SignupPage().open()
    page.fill_email(INVALID_EMAIL_ONLY_LETTERS)
    browser.element(SignupPage.EMAIL_ERROR).should(be.visible)
    page.clear_email().fill_email(VALID_EMAIL)
    browser.element(SignupPage.EMAIL_ERROR).should(be.not_.visible)


# -----------------------
# Password validation
# -----------------------


@pytest.mark.signup5
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
def test_invalid_password_shows_error(invalid_password, expected_error):
    page = SignupPage().open()
    page.fill_password(invalid_password)
    browser.element(SignupPage.PASSWORD_ERROR).should(be.visible).should(have.text(expected_error))
    browser.element(SignupPage.SUBMIT_BUTTON).should(be.disabled)


@pytest.mark.signup6
def test_hide_validation_error_for_password():
    page = SignupPage().open()
    page.fill_password(INVALID_PASSWORD_SHORT)
    browser.element(SignupPage.PASSWORD_ERROR).should(be.visible)
    page.clear_password().fill_password(VALID_PASSWORD)
    browser.element(SignupPage.PASSWORD_ERROR).should(be.not_.visible)


# -----------------------
# Submit button state
# -----------------------


@pytest.mark.signup7
def test_submit_disabled_with_empty_email():
    page = SignupPage().open()
    page.fill_password(PASSWORD)
    browser.element(SignupPage.SUBMIT_BUTTON).should(be.disabled)


@pytest.mark.signup8
def test_submit_disabled_with_empty_password():
    page = SignupPage().open()
    page.fill_email(EMAIL)
    browser.element(SignupPage.SUBMIT_BUTTON).should(be.disabled)


# -----------------------
# Unexisting credentials
# -----------------------


@pytest.mark.signup9
def test_error_for_unexisting_email():
    page = SignupPage().open()
    page.fill_email(UNEXISTING_EMAIL).fill_password(VALID_PASSWORD).submit_with_enter()
    browser.element('#error-message #top-reset-password-link').should(be.visible)

@pytest.mark.signup10
def test_error_for_unmatching_password():
    page = SignupPage().open()
    page.fill_email(EMAIL).fill_password(UNMATCHING_PASSWORD).submit_with_enter()
    browser.element('#error-message #top-reset-password-link').should(be.visible)


# -----------------------
# Password toggle
# -----------------------


@pytest.mark.signup11
def test_hide_show_password():
    page = SignupPage().open()
    page.click_password_field()
    page.click_show_password()
    browser.element('button[aria-label="Hide password"] svg').should(be.visible)
    page.click_hide_password()
    browser.element('button[aria-label="Show password"] svg').should(be.visible)


# -----------------------
# Navigation links
# -----------------------


@pytest.mark.signup12
def test_open_log_in_page():
    page = SignupPage().open()
    page.click_log_in()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/login')
    )


@pytest.mark.signup13
def test_open_policy_page():
    page = SignupPage().open()
    page.click_policy()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/policy')
    )


@pytest.mark.signup14
@pytest.mark.skip
def test_open_terms_page():
    page = SignupPage().open()
    page.click_terms()
    WebDriverWait(browser.driver, 4).until(
        EC.url_to_be(f'{BASE_URL}/')
    )


# -----------------------
# Remember me
# -----------------------


@pytest.mark.signup15
def test_show_checked_remember_me():
    SignupPage().open()
    browser.element(SignupPage.REMEMBER_ME).should(have.attribute("data-checked", "true"))


@pytest.mark.signup16
def test_uncheck_remember_me():
    page = SignupPage().open()
    page.toggle_remember_me()
    browser.element(SignupPage.REMEMBER_ME).should(have.attribute("data-checked", "false"))
