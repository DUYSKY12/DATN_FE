from selenium.webdriver.common.by import By

from .base_page import BasePage


class UserOrdersPage(BasePage):
    ORDER_CARD = (By.CSS_SELECTOR, ".order-card")
    FILTER_BUTTONS = (By.CSS_SELECTOR, ".filter-btn")
    MODAL = (By.CSS_SELECTOR, ".modal-box")

    def open_page(self):
        self.open("/user/order")

    def order_count(self) -> int:
        return len(self.driver.find_elements(*self.ORDER_CARD))

    def click_filter_by_text(self, label: str):
        for btn in self.driver.find_elements(*self.FILTER_BUTTONS):
            if btn.text.strip() == label:
                btn.click()
                return
        raise AssertionError(f"Filter button not found: {label}")

    def open_first_order(self):
        cards = self.driver.find_elements(*self.ORDER_CARD)
        if not cards:
            raise AssertionError("No order card to open.")
        cards[0].click()

    def modal_visible(self) -> bool:
        return self.is_visible(*self.MODAL)
