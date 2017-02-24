## Author:  Hao Gu
## File:    pistatd.py
## Date:    02/24/2017
## Purpose: Send a json object with CPU and Network stats to clients
# !/usr/bin/env python3

import json
import time


class CPU:
    # split the file information into a list
    def parse_stat(self):
        list = self.string.split()
        return list

    def calculate_util(self, idle, previous_idle, uptime, previous_uptime):
        utilization = 1 - ((float(idle) - float(previous_idle)) / (float(uptime) - float(previous_uptime)))
        return utilization

    # print the cpu utilization every 1 sec
    def print_util(self):
        f = open('/proc/uptime', 'r')
        self.string = f.read()
        alist = self.parse_stat
        previous_uptime = alist[0]
        previous_idle = alist[1]
        time.sleep(1)
        while True:
            f = open('/proc/uptime', 'r')
            self.string = f.read()
            alist = self.parse_stat
            uptime = alist[0]
            idle = alist[1]
            utilization = self.calculate_util(idle, previous_idle, uptime, previous_uptime)
            previous_idle = idle
            previous_uptime = uptime
            print(utilization)
            time.sleep(1)
