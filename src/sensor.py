import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_MCP3008
import socket
import logging
from influxdb import InfluxDBClient
import ConfigParser

import os
import glob


# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

MV_MAX=2950
MV_MIN=550

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


def config_section_map(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def influx_setup():
    dbhost=config_section_map("InfluxClient")['host']
    dbport=config_section_map("InfluxClient")['port']
    dbuser=config_section_map("InfluxClient")['user']
    dbpwd=config_section_map("InfluxClient")['password']
    dbname=config_section_map("InfluxClient")['databasename']
    influxClient = InfluxDBClient(host=dbhost, port=dbport, username=dbuser, password=dbpwd, database=dbname)



def sensor_data_influx(sensorValue, sensorTag,rawData):
  return [
      	{
      	"measurement": sensorTag,
        "tags": {
            "raw voltage": rawData,
            "host": socket.gethostname()
        },
        "fields": {
            "value": sensorValue }}]

def adc_to_millivolts(adcValue):
    return adcValue * (3300.0 / 1024.0)

def sensor_conversion(sensorMin,sensorMax, millivolts):
    sensorMax=sensorMax
    sensorMin=sensorMin
    mv_range=MV_MAX - MV_MIN
    sensorRange = (sensorMax - sensorMin)  
    sensorValue = (((millivolts - MV_MIN) * sensorRange) / mv_range) + sensorMin
    return sensorValue

def get_config(pinNumber):
    if pinNumber==0:
        dict1={}
        dict1['raw_value']=config_section_map("ChannelZero")['sendrawvalue']
        dict1['min_value']=config_section_map("ChannelZero")['sensormin']
        dict1['max_value']=config_section_map("ChannelZero")['sensormax']
        dict1['name']=config_section_map("ChannelZero")['measurementname']
        return dict1
    elif pinNumber==1:
        dict1={}
        dict1['raw_value']=config_section_map("ChannelOne")['sendrawvalue']
        dict1['min_value']=config_section_map("ChannelOne")['sensormin']
        dict1['max_value']=config_section_map("ChannelOne")['sensormax']
        dict1['name']=config_section_map("ChannelOne")['measurementname']
        return dict1
    elif pinNumber==2:
        dict1={}
        dict1['raw_value']=config_section_map("ChannelTwo")['sendrawvalue']
        dict1['min_value']=config_section_map("ChannelTwo")['sensormin']
        dict1['max_value']=config_section_map("ChannelTwo")['sensormax']
        dict1['name']=config_section_map("ChannelTwo")['measurementname']
        return dict1
    elif pinNumber==3:
        dict1={}
        dict1['raw_value']=config_section_map("ChannelThree")['sendrawvalue']
        dict1['min_value']=config_section_map("ChannelThree")['sensormin']
        dict1['max_value']=config_section_map("ChannelThree")['sensormax']
        dict1['name']=config_section_map("ChannelThree")['measurementname']
        return dict1
    elif pinNumber==4:
        dict1={}
        dict1['raw_value']=config_section_map("ChannelFour")['sendrawvalue']
        dict1['min_value']=config_section_map("ChannelFour")['sensormin']
        dict1['max_value']=config_section_map("ChannelFour")['sensormax']
        dict1['name']=config_section_map("ChannelFour")['measurementname']
        return dict1
    elif pinNumber==5:
        dict1={}
        dict1['raw_value']=config_section_map("ChannelFive")['sendrawvalue']
        dict1['min_value']=config_section_map("ChannelFive")['sensormin']
        dict1['max_value']=config_section_map("ChannelFive")['sensormax']
        dict1['name']=config_section_map("ChannelFive")['measurementname']
        return dict1
    elif pinNumber==6:
        dict1={}
        dict1['raw_value']=config_section_map("ChannelSix")['sendrawvalue']
        dict1['min_value']=config_section_map("ChannelSix")['sensormin']
        dict1['max_value']=config_section_map("ChannelSix")['sensormax']
        dict1['name']=config_section_map("ChannelSix")['measurementname']
        return dict1
    elif pinNumber==7:
        dict1={}
        dict1['raw_value']=config_section_map("ChannelSeven")['sendrawvalue']
        dict1['min_value']=config_section_map("ChannelSeven")['sensormin']
        dict1['max_value']=config_section_map("ChannelSeven")['sensormax']
        dict1['name']=config_section_map("ChannelSeven")['measurementname']
        return dict1

def push_value(value, pinNumber):
    dict_config=get_config(pinNumber)
    if dict_config['raw_value'] == True:
        influxClient.write_points(sensor_data_influx(adc_to_millivolts(value), dict_config['name'], "true"))
    else:
        influxClient.write_points(sensor_data_influx(sensor_conversion(dict_config['min_value'],dict_config['max_value'], adc_to_millivolts(value)), dict_config['name'], "false"))

def read_digital_temp_raw():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir='/sys/bus/w1/devices/'
    device_folder= glob.glob(base_dir+'28*')[0]
    device_file=device_folder+'/w1_slave'
    f = open(device_file,'r')
    lines = f.readlines()
    f.close()
    return lines


def convert_digital_temp():
    lines=read_digital_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f    

# Main program 
config = ConfigParser.ConfigParser()

config.read("sensor_config.ini")

logging.basicConfig(filename='sensor.log', level=logging.DEBUG)

influxClient = None 

influx_setup()

#Main loop to read adc values

while True:
    #Check if digital sensor setup
    if config_section_map("DigitalTemperature")['enable']=="true":
        temp=convert_digital_temp()
        influxClient.write_points(temperature_data(temp, "digital_temperature"),"false")
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
        if values[i] >= MV_MIN and values[i] <= MV_MAX:
            push_value(values[i], i)
    time.sleep(0.5)