from gpiozero import LED
from time import sleep

Led_pin=22
led=LED(Led_pin)
while True:
    print("on")
    led.on()
    sleep(1)
    print("off")
    led.off()
    sleep(1)
    