import streamlit as st
import sqlite3
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Smart Parking System", page_icon="🚗", layout="centered")

# Khởi tạo biến session_state để lưu trạng thái đăng nhập
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

def check_login(username, password):
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# MÀN HÌNH ĐĂNG NHẬP
if not st.session_state['logged_in']:
    st.title("🚗 Hệ thống Đỗ xe Thông minh")
    st.subheader("Đăng nhập hệ thống")
    
    with st.form("login_form"):
        username_input = st.text_input("Tên đăng nhập (Ví dụ: Nguyen Van A)")
        password_input = st.text_input("Mật khẩu (Ví dụ: 123456)", type="password")
        submit_btn = st.form_submit_button("Đăng nhập")
        
        if submit_btn:
            user = check_login(username_input, password_input)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = user[1] # Cột username
                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu!")

# MÀN HÌNH SAU KHI ĐĂNG NHẬP (DASHBOARD)
else:
    st.title(f"👋 Xin chào, {st.session_state['username']}!")
    
    if st.button("Đăng xuất"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.rerun()
        
    st.markdown("---")
    st.subheader("Bảng Thông Tin Thẻ Đỗ Xe Của Bạn")
    
    # Kết nối DB và lấy dữ liệu của user đang đăng nhập
    conn = sqlite3.connect('parking.db')
    df = pd.read_sql_query(f"SELECT uid, role, balance, entry_time, exit_time FROM users WHERE username = '{st.session_state['username']}'", conn)
    conn.close()
    
    # Định dạng lại bảng cho đẹp
    df.columns = ["Mã Thẻ (UID)", "Vai trò", "Số dư (VND)", "Giờ vào gần nhất", "Giờ ra gần nhất"]
    
    # Hiển thị dữ liệu
    st.dataframe(df, use_container_width=True)
    
    # Thêm nút làm mới dữ liệu (Refresh)
    if st.button("🔄 Cập nhật dữ liệu"):
        st.rerun()
        
    # Highlight nếu đang đỗ xe trong bãi
    entry_time_val = df.iloc[0]["Giờ vào gần nhất"]
    if entry_time_val != "":
        st.info("Trạng thái: 🟢 Xe của bạn đang ở trong bãi.")
    else:
        st.warning("Trạng thái: 🔴 Xe của bạn đang ở ngoài bãi.")