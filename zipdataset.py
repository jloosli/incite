#!/usr/bin/python
# -*- coding: utf8 -*-

import zipfile
import os
import requests


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


if __name__ == '__main__':
    main()
