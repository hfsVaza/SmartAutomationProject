from gpiozero import MotionSensor, PWMLED, Button, Buzzer
from time import sleep, time
import json
import paho.mqtt.client as mqtt


# Inputs
left_pir = MotionSensor(16) # left-side PIR on GPIO4
right_pir = MotionSensor(4)
light_raw = Button(22) # light sensor as digital input on GPIO22

# Outputs
left = PWMLED(17) # left LEDs on GPIO17
right = PWMLED(27) # right LEDs on GPIO27
buzzer = Buzzer(23)

#Alarm
LOCKED = True
ALARM_DURATION = 3
alarm_until = 0

#MQTT_SETUP
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_LIGHT_STATE = "smartroom/light/state"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# Brightness levels (0.0..1.0)
OFF = 0.0
DIM = 0.3
FULL = 1.0

OCCUPANCY_HOLD = 1 # seconds

last_left_motion = 0
last_right_motion = 0

print("Smart lighting + daylight demo running... Ctrl+C to stop.")

try:
	while True:
		now = time()

# Update occupancy from PIR
		if left_pir.motion_detected:
			last_left_motion = now

		if right_pir.motion_detected:
			last_right_motion = now
		left_occupied = (now - last_left_motion) < OCCUPANCY_HOLD
		right_occupied = (now - last_right_motion) < OCCUPANCY_HOLD

#Room_lock_mode
		alarm_active = LOCKED and (now < alarm_until)


# --- Read light level as dark/bright ---
# When light sensor output is HIGH, we call that "bright enough"
		is_dark = light_raw.is_pressed # True = bright, False = dark
		is_bright = not is_dark

# ---- Lighting logic ----
		if not left_occupied and not right_occupied:
# Room empty -> lights off always
			left.value = OFF
			right.value = OFF

		else:
# Room occupied somewhere
			if is_dark:
# Only turn on lights when it is dark
				if left_occupied and not right_occupied:
					left.value = FULL
					right.value = DIM
				elif right_occupied and not left_occupied:
					left.value = DIM
					right.value = FULL
				else:
					left.value = FULL
					right.value = FULL
			else:
# It is bright enough -> keep lights off to save energy
				left.value = OFF
				right.value = OFF

		sleep(0.1)
		if LOCKED and (left_occupied or right_occupied):
			alarm_until + now + ALARM_DURATION
		if LOCKED and now < alarm_until:
			buzzer.on()
		else:
			buzzer.off()

		state = {
			"timestamp": now,
			"left": float(left.value),
			"right": float(right.value),
			"locked": LOCKED,
			"alarm": alarm_active,
			"left_occupied": left_occupied,
			"right_ocupied": right_occupied,
			"dark": is_dark,
		}
		mqtt_client.publish(MQTT_TOPIC_LIGHT_STATE, json.dumps(state))
		sleep(0.1)

except KeyboardInterrupt:
	left.value = 0
	right.value = 0
	buzzer.off()
	mqtt_client.loop_stop()
	print('\nStopp.')

