from __future__ import annotations

import allure
from playwright.sync_api import Page, expect


class CartPage:
    """The cart and the checkout form; ends on the order confirmation."""

    def __init__(self, page: Page):
        self.page = page
        self.item_names = page.locator(".inventory_item_name")
        self.checkout_button = page.locator("[data-test=checkout]")
        self.first_name = page.locator("[data-test=firstName]")
        self.last_name = page.locator("[data-test=lastName]")
        self.postal_code = page.locator("[data-test=postalCode]")
        self.continue_button = page.locator("[data-test=continue]")
        self.finish_button = page.locator("[data-test=finish]")
        self.confirmation = page.locator("[data-test=complete-header]")

    @allure.step("Check out as {first} {last}")
    def checkout(self, first: str, last: str, postal_code: str) -> None:
        self.checkout_button.click()
        expect(self.first_name).to_be_visible()
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal_code)
        # Confirm the form kept what we typed before submitting it.
        expect(self.first_name).to_have_value(first)
        expect(self.last_name).to_have_value(last)
        expect(self.postal_code).to_have_value(postal_code)
        self.continue_button.click()
        expect(self.page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
        self.finish_button.click()
        expect(self.confirmation).to_be_visible()
