import RPi.GPIO as GPIO
import time
import datetime
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the GPIO Pins on the Raspi



# MCP3008 to Raspi (PiCobbler) Pin connections
class PINS:
    SPICLK = 18
    SPIMISO = 23
    SPIMOSI = 24
    SPICS = 25

 # set up the SPI interface pins
def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PINS.SPIMOSI, GPIO.OUT)
    GPIO.setup(PINS.SPIMISO, GPIO.IN)
    GPIO.setup(PINS.SPICLK, GPIO.OUT)
    GPIO.setup(PINS.SPICS, GPIO.OUT)


# Function to read data from Analog Pin 0 from MCP3008 (don't need to edit)
# This function will be called in our loop to get the current sensor value
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
            return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
            if (commandout & 0x80):
                    GPIO.output(mosipin, True)
            else:
                    GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                    adcout |= 0x1

    GPIO.output(cspin, True)

    adcout /= 2       # first bit is 'null' so drop it
    return adcout


sensor_pin = 0
initialize()

while True:
    sensor_data = readadc(sensor_pin,
                                  PINS.SPICLK,
                                  PINS.SPIMOSI,
                                  PINS.SPIMISO,
                                  PINS.SPICS)

    millivolts = sensor_data * (3300.0 / 1024.0)
    # 10 mv per degree
    temp_C = ((millivolts - 100.0) / 10.0) - 40.0
    # convert celsius to fahrenheit
    temp_F = (temp_C * 9.0 / 5.0) + 32
    # remove decimal point from millivolts
    millivolts = "%d" % millivolts
    # show only one decimal place for temprature and voltage readings
    temp_C = "%.1f" % temp_C
    temp_F = "%.1f" % temp_F

    print(temp_F)
    time.sleep(1)
