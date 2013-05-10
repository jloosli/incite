#!/usr/bin/python
# -*- coding: utf8 -*-

import zipfile
import sqlite3
import tempfile
import csv
import os


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
    z = zipData()
    z.setData([[0,1,2,3], [4,5,6,7]])
    z.setFile('temp.zip')
    z.write()

if __name__ == '__main__':
    main()
