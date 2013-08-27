#!/usr/bin/python
# -*- coding: utf8 -*-

import sys, logging, os, traceback
theDir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(theDir, 'data/samples.db')
logger=logging.getLogger('mylogger')
hdlr = logging.FileHandler(os.path.join(theDir,'error.log'))
formatter = logging.Formatter('%(asctime)s - ln:%(lineno)s - [%(levelname)s] - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
def my_handler(type, value, tb):
  logger.exception("Uncaught exception: {0}  \nline: {1}".format(str(value), traceback.tb_lineno(tb)))

sys.excepthook = my_handler

logger.info("Logger started")


from adafruit.Adafruit_ADS1x15.Adafruit_ADS1x15 import ADS1x15
from gpsPoller import GpsPoller
import time, math, sqlite3, os, signal, sys, logging
import datetime
from adafruit.Adafruit_LEDBackpack.Adafruit_8x8 import EightByEight
from adafruit.Adafruit_LEDBackpack import Adafruit_LEDBackpack
import pprint
pp = pprint.PrettyPrinter(indent=4)


# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
grid = EightByEight(address=0x70)
led = Adafruit_LEDBackpack.LEDBackpack(0x70)
led.setBrightness = 1
hasGrid = True
displayChannels = 2



def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

display = 0

# ============================================================================
# Example Code
# ============================================================================
ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01  # 16-bit ADC

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ToDo: Change the value below depending on which chip you're using!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ADS_Current = ADS1115

# Initialise the ADC using the default mode (use default I2C address)
adc = ADS1x15(ic=ADS_Current, debug=True)

conn = sqlite3.connect(filename)
c = conn.cursor()
# c.execute('SHOW databases')
# print c.fetchall()

c.execute('SELECT max(dataset) FROM samples')
results = c.fetchone()
dataset = results[0] if results[0] is not None else -1
dataset += 1
logger.info("Dataset: %d" % dataset)
# c.execute('SELECT * FROM samples WHERE dataset = ?', (dataset - 1,))
# for row in c.fetchall():
#     print row
conn.commit()
conn.close()

withoutGPS = "insert into samples(dataset,date,ch0,ch1,ch2,ch3) values (?, ?, ?, ?, ?, ?)"
withGPS = "insert into samples(dataset,date,ch0,ch1,ch2,ch3,lat,lon,speed, gpstime) values (?, ?, ?, ?, ?, ?,?,?,?,?)"

try:
  g=GpsPoller()
  g.start()
except Exception, e:
  g = False



while 1:
  ch = [0,0,0,0]
  for i in range(0,4):
    result = adc.readADCSingleEnded(i,6144)
    ch[i]=result
  print "{0:.6f} {1:.6f} {2:.6f} {3:.6f}".format(*ch)


  current = g.get_current_value()
  gpsData=None
  if 'TPV' in current:
    gpsData=current['TPV']


  conn = sqlite3.connect(filename)
  c = conn.cursor()
  ts = datetime.datetime.now()
  if gpsData != None and set(gpsData.keys()).issuperset(['lat','lon','speed','time']):
    c.execute(withGPS,
              (dataset, ts, ch[0],ch[1],ch[2],ch[3],gpsData['lat'],gpsData['lon'],gpsData['speed'],gpsData['time']))
  else:
    c.execute(withoutGPS, (dataset, ts, ch[0],ch[1],ch[2],ch[3]))
  conn.commit()
  conn.close()

  if hasGrid and grid.clear() == -1:
    hasGrid = False



  if hasGrid:
    steps=[None]*displayChannels
    for i in range(displayChannels):
      steps[i] = int(math.floor(ch[i] / 5000 * 64 / displayChannels))
      fullrows = int(math.floor(steps[i]/8))
      partrows = int(steps[i] % 8)
      for x in range(fullrows):
        for y in range(8):
          grid.setPixel(x+i*8/displayChannels,y)
      for y in range(partrows):
        grid.setPixel(fullrows+i*8/displayChannels,y)
    # print "Channels: %.3f, %.3f, %.3f, %.3f V" % (ch[0],ch[1],ch[2],ch[3])
    # print "Steps = %d" % (steps)
    # i=0
    # for x in range(0, 8):
    #   for y in range(0, 8):
    #     if i < steps:
    #       grid.setPixel(x, y)
    #     i += 1

  time.sleep(.1)
