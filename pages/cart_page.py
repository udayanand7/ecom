"""
CartPage – /cart.html
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger("cart_page")


class CartPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    CART_ITEMS       = (By.CLASS_NAME, "cart_item")
    ITEM_NAME        = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE       = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QTY         = (By.CLASS_NAME, "cart_quantity")
    REMOVE_BUTTONS   = (By.CSS_SELECTOR, "button[data-test^='remove']")
    CONTINUE_SHOPPING= (By.ID, "continue-shopping")
    CHECKOUT_BUTTON  = (By.ID, "checkout")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def is_on_cart_page(self) -> bool:
        return "cart" in self.current_url

    def get_cart_items(self) -> list:
        items = self.find_all(*self.CART_ITEMS)
        result = []
        for item in items:
            name  = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
            qty   = item.find_element(By.CLASS_NAME, "cart_quantity").text
            result.append({"name": name, "price": price, "qty": qty})
        return result

    def get_cart_item_count(self) -> int:
        return len(self.find_all(*self.CART_ITEMS))

    def remove_item_by_name(self, product_name: str):
        log.info(f"Removing from cart: {product_name}")
        items = self.find_all(*self.CART_ITEMS)
        for item in items:
            name_el = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_el.text.strip().lower() == product_name.lower():
                remove_btn = item.find_element(By.CSS_SELECTOR, "button")
                remove_btn.click()
                log.info(f"Removed: {product_name}")
                return
        raise ValueError(f"Product not in cart: {product_name}")

    def remove_all_items(self):
        log.info("Removing all items from cart")
        while True:
            btns = self.find_all(*self.REMOVE_BUTTONS)
            if not btns:
                break
            btns[0].click()

    def continue_shopping(self):
        log.info("Clicking 'Continue Shopping'")
        self.click(*self.CONTINUE_SHOPPING)

    def proceed_to_checkout(self):
        log.info("Clicking 'Checkout'")
        self.click(*self.CHECKOUT_BUTTON)
