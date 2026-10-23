import time
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = False   # LED ON (this LED is active-low)
    print("LED on")
    time.sleep(0.5)
    led.value = True    # LED OFF
    print("LED off")
    time.sleep(0.5)