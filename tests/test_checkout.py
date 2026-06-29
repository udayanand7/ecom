"""
Tests for the full checkout flow:
  products → cart → step 1 (info) → step 2 (review) → confirmation
Data-driven: reads checkout data from test_data/checkout_data.xlsx
"""

import pytest

from config.config import CHECKOUT_EXCEL
from pages.products_page import ProductsPage
from pages.cart_page     import CartPage
from pages.checkout_page import (
    CheckoutStepOnePage, CheckoutStepTwoPage, OrderConfirmationPage
)
from utils.data_reader import read_excel
from utils.logger      import get_logger

log = get_logger("test_checkout")


# ── Shared fixture: add items and open cart ───────────────────────────────────
@pytest.fixture
def checkout_ready(logged_in_driver):
    """Add 2 products and navigate to cart."""
    pp = ProductsPage(logged_in_driver)
    pp.add_first_n_products(2)
    pp.go_to_cart()
    CartPage(logged_in_driver).proceed_to_checkout()
    yield logged_in_driver


# ── Step 1 ────────────────────────────────────────────────────────────────────
class TestCheckoutStepOne:
    def test_step_one_page_loads(self, checkout_ready):
        step1 = CheckoutStepOnePage(checkout_ready)
        assert step1.is_on_step_one(), "Should be on checkout step 1"

    def test_fill_valid_info(self, checkout_ready):
        step1 = CheckoutStepOnePage(checkout_ready)
        step1.fill_info("John", "Doe", "12345")
        step1.click_continue()
        step2 = CheckoutStepTwoPage(checkout_ready)
        assert step2.is_on_step_two(), "Should advance to step 2"
        log.info("PASS: valid info → step 2")

    def test_missing_first_name(self, checkout_ready):
        step1 = CheckoutStepOnePage(checkout_ready)
        step1.fill_info("", "Doe", "12345")
        step1.click_continue()
        assert step1.is_error_shown()
        assert "First Name is required" in step1.get_error()

    def test_missing_last_name(self, checkout_ready):
        step1 = CheckoutStepOnePage(checkout_ready)
        step1.fill_info("John", "", "12345")
        step1.click_continue()
        assert step1.is_error_shown()

    def test_missing_postal_code(self, checkout_ready):
        step1 = CheckoutStepOnePage(checkout_ready)
        step1.fill_info("John", "Doe", "")
        step1.click_continue()
        assert step1.is_error_shown()

    def test_cancel_returns_to_cart(self, checkout_ready):
        step1 = CheckoutStepOnePage(checkout_ready)
        step1.click_cancel()
        assert CartPage(checkout_ready).is_on_cart_page()
        log.info("PASS: cancel → cart page")


# ── Step 2 (review) ───────────────────────────────────────────────────────────
class TestCheckoutStepTwo:
    @pytest.fixture
    def on_step_two(self, checkout_ready):
        step1 = CheckoutStepOnePage(checkout_ready)
        step1.fill_info("Jane", "Smith", "54321")
        step1.click_continue()
        return checkout_ready

    def test_order_summary_displayed(self, on_step_two):
        step2   = CheckoutStepTwoPage(on_step_two)
        summary = step2.get_order_summary()
        assert len(summary["items"]) == 2, "2 items should be in review"
        assert summary["subtotal"] > 0
        assert summary["total"] > summary["subtotal"]
        log.info(f"PASS: summary {summary}")

    def test_total_equals_subtotal_plus_tax(self, on_step_two):
        step2   = CheckoutStepTwoPage(on_step_two)
        summary = step2.get_order_summary()
        expected = round(summary["subtotal"] + summary["tax"], 2)
        assert round(summary["total"], 2) == expected, \
            f"Total mismatch: {summary['total']} ≠ {expected}"
        log.info("PASS: total = subtotal + tax")

    def test_cancel_from_step_two(self, on_step_two):
        CheckoutStepTwoPage(on_step_two).click_cancel()
        assert ProductsPage(on_step_two).is_on_products_page()
        log.info("PASS: cancel from step 2 → inventory")


# ── Order confirmation ────────────────────────────────────────────────────────
class TestOrderConfirmation:
    @pytest.fixture
    def place_order(self, checkout_ready):
        step1 = CheckoutStepOnePage(checkout_ready)
        step1.fill_info("Alice", "Wonder", "99999")
        step1.click_continue()
        CheckoutStepTwoPage(checkout_ready).click_finish()
        return checkout_ready

    def test_confirmation_page_shown(self, place_order):
        confirm = OrderConfirmationPage(place_order)
        assert confirm.is_order_placed(), "Should be on confirmation page"
        log.info("PASS: order placed → confirmation page")

    def test_confirmation_message(self, place_order):
        confirm = OrderConfirmationPage(place_order)
        header  = confirm.get_confirmation_header()
        assert "Thank you" in header, f"Unexpected header: '{header}'"
        log.info(f"PASS: confirmation header = '{header}'")

    def test_back_to_products_after_order(self, place_order):
        confirm = OrderConfirmationPage(place_order)
        confirm.back_to_products()
        assert ProductsPage(place_order).is_on_products_page()
        log.info("PASS: back to products after order")


# ── Data-driven checkout ──────────────────────────────────────────────────────
def get_checkout_data():
    rows = read_excel(CHECKOUT_EXCEL)
    if not rows:
        return [
            ("Bob",   "Builder", "10001", True),
            ("",      "Smith",   "10002", False),
            ("Carol", "",        "10003", False),
            ("Dave",  "Jones",   "",      False),
        ]
    return [
        (r["first_name"], r["last_name"], r["zip_code"],
         str(r["should_pass"]).lower() == "true")
        for r in rows
    ]


@pytest.mark.parametrize("first,last,zip_code,should_pass", get_checkout_data())
def test_checkout_data_driven(logged_in_driver, first, last, zip_code, should_pass):
    """Data-driven checkout form validation from checkout_data.xlsx."""
    pp = ProductsPage(logged_in_driver)
    pp.add_first_n_products(1)
    pp.go_to_cart()
    CartPage(logged_in_driver).proceed_to_checkout()

    step1 = CheckoutStepOnePage(logged_in_driver)
    step1.fill_info(first, last, zip_code)
    step1.click_continue()

    if should_pass:
        assert CheckoutStepTwoPage(logged_in_driver).is_on_step_two()
        log.info(f"PASS: {first} {last} {zip_code} → step 2")
    else:
        assert step1.is_error_shown()
        log.info(f"PASS: invalid data correctly rejected")
