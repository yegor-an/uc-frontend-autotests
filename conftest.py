import tempfile, shutil
from pathlib import Path

import pytest
from selene import browser, Config
from selenium.webdriver.chrome.options import Options
from qase.pytest import qase
from config import BASE_URL


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    tmp_profile = tempfile.mkdtemp(prefix="chrome-profile-")

    opts = Options()
    opts.add_argument(f"--user-data-dir={tmp_profile}")
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    browser.config = Config(
        base_url=BASE_URL,
        window_width=1920,
        window_height=1080,
        driver_options=opts,
    )

    try:
        yield
    finally:
        # закрыть драйвер и убрать профиль
        try:
            browser.quit()
        finally:
            shutil.rmtree(tmp_profile, ignore_errors=True)


@pytest.fixture(autouse=True)
def take_screenshot_on_failure(request):
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        try:
            Path("screenshots").mkdir(parents=True, exist_ok=True)
            path = f"screenshots/{request.node.name}.png"
            browser.driver.save_screenshot(path)
            qase.attach.file(path, "Screenshot on failure")
        except Exception:
            # не мешаем падать тесту из-за проблем со скриншотом
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
