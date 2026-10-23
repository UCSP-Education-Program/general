import board
import analogio
import time
import math
import digitalio

# initialise ADC
adc = analogio.AnalogIn(board.A0)
led = digitalio.DigitalInOut(board.D5)
led.direction = digitalio.Direction.OUTPUT

R_FIXED = 10000.0
R0 = 10000.0
B = 3950.0
T0 = 298.15

def readTempC(value):    
    r = R_FIXED * value / (65535.0 - value) 
    invT = 1.0 / T0 + math.log(r / R0) / B
    return 1.0 / invT - 273.15




while True:
    value = adc.value
    print("ADC Value:", value)
    if (t :=readTempC(value)) > 30:
        led.value = True;
    else:
        led.value = False;
    print("ADC temp:", t)
    time.sleep(1)
