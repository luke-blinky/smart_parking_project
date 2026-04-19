import streamlit as st
# Import các logic từ folder services đã chia task
from services.auth_task import verify_card
from services.parking_task import get_zone_status
from services.payment_task import calculate_parking_fee
from services.system_task import log_incident

# --- CẤU HÌNH GIAO DIỆN CHUNG ---
st.set_page_config(page_title="HCMUT IoT-SPMS", layout="wide")

# --- ĐIỀU HƯỚNG (SIDEBAR) ---
st.sidebar.image("https://hcmut.edu.vn/logo.png", width=100) # Logo BK
st.sidebar.title("Hệ thống SPMS")
role = st.sidebar.radio("Chọn vai trò:", ["Người học", "Bảng điện tử", "Nhân viên bãi xe", "Quản trị viên"])

# --- TASK 1: DASHBOARD NGƯỜI HỌC (STUDENT) ---
def student_dashboard():
    st.title("Chào mừng Vo Trung Thanh") # Ví dụ tên user [cite: 138]
    # Code UI cho student ở đây...

# --- TASK 2: BẢNG ĐIỆN TỬ (SIGNAGE - UC2) ---
def signage_dashboard():
    st.title("Thông tin bãi xe thời gian thực")
    # Code UI hiển thị Xanh/Vàng/Đỏ ở đây... [cite: 19, 44]

# --- TASK 3: NHÂN VIÊN (ATTENDANT - UC3) ---
def attendant_dashboard():
    st.title("Hệ thống kiểm soát cổng")
    # Code UI quét thẻ, xử lý ngoại lệ ở đây... [cite: 189, 366]

# --- TASK 4: QUẢN TRỊ (ADMIN - UC6) ---
def admin_dashboard():
    st.title("Bảng điều khiển hệ thống")
    # Code UI cấu hình giá, xem log lỗi ở đây... [cite: 193, 264]

# --- ĐIỀU KIỆN ĐỂ HIỂN THỊ ---
if role == "Người học":
    student_dashboard()
elif role == "Bảng điện tử":
    signage_dashboard()
elif role == "Nhân viên bãi xe":
    attendant_dashboard()
elif role == "Quản trị viên":
    admin_dashboard()
