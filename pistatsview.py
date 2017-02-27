###############################################################################
## Name: pistatsview.py
## Author: Beichen Liu
## Date: 2.23.2017
## Description: This script is used to monitor, store, and display the hosts 
##              info
## TODO: loop
##       database
#!/usr/bin/env python3
import os
import time
import json   
import pymongo # database
import pika    
from RabbitMQClient import MQClient, Consumer 
import argparse

stats = '{ "net": {"lo": {"rx": 5,"tx": 3},"wlan0": {"rx": 708,"tx": 1192}, \
          "eth0": {"rx": 2,"tx":1}},"cpu": 0.2771314211797171}'

Data = json.loads(stats)


def argvparser():
    global arg
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', nargs=1,dest='msgbroker',\
                        help="This is the IP address or named address \
                        of the message broker to connect to")
    parser.add_argument('-p', nargs=1, 
                        help= "This is the virtual host to connect to on the\
                        message broker. If not specified, should default to \
                        the root virtual host (i.e. ‘/’)")
    parser.add_argument('-c', nargs=1,\
                        help='Use the given credentials when connecting to the\
                        message broker. If not specified,should default to a\
                        guest login')
    parser.add_argument('-k',nargs=1, dest='routkey' ,\
                        help='The routing key to use for filtering when \
                        subscribing to the pi_utilization exchange\
                        on the message broker')
    arg = vars(parser.parse_args())

def init__LED():
    os.system("echo 17 > /sys/class/gpio/export") # blue
    os.system("echo 19 > /sys/class/gpio/export") # green
    os.system("echo 21 > /sys/class/gpio/export") # red
    os.system("echo out > /sys/class/gpio/gpio17/direction")
    os.system("echo out > /sys/class/gpio/gpio19/direction")
    os.system("echo out > /sys/class/gpio/gpio21/direction")

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

def recv(msg):
    global Data
    Data = json.loads(msg)

def receive(msgbroker,routingkey,vhost='/',credentials='guest'):
    if credentials != "guest":
        credentials = str(credentials).split(':'); 
        try:
        #create connection
            client = MQClient(msgbroker,'tester1',credentials[0],\
                              credentials[1],vhost,Consumer.Debug)
            client.subscribe(recv)
        except KeyboardInterrupt:
            print("Exiting...")
    else :	
        try:
            #create connection
            client = MQClient(msgbroker,'tester1','guest','guest',\
                              vhost,Consumer.Debug)
            client.subscribe(recv)
        except KeyboardInterrupt:
            print("Exiting...")

def savedb(data):
    db = pymongo.MongoClient().hw2
    db.utilization.insert(data)

def run():
    if(arg['c']!= 'None' and arg['p']!= 'None'):
        receive(arg['msgbroker'],arg['routkey'],arg['p'],arg['c'])
    elif(arg['c']!= 'None'):
        receive(arg['msgbroker'],arg['routkey'],credential = arg['c'])
    elif(arg['p']!='None'):
        receive(arg['msgbroker'],arg['routkey'],vhost = arg['p'])
    else:
        receive(arg['msgbroker'],arg['routkey'])


def Print(host,data):
    CPUHigh = 0
    CPULow = 10000

    loHighRX = 0
    loLowRX = 10000
    loHighTX = 0
    loLowTX = 10000

    eth0HighRX = 0
    eth0LowRX = 10000
    eth0HighTX = 0
    eth0LowTX = 10000

    wlan0HighRX = 0
    wlan0LowRX = 10000
    wlan0HighTX = 0
    wlan0LowTX = 10000

    if data['cpu'] > CPUHigh:
        CPUPHigh = data['cpu']
    if data['cpu'] < CPULow:
        CPULow = data['cpu']

    if data['net']['lo']['rx']> loHighRX:
        loHighRX = data['net']['lo']['rx'] 
    if data['net']['lo']['rx'] < loLowRX:
        loLowRX = data['net']['lo']['rx']
    if data['net']['lo']['tx']> loHighTX:
        loHighTX = data['net']['lo']['tx'] 
    if data['net']['lo']['tx'] < loLowTX:
        loLowTX = data['net']['lo']['tx']

    if data['net']['eth0']['rx']> eth0HighRX:
        eth0HighRX = data['net']['eth0']['rx'] 
    if data['net']['eth0']['rx'] < eth0LowRX:
        eth0LowRX = data['net']['eth0']['rx']
    if data['net']['eth0']['tx']> eth0HighTX:
        eth0HighTX = data['net']['eth0']['tx'] 
    if data['net']['eth0']['tx'] < eth0LowTX:
        eth0LowTX = data['net']['eth0']['tx']

    if data['net']['wlan0']['rx']> wlan0HighRX:
        wlan0HighRX = data['net']['wlan0']['rx'] 
    if data['net']['wlan0']['rx'] < wlan0LowRX:
        wlan0LowRX = data['net']['wlan0']['rx']
    if data['net']['wlan0']['tx']> wlan0HighTX:
        wlan0HighTX = data['net']['wlan0']['tx'] 
    if data['net']['wlan0']['tx'] < wlan0LowTX:
        wlan0LowTX = data['net']['wlan0']['tx']
 
    print(host);
    print("cpu: ", data['cpu'],
          "[Hi: ", CPUHigh, ","\
          " Lo: ", CPULow,"]");
    print("lo: rx=",data['net']['lo']['rx']," B/s",\
          "[Hi: ",  loHighRX, " B/s,",\
          " Lo: ",  loLowRX,  " B/s],",\
          " tx= ",  data['net']['lo']['tx']," B/s",\
          " [Hi: ", loHighTX, " B/s,",\
          " Lo: ",  loLowTX,  " B/s]")
    print("eth0: rx=",data['net']['eth0']['rx'],"B/s",
          "[Hi: ",  eth0HighRX, " B/s,",\
          " Lo: ",  eth0LowRX,  " B/s],",\
          " tx= ",  data['net']['eth0']['tx']," B/s",\
          " [Hi: ", eth0HighTX, " B/s,",\
          " Lo: ",  eth0LowTX,  " B/s]")
    print("wlan0: rx=",data['net']['wlan0']['rx']," B/s ",\
          "[Hi: ", wlan0HighRX, " B/s,",\
          " Lo: ", wlan0LowRX,  " B/s],",\
          " tx= ", data['net']['wlan0']['tx']," B/s ",\
          "[Hi: ", wlan0HighTX, " B/s,",\
          " Lo: ", wlan0LowTX, " B/s]")
    time.sleep(1)


      
def main():
    argvparser()
    init__LED()
    run()
    Print("Host_1", Data)
    savedb(Data)
    LED(data['cpu'])
    

main()    


