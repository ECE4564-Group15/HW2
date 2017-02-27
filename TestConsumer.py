#!/usr/bin/env python3

#simple consumer example

from RabbitMQClient import MQClient, Consumer

def on_recv(message):
    print("GOT: '%s'" % (str(message),))

def main():
    try:
        #create connection
        client = MQClient('127.0.0.1','tester1','Usage','team15','usage_vhost',Consumer.Debug)

        client.subscribe(on_recv)
    except KeyboardInterrupt:
        print("Exiting...")
main()
