import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_MCP3008
import socket
import logging
from influxdb import InfluxDBClient

logging.basicConfig(filename='sensor.log', level=logging.DEBUG)
influxClient = InfluxDBClient(host='23.28.208.70', port=8086, username='temp_sensor_user', password='Setup03', database='four_to_twenty')
influxClient.create_database('four_to_twenty')
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

def raw_mv_data(millivolts):
  return [
      	{
      	"measurement": "millivolts",
        "tags": {
            "sensor": "analog",
            "host": socket.gethostname()
        },
        "fields": {
            "value": millivolts }}]

def pressure_data(pressure):
  return [
      	{
      	"measurement": "pressure",
        "tags": {
            "sensor": "analog",
            "host": socket.gethostname()
        },
        "fields": {
            "value": pressure }}]

# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Print the ADC values.
    millivolts = values[1] * (3300.0 / 1024.0)
    # Pause for half a second.
    #print millivolts
    sensorMax=100
    sensorMin=0
    mv_range = (3000 - 550)  
    sensorRange = (sensorMax - sensorMin)  
    sensorValue = (((millivolts - 550) * sensorRange) / mv_range) + sensorMin
    #print sensorValue
    log=influxClient.write_points(pressure_data(sensorValue))
    log=influxClient.write_points(raw_mv_data(millivolts))
    time.sleep(0.5)
