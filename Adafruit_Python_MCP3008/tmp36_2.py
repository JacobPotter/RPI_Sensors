#from __future__ import print_function
# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time
# Import SPI library (for hardware SPI) and MCP3008 library.
#import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import os
import socket
import socket

import logging
from influxdb import InfluxDBClient

logging.basicConfig(filename='sensor.log', level=logging.DEBUG)
influxClient = InfluxDBClient(host='23.28.208.70', port=8086, username='temp_sensor_user', password='Setup03', database='temperature')
#def print(s, end="", file=sys.stdout):
#    file.write(s + end)
#    file.flush()

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


def temperature_data(temp_f):
  return [
        {
        "measurement": "temperature",
        "tags": {
            "sensor": "analog",
            "host": socket.gethostname()
        },
        "fields": {
            "value": temp_f }}]

# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    
    # Pause for half a second.


    millivolts = values[0] * (3300.0 / 1024.0)


    
    
    # 10 mv per degree
    temp_C = float((millivolts - 100.0) / 10.0) - 40.0
    # convert celsius to fahrenheit
    temp_F = (temp_C * 9.0 / 5.0) + 32
    # remove decimal point from millivolts
    millivolts = "%d" % millivolts
    # show only one decimal place for temprature and voltage readings
    
   
    print ("F: %s, C: %s" % (temp_F,temp_C))
    #sys.stdout.flush()
    temp_json=temperature_data(temp_F)
    
    #log=
    influxClient.write_points(temp_json)
    time.sleep(1)
