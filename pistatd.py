## Author:  Hao Gu
## File:    pistatd.py
## Date:    02/24/2017
## Purpose: Send a json object with CPU and Network stats to clients
# !/usr/bin/env python3

import json
import time

class CPU:
    def __init__(self):
        f = open('/proc/uptime', 'r')
        self.string = f.read()
        #self.string = '7342.09 33222.32\n'

    @property
    #split the file information into a list
    def parse_stat(self):
        list = self.string.split()
        return list

    #print the cpu utilization every 1 sec
    def calculate_util(self):
        alist = self.parse_stat
        previous_uptime = int(alist[0])
        previous_idle = int(alist[1])
        time.sleep(1)
        while True:
            alist = self.parse_stat
            uptime = alist[0]
            idle = alist[1]
            utilization = 1 - ((idle - previous_idle)/(uptime - previous_uptime))
            print (utilization)
            time.sleep(1)
            previous_idle = idle
            previous_uptime = uptime

