#!/usr/bin/python

import serial
import sqlite3 as db
from time import sleep
from threading import Thread
import random
import time, datetime



class GPS:
	formats = {
	'$GPRMC' : ('format','time','validity','lat','ns','lng','ew',
		'speed','course','date','var','ew_checksum')
	}

	def decode(self,gpsString):
		parts=gpsString.split(',');
		if parts[0] in self.formats.keys():
			return dict(zip(self.formats[parts[0]], parts))
		#raise Exception("Can't find format")
		return None


class DataLog:
	con=db.connect('/home/jared/django/projects/football/football.db')
	cur = con.cursor()
	currentSet = None
	g=GPS()

	def log(self, vals):
		if not self.currentSet: self.newSet()
		sql = "INSERT INTO gps_datum(dataset_id,gpsstring,speed) values (?,?,?)"
		self.cur.execute(sql, (self.currentSet,vals,self.g.decode(vals)['speed']))
		self.con.commit()

	def newSet(self):
		sql = "INSERT INTO gps_dataset(start) VALUES (?)"
		self.cur.execute(sql, (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
		self.con.commit()
		self.currentSet=self.cur.lastrowid

	def __del__(self):
		self.cur.close()
		self.con.close()

class Display():
	g=GPS()
	l=DataLog()
	def run(self):
		while True:
			data=self.input.readline()
			if data: 
				if data.startswith('$GPRMC'):
					decoded=self.g.decode(data) 
					print decoded
					print ("Data is %s" % ("valid" if decoded['validity']=="A" else "not valid"))
					print ("Speed is %s " % decoded['speed'])
					print(data)
					self.l.log(data)
			# sleep(1)




t=Display()
t.input= serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
t.run()

'''
$GPRMC speed/lat/long
$GPGSA # of satellites
$GPGGA time
$GPGSV 
'''
# g=GPS()
# decoded = g.decode('$GPRMC,225446,A,4916.45,N,12311.12,W,020.5,054.7,191194,020.3,E*68')
# print decoded['speed']
# print decoded
