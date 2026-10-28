from selenium.webdriver.common.by import By

from .base_page import BasePage


class AdminOrdersPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, ".search-input")
    DETAIL_BUTTON = (By.CSS_SELECTOR, ".btn-detail")
    STATUS_SELECT = (By.CSS_SELECTOR, "select.form-input")
    SAVE_BUTTON = (By.CSS_SELECTOR, ".btn-save")

    def open_page(self):
        self.open("/admin/order")

    def search_phone(self, phone: str):
        self.type(*self.SEARCH_INPUT, value=phone)
        self.driver.find_element(*self.SEARCH_INPUT).submit()

    def open_first_detail(self):
        buttons = self.driver.find_elements(*self.DETAIL_BUTTON)
        if not buttons:
            raise AssertionError("No detail button found.")
        buttons[0].click()

    def update_status_to(self, visible_text: str):
        options = self.driver.find_elements(By.CSS_SELECTOR, "select.form-input option")
        target = None
        for opt in options:
            if opt.text.strip() == visible_text:
                target = opt
                break
        if target is None:
            raise AssertionError(f"Status option not found: {visible_text}")
        target.click()
        self.click(*self.SAVE_BUTTON)
