import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_MCP3008


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
    print millivolts
    sensorMax=100
    sensorMin=0
    mv_range = (3000 - 550)  
    sensorRange = (sensorMax - sensorMin)  
    sensorValue = (((millivolts - 550) * sensorRange) / mv_range) + sensorMin
    print sensorValue
    time.sleep(0.5)
