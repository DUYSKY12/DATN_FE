import pytest
from selenium.webdriver.common.by import By

from pages.admin_orders_page import AdminOrdersPage
from pages.cart_page import CartPage
from pages.user_orders_page import UserOrdersPage


def inject_token(driver, base_url: str, token: str):
    if not token:
        pytest.skip("Missing TEST_USER_TOKEN. Set env to run authenticated tests.")
    driver.get(base_url)
    driver.execute_script("window.localStorage.setItem('token', arguments[0]);", token)


def test_cart_checkout_confirm_flow(driver, config):
    inject_token(driver, config.base_url, config.token)
    cart = CartPage(driver, config.base_url)
    cart.open_page()

    if not cart.has_items():
        pytest.skip("No cart items available for checkout flow test.")

    cart.select_first_item()
    cart.submit_checkout()
    assert cart.confirm_modal_visible(), "Confirm modal should appear before placing order."


def test_cart_validation_required_fields(driver, config):
    inject_token(driver, config.base_url, config.token)
    cart = CartPage(driver, config.base_url)
    cart.open_page()

    if not cart.has_items():
        pytest.skip("No cart items available for validation test.")

    cart.select_first_item()
    cart.clear_phone()
    cart.clear_address()
    cart.submit_checkout()
    assert cart.error_visible(), "Validation error text should be shown."


def test_user_orders_filter_and_detail(driver, config):
    inject_token(driver, config.base_url, config.token)
    page = UserOrdersPage(driver, config.base_url)
    page.open_page()

    if page.order_count() == 0:
        pytest.skip("No user order available to verify filter and detail.")

    page.click_filter_by_text("Chờ xác nhận")
    page.open_first_order()
    assert page.modal_visible(), "Order detail modal should be visible."


def test_admin_order_search_and_status_update(driver, config):
    if not config.admin_phone:
        pytest.skip("Missing TEST_ADMIN_PHONE for admin search test.")

    inject_token(driver, config.base_url, config.token)
    page = AdminOrdersPage(driver, config.base_url)
    page.open_page()
    page.search_phone(config.admin_phone)
    page.open_first_detail()

    status_selects = driver.find_elements(By.CSS_SELECTOR, "select.form-input")
    if not status_selects:
        pytest.skip("Status select not found. Admin role/data may be unavailable.")

    page.update_status_to("Đang xử lý")
