#!/usr/bin/python
# -*- coding: utf8 -*-

import zipfile
import os
import requests
import re
import subprocess 


def getUnique():
    uniqueID = ""
    try:
        cpuinfo = subprocess.check_output('cat /proc/cpuinfo | grep Serial', shell=True)
        serialRE = re.compile(r':(.+)')
        serialResult = re.search(cpuinfo, serialRE)
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
    records = 1000
    theDir = os.path.dirname(os.path.abspath(__file__))
    dbfilename = os.path.join(theDir, 'data/samples.db')
    unique = getUnique()
    payload = {'check' : 1, 'mac' : unique}

    url = 'http://incite.avantidevelopment.com/sampleupload.php'
    url = 'http://localhost/incite/sampleupload.php'

    try:
        r = requests.post(url, data=payload)
        print r.json()
    except requests.exceptions.ConnectionError, e:
        print "No internet connection"

    # conn = sqlite3.connect(dbfilename)
    # c = conn.cursor()

   


if __name__ == '__main__':
    main2()
    #main()
