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


# function to transform HEX to DEC
def hex2dec(s):
    """return the integer value of a hexadecimal string s"""
    return int(s, 16)

# clean exit
def abortprogram(signal,frame):
    # Housekeeping -> nothing to cleanup 
    print('STRG + C = end program')
    sys.exit(0)


def fixold(smainfoasci):
  smaserial=hex2dec(smainfoasci[40:48])
  pregard=hex2dec(smainfoasci[64:72])/10.0
  pregardcounter=hex2dec(smainfoasci[80:96])/3600000.0
  psurplus=hex2dec(smainfoasci[104:112])/10.0
  psurpluscounter=hex2dec(smainfoasci[120:136])/3600000.0
  qregard=hex2dec(smainfoasci[144:152])/10.0
  qregardcounter=hex2dec(smainfoasci[160:176])/3600000.0
  qsurplus=hex2dec(smainfoasci[184:192])/10.0
  qsurpluscounter=hex2dec(smainfoasci[200:216])/3600000.0
  sregard=hex2dec(smainfoasci[224:232])/10.0
  sregardcounter=hex2dec(smainfoasci[240:256])/3600000.0
  ssurplus=hex2dec(smainfoasci[264:272])/10.0
  ssurpluscounter=hex2dec(smainfoasci[280:296])/3600000.0
  cosphi=hex2dec(smainfoasci[304:312])/1000.0
  #L1
  p1regard=hex2dec(smainfoasci[320:328])/10.0
  p1regardcounter=hex2dec(smainfoasci[336:352])/3600000.0
  p1surplus=hex2dec(smainfoasci[360:368])/10.0
  p1surpluscounter=hex2dec(smainfoasci[376:392])/3600000.0
  q1regard=hex2dec(smainfoasci[400:408])/10.0
  q1regardcounter=hex2dec(smainfoasci[416:432])/3600000.0
  q1surplus=hex2dec(smainfoasci[440:448])/10.0
  q1surpluscounter=hex2dec(smainfoasci[456:472])/3600000.0
  s1regard=hex2dec(smainfoasci[480:488])/10.0
  s1regardcounter=hex2dec(smainfoasci[496:512])/3600000.0
  s1surplus=hex2dec(smainfoasci[520:528])/10.0
  s1surpluscounter=hex2dec(smainfoasci[536:552])/3600000.0
  thd1=hex2dec(smainfoasci[560:568])
  v1=hex2dec(smainfoasci[576:584])/1000.0
  cosphi1=hex2dec(smainfoasci[592:600])/1000.0



  #L2
  p2regard=hex2dec(smainfoasci[608:616])/10.0
  p2regardcounter=hex2dec(smainfoasci[624:640])/3600000.0
  p2surplus=hex2dec(smainfoasci[648:656])/10.0
  p2surpluscounter=hex2dec(smainfoasci[664:680])/3600000.0
  q2regard=hex2dec(smainfoasci[688:696])/10.0
  q2regardcounter=hex2dec(smainfoasci[704:720])/3600000.0
  q2surplus=hex2dec(smainfoasci[728:736])/10.0
  q2surpluscounter=hex2dec(smainfoasci[744:760])/3600000.0
  s2regard=hex2dec(smainfoasci[768:776])/10.0
  s2regardcounter=hex2dec(smainfoasci[784:800])/3600000.0
  s2surplus=hex2dec(smainfoasci[808:816])/10.0
  s2surpluscounter=hex2dec(smainfoasci[824:840])/3600000.0
  thd2=hex2dec(smainfoasci[848:856])/1000.0
  v2=hex2dec(smainfoasci[864:872])/1000.0
  cosphi2=hex2dec(smainfoasci[880:888])/1000.0
  #L3
  p3regard=hex2dec(smainfoasci[896:904])/10.0
  p3regardcounter=hex2dec(smainfoasci[912:928])/3600000.0
  p3surplus=hex2dec(smainfoasci[936:944])/10.0
  p3surpluscounter=hex2dec(smainfoasci[952:968])/3600000.0
  q3regard=hex2dec(smainfoasci[976:984])/10.0
  q3regardcounter=hex2dec(smainfoasci[992:1008])/3600000.0
  q3surplus=hex2dec(smainfoasci[1016:1024])/10.0
  q3surpluscounter=hex2dec(smainfoasci[1032:1048])/3600000.0
  s3regard=hex2dec(smainfoasci[1056:1064])/10.0
  s3regardcounter=hex2dec(smainfoasci[1072:1088])/3600000.0
  s3surplus=hex2dec(smainfoasci[1096:1104])/10.0
  s3surpluscounter=hex2dec(smainfoasci[1112:1128])/3600000.0
  thd3=hex2dec(smainfoasci[1136:1144])/1000.0
  v3=hex2dec(smainfoasci[1152:1160])/1000.0
  cosphi3=hex2dec(smainfoasci[1168:1176])/1000.0

  emparts = {'serial':smaserial,'pregard':pregard,'pregardcounter':pregardcounter,'psurplus':psurplus,'psurpluscounter':psurpluscounter,
  'sregard':sregard,'sregardcounter':sregardcounter,'ssurplus':ssurplus,'ssurpluscounter':ssurpluscounter, 
  'qregard':qregard,'qregardcounter':qregardcounter,'qsurplus':qsurplus,'qsurpluscounter':qsurpluscounter,
  'cosphi':cosphi,
  'p1regard':p1regard,'p1regardcounter':p1regardcounter,'p1surplus':p1surplus,'p1surpluscounter':p1surpluscounter,
  's1regard':s1regard,'s1regardcounter':s1regardcounter,'s1surplus':s1surplus,'s1surpluscounter':s1surpluscounter,
  'q1regard':q1regard,'q1regardcounter':q1regardcounter,'q1surplus':q1surplus,'q1surpluscounter':q1surpluscounter,
  'v1':v1,'thd1':thd1,'cosphi1':cosphi1,
  'p2regard':p2regard,'p2regardcounter':p2regardcounter,'p2surplus':p2surplus,'p2surpluscounter':p2surpluscounter,
  's2regard':s2regard,'s2regardcounter':s2regardcounter,'s2surplus':s2surplus,'s2surpluscounter':s2surpluscounter,
  'q2regard':q2regard,'q2regardcounter':q2regardcounter,'q2surplus':q2surplus,'q2surpluscounter':q2surpluscounter,
  'v2':v2,'thd2':thd2,'cosphi2':cosphi2,
  'p3regard':p3regard,'p3regardcounter':p3regardcounter,'p3surplus':p3surplus,'p3surpluscounter':p3surpluscounter,
  's3regard':s3regard,'s3regardcounter':s3regardcounter,'s3surplus':s3surplus,'s3surpluscounter':s3surpluscounter,
  'q3regard':q3regard,'q3regardcounter':q3regardcounter,'q3surplus':q3surplus,'q3surpluscounter':q3surpluscounter,
  'v3':v3,'thd3':thd3,'cosphi3':cosphi3 }
  return emparts



def log_to_influx(sock, db_client):
    threading.Timer(1.0, log_to_influx, args=[sock, db_client]).start()
    try:
      smainfo=sock.recv(600)
      smainfoasci=binascii.b2a_hex(smainfo)
      print smainfoasci
      deg=smainfo[28:]
      smatext={}
      currtime = int(time.time())
      while len(deg)>8:
          index=struct.unpack('>b',deg[1:2])[0]
          print index
          print struct.unpack('>b',deg[1:2])
          bytesnext=struct.unpack('>b',deg[2:3])[0]
          print bytesnext
          print struct.unpack('>b',deg[2:3])
          print len(deg)
          deg=deg[4:]
          print len(deg)
          if bytesnext==4:
              smatext[str(index) +'.'+str(bytesnext)]=struct.unpack('>I',deg[0:bytesnext])[0]
          elif bytesnext==8:
              smatext[str(index) +'.'+str(bytesnext)]=struct.unpack('>q',deg[0:bytesnext])[0]
          deg=deg[bytesnext:]
#          print smatext



      emparts=fixold(smainfoasci)

      print ('\n')
      print ('SMA-EM Serial:{}'.format(emparts['serial']))
      print ('----sum----')
      print ('1P: regard:{}W {}kWh surplus:{}W {}kWh'.format(emparts['pregard'],emparts['pregardcounter'],emparts['psurplus'],emparts['psurpluscounter']))
      print ('2P: regard:{}W {}kWh surplus:{}W {}kWh'.format(smatext['1.4']/10.0,smatext['1.8']/3600000.0,smatext['2.4']/10.0,smatext['2.8']/3600000.0))
      print ('1Q: cap:{}var {}kvarh ind {}var {}kvarh'.format(emparts['qregard'],emparts['qregardcounter'],emparts['qsurplus'],emparts['qsurpluscounter']))
      print ('2Q: cap:{}var {}kvarh ind:{}var {}kvarh'.format(smatext['3.4']/10.0,smatext['3.8']/3600000.0,smatext['4.4']/10.0,smatext['4.8']/3600000.0) )

      print ('1S: regard:{}VA {}kVAh surplus:{}VA {}KVAh'.format(emparts['sregard'],emparts['sregardcounter'],emparts['ssurplus'],emparts['ssurpluscounter']))
      print ('2S: regard:{}VA {}kVAh surplus {}VA {}kVAh'.format(smatext['9.4']/10.0,smatext['9.8']/3600000.0,smatext['10.4']/10.0,smatext['10.8']/3600000.0))


      print ('1cos phi:{}'.format(emparts['cosphi']))
      print ('2cos phi:{}'.format(smatext['13.4']/1000.0))

      print ('----L1----')
      print ('1P: regard:{}W {}kWh surplus:{}W {}kWh'.format(emparts['p1regard'],emparts['p1regardcounter'],emparts['p1surplus'],emparts['p1surpluscounter']))
      print ('2P: regard:{}W {}kWh surplus:{}W {}kWh'.format(smatext['21.4']/10.0,smatext['21.8']/3600000.0,smatext['22.4']/10.0,smatext['22.8']/3600000.0))
      print ('1Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['q1regard'],emparts['q1regardcounter'],emparts['q1surplus'],emparts['q1surpluscounter']))
      print ('2Q: cap:{}var {}kvarh ind:{}var {}kvarh'.format(smatext['23.4']/10.0,smatext['23.8']/3600000.0,smatext['24.4']/10.0,smatext['24.8']/3600000.0) )

      print ('1S: regard:{}VA {}kVAh surplus:{}VA {}kVAh'.format(emparts['s1regard'],emparts['s1regardcounter'],emparts['s1surplus'],emparts['s1surpluscounter']))
      print ('2S: regard:{}VA {}kVAh surplus {}VA {}kVAh'.format(smatext['29.4']/10.0,smatext['29.8']/3600000.0,smatext['30.4']/10.0,smatext['30.8']/3600000.0))

      print ('1i: {}A V:{} '.format(emparts['thd1'],emparts['v1']))
      print ('2i: {}A V:{} '.format(smatext['31.4']/1000.0,smatext['32.4']))

      print ('----L2----')
      print ('1P: regard:{}W {}kWh surplus:{}W {}kWh'.format(emparts['p2regard'],emparts['p2regardcounter'],emparts['p2surplus'],emparts['p2surpluscounter']))
      print ('2P: regard:{}W {}kWh surplus:{}W {}kWh'.format(smatext['41.4']/10.0,smatext['41.8']/3600000.0,smatext['42.4']/10.0,smatext['42.8']/3600000.0))
      print ('1Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['q2regard'],emparts['q2regardcounter'],emparts['q2surplus'],emparts['q2surpluscounter']))
      print ('2Q: cap:{}var {}kvarh ind:{}var {}kvarh'.format(smatext['43.4']/10.0,smatext['43.8']/3600000.0,smatext['44.4']/10.0,smatext['44.8']/3600000.0) )

      print ('1S: regard:{}VA {}kVAh surplus:{}VA {}kVAh'.format(emparts['s2regard'],emparts['s2regardcounter'],emparts['s2surplus'],emparts['s2surpluscounter']))
      print ('2S: regard:{}VA {}kVAh surplus {}VA {}kVAh'.format(smatext['49.4']/10.0,smatext['49.8']/3600000.0,smatext['50.4']/10.0,smatext['50.8']/3600000.0))

      print ('1i: {}A V:{} '.format(emparts['thd2'],emparts['v2']))
      print ('2i: {}A V:{} '.format(smatext['51.4']/1000.0,smatext['52.4']/1000.0))

      print ('----L3----')
      print ('1P: regard:{}W {}kWh surplus:{}W {}kWh'.format(emparts['p3regard'],emparts['p3regardcounter'],emparts['p3surplus'],emparts['p3surpluscounter']))
      print ('2P: regard:{}W {}kWh surplus:{}W {}kWh'.format(smatext['61.4']/10.0,smatext['61.8']/3600000.0,smatext['62.4']/10.0,smatext['62.8']/3600000.0))
      print ('1Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['q3regard'],emparts['q3regardcounter'],emparts['q3surplus'],emparts['q3surpluscounter']))
      print ('2Q: cap:{}var {}kvarh ind:{}var {}kvarh'.format(smatext['63.4']/10.0,smatext['63.8']/3600000.0,smatext['64.4']/10.0,smatext['64.8']/3600000.0) )

      print ('1S: regard:{}VA {}kVAh surplus:{}VA {}kVAh'.format(emparts['s3regard'],emparts['s3regardcounter'],emparts['s3surplus'],emparts['s3surpluscounter']))
      print ('2S: regard:{}VA {}kVAh surplus {}VA {}kVAh'.format(smatext['69.4']/10.0,smatext['69.8']/3600000.0,smatext['70.4']/10.0,smatext['70.8']/3600000.0))

      print ('1i: {}A V:{} '.format(emparts['thd3'],emparts['v3']))
      print ('2i: {}A V:{} '.format(smatext['71.4']/1000.0,smatext['72.4']/1000.0))

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
