# Cart/Order Frontend + Backend Report

## 1. Scope
- Module: Shopping Cart Management and Order Processing
- Frontend fixes:
  - `src/views/Product/user-cart.vue`
  - `src/views/User/UserOrders.vue`
  - `src/views/Booking/BookingRepair.vue`
  - `src/views/Product/Order.vue`
- Backend fixes:
  - `D:\Documentation\DATN_BE-main\DATN_BE-main\src\main\java\com\DATN\Bej\service\guest\CartService.java`
  - `D:\Documentation\DATN_BE-main\DATN_BE-main\src\main\java\com\DATN\Bej\controller\cart\OrdersManageController.java`
- Automation:
  - `tests/selenium/test_cart_order_flow.py`
  - `tests/selenium/pages/*.py`

## 2. Fixed Issues
- `user-cart.vue`
  - Fixed undefined router usage.
  - Fixed invalid field mapping in validation (`phoneNumber`, `address`).
  - Removed double submit flow (`@submit` + `@click`) and kept confirm-first flow.
  - Fixed selected count to use `cartItems`.
  - Fixed confirm action to call place-order API.
- `UserOrders.vue`
  - Fixed filter logic by mapping button labels to numeric statuses.
  - Fixed modal order-type display to use `selectedOrder.type`.
  - Removed duplicate mounted fetch and redundant imports.
- `BookingRepair.vue`
  - Added router initialization to prevent runtime crash.
  - Fixed error-description min length validation mismatch (17 chars).
  - Normalized user profile prefill to avoid overwriting form with unrelated fields.
- `Order.vue`
  - Fixed search binding (`keyWord` -> `searchQuery`).
  - Switched table rendering to `filteredOrders`.
  - Fixed computed filtering to use `orders.value` and safe matching.
  - Fixed new-order item removal (`newOrderForm.items`).
  - Fixed reactive object usage (`formData` without `.value`).
  - Added `newDescription` to reactive form state.

## 3. Selenium WebDriver 4.x + Pytest Suite
- Framework: Page Object Model
- Files:
  - `tests/selenium/conftest.py`
  - `tests/selenium/pages/base_page.py`
  - `tests/selenium/pages/cart_page.py`
  - `tests/selenium/pages/user_orders_page.py`
  - `tests/selenium/pages/admin_orders_page.py`
  - `tests/selenium/test_cart_order_flow.py`
  - `tests/selenium/pytest.ini`
  - `tests/selenium/requirements.txt`

## 4. Implemented Test Cases
- TC01: Checkout opens confirm modal before placing order.
- TC02: Checkout required-field validation for phone/address.
- TC03: User orders filter and detail modal behavior.
- TC04: Admin order search by phone and status update flow.

## 5. Backend Fixes and Tests
- Implemented backend fixes:
  - Corrected order total price in `placeOrder` to `sum(price * quantity)`.
  - Added ownership/type validation in `confirmRepairOrder`.
  - Persisted repair confirmation change with `ordersRepository.save(...)`.
  - Restricted `/manage/orders/{orderId}/items` with `ROLE_ADMIN`.
- Added backend test coverage:
  - `CartServiceTest`:
    - `placeOrder_Success_TotalPriceUsesQuantity`
    - `confirmRepairOrder_Success_SaveAndAddNote`
    - `confirmRepairOrder_Fail_NotOwner`
    - `confirmRepairOrder_Fail_InvalidOrderType`
  - `CartOrderApiIntegrationTest`:
    - `tcApi14_customerCannotUpdateAdminOrderItems`

## 6. Run Instructions
```bash
cd tests/selenium
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set TEST_BASE_URL=http://localhost:5173
set TEST_USER_TOKEN=your_jwt_token
set TEST_ADMIN_PHONE=0900000000
pytest -q
```

Optional env vars:
- `TEST_BROWSER=chrome|edge` (default: chrome)
- `TEST_HEADLESS=1` for headless mode
- `TEST_IMPLICIT_WAIT=5`

Backend verification commands:
```bash
cd D:\Documentation\DATN_BE-main\DATN_BE-main
.\mvnw.cmd "-Dtest=CartServiceTest,CartOrderApiIntegrationTest" test
```

## 7. Execution Results
- Frontend Selenium:
  - Dependency install: Passed (`pip install -r tests/selenium/requirements.txt`)
  - Test discovery: Passed (`4 tests collected`)
  - Full browser run: Requires running FE/BE services and valid JWT data.
- Backend Maven tests:
  - Command: `.\mvnw.cmd "-Dtest=CartServiceTest,CartOrderApiIntegrationTest" test`
  - Result: `BUILD SUCCESS`
  - Summary: `Tests run: 29, Failures: 0, Errors: 0, Skipped: 0`

## 8. Notes
- Selenium full execution still depends on running frontend/backend and valid runtime test accounts/tokens.
- Test cases use skip guards when required data/token is missing to keep suite stable in CI/local runs.
