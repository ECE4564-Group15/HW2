#!/usr/bin/env python3
import time
import json
import os
# 	import pymongo

stats = '{ "net": {"lo": {"rx": 0,"tx": 0},"wlan0": {"rx": 708,"tx": 1192},"eth0": {"rx": 0,"tx":0}},"cpu": 0.2771314211797171}'

data = json.loads(stats)

def Print(host,data):
    High = 1
    Low = 0
    print(host);
    print("cpu: ", data['cpu']);
    print("lo: rx=",data['net']['lo']['rx'],"[Hi: ", High, " B/s, Lo: ", \
           Low,  " B/s], tx= ", data['net']['lo']['tx']," B/s [Hi: ", High, " B/s, Lo: ", \
           Low,  " B/s]")
    print("eth0: rx=",data['net']['eth0']['rx'],"[Hi: ", High, " B/s, Lo: ", \
           Low,  " B/s], tx= ", data['net']['eth0']['tx']," B/s [Hi: ", High, " B/s, Lo: ", \
           Low,  " B/s]")
    print("wlan0: rx=",data['net']['wlan0']['rx'],"[Hi: ", High, " B/s, Lo: ", \
           Low,  " B/s], tx= ", data['net']['wlan0']['tx']," B/s [Hi: ", High, " B/s, Lo: ", \
           Low,  " B/s]")
    time.sleep(1)

def LED(cpuU) :
   os.system("echo 0 >/sys/class/gpio/gpio17/value")
   os.system("echo 0 >/sys/class/gpio/gpio19/value")
   os.system("echo 0 >/sys/class/gpio/gpio21/value")
   if cpuU <0.25:
       os.system("echo 1 >/sys/class/gpio/gpio19/value")
   elif cpuU >= 0.25 and cpuU < 0.5:
       os.system("echo 1 >/sys/class/gpio/gpio17/value")
   else : 
       os.system("echo 1 >/sys/class/gpio/gpio21/value")

       
def main():
    os.system("echo 17 > /sys/class/gpio/export") # blue
    os.system("echo 19 > /sys/class/gpio/export") # green
    os.system("echo 21 > /sys/class/gpio/export") # red
    os.system("echo out > /sys/class/gpio/gpio17/direction")
    os.system("echo out > /sys/class/gpio/gpio19/direction")
    os.system("echo out > /sys/class/gpio/gpio21/direction")
    Print("Host_1", data)
    LED(data['cpu'])
    

main()
