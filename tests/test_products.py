"""
Tests for product listing: sorting, filtering, and product data validation.
Data-driven: reads expected products from test_data/products.csv
"""

import pytest

from config.config import PRODUCTS_CSV
from pages.products_page import ProductsPage
from utils.data_reader   import read_csv
from utils.logger        import get_logger

log = get_logger("test_products")


@pytest.fixture
def products_page(logged_in_driver):
    return ProductsPage(logged_in_driver)


# ── Page basics ───────────────────────────────────────────────────────────────
class TestProductPage:
    def test_products_page_loads(self, products_page):
        assert products_page.is_on_products_page()
        assert products_page.get_page_title() == "Products"

    def test_product_count(self, products_page):
        count = products_page.get_product_count()
        assert count == 6, f"Expected 6 products, got {count}"
        log.info(f"Product count: {count}")


# ── Sorting ───────────────────────────────────────────────────────────────────
class TestProductSorting:
    def test_sort_name_az(self, products_page):
        products_page.sort_products(ProductsPage.SORT_AZ)
        names = products_page.get_all_product_names()
        assert names == sorted(names), "Products should be A→Z"
        log.info("PASS: A→Z sort")

    def test_sort_name_za(self, products_page):
        products_page.sort_products(ProductsPage.SORT_ZA)
        names = products_page.get_all_product_names()
        assert names == sorted(names, reverse=True), "Products should be Z→A"
        log.info("PASS: Z→A sort")

    def test_sort_price_low_to_high(self, products_page):
        products_page.sort_products(ProductsPage.SORT_LOHI)
        prices = products_page.get_all_product_prices()
        assert prices == sorted(prices), "Prices should be low→high"
        log.info(f"PASS: price low→high  {prices}")

    def test_sort_price_high_to_low(self, products_page):
        products_page.sort_products(ProductsPage.SORT_HILO)
        prices = products_page.get_all_product_prices()
        assert prices == sorted(prices, reverse=True), "Prices should be high→low"
        log.info(f"PASS: price high→low  {prices}")


# ── Data-driven product validation ───────────────────────────────────────────
def get_expected_products():
    rows = read_csv(PRODUCTS_CSV)
    if not rows:
        # Fallback defaults matching SauceDemo catalogue
        return [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Fleece Jacket",
            "Sauce Labs Onesie",
            "Test.allTheThings() T-Shirt (Red)",
        ]
    return [r["product_name"] for r in rows]


@pytest.mark.parametrize("expected_product", get_expected_products())
def test_product_in_catalogue(products_page, expected_product):
    """Every product in products.csv should appear on the page."""
    actual_names = [n.lower() for n in products_page.get_all_product_names()]
    assert expected_product.lower() in actual_names, \
        f"'{expected_product}' not found in catalogue"
    log.info(f"PASS: '{expected_product}' is in catalogue")
