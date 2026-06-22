from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from datetime import datetime
from gpiozero import LED
import adafruit_dht
import board
import time


led = LED(17)
dht = adafruit_dht.DHT11
pin = 18
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
temp=dht.temperature
hum=dht.humidity  
print(f"{timestamp} | Nhiet do: {temp} do C | Do am: {hum} %")

with open("log.txt","a") as f:
	f.write(f"{timestamp} {temp} do C {hum} % \n")
		
fig=plt.firgure()
ax = plt.axes(xlim=(0,30), ylim=(15,45))
max_points=30
line, = ax.plot(np.arange(max_points),
				np.ones(max_points,dtype=np.float)*np.nan, lw=1, c='blue', marker='d', ms=2)

def init():
	return line
	
h,t=adafruit_dht.read_retry(dht,pin)

def animate(i):
	h,t=adafruit_dht.read_retry(dht,pin)
	y=t
	old_y=line.get_ydata()
	new_y=np.r_[old_y[1:],y]
	line.set_ydata(new_y)
	return line,
	
anim = animation.FuncAnimation(fig,animate,init_func=init,frames=200,interval=20,blit=False)
plt.show()	
time.sleep(2)

