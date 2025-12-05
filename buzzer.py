from gpiozero import Buzzer
from time import sleep

bz = Buzzer(23)
for i in range(5):
        bz.on()
        sleep(0.3)
        bz.off()
        sleep(0.3)

