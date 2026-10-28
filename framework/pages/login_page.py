from __future__ import annotations

import allure
from playwright.sync_api import Page


class LoginPage:
    """The login screen: where things are, and how to use them."""

    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("[data-test=username]")
        self.password = page.locator("[data-test=password]")
        self.submit = page.locator("[data-test=login-button]")
        self.error = page.locator("[data-test=error]")

    @allure.step("Open the login page")
    def open(self) -> "LoginPage":
        self.page.goto(self.URL)
        return self

    @allure.step("Log in as {user}")
    def login(self, user: str, password: str) -> None:
        self.username.fill(user)
        self.password.fill(password)
        self.submit.click()
