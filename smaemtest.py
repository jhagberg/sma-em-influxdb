import socket
import struct
import binascii
import struct
import influxdb
import time
import threading


MCAST_GRP = '239.12.255.254'
MCAST_PORT = 9522

db_client=influxdb.InfluxDBClient('localhost', database='sma_em')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock.settimeout(10)

def log_to_influx(sock, db_client):
    threading.Timer(1.0, log_to_influx, args=[sock, db_client]).start()
    try:
      smainfo=sock.recv(600)
      deg=smainfo[28:]
      smatext={}
      currtime = int(time.time())
      while len(deg)>8:
          index=struct.unpack('>b',deg[1:2])[0]
          bytesnext=struct.unpack('>b',deg[2:3])[0]
          deg=deg[4:]
          if bytesnext==4:
              smatext[str(index) +'.'+str(bytesnext)]=struct.unpack('>I',deg[0:bytesnext])[0]
          elif bytesnext==8:
              smatext[str(index) +'.'+str(bytesnext)]=struct.unpack('>q',deg[0:bytesnext])[0]
          deg=deg[bytesnext:]
          print smatext

      json_body = [

            {

                "measurement": "grid",
                "tags": {
                    "phase": "SUMS",
                      },
                "fields": {
                    "active_power+":   smatext['1.4']/10.0,
                    "active_power-":   smatext['2.4']/10.0,
                    "reactive_power+": smatext['3.4']/10.0,
                    "reactive_power-": smatext['4.4']/10.0,
                    "apparent_power+": smatext['9.4']/10.0,
                    "apparent_power-": smatext['10.4']/10.0,
                    "power_factor":    smatext['13.4']/1000.0,
                }

            },
            {

                "measurement": "grid",
                "tags": {
                    "phase": "L1",
                      },
                "fields": {
                    "active_power+":   smatext['21.4']/10.0,
                    "active_power-":   smatext['22.4']/10.0,
                    "reactive_power+": smatext['23.4']/10.0,
                    "reactive_power-": smatext['24.4']/10.0,
                    "apparent_power+": smatext['29.4']/10.0,
                    "apparent_power-": smatext['30.4']/10.0,
                    "current":         smatext['31.4']/1000.0,
                    "voltage":         smatext['32.4']/1000.0,
                    "power_factor":    smatext['33.4']/1000.0,

                }

            },
             {

                "measurement": "grid",
                "tags": {
                    "phase": "L2",
                      },
                "fields": {
                    "active_power+":   smatext['41.4']/10.0,
                    "active_power-":   smatext['42.4']/10.0,
                    "reactive_power+": smatext['43.4']/10.0,
                    "reactive_power-": smatext['44.4']/10.0,
                    "apparent_power+": smatext['49.4']/10.0,
                    "apparent_power-": smatext['50.4']/10.0,
                    "current":         smatext['51.4']/1000.0,
                    "voltage":         smatext['52.4']/1000.0,
                    "power_factor":    smatext['53.4']/1000.0,

                }

            },
            {

                "measurement": "grid",
                "tags": {
                    "phase": "L3",
                      },
                "fields": {
                    "active_power+":   smatext['61.4']/10.0,
                    "active_power-":   smatext['62.4']/10.0,
                    "reactive_power+": smatext['63.4']/10.0,
                    "reactive_power-": smatext['64.4']/10.0,
                    "apparent_power+": smatext['69.4']/10.0,
                    "apparent_power-": smatext['70.4']/10.0,
                    "current":         smatext['71.4']/1000.0,
                    "voltage":         smatext['72.4']/1000.0,
                    "power_factor":    smatext['73.4']/1000.0,

                }

            },

        ]
      print json_body
#      db_client.write_points(json_body)
    finally:
        pass

log_to_influx(sock, db_client)
