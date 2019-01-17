#!/usr/bin/python

#import argparse
import json

#from time import sleep, time, timezone

csvfilename = "VIP_Master_List.csv"
f5filename = "bigip.conf"


#Read JSON data into the datastore variable
csvfile = open(csvfilename, 'r')
f5file = open(f5filename, 'r')
f5result = open("f5output.cfg", 'w')

line = f5file.readline()
while line != "":
    csvline = csvfile.readline()

    while csvline != "":
        csvlist = csvline.split(",")
        if line.find(csvlist[1]) > 0:
            line = line.replace(csvlist[1], csvlist[12])
            print("Changed VS name from: " + csvlist[1] + " to " + csvlist[12])  

        if line.find(csvlist[3]) > 0:
            line = line.replace(csvlist[3], csvlist[13])
            print("Changed IP addr from: " + csvlist[3] + " to " + csvlist[13])

        csvline = csvfile.readline()
    csvfile.seek(0)
    f5result.write(line)
    line = f5file.readline()

csvfile.close()
f5file.close()
f5result.close()