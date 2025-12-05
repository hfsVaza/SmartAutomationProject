from gpiozero import MotionSensor
from time import sleep

pir = MotionSensor(4) # GPIO4, assuming you used that pin

print("Move your hand in front of the PIR... Ctrl+C to stop.")

while True:
	if pir.motion_detected:
		print("MOTION!")
	else:
		print("no motion")
	sleep(0.5)

