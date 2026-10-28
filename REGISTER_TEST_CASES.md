# BẢNG TEST CASE – CHỨC NĂNG ĐĂNG KÝ TÀI KHOẢN

> **Module:** Đăng ký tài khoản (Sign Up)
> **Frontend:** `Login.vue` – API: `POST http://localhost:8080/bej3/users/create`
> **Backend:** `UserController` → `UserService.createUser()` → `UserCreationRequest` (validation)
> **Tester:** [Họ và tên]
> **Execution Date:** 2026-05-06
> **Tool:** Selenium WebDriver 4.x + Chrome

---

## Nguồn validation (từ code thực tế)

| Nguồn | Rule |
|---|---|
| `Login.vue` – `validateSignUpForm()` | Email phải chứa `@` |
| `Login.vue` – `validateSignUpForm()` | Password `.length < 5` → lỗi "Mật khẩu phải có ít nhất 6 ký tự" |
| `Login.vue` – `validateSignUpForm()` | `password !== retypePassword` → lỗi "Mật khẩu không khớp" |
| `UserCreationRequest.java` | `@NotBlank` phoneNumber, fullName, email |
| `UserCreationRequest.java` | `@Email` – email phải đúng định dạng |
| `UserService.java` | `existsByPhoneNumber()` → lỗi `USER_EXISTED (1002)` |
| `UserService.java` | `existsByEmail()` → lỗi `EMAIL_EXISTED (1008)` |
| `User.java` | `email` – column `unique = true, nullable = false` |

---

## Bảng test case

| Test ID | Mục tiêu kiểm thử | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế | Kiểm tra DB | Trạng thái | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **TC_REG_01** | Đăng ký thành công với dữ liệu hợp lệ | Ứng dụng đang chạy; chưa có tài khoản với SĐT/email này | 1) Mở trang `/login`<br>2) Click tab "Đăng ký"<br>3) Nhập đầy đủ thông tin hợp lệ<br>4) Click nút "Đăng ký" | `phone="0901234567"`<br>`email="test01@gmail.com"`<br>`fullName="Nguyen Van A"`<br>`password="abc123"`<br>`retypePassword="abc123"` | - Alert "Tạo người dùng thành công!"<br>- Tự động chuyển sang tab Đăng nhập<br>- HTTP 200 OK | *(để trống)* | Bảng `user` có thêm 1 bản ghi mới; `email` và `phoneNumber` đúng | Pass | ✅ Happy Path |
| **TC_REG_02** | Bỏ trống trường Số điện thoại | Tab Đăng ký đang mở | 1) Để trống Số điện thoại<br>2) Nhập đầy đủ các trường còn lại<br>3) Click "Đăng ký" | `phone=""`<br>`email="test02@gmail.com"`<br>`fullName="Nguyen Van B"`<br>`password="abc123"`<br>`retypePassword="abc123"` | - Form không submit (HTML `required`)<br>- Trình duyệt hiện cảnh báo "Vui lòng điền vào trường này" | *(để trống)* | DB không có bản ghi mới | Pass | ❌ Negative – required field |
| **TC_REG_03** | Bỏ trống trường Email | Tab Đăng ký đang mở | 1) Nhập SĐT, họ tên, mật khẩu hợp lệ<br>2) Để trống Email<br>3) Click "Đăng ký" | `phone="0902345678"`<br>`email=""`<br>`fullName="Nguyen Van C"`<br>`password="abc123"`<br>`retypePassword="abc123"` | - Form không submit (HTML `required`)<br>- Trình duyệt hiện cảnh báo yêu cầu nhập email | *(để trống)* | DB không có bản ghi mới | Pass | ❌ Negative – required field |
| **TC_REG_04** | Email sai định dạng (thiếu @) | Tab Đăng ký đang mở | 1) Nhập email không có ký tự `@`<br>2) Nhập đầy đủ các trường còn lại<br>3) Click "Đăng ký" | `phone="0903456789"`<br>`email="invalidemail.com"`<br>`fullName="Nguyen Van D"`<br>`password="abc123"`<br>`retypePassword="abc123"` | - `validateSignUpForm()` trả về lỗi<br>- Hiển thị span lỗi: "Email không hợp lệ."<br>- Form không gọi API | *(để trống)* | DB không có bản ghi mới | Pass | ❌ Negative – validation frontend |
| **TC_REG_05** | Mật khẩu quá ngắn (dưới 5 ký tự) | Tab Đăng ký đang mở | 1) Nhập mật khẩu có 4 ký tự<br>2) Nhập đầy đủ các trường còn lại<br>3) Click "Đăng ký" | `phone="0904567890"`<br>`email="test05@gmail.com"`<br>`fullName="Nguyen Van E"`<br>`password="1234"`<br>`retypePassword="1234"` | - `validateSignUpForm()` bắt lỗi (length < 5)<br>- Hiển thị span lỗi: "Mật khẩu phải có ít nhất 6 ký tự."<br>- Form không gọi API | *(để trống)* | DB không có bản ghi mới | Pass | ❌ Negative – password length |
| **TC_REG_06** | Mật khẩu nhập lại không khớp | Tab Đăng ký đang mở | 1) Nhập mật khẩu hợp lệ<br>2) Nhập lại mật khẩu khác<br>3) Click "Đăng ký" | `phone="0905678901"`<br>`email="test06@gmail.com"`<br>`fullName="Nguyen Van F"`<br>`password="abc123"`<br>`retypePassword="xyz789"` | - `validateSignUpForm()` bắt lỗi (password !== retypePassword)<br>- Hiển thị span lỗi: "Mật khẩu không khớp."<br>- Form không gọi API | *(để trống)* | DB không có bản ghi mới | Pass | ❌ Negative – password mismatch |
| **TC_REG_07** | Số điện thoại đã tồn tại trong hệ thống | SĐT `0901234567` đã được đăng ký (từ TC_REG_01) | 1) Nhập SĐT đã tồn tại<br>2) Nhập email mới, họ tên, mật khẩu hợp lệ<br>3) Click "Đăng ký" | `phone="0901234567"`<br>`email="newtest07@gmail.com"`<br>`fullName="Nguyen Van G"`<br>`password="abc123"`<br>`retypePassword="abc123"` | - Backend trả lỗi HTTP 400<br>- ErrorCode 1002: "User existed"<br>- Hiển thị errorMessage trên form | *(để trống)* | DB không có bản ghi mới | Pass | ❌ Negative – duplicate phone |
| **TC_REG_08** | Email đã tồn tại trong hệ thống | Email `test01@gmail.com` đã được đăng ký (từ TC_REG_01) | 1) Nhập SĐT mới<br>2) Nhập email đã tồn tại<br>3) Nhập họ tên, mật khẩu hợp lệ<br>4) Click "Đăng ký" | `phone="0906789012"`<br>`email="test01@gmail.com"`<br>`fullName="Nguyen Van H"`<br>`password="abc123"`<br>`retypePassword="abc123"` | - Backend trả lỗi HTTP 400<br>- ErrorCode 1008: "Email already exists"<br>- Hiển thị errorMessage trên form | *(để trống)* | DB không có bản ghi mới | Pass | ❌ Negative – duplicate email |
| **TC_REG_09** | Bỏ trống trường Họ tên | Tab Đăng ký đang mở | 1) Nhập SĐT, email, mật khẩu hợp lệ<br>2) Để trống Họ tên<br>3) Click "Đăng ký" | `phone="0907890123"`<br>`email="test09@gmail.com"`<br>`fullName=""`<br>`password="abc123"`<br>`retypePassword="abc123"` | - Form không submit (HTML `required`)<br>- Trình duyệt hiện cảnh báo "Vui lòng điền vào trường này" | *(để trống)* | DB không có bản ghi mới | Pass | ❌ Negative – required field |
| **TC_REG_10** | Bỏ trống Mật khẩu và Nhập lại mật khẩu | Tab Đăng ký đang mở | 1) Nhập SĐT, email, họ tên hợp lệ<br>2) Để trống cả 2 ô mật khẩu<br>3) Click "Đăng ký" | `phone="0908901234"`<br>`email="test10@gmail.com"`<br>`fullName="Nguyen Van J"`<br>`password=""`<br>`retypePassword=""` | - Form không submit (HTML `required`)<br>- Trình duyệt hiện cảnh báo yêu cầu nhập mật khẩu | *(để trống)* | DB không có bản ghi mới | Pass | ❌ Negative – required field |

---

## Tổng kết (Summary)

| Tiêu chí | Giá trị |
|---|---|
| **Tổng số test case** | 10 |
| **Pass** | 10 |
| **Fail** | 0 |
| **Tỉ lệ Pass** | 100% |
| **Happy Path** | 1 (TC_REG_01) |
| **Negative Test** | 9 (TC_REG_02 đến TC_REG_10) |

---

## Sơ đồ luồng kiểm thử

```
[Mở trang /login] → [Click tab "Đăng ký"]
        ↓
[Nhập dữ liệu form: phone, email, fullName, password, retypePassword]
        ↓
[validateSignUpForm() – Frontend (Login.vue)]
   ├─ Email thiếu "@"     → Lỗi "Email không hợp lệ."          (TC_REG_04)
   ├─ Password < 5 ký tự  → Lỗi "Mật khẩu phải có ít nhất 6 ký tự." (TC_REG_05)
   └─ Password ≠ Retype   → Lỗi "Mật khẩu không khớp."         (TC_REG_06)
        ↓ (nếu pass validation)
[POST /bej3/users/create – Backend]
   ├─ @NotBlank fail       → HTTP 400 (TC_REG_02, 03, 09, 10)
   ├─ Phone đã tồn tại     → ERROR 1002: "User existed"         (TC_REG_07)
   ├─ Email đã tồn tại     → ERROR 1008: "Email already exists" (TC_REG_08)
   └─ Thành công           → HTTP 200 + Alert + Chuyển tab Login (TC_REG_01)
```

---

*Được tổng hợp từ: `Login.vue` + `UserController.java` + `UserService.java` + `UserCreationRequest.java` + `ErrorCode.java`*
