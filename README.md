# MDT Sensors

To Setup, do the following:

1.Clone Repository

`git clone https://github.com/JacobPotter/RPI_Sensors_MDT.git`

2.Run package setup
```
cd RPI_Sensors_MDT/src
sudo python setup.py develop
```
3.Install Supervisor
```
sudo apt-get install supervisor
sudo service supervisor restart
```
4.Create Supervisor conf file
```
nano /etc/supervisor/conf.d/sensor.conf
```
5.Then copy/paste the following with ctrl+c and ctrl+v and press ctrl+x to save. Change directory to whereever the sensor.py file is saved.
```
[program:sensor]
directory=/home/pi/RPI_Sensors_MDT/src/
command=python /home/pi/RPI_Sensors_MDT/src/python sensor.py
autostart=true
autorestart=true
```
6.Then run:
```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start sensors
```
