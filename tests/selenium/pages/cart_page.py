from selenium.webdriver.common.by import By

from .base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = (By.CSS_SELECTOR, ".product-item")
    SELECTED_CHECKBOX = (By.CSS_SELECTOR, ".product-item input[type='checkbox']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, ".form-actions button[type='submit']")
    CONFIRM_MODAL = (By.CSS_SELECTOR, ".confirm-dialog")
    CONFIRM_PLACE_BUTTON = (By.CSS_SELECTOR, ".confirm-actions .btn-primary")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".total-price")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[type='tel']")
    ADDRESS_INPUT = (By.CSS_SELECTOR, "textarea")
    ERROR_TEXT = (By.CSS_SELECTOR, ".error-text")

    def open_page(self):
        self.open("/user/cart")

    def has_items(self) -> bool:
        return len(self.driver.find_elements(*self.CART_ITEM)) > 0

    def select_first_item(self):
        self.click(*self.SELECTED_CHECKBOX)

    def submit_checkout(self):
        self.click(*self.SUBMIT_BUTTON)

    def confirm_modal_visible(self) -> bool:
        return self.is_visible(*self.CONFIRM_MODAL)

    def confirm_place_order(self):
        self.click(*self.CONFIRM_PLACE_BUTTON)

    def clear_phone(self):
        self.type(*self.PHONE_INPUT, value="")

    def clear_address(self):
        self.type(*self.ADDRESS_INPUT, value="")

    def error_visible(self) -> bool:
        return len(self.driver.find_elements(*self.ERROR_TEXT)) > 0

    def total_price_text(self) -> str:
        return self.text(*self.TOTAL_PRICE)
