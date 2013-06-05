#!/usr/bin/python
# -*- coding: utf8 -*-

import zipfile
import os
import requests
import re
import subprocess
import sqlite3
import json
import base64


def getUnique():
    uniqueID = ""
    try:
        cpuinfo = subprocess.check_output('cat /proc/cpuinfo | grep Serial', shell=True)
        serialRE = re.compile(r':(.+)')
        serialResult = re.search(serialRE, cpuinfo)
        if serialResult:
            uniqueID = serialResult.group(1)
    except subprocess.CalledProcessError, e:
        print "cpuinfo not available"

    if uniqueID == "":
        try:
            ifconfig = subprocess.check_output('ifconfig | grep -B3 "BROADCAST RUNNING"', shell=True).splitlines()
            mac = re.compile(r"HWaddr ([a-z0-9:]+)")
            for line in ifconfig:
                macResult = re.search(mac, line)
                if macResult:
                    uniqueID = macResult.group(1)
                    break
        except subprocess.CalledProcessError, e:
            print "No connection"
    return uniqueID

class zipData:

    def setFile(self, name):
        self.filename = name

    def setData(self, data):
        self.data = data

    def write(self):
        print self.filename
        csvfile = open('tempdata.csv','w')
        writer = csv.writer(csvfile)
        writer.writerows(self.data)
        csvfile.close()
        with zipfile.ZipFile(self.filename, 'w') as theZip:
            theZip.write(csvfile.name)
        os.remove('tempdata.csv')



def main():
    theDir = os.path.dirname(os.path.abspath(__file__))
    dbfilename = os.path.join(theDir, 'data/samples.db')
    zipfilename = os.path.join(theDir, 'data/samples.zip')

    print "Creating Zip File"
    with zipfile.ZipFile(zipfilename,'w') as dbzip:
        dbzip.write(dbfilename, arcname='samples.db')
    print "Zip file created"

    print "Uploading file"
    url = 'http://incite.avantidevelopment.com/sampleupload.php'
    files = {'file': ('samples.zip', open(zipfilename, 'rb'))}

    r = requests.post(url, files=files)
    print r.text
    print "File uploaded"
    print 'Process completed'

def main2():
    theDir = os.path.dirname(os.path.abspath(__file__))
    dbfilename = os.path.join(theDir, 'data/samples.db')
    unique = getUnique()
    payload = {'check' : 1, 'unique' : unique}

    url = 'http://incite.avantidevelopment.com/sampleupload.php'
    # url = 'http://localhost/incite/sampleupload.php'

    try:
        r = requests.post(url, data=payload)
        print r.text
        init = r.json()
        print init
        conn = sqlite3.connect(dbfilename)
        c = conn.cursor()
        hasResults = True;
        nextval = init['nextval']
        while hasResults:
            c.execute('SELECT * FROM samples WHERE id > ? LIMIT ?', (nextval, init['receive']))
            results = c.fetchall()
            print len(results)
            if len(results) != 0 and len(results) == int(init['receive']):
                keys = [(x[0] if x[0] != "id" else "sys_id") for x in c.description]
                # print keys
                # print results
                dataload = {
                    'keys': json.dumps(keys), 
                    'datasets': base64.b64encode(json.dumps(results)), 
                    'unique' : unique
                }
                # print dataload
                r = requests.post(url, data=dataload)
                print r.text
                nextval += init['receive']
                if 'success' in r.json().keys() and r.json()['success'] == 1:
                    hasResults = True
                else:
                    hasResults = False

            else:
                hasResults = False



    except requests.exceptions.ConnectionError, e:
        print "No internet connection"




if __name__ == '__main__':
    main2()
    #main()
