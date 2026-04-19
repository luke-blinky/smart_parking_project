# IoT-based Smart Parking Management System (IoT-SPMS) - HCMUT

## 1. Giới thiệu dự án
Hệ thống Quản lý Bãi đỗ xe Thông minh (IoT-SPMS) được thiết kế dành riêng cho khuôn viên **Đại học Bách Khoa TP.HCM (HCMUT)**. Dự án tập trung vào việc tối ưu hóa luồng xe, hiển thị trạng thái bãi xe thời gian thực và tự động hóa thanh toán phí gửi xe cho sinh viên, cán bộ và khách vãng lai.

## 2. Kiến trúc hệ thống (Software Architecture)
Hệ thống được xây dựng theo mô hình **Layered Architecture** (Kiến trúc phân lớp) tinh gọn. Toàn bộ logic và giao diện được triển khai bằng **Python** để đảm bảo tính đồng bộ và tốc độ phát triển.

## 3. Giải thích các thành phần
app.py: Trung tâm điều hướng của ứng dụng. Sử dụng thư viện Streamlit để hiển thị Dashboard cho 4 vai trò: Sinh viên, Bảng điện tử (Signage), Nhân viên bãi xe và Quản trị viên.
services/: Folder chứa toàn bộ "não bộ" của hệ thống. Việc chia nhỏ thành 4 file .py giúp các thành viên trong nhóm có thể lập trình song song mà không gây xung đột code.

data_manager.py: Đảm bảo việc đọc và ghi dữ liệu vào file JSON diễn ra an toàn, tránh việc ghi đè dữ liệu sai lệch khi nhiều chức năng cùng hoạt động.

db.json: Lưu trữ toàn bộ thông tin về người dùng, trạng thái các vị trí đỗ xe (Parking Slots) và lịch sử giao dịch.
## 4. Hướng dẫn cài đặt và khởi chạy
Yêu cầu hệ thống: Đã cài đặt Python (phiên bản 3.8 trở lên).

Cài đặt thư viện Streamlit:

Bash
pip install streamlit
Khởi chạy ứng dụng:

Bash
streamlit run app.py
### Cấu trúc thư mục:
```text
SPMS/
├── app.py                # Giao diện chính (Hội tụ UI cho mọi vai trò người dùng)
├── data_manager.py       # Tầng truy xuất dữ liệu (Đọc/Ghi db.json)
├── data/
│   └── db.json           # Cơ sở dữ liệu giả lập (Mock Database dạng JSON)
└── services/             # Tầng nghiệp vụ (Business Logic) chia theo Task
    ├── __init__.py       # Khởi tạo package
    ├── auth_task.py      # Task 1: Xác thực thẻ ID & HCMUT_SSO (UC1)
    ├── parking_task.py   # Task 2: Điều hướng & Trạng thái bãi xe (UC2)
    ├── payment_task.py   # Task 3: Tính toán phí & Tích hợp BKPay (UC5)
    └── system_task.py    # Task 4: Xử lý ngoại lệ & Quản trị hệ thống (UC4, UC6)
