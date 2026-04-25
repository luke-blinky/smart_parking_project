import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
import time

# CẤU HÌNH MQTT (Sửa lại IP máy tính của ông)
MQTT_BROKER = "192.168.x.x"  
MQTT_PORT = 1883
TOPIC_SCAN = "parking/rfid/scan"
TOPIC_CONTROL = "parking/gate/control"

# Phí gửi xe mỗi lần
FEE = 5000

def check_and_process_rfid(uid):
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    
    # Tìm thẻ trong DB
    cursor.execute('SELECT * FROM users WHERE uid = ?', (uid,))
    user = cursor.fetchone()
    
    if user is None:
        print(f"[-] UID {uid} không tồn tại (Visitor).")
        conn.close()
        return "DENY"

    # Lấy thông tin user (dựa theo thứ tự cột trong DB)
    username = user[1]
    role = user[3]
    balance = user[4]
    entry_time = user[5]
    
    if role != "university_member":
         print(f"[-] {username} không có quyền vào.")
         conn.close()
         return "DENY"

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # LOGIC: Xe đi VÀO (entry_time đang trống)
    if not entry_time:
        if balance < FEE:
            print(f"[-] {username} không đủ số dư ({balance} VND). TỪ CHỐI!")
            conn.close()
            return "DENY"
            
        print(f"[+] {username} đi VÀO. Cập nhật entry_time.")
        cursor.execute('UPDATE users SET entry_time = ?, exit_time = "" WHERE uid = ?', (now_str, uid))
        conn.commit()
        conn.close()
        return "OPEN"

    # LOGIC: Xe đi RA (entry_time đã có dữ liệu)
    else:
        new_balance = balance - FEE
        print(f"[+] {username} đi RA. Trừ phí: {FEE} VND. Số dư mới: {new_balance} VND.")
        # Cập nhật giờ ra, trừ tiền, và XÓA giờ vào để reset chu kỳ
        cursor.execute('''
            UPDATE users 
            SET balance = ?, exit_time = ?, entry_time = "" 
            WHERE uid = ?
        ''', (new_balance, now_str, uid))
        
        conn.commit()
        conn.close()
        return "OPEN"

# Các hàm callback của MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Đã kết nối MQTT Broker với mã lỗi: {rc}")
    client.subscribe(TOPIC_SCAN)
    print(f"Đang lắng nghe tại topic: {TOPIC_SCAN}")

def on_message(client, userdata, msg):
    uid = msg.payload.decode("utf-8").strip()
    print(f"\n[>>>] Nhận được UID quét: {uid}")
    
    # Xử lý logic database
    command = check_and_process_rfid(uid)
    
    # Gửi lệnh lại cho ESP32
    print(f"[<<<] Gửi lệnh về ESP32: {command}")
    client.publish(TOPIC_CONTROL, command)

# Khởi tạo MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"Đang kết nối tới Broker {MQTT_BROKER}...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Duy trì vòng lặp vĩnh viễn để nhận tin nhắn
client.loop_forever()