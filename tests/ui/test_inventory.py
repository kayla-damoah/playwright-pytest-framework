import allure
import pytest
from playwright.sync_api import expect

pytestmark = [pytest.mark.ui, allure.feature("Inventory")]


@pytest.mark.smoke
def test_inventory_lists_six_products(inventory):
    expect(inventory.items).to_have_count(6)


def test_cart_badge_tracks_adds_and_removes(inventory):
    inventory.add_to_cart("sauce-labs-backpack")
    expect(inventory.cart_badge).to_have_text("1")
    inventory.add_to_cart("sauce-labs-bike-light")
    expect(inventory.cart_badge).to_have_text("2")
    inventory.remove_from_cart("sauce-labs-backpack")
    expect(inventory.cart_badge).to_have_text("1")


def test_sort_price_low_to_high(inventory):
    inventory.sort_by("lohi")
    prices = inventory.prices()
    assert prices == sorted(prices)


def test_sort_price_high_to_low(inventory):
    inventory.sort_by("hilo")
    prices = inventory.prices()
    assert prices == sorted(prices, reverse=True)
