## Author:  Hao Gu
## File:    pistatd.py
## Date:    02/24/2017
## Purpose: Send a json object with CPU and Network stats to clients
# !/usr/bin/env python3

from __future__ import print_function
from RabbitMQClient import MQClient, Publisher
import socket
import json
import time
import argparse


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


IP_ADDRESS = get_ip_address()


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
            # print (list)

            if list[0] == 'wlan0:':
                wlan = Net_key(list[1], list[9])
            if list[0] == 'lo:':
                lo = Net_key(list[1], list[9])
            if list[0] == 'eth0:':
                eth = Net_key(list[1], list[9])
        return [wlan, lo, eth]


class Util:

    # print the cpu utilization every 1 sec
    def print_util(self):
        '''
        message_broker = arg['msgbroker']
        if (arg['p'] == None):
            virtual_host = '/'
        else:
            virtual_host = arg['p']
        if (arg['c']):
            login = 'guest'
            password = 'guest'
        else:
            login_password = arg['c']
            words = login_password.split(':')
            login = words[0]
            password = words[1]
        routing_key = arg['routkey']
        # create a connection
        #client = MQClient(message_broker, routing_key, login, password, virtual_host, Publisher.Normal)
        '''
        message_broker = arg['msgbroker']
        mes = message_broker[0]

        if (arg['p'] == None):
            virtual_host = '/'
        else:
            vhost = arg['p']
            virtual_host = vhost[0]

        routkey = arg['routkey']
        routing_key = routkey[0]

        if (arg['c'] == None):
            login = 'guest'
            password = 'guest'
        else:
            login_password_list = arg['c']
            login_password = login_password_list[0]
            words = login_password.split(':')
            login = str(words[0])
            password = str(words[1])
        #print (message_broker)

        #client = MQClient(mes, 'tester1', 'Usage', 'team15', ' ', Publisher.Debug)
        client = MQClient(mes, routing_key, login, password, virtual_host, Publisher.Debug)
        last_idle = last_total = 0
        last_wlan_receive = last_wlan_transmit = 0
        last_lo_receive = last_lo_transmit = 0
        last_eth_receive = last_eth_transmit = 0

        try:
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

                last_wlan_receive, last_wlan_transmit = net_list[0].receive_bytes, net_list[0].transmit_bytes
                last_lo_receive, last_lo_transmit = net_list[1].receive_bytes, net_list[1].transmit_bytes
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

                json_obj = json.dumps(d, sort_keys=True, indent=4)
                #print(json_obj)
                client.send_message(json_obj)

                #client.send_message('guhao')
                time.sleep(1)

        except KeyboardInterrupt:
            print("Exit Program")



def argvparser():
    global arg
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', nargs=1, dest='msgbroker',
                        help="This is the IP address or named address "
                             "of the message broker to connect to")
    parser.add_argument('-p', nargs=1,
                        help="This is the virtual host to connect to on the "
                             "message broker. If not specified, should default to "
                             "the root virtual host (i.e. ‘/’)")
    parser.add_argument('-c', nargs=1,
                        help='Use the given credentials when connecting to the '
                             'message broker. If not specified,should default to a '
                             'guest login')
    parser.add_argument('-k', nargs=1, dest='routkey',
                        help='The routing key to use for filtering when '
                             'subscribing to the pi_utilization exchange '
                             'on the message broker')
    arg = vars(parser.parse_args())


def main():
    argvparser()
    a = Util()
    a.print_util()
    '''
    client = MQClient('127.0.0.1', 'tester1', 'Usage', 'team15', 'usage_vhost', Publisher.Debug)

    while True:
        client.send_message('guhao')
        time.sleep(0.5)
    '''
main()
