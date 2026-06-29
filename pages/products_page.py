"""
ProductsPage – the main inventory listing at /inventory.html
Covers: search-like filtering, sort, add-to-cart, remove.
Note: SauceDemo has no search box – we filter by name in Python (realistic pattern).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger("products_page")


class ProductsPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    PAGE_TITLE       = (By.CLASS_NAME, "title")
    SORT_DROPDOWN    = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_ITEMS    = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME     = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE    = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BTN  = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    REMOVE_BTN       = (By.CSS_SELECTOR, "button[data-test^='remove']")
    CART_BADGE       = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON        = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU      = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK      = (By.ID, "logout_sidebar_link")

    # ── Sort options (value attribute of <option>) ─────────────────────────────
    SORT_AZ    = "az"
    SORT_ZA    = "za"
    SORT_LOHI  = "lohi"
    SORT_HILO  = "hilo"

    # ── Page verifications ────────────────────────────────────────────────────
    def is_on_products_page(self) -> bool:
        return "inventory" in self.current_url

    def get_page_title(self) -> str:
        return self.get_text(*self.PAGE_TITLE)

    # ── Sort ─────────────────────────────────────────────────────────────────
    def sort_products(self, option: str = SORT_AZ):
        """Sort by one of: az, za, lohi, hilo"""
        log.info(f"Sorting products by: {option}")
        dropdown = Select(self.find(*self.SORT_DROPDOWN))
        dropdown.select_by_value(option)

    def get_current_sort(self) -> str:
        dropdown = Select(self.find(*self.SORT_DROPDOWN))
        return dropdown.first_selected_option.get_attribute("value")

    # ── Product list helpers ──────────────────────────────────────────────────
    def get_all_product_names(self) -> list:
        names = self.find_all(*self.PRODUCT_NAME)
        return [n.text.strip() for n in names]

    def get_all_product_prices(self) -> list:
        prices = self.find_all(*self.PRODUCT_PRICE)
        return [float(p.text.replace("$", "")) for p in prices]

    def get_product_count(self) -> int:
        return len(self.find_all(*self.PRODUCT_ITEMS))

    # ── Add / Remove ──────────────────────────────────────────────────────────
    def add_product_to_cart_by_name(self, product_name: str):
        """Find product card by name and click its Add to cart button."""
        log.info(f"Adding to cart: {product_name}")
        items = self.find_all(*self.PRODUCT_ITEMS)
        for item in items:
            name_el = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_el.text.strip().lower() == product_name.lower():
                btn = item.find_element(By.CSS_SELECTOR, "button")
                self.scroll_to(btn)
                btn.click()
                log.info(f"Added '{product_name}' to cart")
                return
        raise ValueError(f"Product not found: {product_name}")

    def add_first_n_products(self, n: int = 1):
        """Add the first n products to the cart."""
        add_buttons = self.find_all(*self.ADD_TO_CART_BTN)
        added = []
        for btn in add_buttons[:n]:
            item  = btn.find_element(By.XPATH, "./ancestor::div[@class='inventory_item']")
            name  = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            self.scroll_to(btn)
            btn.click()
            added.append(name)
            log.info(f"Added to cart: {name}")
        return added

    def remove_product_from_cart_by_name(self, product_name: str):
        log.info(f"Removing from cart: {product_name}")
        items = self.find_all(*self.PRODUCT_ITEMS)
        for item in items:
            name_el = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_el.text.strip().lower() == product_name.lower():
                btn = item.find_element(By.CSS_SELECTOR, "button")
                self.scroll_to(btn)
                btn.click()
                return
        raise ValueError(f"Product not found: {product_name}")

    # ── Cart badge ────────────────────────────────────────────────────────────
    def get_cart_count(self) -> int:
        try:
            badge = self.find(*self.CART_BADGE)
            return int(badge.text)
        except Exception:
            return 0

    def go_to_cart(self):
        log.info("Navigating to cart")
        self.click(*self.CART_ICON)

    # ── Logout ────────────────────────────────────────────────────────────────
    def logout(self):
        log.info("Logging out")
        self.click(*self.BURGER_MENU)
        self.click(*self.LOGOUT_LINK)
