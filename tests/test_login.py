import pytest
from config import EMAIL, PASSWORD, USERNAME
from pages.login_page import LoginPage


@pytest.mark.qase(id=1)
def test_login_with_enter():
    (LoginPage()
        .open()
        .login_with_enter(EMAIL, PASSWORD)
        .should_be_loaded()
        .sidebar.should_see_profile_with(USERNAME))


@pytest.mark.qase(id=1)
def test_login_with_button():
    (LoginPage()
        .open()
        .login_with_button(EMAIL, PASSWORD)
        .should_be_loaded()
        .sidebar.should_see_profile_with(USERNAME))