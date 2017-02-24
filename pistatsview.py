#!/usr/bin/env python3
import time
import json
import pymongo

stats = '{ "net": {"lo": {"rx": 0,"tx": 0},"wlan0": {"rx": 708,"tx": 1192},"eth0": {"rx": 0,"tx":0}},"cpu": 0.2771314211797171}'

data = json.loads(stats)

def Print(data):
    while True:
        print("Host_1: ");
        print("cpu: ", data['cpu']);
        print("lo: rx=",data['net']['lo']['rx'])
        time.sleep(1)

def main():
    Print(data)

main()
