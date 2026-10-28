from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, 10)

    def open(self, path: str):
        self.driver.get(f"{self.base_url}{path}")

    def click(self, by: By, selector: str):
        self.wait.until(ec.element_to_be_clickable((by, selector))).click()

    def type(self, by: By, selector: str, value: str, clear: bool = True):
        elem = self.wait.until(ec.visibility_of_element_located((by, selector)))
        if clear:
            elem.clear()
        elem.send_keys(value)

    def text(self, by: By, selector: str) -> str:
        return self.wait.until(ec.visibility_of_element_located((by, selector))).text

    def is_visible(self, by: By, selector: str) -> bool:
        try:
            self.wait.until(ec.visibility_of_element_located((by, selector)))
            return True
        except Exception:
            return False
