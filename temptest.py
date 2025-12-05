import Adafruit_DHT
from time import sleep
import seeed_dht
# DHT22/AM2302 sensor type
SENSOR = seeed_dht.DHT("22", 24)

# We wired DATA to GPIO24 (BCM numbering)


print("Reading AM2302 (DHT22) on GPIO18... Ctrl+C to stop.")

try:
	while True:
		humidity, temperature = sensor.read()

		if humidity is not None and temperature is not None:
			# temperature is in °C by default
			print(f"Temp: {temperature:.1f} °C Humidity: {humidity:.1f} %")
		else:
			print("Failed to read from sensor (got None)")

	sleep(2)

except KeyboardInterrupt:
	print("\nStopped.")
