from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page, expect

from framework.pages.inventory_page import InventoryPage
from framework.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """A consistent desktop-sized window for every test."""
    return {**browser_context_args, "viewport": {"width": 1400, "height": 1000}}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Remember each phase's outcome on the test item so fixtures can see whether it failed."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(request, page: Page):
    """After a failed UI test, attach a screenshot to the Allure report."""
    yield
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        allure.attach(page.screenshot(), name="Screenshot on failure", attachment_type=allure.attachment_type.PNG)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def inventory(page: Page, login_page: LoginPage) -> InventoryPage:
    """A logged-in session, sitting on the product list."""
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    return InventoryPage(page)
