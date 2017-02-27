#!/usr/bin/env python3

from RabbitMQClient import MQClient, Publisher

def main():
    #create a connection
    client = MQClient('127.0.0.1','tester1','Usage','team15','usage_vhost',Publisher.Debug)

    try:
        while True:
            msg = input('> ')
            client.send_message(msg)
    except KeyboardInterrupt:
        print("Exiting...")

main()
