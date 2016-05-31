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


MV_MAX=3000
MV_MIN=600

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
    logging.debug('Dict in section map %s'%dict1)
    return dict1




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
#default reference voltage should be 3.3
def adc_to_millivolts(adcValue):
    return adcValue * (config_section_map('Etc')['referencevoltage'] / 1023.0)

def sensor_conversion(SensorMin,SensorMax, millivolts):
    SensorMax=SensorMax
    SensorMin=SensorMin
    mv_range=MV_MAX - MV_MIN
    sensorRange = (SensorMax - SensorMin)  
    sensorValue = (((millivolts - MV_MIN) * sensorRange) / mv_range) + SensorMin
    return sensorValue

def get_config(pinNumber):
    try:
        if pinNumber==0:
            dict1={}
            dict1['raw_value']=config_section_map("ChannelZero")['sendrawvalue']
            dict1['name']=config_section_map("ChannelZero")['measurementname']
            if dict1['raw_value'] == "False":
                dict1['min_value']=config_section_map("ChannelThree")['SensorMin']
                dict1['max_value']=config_section_map("ChannelThree")['SensorMax']
            return dict1
        elif pinNumber==1:
            dict1={}
            dict1['raw_value']=config_section_map("ChannelOne")['sendrawvalue']
            dict1['name']=config_section_map("ChannelOne")['measurementname']
            if dict1['raw_value'] == "False":
                dict1['min_value']=config_section_map("ChannelThree")['SensorMin']
                dict1['max_value']=config_section_map("ChannelThree")['SensorMax']
            return dict1
        elif pinNumber==2:
            dict1={}
            dict1['raw_value']=config_section_map("ChannelTwo")['sendrawvalue']
            dict1['name']=config_section_map("ChannelTwo")['measurementname']
            if dict1['raw_value'] == "False":
                dict1['min_value']=config_section_map("ChannelThree")['SensorMin']
                dict1['max_value']=config_section_map("ChannelThree")['SensorMax']
            return dict1
        elif pinNumber==3:
            dict1={}
            dict1['raw_value']=config_section_map("ChannelThree")['sendrawvalue']
            dict1['name']=config_section_map("ChannelThree")['measurementname']
            if dict1['raw_value'] == "False":
                dict1['min_value']=config_section_map("ChannelThree")['SensorMin']
                dict1['max_value']=config_section_map("ChannelThree")['SensorMax']
            return dict1
        elif pinNumber==4:
            dict1={}
            dict1['raw_value']=config_section_map("ChannelFour")['sendrawvalue']
            dict1['name']=config_section_map("ChannelFour")['measurementname']
            if dict1['raw_value'] == "False":
                dict1['min_value']=config_section_map("ChannelThree")['SensorMin']
                dict1['max_value']=config_section_map("ChannelThree")['SensorMax']
            return dict1
        elif pinNumber==5:
            dict1={}
            dict1['raw_value']=config_section_map("ChannelFive")['sendrawvalue']
            dict1['name']=config_section_map("ChannelFive")['measurementname']
            if dict1['raw_value'] == "False":
                dict1['min_value']=config_section_map("ChannelThree")['SensorMin']
                dict1['max_value']=config_section_map("ChannelThree")['SensorMax']
            return dict1
        elif pinNumber==6:
            dict1={}
            dict1['raw_value']=config_section_map("ChannelSix")['sendrawvalue']
            dict1['name']=config_section_map("ChannelSix")['measurementname']
            if dict1['raw_value'] == "False":
                dict1['min_value']=config_section_map("ChannelThree")['SensorMin']
                dict1['max_value']=config_section_map("ChannelThree")['SensorMax']
            return dict1
        elif pinNumber==7:
            dict1={}
            dict1['raw_value']=config_section_map("ChannelSeven")['sendrawvalue']
            dict1['name']=config_section_map("ChannelSeven")['measurementname']
            if dict1['raw_value'] == "False":
                dict1['min_value']=config_section_map("ChannelThree")['SensorMin']
                dict1['max_value']=config_section_map("ChannelThree")['SensorMax']
            return dict1
    except Exception, e:
        logging.severe('Config error')
        raise e
    

def push_value(value, pinNumber):
    dict_config=get_config(pinNumber)
    logging.debug(dict_config)
    try:
        if dict_config['raw_value'] == "True":
            log=influxClient.write_points(sensor_data_influx(value, dict_config['name'], "true"))
            logging.info(log)
        else:
            log=influxClient.write_points(sensor_data_influx(sensor_conversion(dict_config['min_value'],dict_config['max_value'], value), dict_config['name'], "false"))
    except Exception, e:
        logging.severe('Error Writing to DB or connection lost')
        raise e

# Main program 
path=os.path.realpath(__file__)
path=path[:-10]
print path
config = ConfigParser.ConfigParser()

config.read("%s/sensor_config.ini" % path)

logging.basicConfig(filename='sensor.log', level=logging.DEBUG)
logging.info('execution started')

CLK  = int(config_section_map("Etc")['spiclk'])
MISO = int(config_section_map("Etc")['spimiso'])
MOSI = int(config_section_map("Etc")['spimosi'])
CS   = int(config_section_map("Etc")['spics'])
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


dbhost=config_section_map("InfluxClient")['host']
dbport=config_section_map("InfluxClient")['port']
dbuser=config_section_map("InfluxClient")['user']
dbpwd=config_section_map("InfluxClient")['password']
dbname=config_section_map("InfluxClient")['databasename']

try:
    influxClient = InfluxDBClient(host=dbhost, port=dbport, username=dbuser, password=dbpwd, database=dbname)
    influxClient.create(dbname)
    #Main loop to read adc values
    
except Exception, e:
    loggin.severe('Influx DB Connection error')
    raise e
logging.debug('looping')
while True:
    #Check if digital sensor setup
    # if config_section_map("DigitalTemperature")['enable']=="true":
    #     temp=convert_digital_temp()
    #     influxClient.write_points(temperature_data(temp, "digital_temperature"),"false")
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        
        values[i] = mcp.read_adc(i)
        values[i] = adc_to_millivolts(values[i])
        # logging.debug('ADC value %d, Pin: %d' % values[i], i)
        if values[i] >= MV_MIN and values[i] <= MV_MAX:
            push_value(values[i], i)
    time.sleep(1)
