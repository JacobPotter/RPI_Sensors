import os
import glob
import time

from influxdb import InfluxDBClient


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir='/sys/bus/w1/devices/'
device_folder= glob.glob(base_dir+'28*')[0]
device_file=device_folder+'/w1_slave'

influxClient = InfluxDBClient(host='192.168.1.5', port=8086, username='temperature', password='testpass', database='temp_test')

def read_temp_raw():
	f = open(device_file,'r')
	lines = f.readlines()
	f.close()
	return lines

def temperature_data(temp_f):
  return [
      	{
      	"measurement": "Temperature",
        "fields": {
            "value": temp_f }}]


def read_temp():
	lines=read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_f

while True:
	temp=read_temp()
	print(temp)
	# 10.0.250.115
	influxClient.write_points(temperature_data(temp))
	time.sleep(1)
