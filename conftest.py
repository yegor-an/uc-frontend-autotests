import pytest
from selene import browser
from qase.pytest import qase
from config import BASE_URL


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    browser.config.base_url = BASE_URL
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    yield
    browser.quit()


@pytest.fixture(autouse=True)
def take_screenshot_on_failure(request):
    yield
    # после выполнения теста
    if request.node.rep_call.failed:  # если тест упал
        screenshot_path = f'screenshots/{request.node.name}.png'
        browser.driver.save_screenshot(screenshot_path)
        qase.attach.file(screenshot_path, "Screenshot on failure")
        

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)
