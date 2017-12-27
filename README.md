# SMA-EM-influxdb
SMA energy meter to Influxdb Python script. 
This code is based on the document Technical Information SMA ENERGY METER meter Protocol found here:
https://www.sma.de/fileadmin/content/global/Partner/Documents/SMA_Labs/EMETER-Protokoll-TI-en-10.pdf

The Influxdb schema is based after the discusssion here https://stackoverflow.com/questions/40549025/influxdb-design-storing-energy-values-from-sma-em-meter 

One way to run this is as a service is using supervisor 
Add something like this to /etc/supervisor/supervisord.conf 

```[program:smaem2influxdb]
command=/usr/bin/python /PATH/TO/smaem2influxdb.py
autorestart=true
autostart=true
stderr_logfile = /var/log/sma2eminfluxdb-stderr.log
stdout_logfile = /var/log/sma2eminfluxdb-stdout.log
```

