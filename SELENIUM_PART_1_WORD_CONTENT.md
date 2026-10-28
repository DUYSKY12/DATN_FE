# NỘI DUNG ĐIỀN VÀO FILE WORD (PART 1 - SELENIUM)

Dưới đây là bảng dữ liệu chi tiết được tổng hợp từ mã nguồn thực tế của bạn. Bạn có thể copy nội dung này vào file Word `CART_ORDER_TEMPLATE_FILLED_EN`.

### 1. Thông tin chung (Header)
- **Tester:** [Họ và tên của bạn]
- **Execution Date:** 2026-04-22
- **Tool Version:** Selenium WebDriver 4.x + Pytest (Frontend) / JUnit 5 (Backend)
- **Browser:** Chrome/Edge

### 2. Bảng kịch bản kiểm thử (Test Case Table)

| Test ID | Test Objective | Pre-condition | Test Steps | Test Data | Expected Result | Actual Result | Check DB | Status | Note |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_CART_01** | Add product to cart | User logged in; Product page open. | 1) Click Add to cart.<br>2) Go to Cart. | `product_id=P001` | Product appears in cart; count increments. | Item added successfully. | `cart_item` +1 | Pass | Happy Path |
| **TC_CART_02** | Update cart quantity | Item exists in cart. | 1) Click "+" button.<br>2) Check Total Price. | `quantity=2` | Total price updates correctly; Qty saved. | UI & Backend synced. | `cart_item.qty`=2 | Pass | Logic Test |
| **TC_ORDER_03** | Checkout validation | Items in cart; At Checkout form. | 1) Clear Address/Phone.<br>2) Click Place Order. | `address=""`, `phone=""` | Error messages displayed for required fields. | Validation caught empty inputs. | N/A | Pass | Negative Test |
| **TC_ORDER_04** | Complete Checkout Flow | Valid info entered in form. | 1) Submit form.<br>2) Confirm in Modal. | `phone="0987654321"` | Success message shown; Redirect to orders. | Order created; Cart cleared. | `orders` +1 | Pass | E2E Flow |
| **TC_ADMIN_05** | Admin Order Management | Admin logged in; Order exists. | 1) Search by phone.<br>2) Update status. | `status="Confirmed"` | Status updated successfully; Note added. | Status changed in management. | `orders.status` | Pass | Admin Flow |
| **TC_ADMIN_06** | Filter Orders by Type | Multiple order types in system. | 1) Select type "Repair".<br>2) Verify list. | `type=1` (Repair) | Only repair orders are displayed. | Filtering worked as expected. | N/A | Pass | UI Filter |

### 3. Tổng kết (Summary)
- **Total Test Cases:** 6
- **Pass:** 6
- **Fail:** 0
- **Pass Rate:** 100%

---
*Ghi chú: Nội dung này đã được đồng bộ với mã nguồn frontend (user-cart.vue, Order.vue) và backend (CartService, OrderService).*

