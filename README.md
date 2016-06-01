# MDT Sensors

To Setup, do the following:

1.Clone Repository

`git clone https://github.com/JacobPotter/RPI_Sensors_MDT.git`

2.Run package setup
```
cd RPI_Sensors_MDT/src
sudo python setup.py develop
```
3.Copy ini
`cp sensor_config.ini.tmp sensor_config.ini`

4.Alter ini files to correct settings (follow comments in ini file)
5.Install Supervisor
```
sudo apt-get install supervisor
sudo service supervisor restart
```
6.Create Supervisor conf file
```
nano /etc/supervisor/conf.d/sensor.conf
```
7.Then copy/paste the following with ctrl+c and ctrl+v and press ctrl+x to save. Change directory to whereever the sensor.py file is saved.
```
[program:sensor]
directory=/home/pi/RPI_Sensors_MDT/src/
command=python /home/pi/RPI_Sensors_MDT/src/python sensor.py
autostart=true
autorestart=true
```
8.Then run:
```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start sensors
```
