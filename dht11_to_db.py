# -*- coding: utf-8 -*-

import time
import adafruit_dht
import board
import pymysql

dht = adafruit_dht.DHT11(board.D4)

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = '1234'        
DB_NAME = 'iot_db' 

current_led_status = 0 

def save_to_database(temp, humid, led_state):
	try:
		conn = pymysql.connect(
			host=DB_HOST,
			user=DB_USER,
			password=DB_PASS,
			database=DB_NAME
			)
		cursor = conn.cursor()
		sql = "INSERT INTO sensor_data (temperature, humidity, led_status) VALUES (%s, %s, %s)"
		cursor.execute(sql, (temp, humid, led_state))
		conn.commit()
		print(f"[DA LUU CSDL] Nhiet do: {temp}C | Do am: {humid}% | LED: {led_state}")    
	except Exception as e:
		print(f"Loi ghi du lieu vao CSDL: {e}")
	finally:
		try:
			conn.close()
		except:
			pass

print("=== BAT DAU DOC DHT11 VA DAY LEN CSDL ===")
try:
	while True:
		temp = dht.temperature
		hum = dht.humidity
		current_led_status = 0
		if hum is not None and temp is not None:
			save_to_database(temp, hum, current_led_status)
		else:
			print("Loi: Khong doc duoc du lieu tu cam bien DHT11. Dang thu lai...")    
			time.sleep(5)
except KeyboardInterrupt:print("\nChuong trinh da dung theo yeu cau.")
