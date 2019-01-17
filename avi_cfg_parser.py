#!/usr/bin/python

#import argparse
import json

from time import sleep, time, timezone
from avi.sdk.avi_api import ApiSession
from avi.sdk.utils.api_utils import ApiUtils
from requests.packages import urllib3

from avi.protobuf import vs_pb2 

#filename = "backup_Default-Scheduler_20180806_100951.json"
filename = "backup_Default-Scheduler_20180802_094433.json"

#Read JSON data into the datastore variable
with open(filename, 'r') as f:
    datastore = json.load(f)

#Use the new datastore datastructure
for obj in datastore["ServiceEngine"]:
    print obj['name']
    print obj['resources']
    #print " " + vs['vrf_context_ref']
    #print " " + vs['cloud_type']
    #print obj

type(vs_pb2)