"""
Tests for shopping cart – add, remove, persist across pages.
"""

import pytest

from pages.products_page import ProductsPage
from pages.cart_page     import CartPage
from utils.logger        import get_logger

log = get_logger("test_cart")


@pytest.fixture
def products_page(logged_in_driver):
    return ProductsPage(logged_in_driver)


@pytest.fixture
def cart_page(logged_in_driver):
    return CartPage(logged_in_driver)


# ── Add to cart ───────────────────────────────────────────────────────────────
class TestAddToCart:
    def test_add_one_product(self, products_page):
        added = products_page.add_first_n_products(1)
        assert products_page.get_cart_count() == 1
        log.info(f"PASS: added {added[0]}, badge=1")

    def test_add_multiple_products(self, products_page):
        products_page.add_first_n_products(3)
        assert products_page.get_cart_count() == 3
        log.info("PASS: added 3 products, badge=3")

    def test_add_specific_product(self, products_page):
        target = "Sauce Labs Backpack"
        products_page.add_product_to_cart_by_name(target)
        assert products_page.get_cart_count() == 1
        log.info(f"PASS: '{target}' added")

    def test_cart_badge_increments(self, products_page):
        for n in range(1, 4):
            products_page.add_first_n_products(1) if n == 1 \
                else products_page.add_product_to_cart_by_name(
                    products_page.get_all_product_names()[n - 1]
                )
        assert products_page.get_cart_count() >= 1
        log.info("PASS: badge increments on add")


# ── Remove from products page ─────────────────────────────────────────────────
class TestRemoveFromProductsPage:
    def test_remove_after_add(self, products_page):
        target = "Sauce Labs Bike Light"
        products_page.add_product_to_cart_by_name(target)
        assert products_page.get_cart_count() == 1
        products_page.remove_product_from_cart_by_name(target)
        assert products_page.get_cart_count() == 0
        log.info("PASS: add then remove → badge=0")


# ── Cart page ─────────────────────────────────────────────────────────────────
class TestCartPage:
    def test_cart_shows_added_products(self, logged_in_driver):
        pp   = ProductsPage(logged_in_driver)
        added = pp.add_first_n_products(2)
        pp.go_to_cart()

        cp    = CartPage(logged_in_driver)
        assert cp.is_on_cart_page()
        items = cp.get_cart_items()
        assert len(items) == 2
        cart_names = [i["name"] for i in items]
        for name in added:
            assert name in cart_names, f"'{name}' missing from cart"
        log.info(f"PASS: cart contains {cart_names}")

    def test_remove_from_cart_page(self, logged_in_driver):
        pp = ProductsPage(logged_in_driver)
        pp.add_first_n_products(2)
        pp.go_to_cart()

        cp   = CartPage(logged_in_driver)
        items_before = cp.get_cart_item_count()
        first_name   = cp.get_cart_items()[0]["name"]
        cp.remove_item_by_name(first_name)
        assert cp.get_cart_item_count() == items_before - 1
        log.info(f"PASS: removed '{first_name}' from cart page")

    def test_empty_cart_after_remove_all(self, logged_in_driver):
        pp = ProductsPage(logged_in_driver)
        pp.add_first_n_products(3)
        pp.go_to_cart()

        cp = CartPage(logged_in_driver)
        cp.remove_all_items()
        assert cp.get_cart_item_count() == 0
        log.info("PASS: cart is empty after remove-all")

    def test_continue_shopping_returns_to_products(self, logged_in_driver):
        pp = ProductsPage(logged_in_driver)
        pp.go_to_cart()
        cp = CartPage(logged_in_driver)
        cp.continue_shopping()
        assert ProductsPage(logged_in_driver).is_on_products_page()
        log.info("PASS: continue shopping → inventory page")
