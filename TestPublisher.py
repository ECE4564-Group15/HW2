#!/usr/bin/env python3

from RabbitMQClient import MQClient, Publisher

def main():
    #create a connection
    client = MQClient('172.29.35.28','tester1',Publisher.Debug)

    try:
        while True:
            msg = input('> ')
            client.send_message(msg)
    except KeyboardInterrupt:
        print("Exiting...")

main()
