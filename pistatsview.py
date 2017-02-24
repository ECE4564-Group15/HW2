###############################################################################
## Name: pistatsview.py
## Author: Beichen Liu
## Date: 2.23.2017
## Description: This script is used to monitor, store, and display the hosts 
##              info
## TODO: loop
##       database
##       find high and low
#!/usr/bin/env python3
import os
import time
import json   
# import pymongo # database
# import pika    
# from RabbitMQClient import MQClient, Consumer 
import argparse

stats = '{ "net": {"lo": {"rx": 0,"tx": 0},"wlan0": {"rx": 708,"tx": 1192}, \
          "eth0": {"rx": 0,"tx":0}},"cpu": 0.2771314211797171}'

data = json.loads(stats)


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
    global data
    data = json.loads(msg)

def receive(msgbroker,routingkey,vhost='/',credentials='guest'):
    if credentials != 'guest':
        credentials = credentials.split(':'); 
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
            client = MQClient(msgbroker,'tester1','Usage','team15',\
                              vhost,Consumer.Debug)
            client.subscribe(recv)
        except KeyboardInterrupt:
            print("Exiting...")
def run():
    if(c!= 'None' && c!= 'None'):
        receive(msgbroker,routingkey,p,c):
    elif(c!= 'None'):
        receive(msgbroker,routingkey,credential = c):
    elif(p!='None'):
        receive(msgbroker,routingkey,vhost = p):
    else:
        receive(msgbroker,routingkey)


def Print(host,data):
    High = 1
    Low = 0
    print(host);
    print("cpu: ", data['cpu']);
    print("lo: rx=",data['net']['lo']['rx'],"[Hi: ", High, " B/s, Lo: ", \
           Low,  " B/s], tx= ", data['net']['lo']['tx']," B/s [Hi: ",\
            High, " B/s, Lo: ", Low,  " B/s]")
    print("eth0: rx=",data['net']['eth0']['rx'],"[Hi: ", High, " B/s, Lo: ",\
           Low,  " B/s], tx= ", data['net']['eth0']['tx']," B/s [Hi: ", High,\
           " B/s, Lo: ", Low,  " B/s]")
    print("wlan0: rx=",data['net']['wlan0']['rx'],"[Hi: ", High, " B/s, Lo: ",\
           Low,  " B/s], tx= ", data['net']['wlan0']['tx']," B/s [Hi: ", High,\
           " B/s, Lo: ", Low,  " B/s]")
    time.sleep(1)


       
def main():
    argvparser()
    run()
    init__LED()
    Print("Host_1", data)
    LED(data['cpu'])
    

main()    
