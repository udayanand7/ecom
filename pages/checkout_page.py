"""
CheckoutPage – covers both checkout steps and order confirmation.

Step 1  /checkout-step-one.html   → fill personal info
Step 2  /checkout-step-two.html   → review order
Confirm /checkout-complete.html   → order placed
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger("checkout_page")


class CheckoutStepOnePage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    FIRST_NAME   = (By.ID, "first-name")
    LAST_NAME    = (By.ID, "last-name")
    POSTAL_CODE  = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    CANCEL_BTN   = (By.ID, "cancel")
    ERROR_MSG    = (By.CSS_SELECTOR, "[data-test='error']")

    def is_on_step_one(self) -> bool:
        return "checkout-step-one" in self.current_url

    def fill_info(self, first: str, last: str, zip_code: str):
        log.info(f"Filling checkout info: {first} {last}, {zip_code}")
        self.type(*self.FIRST_NAME, first)
        self.type(*self.LAST_NAME, last)
        self.type(*self.POSTAL_CODE, zip_code)

    def click_continue(self):
        log.info("Clicking Continue")
        self.click(*self.CONTINUE_BTN)

    def click_cancel(self):
        log.info("Clicking Cancel")
        self.click(*self.CANCEL_BTN)

    def get_error(self) -> str:
        return self.get_text(*self.ERROR_MSG)

    def is_error_shown(self) -> bool:
        return self.is_displayed(*self.ERROR_MSG)


class CheckoutStepTwoPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    ORDER_ITEMS    = (By.CLASS_NAME, "cart_item")
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL      = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL    = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN     = (By.ID, "finish")
    CANCEL_BTN     = (By.ID, "cancel")

    def is_on_step_two(self) -> bool:
        return "checkout-step-two" in self.current_url

    def get_subtotal(self) -> float:
        text = self.get_text(*self.SUBTOTAL_LABEL)
        return float(text.split("$")[-1])

    def get_tax(self) -> float:
        text = self.get_text(*self.TAX_LABEL)
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        text = self.get_text(*self.TOTAL_LABEL)
        return float(text.split("$")[-1])

    def get_order_summary(self) -> dict:
        items = []
        for item in self.find_all(*self.ORDER_ITEMS):
            name  = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
            items.append({"name": name, "price": price})

        return {
            "items":    items,
            "subtotal": self.get_subtotal(),
            "tax":      self.get_tax(),
            "total":    self.get_total(),
        }

    def click_finish(self):
        log.info("Placing order (Finish)")
        self.click(*self.FINISH_BTN)

    def click_cancel(self):
        log.info("Cancelling order")
        self.click(*self.CANCEL_BTN)


class OrderConfirmationPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")
    CONFIRMATION_TEXT   = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BTN       = (By.ID, "back-to-products")

    def is_order_placed(self) -> bool:
        return "checkout-complete" in self.current_url

    def get_confirmation_header(self) -> str:
        return self.get_text(*self.CONFIRMATION_HEADER)

    def get_confirmation_text(self) -> str:
        return self.get_text(*self.CONFIRMATION_TEXT)

    def back_to_products(self):
        log.info("Back to products")
        self.click(*self.BACK_HOME_BTN)
