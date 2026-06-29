"""
End-to-End Tests – full user journey from login to order confirmation.
"""

from pages.login_page    import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page     import CartPage
from pages.checkout_page import (
    CheckoutStepOnePage, CheckoutStepTwoPage, OrderConfirmationPage
)
from config.config import VALID_USERNAME, VALID_PASSWORD
from utils.logger  import get_logger

log = get_logger("test_e2e")


class TestFullJourney:
    """Complete happy-path: Login → browse → sort → add → review cart → checkout → confirm."""

    def test_complete_purchase_flow(self, driver):
        log.info("=" * 60)
        log.info("E2E: FULL PURCHASE JOURNEY START")
        log.info("=" * 60)

        # 1. Login
        login = LoginPage(driver)
        login.open_login_page()
        login.login(VALID_USERNAME, VALID_PASSWORD)
        login.wait_for_url_contains("inventory")
        log.info("Step 1 ✓ Logged in")

        # 2. Sort products price low→high
        products = ProductsPage(driver)
        products.sort_products(ProductsPage.SORT_LOHI)
        prices = products.get_all_product_prices()
        assert prices == sorted(prices)
        log.info("Step 2 ✓ Products sorted low→high")

        # 3. Add two specific products
        products.add_product_to_cart_by_name("Sauce Labs Onesie")
        products.add_product_to_cart_by_name("Sauce Labs Backpack")
        assert products.get_cart_count() == 2
        log.info("Step 3 ✓ 2 items added to cart")

        # 4. View cart and verify items
        products.go_to_cart()
        cart  = CartPage(driver)
        items = cart.get_cart_items()
        assert len(items) == 2
        log.info(f"Step 4 ✓ Cart contains: {[i['name'] for i in items]}")

        # 5. Remove one item from cart
        cart.remove_item_by_name("Sauce Labs Backpack")
        assert cart.get_cart_item_count() == 1
        log.info("Step 5 ✓ Removed 1 item; cart has 1")

        # 6. Proceed to checkout step 1
        cart.proceed_to_checkout()
        step1 = CheckoutStepOnePage(driver)
        assert step1.is_on_step_one()
        step1.fill_info("Test", "User", "12345")
        step1.click_continue()
        log.info("Step 6 ✓ Checkout info filled")

        # 7. Review order on step 2
        step2   = CheckoutStepTwoPage(driver)
        assert step2.is_on_step_two()
        summary = step2.get_order_summary()
        assert len(summary["items"]) == 1
        expected_total = round(summary["subtotal"] + summary["tax"], 2)
        assert round(summary["total"], 2) == expected_total
        log.info(f"Step 7 ✓ Order review: total=${summary['total']}")

        # 8. Place order
        step2.click_finish()
        confirm = OrderConfirmationPage(driver)
        assert confirm.is_order_placed()
        assert "Thank you" in confirm.get_confirmation_header()
        log.info("Step 8 ✓ Order placed successfully!")

        # 9. Back to products
        confirm.back_to_products()
        assert products.is_on_products_page()
        log.info("Step 9 ✓ Returned to inventory")

        log.info("=" * 60)
        log.info("E2E: FULL PURCHASE JOURNEY PASSED ✓")
        log.info("=" * 60)

    def test_purchase_with_sort_and_multiple_items(self, driver):
        """E2E: Add 3 items sorted Z→A, checkout all."""
        login = LoginPage(driver)
        login.open_login_page()
        login.login(VALID_USERNAME, VALID_PASSWORD)
        login.wait_for_url_contains("inventory")

        products = ProductsPage(driver)
        products.sort_products(ProductsPage.SORT_ZA)
        added = products.add_first_n_products(3)
        assert products.get_cart_count() == 3

        products.go_to_cart()
        CartPage(driver).proceed_to_checkout()

        step1 = CheckoutStepOnePage(driver)
        step1.fill_info("Multi", "Item", "99001")
        step1.click_continue()

        step2 = CheckoutStepTwoPage(driver)
        assert len(step2.get_order_summary()["items"]) == 3
        step2.click_finish()

        confirm = OrderConfirmationPage(driver)
        assert confirm.is_order_placed()
        log.info(f"PASS: 3-item order confirmed. Items: {added}")
