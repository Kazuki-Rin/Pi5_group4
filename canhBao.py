import RPi.GPIO as GPIO
import time
import datetime

# --- CẤU HÌNH CÁC CHÂN GPIO (ĐÁNH SỐ BCM) ---
PIN_A = 5
PIN_B = 6

PIN_ECHO = 27
PIN_TRIG = 22

PIN_LED = 17

# Biến toàn cục lưu khoảng cách cài đặt ban đầu (đơn vị: cm)
khoang_cach_a = 20  

def setup_he_thong():
	"""Thiết lập các chế độ và cấu hình ngắt cho toàn bộ thiết bị"""
	GPIO.setmode(GPIO.BCM)
	
	# 1. Thiết lập cho Rotary Encoder (Sử dụng Pull-up nội trở)
	GPIO.setup(PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	# Kích hoạt ngắt cạnh (cả lên và xuống) cho chân A để bắt tín hiệu xoay nhanh nhất
	GPIO.add_event_detect(PIN_A, GPIO.BOTH, callback=xu_ly_tin_hieu_xoay)
	
	# 2. Thiết lập cho Cảm biến siêu âm HC-SR04
	GPIO.setup(PIN_TRIG, GPIO.OUT)
	GPIO.setup(PIN_ECHO, GPIO.IN)
	
	GPIO.setup(PIN_LED, GPIO.OUT)
	GPIO.output(PIN_LED, GPIO.LOW)
	
	# Đảm bảo chân Trig ban đầu ở mức thấp (LOW)
	GPIO.output(PIN_TRIG, GPIO.LOW)
	print("Đang khởi tạo cảm biến siêu âm...")
	time.sleep(2)  # Chờ cảm biến ổn định trạng thái
	print("Hệ thống đã sẵn sàng hoạt động.")

def xu_ly_tin_hieu_xoay(channel):
	"""Hàm ngắt (Callback) tự động kích hoạt khi xoay Encoder để điều chỉnh giá trị a"""
	global khoang_cach_a
	
	trang_thai_A = GPIO.input(PIN_A)
	trang_thai_B = GPIO.input(PIN_B)
	
	# So sánh trạng thái hai pha để nhận diện chiều quay
	if trang_thai_A == trang_thai_B:
		khoang_cach_a += 1  # Xoay thuận -> tăng ngưỡng khoảng cách cảnh báo
	else:
		khoang_cach_a -= 1  # Xoay ngược -> giảm ngưỡng khoảng cách cảnh báo
		if khoang_cach_a < 5: 
			khoang_cach_a = 5  # Giới hạn tối thiểu là 5cm để tránh giá trị âm hoặc quá nhỏ
			
	print(f"[Cập nhật] Ngưỡng cảnh báo mới (a) = {khoang_cach_a} cm")

def doc_khoang_cach_hien_tai():
	"""Hàm phát xung và tính toán khoảng cách thực tế từ HC-SR04"""
	# Phát một xung HIGH dài đúng 10 micro-giây vào chân Trig
	GPIO.output(PIN_TRIG, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(PIN_TRIG, GPIO.LOW)
	
	start_time = time.time()
	stop_time = time.time()
	
	# Vòng lặp chờ chân Echo chuyển lên mức HIGH (bắt đầu nhận sóng phản hồi)
	while GPIO.input(PIN_ECHO) == 0:
		start_time = time.time()
        
    # Vòng lặp chờ chân Echo quay về mức LOW (kết thúc nhận sóng phản hồi)
	while GPIO.input(PIN_ECHO) == 1:
		stop_time = time.time()
        
    # Tính thời gian sóng đi và về
	thoi_gian_xung = stop_time - start_time
    
    # Tính khoảng cách (Vận tốc âm thanh trong không khí lấy gần đúng là 34300 cm/s)
    # Chia 2 vì thời gian tính cho cả đường đi lẫn đường về của sóng âm
	khoang_cach = (thoi_gian_xung * 34300) / 2
    
	return round(khoang_cach, 2)

def ghi_log(khoang_cach):
	"""Hàm định dạng thời gian và ghi dữ liệu cảnh báo vào file log"""
	thoi_gian_thuc = datetime.datetime.now()
	dinh_dang_thoi_gian = thoi_gian_thuc.strftime("%Y-%m-%d %H:%M:%S")
    
	thong_tin_log = f"[{dinh_dang_thoi_gian}] Canh bao: Vat can o khoang cach {khoang_cach} cm\n"
    
    # Ghi đè tiếp tục (append mode) vào file log trên Raspberry Pi
	with open("/home/pi/Documents/Raspberry_project_nhom4/canhbao_log.txt", "a", encoding="utf-8") as file_log:
		file_log.write(thong_tin_log)
	print(f"[LOGGED] {thong_tin_log.strip()}")

# --- VÒNG LẶP CHÍNH ---
if __name__ == "__main__":
	try:
		setup_he_thong()
		while True:
            # Đọc khoảng cách thực tế từ cảm biến siêu âm
			khoang_cach_thuc_te = doc_khoang_cach_hien_tai()
            
            # Hiển thị thông số thời gian thực lên Terminal để theo dõi
			print(f"Thực tế: {khoang_cach_thuc_te} cm | Ngưỡng cài đặt (a): {khoang_cach_a} cm")
            
            # Kiểm tra xem khoảng cách thực tế có nhỏ hơn ngưỡng a do encoder thiết lập không
			if khoang_cach_thuc_te < khoang_cach_a:
				GPIO.output(PIN_LED, GPIO.HIGH)
				ghi_log(khoang_cach_thuc_te)
				time.sleep(2)  # Tạm dừng 2 giây sau khi ghi log để tránh ghi dữ liệu dồn dập
			else:
				GPIO.output(PIN_LED, GPIO.LOW)
                
			time.sleep(0.3)  # Khoảng thời gian nghỉ nhỏ giữa các lần quét cảm biến (chu kỳ ~300ms)
            
	except KeyboardInterrupt:
		print("\nĐang dừng chương trình và giải phóng các chân GPIO...")
	finally:
		GPIO.cleanup()  # Đưa các chân GPIO về trạng thái an toàn trước khi thoát
