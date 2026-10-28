from __future__ import annotations

import allure
from playwright.sync_api import Page, expect

from framework.pages.cart_page import CartPage


class InventoryPage:
    """The product list shown after login."""

    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort = page.locator("[data-test=product-sort-container]")

    def _add_button(self, slug: str):
        return self.page.locator(f"[data-test=add-to-cart-{slug}]")

    def _remove_button(self, slug: str):
        return self.page.locator(f"[data-test=remove-{slug}]")

    @allure.step("Add {slug} to the cart")
    def add_to_cart(self, slug: str) -> None:
        self._add_button(slug).click()
        expect(self._remove_button(slug)).to_be_visible()  # the button flips once the page has updated

    @allure.step("Remove {slug} from the cart")
    def remove_from_cart(self, slug: str) -> None:
        self._remove_button(slug).click()
        expect(self._add_button(slug)).to_be_visible()

    @allure.step("Sort products by {value}")
    def sort_by(self, value: str) -> None:
        self.sort.select_option(value)

    def prices(self) -> list[float]:
        expect(self.items.first).to_be_visible()
        texts = self.page.locator(".inventory_item_price").all_inner_texts()
        return [float(t.replace("$", "")) for t in texts]

    @allure.step("Open the cart")
    def open_cart(self) -> CartPage:
        self.cart_link.click()
        expect(self.page).to_have_url("https://www.saucedemo.com/cart.html")
        return CartPage(self.page)
