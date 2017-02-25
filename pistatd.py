## Author:  Hao Gu
## File:    pistatd.py
## Date:    02/24/2017
## Purpose: Send a json object with CPU and Network stats to clients
# !/usr/bin/env python3

from __future__ import print_function
import json
import time

class Net_key:
    def __init__(self, r, t):
        self.receive_bytes = float(r)
        self.transmit_bytes = float(t)

class Net_stat:
    def get_stat(self):
        inputfile = open('/proc/net/dev')
        text = inputfile.readlines()[2:]
        for line in text:
            list = line.split()
            #print (list)

            if list[0] == 'wlan0:':
                wlan = Net_key(list[1],list[9])
            if list[0] == 'lo:':
                lo = Net_key(list[1], list[9])
            if list[0] == 'eth0:':
                eth = Net_key(list[1], list[9])
        return [wlan, lo, eth]


class Util:
    # print the cpu utilization every 1 sec
    def print_util(self):
        last_idle = last_total = 0
        last_wlan_receive = last_wlan_transmit = 0
        last_lo_receive = last_lo_transmit = 0
        last_eth_receive = last_eth_transmit = 0

        while True:
            with open('/proc/stat') as f:
                fields = [float(column) for column in f.readline().strip().split()[1:]]
            idle, total = fields[3], sum(fields)
            idle_delta, total_delta = idle - last_idle, total - last_total
            last_idle, last_total = idle, total
            utilisation = (1.0 - idle_delta / total_delta)

            a = Net_stat()
            net_list = a.get_stat()

            wlan_receive = net_list[0].receive_bytes - last_wlan_receive
            wlan_transmit = net_list[0].transmit_bytes - last_wlan_transmit
            lo_receive = net_list[1].receive_bytes - last_lo_receive
            lo_transmit = net_list[1].transmit_bytes - last_lo_transmit
            eth_receive = net_list[2].receive_bytes - last_eth_receive
            eth_transmit = net_list[2].transmit_bytes - last_eth_transmit

            last_wlan_receive,last_wlan_transmit = net_list[0].receive_bytes, net_list[0].transmit_bytes
            last_lo_receive,last_lo_transmit = net_list[1].receive_bytes, net_list[1].transmit_bytes
            last_eth_receive, last_eth_transmit = net_list[2].receive_bytes, net_list[2].transmit_bytes

            d = {}
            d['net'] = {}
            d['net']['lo'] = {}
            d['net']['lo']['rx'] = lo_receive
            d['net']['lo']['tx'] = lo_transmit
            d['net']['wlan0'] = {}
            d['net']['wlan0']['rx'] = wlan_receive
            d['net']['wlan0']['tx'] = wlan_transmit
            d['net']['eth0'] = {}
            d['net']['eth0']['rx'] = eth_receive
            d['net']['eth0']['tx'] = eth_transmit
            d['cpu'] = utilisation

            print(json.dumps(d, sort_keys=True, indent=4))
            #print(d)
            '''
            print(wlan_receive,wlan_transmit,lo_receive,lo_transmit,eth_receive,eth_transmit)
            print('utilization is ', utilisation)
            '''
            time.sleep(1)
