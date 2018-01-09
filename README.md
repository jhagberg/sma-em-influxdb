# SMA-EM-influxdb
SMA energy meter to Influxdb Python script. 
This code is based on the document Technical Information SMA ENERGY METER meter Protocol found here:
https://www.sma.de/fileadmin/content/global/Partner/Documents/SMA_Labs/EMETER-Protokoll-TI-en-10.pdf

The Influxdb schema is based after the discusssion here https://stackoverflow.com/questions/40549025/influxdb-design-storing-energy-values-from-sma-em-meter 

One way to run this is as a service is using supervisor 
Add something like this to /etc/supervisor/supervisord.conf 

```
[program:smaem2influxdb]
command=/usr/bin/python /PATH/TO/smaem2influxdb.py
autorestart=true
autostart=true
stderr_logfile = /var/log/sma2eminfluxdb-stderr.log
stdout_logfile = /var/log/sma2eminfluxdb-stdout.log
```
then start it with

```
sudo supervisorctl start smaem2influxdb
```

# SMA-EM-influxdb on Rasbian on a PI Debain 9

Install supervisor and python deps and git

```
sudo apt-get update
sudo apt-get -y install supervisor python-influxdb git
```
Install influxdb 
https://docs.influxdata.com/influxdb/v1.3/introduction/installation/#installation
```
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
test $VERSION_ID = "9" && echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update && sudo apt-get install influxdb
sudo service influxdb start
```
create database 
run cmd ```influx``` to start influx comdline
then type
```
create database sma_em
exit
```
clone gitrepo

``` git clone https://github.com/jhagberg/sma-em-influxdb.git
```

Configure Supervisor 

```
echo "[program:smaem2influxdb]
command=/usr/bin/python /home/pi/sma-em-influxdb/smaem2influxdb.py
autorestart=true
autostart=true
stderr_logfile = /var/log/sma2eminfluxdb-stderr.log
stdout_logfile = /var/log/sma2eminfluxdb-stdout.log" >smaem.conf 
sudo cp smaem.conf /etc/supervisor/conf.d/smaem.conf
sudo supervisorctl reload 
sudo supervisorctl status
```
Check influx data

influx
use sma_em
SELECT "energy+" from grid

Voila

 


