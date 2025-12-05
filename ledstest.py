from gpiozero import PWMLED
from time import sleep

left = PWMLED(17)
right = PWMLED(27)

while True:
	left.value = 0.0 # off
	right.value = 0.0
	sleep(1)

	left.value = 1.0 # dim
	right.value = 0.3
	sleep(1)
	
	left.value = 0.30 # full
	right.value = 1.0
	sleep(1)

	left.value = 1.0
	right.value = 0.5
	sleep(1)

	left.value = 0.75
	right.value = 1.0
	sleep(1)
