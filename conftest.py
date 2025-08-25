import tempfile, shutil
from pathlib import Path
import pytest
from selene import browser
from selenium.webdriver.chrome.options import Options
from qase.pytest import qase
from config import BASE_URL


@pytest.fixture(autouse=True)
def setup_browser():
    tmp_profile = tempfile.mkdtemp(prefix="chrome-profile-")

    opts = Options()
    opts.add_argument("--headless=new")        # запуск без окна
    opts.add_argument("--disable-gpu")         # убирает ошибки SharedImageManager на Windows
    opts.add_argument("--log-level=3")         # только ошибки, без инфо/ворнингов
    opts.add_argument("--disable-logging")     # глушит лишние логи движка
    opts.add_argument("--silent")              # делает Chrome максимально "тихим"

    browser.config.base_url = BASE_URL
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.driver_options = opts

    try:
        yield
    finally:
        try:
            browser.quit()
        finally:
            shutil.rmtree(tmp_profile, ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # let pytest run the test and produce a report
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    # only after actual call phase, only if it truly failed (not xfail)
    if rep.when == "call" and rep.failed and not getattr(rep, "wasxfail", False):
        try:
            if getattr(browser, "driver", None):
                Path("screenshots").mkdir(parents=True, exist_ok=True)
                path = Path("screenshots") / f"{item.name}.png"
                browser.driver.save_screenshot(str(path))
                qase.attach.file(str(path), "Screenshot on failure")
        except Exception:
            # keep CI green even if attachment fails
            pass
