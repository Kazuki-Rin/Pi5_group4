from datetime import datetime
from gpiozero import LED
import adafruit_dht
import board
import time


led = LED(17)
dht = adafruit_dht.DHT11(board.D18)

while True:
	try:
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		temp=dht.temperature
		hum=dht.humidity  
		print(f"{timestamp} | Nhiet do: {temp} do C | Do am: {hum} %")

		with open("log.txt","a") as f:
			f.write(f"{timestamp} {temp} do C {hum} % \n")
		
		if temp > 30:
			led.on()
		else:
			led.off()
	except RuntimeError:
		pass
		
	time.sleep(2)

