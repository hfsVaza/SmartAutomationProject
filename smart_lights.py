from gpiozero import MotionSensor, PWMLED
from time import sleep, time

# Inputs
pir = MotionSensor(4) # left-side PIR on GPIO4

# Outputs
left = PWMLED(17) # left LEDs on GPIO17
right = PWMLED(27) # right LEDs on GPIO27

# Brightness levels
OFF = 0.0
DIM = 0.3
FULL = 1.0

# How long to remember motion (seconds)
OCCUPANCY_HOLD = 5

last_left_motion = 0

print("Smart lighting demo running... Ctrl+C to stop.")

try:
	while True:
		now = time()

# Update last motion time when PIR sees movement
		if pir.motion_detected:
			last_left_motion = now

# For now we only have a left PIR
		left_occupied = (now - last_left_motion) < OCCUPANCY_HOLD
		right_occupied = False # later this will come from a right PIR

# ---- Lighting logic ----
		if not left_occupied and not right_occupied:
		# Room empty
			left.value = OFF
			right.value = OFF

		elif left_occupied and not right_occupied:
# Only left occupied
			left.value = FULL
			right.value = DIM

		elif right_occupied and not left_occupied:
# Only right occupied (future)
			left.value = DIM
			right.value = FULL

		else:
# Both occupied (future)
			left.value = FULL
			right.value = FULL

		sleep(0.1)

except KeyboardInterrupt:
	left.value = 0
	right.value = 0
	print("\nStopped.")
