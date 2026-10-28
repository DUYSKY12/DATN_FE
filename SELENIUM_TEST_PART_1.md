# PHẦN 1: KẾ HOẠCH VÀ KỊCH BẢN KIỂM THỨ TỰ ĐỘNG (SELENIUM)

## 1. Tổng quan hệ thống kiểm thử
Hệ thống kiểm thử tự động (Automation Testing) được xây dựng nhằm đảm bảo tính ổn định của luồng nghiệp vụ **Giỏ hàng (Cart)** và **Đơn hàng (Order)** trên cả hai phương diện:
- **Frontend (Giao diện người dùng):** Sử dụng Selenium WebDriver kết hợp với Python/Pytest và mô hình Page Object Model (POM) để kiểm thử các tương tác trực tiếp của người dùng trên trình duyệt.
- **Backend (Logic và Dữ liệu):** Sử dụng Selenium trong môi trường Spring Boot (Java) để thực hiện các bài kiểm tra tích hợp thông qua cơ chế thực thi Script trong trình duyệt, đảm bảo API hoạt động đúng trong môi trường runtime thực tế.

## 2. Môi trường kiểm thử (Test Environment)
- **Trình duyệt:** Google Chrome (hoặc Microsoft Edge).
- **Driver:** ChromeDriver tương thích với phiên bản trình duyệt.
- **Frameworks:**
  - Frontend Test: `pytest`, `selenium 4.x`.
  - Backend Test: `JUnit 5`, `Selenium WebDriver`, `WebDriverManager`.
- **Dữ liệu kiểm thử:** Được khởi tạo sẵn thông qua `CartOrderTestDataSeeder` ở backend để đảm bảo tính nhất quán.

## 3. Kịch bản kiểm thử chi tiết (Test Scenarios)

### 3.1. Nhóm kịch bản Giỏ hàng (Cart Scenarios)
| Mã TC | Tên Test Case | Mô tả | Kết quả mong đợi | Check DB |
|-------|---------------|-------|------------------|----------|
| TC-C01 | Thêm sản phẩm vào giỏ | Người dùng nhấn "Thêm vào giỏ" từ trang sản phẩm. | Sản phẩm xuất hiện trong giỏ hàng, số lượng tăng lên 1. | `cart_item` +1 dòng |
| TC-C02 | Cập nhật số lượng | Thay đổi số lượng (tăng/giảm) trong trang giỏ hàng. | Thành tiền thay đổi tương ứng, dữ liệu được cập nhật xuống DB. | `cart_item.quantity` cập nhật |
| TC-C03 | Xóa sản phẩm | Nhấn biểu tượng thùng rác để xóa item khỏi giỏ. | Item biến mất khỏi giao diện và database. | `cart_item` -1 dòng |

### 3.2. Nhóm kịch bản Đơn hàng (Order Scenarios)
| Mã TC | Tên Test Case | Mô tả | Kết quả mong đợi | Check DB |
|-------|---------------|-------|------------------|----------|
| TC-O01 | Validate thông tin thanh toán | Để trống Địa chỉ/SĐT khi nhấn "Xác nhận & Đặt hàng". | Hiển thị lỗi "Vui lòng nhập..." tại các trường tương ứng. | N/A |
| TC-O02 | Quy trình đặt hàng (Happy Path) | Chọn sản phẩm -> Nhập thông tin -> Xác nhận modal. | Đơn hàng được tạo thành công, giỏ hàng được làm trống. | `orders` +1, `cart_item` xóa |
| TC-O03 | Quản lý đơn hàng (Admin) | Admin tìm kiếm theo SĐT và cập nhật trạng thái đơn. | Trạng thái được cập nhật thành công (ví dụ: sang "Đã xác nhận"). | `orders.status` cập nhật |
| TC-O04 | Lọc đơn hàng theo loại | Admin lọc danh sách theo loại "Sửa chữa" hoặc "Mua bán". | Danh sách chỉ hiển thị các đơn hàng có loại tương ứng. | N/A |


## 4. Cấu trúc mã nguồn Selenium (POM - Page Object Model)
Việc triển khai được tổ chức theo cấu trúc chuyên nghiệp để dễ bảo trì:

### 4.1. Cấu trúc phía Frontend (Python)
- `pages/base_page.py`: Chứa các phương thức tương tác cơ bản (click, type, wait).
- `pages/cart_page.py`: Định nghĩa các locator (ID, CSS Selector) cho trang giỏ hàng.
- `pages/user_orders_page.py`: Xử lý các thao tác trên danh sách đơn hàng của User.
- `pages/admin_orders_page.py`: Xử lý giao diện quản lý đơn hàng của Admin.

### 4.2. Cấu trúc phía Backend (Java)
- `CartOrderSeleniumTest.java`: Thực thi các kịch bản kiểm thử tích hợp.
- `CartOrderTestDataSeeder.java`: Tự động reset và chuẩn bị dữ liệu mẫu (Database Rollback/Reset).

## 5. Hướng dẫn thực thi (Execution Guide)

### Bước 1: Chạy Backend & Frontend
Đảm bảo Backend (Port 8080) và Frontend (Port 5173) đang hoạt động.

### Bước 2: Thực thi kiểm thử Frontend
```bash
cd tests/selenium
pip install -r requirements.txt
pytest -v
```

### Bước 3: Thực thi kiểm thử Backend
```bash
cd D:\Documentation\DATN_BE-main\DATN_BE-main
.\mvnw.cmd "-Dtest=CartOrderSeleniumTest" test
```

---
*Ghi chú: Tài liệu được tổng hợp dựa trên mã nguồn thực tế của dự án.*
