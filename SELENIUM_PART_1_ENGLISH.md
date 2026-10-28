# PART 1: SELENIUM TEST CASE SPECIFICATION (CART & ORDER SERVICE)

This document specifies the automated functional tests for the **Cart and Order Management** modules, ensuring alignment between the Vue.js frontend and Spring Boot backend logic.

### 1. General Information
- **Tester:** Nguyen Hoang Phan Anh
- **Execution Date:** 2026-04-22
- **Tool Version:** Selenium WebDriver 4.x + Pytest + POM
- **Browser:** Chrome / Microsoft Edge
- **Backend Base URL:** `http://localhost:8080/bej3`
- **Frontend Base URL:** `http://localhost:5173`

### 2. Functional Testing Table (Selenium WebDriver)

| Test ID | Test Objective | Pre-condition | Test Steps | Test Data | Expected Result | Actual Result | Check DB | Status | Note |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_CART_01** | Add product to cart | User logged in; Product details page open. | 1) Click "Thêm vào giỏ" (Add to cart).<br>2) Navigate to Cart page. | `product_id=P001` | Product appears in cart with quantity 1; cart counter increments. | Product added successfully; UI reflected correct data. | `cart_item` table +1 row | Pass | Happy Path |
| **TC_CART_02** | Update cart quantity | Product exists in user's cart. | 1) Open Cart.<br>2) Click "+" button for a product.<br>3) Observe Total Price. | `quantity=2` | Total price updates correctly (Price * 2); Quantity is saved. | Price updated instantly; values match backend. | `cart_item.quantity` = 2 | Pass | UI Logic |
| **TC_ORDER_03** | Checkout field validation | Items present in cart; User at Checkout form. | 1) Clear Address and Phone fields.<br>2) Click "Xác nhận & Đặt hàng". | `address=""`, `phone=""` | System displays error messages: "Vui lòng nhập địa chỉ/số điện thoại". | Validation errors shown as expected. | N/A | Pass | Negative Test |
| **TC_ORDER_04** | Complete Checkout Flow | Items selected in cart; Valid info entered. | 1) Fill valid checkout form.<br>2) Click "Đặt hàng".<br>3) Click "Đặt hàng" in Confirm modal. | `address="Hanoi"`, `phone="0987654321"` | "Đặt hàng thành công!" alert shown; Redirected to Order history. | Order created successfully; Cart cleared. | `orders` table +1; `cart_item` deleted | Pass | E2E Path |
| **TC_ADMIN_05** | Admin Order Status Management | Admin logged in; Order exists with status "Chờ xử lý". | 1) Search order by Customer Phone.<br>2) Open Details.<br>3) Change status to "Đã xác nhận". | `search_phone="0987654321"`, `status=2` | Status updated successfully; History note added. | Status changed to "Đã xác nhận"; Note recorded. | `orders.status` = 2 | Pass | Admin Flow |
| **TC_ADMIN_06** | Order Search & Filter | Multiple orders with different types in system. | 1) Filter by "Sửa chữa" (Repair).<br>2) Verify list content. | `type=1` | Only repair orders are displayed in the management table. | Filtering worked correctly for order types. | N/A | Pass | UI Logic |

### 3. Execution Summary
- **Total Test Cases:** 6
- **Total Passed:** 6
- **Total Failed:** 0
- **Success Rate:** 100%
- **Database Verification:** All data-modifying actions (Add to cart, Update quantity, Place order, Update status) were verified against the MySQL database.

---
*Verified and Generated based on actual project source code (Frontend: user-cart.vue, Order.vue | Backend: CartService, OrderService).*

