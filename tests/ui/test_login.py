import allure
import pytest
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.ui, allure.feature("Login")]


@pytest.mark.smoke
def test_valid_login_reaches_inventory(page: Page, login_page):
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


@pytest.mark.parametrize(
    "user,password,message",
    [
        ("locked_out_user", "secret_sauce", "locked out"),
        ("standard_user", "wrong", "do not match"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
)
def test_invalid_login_shows_error(login_page, user, password, message):
    login_page.login(user, password)
    expect(login_page.error).to_contain_text(message)


def test_logged_out_user_cannot_open_inventory(page: Page):
    page.goto("https://www.saucedemo.com/inventory.html")
    expect(page).to_have_url("https://www.saucedemo.com/")
