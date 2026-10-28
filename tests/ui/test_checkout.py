import allure
import pytest
from playwright.sync_api import expect

pytestmark = [pytest.mark.ui, allure.feature("Checkout")]


def test_cart_shows_the_item_that_was_added(inventory):
    inventory.add_to_cart("sauce-labs-backpack")
    cart = inventory.open_cart()
    expect(cart.item_names).to_have_text(["Sauce Labs Backpack"])


@pytest.mark.smoke
def test_end_to_end_checkout_shows_confirmation(inventory):
    inventory.add_to_cart("sauce-labs-bolt-t-shirt")
    cart = inventory.open_cart()
    cart.checkout("Test", "User", "07001")
    expect(cart.confirmation).to_contain_text("Thank you")
