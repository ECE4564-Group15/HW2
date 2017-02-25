#!/usr/bin/env python3
# coding=utf-8

class Net_stat:
    def get_stat(self):
        inputfile = open('/proc/net/dev')
        text = inputfile.readlines()[2:]
        for line in text:
            list = line.split()
            print (list)

            if list[0] == 'wlan0:':
                print(list[1], ' ', list[9]),
            if list[0] == 'eth0:':
                print(list[1], ' ', list[9])


def main():
    a = Net_stat()
    a.get_stat()


main()
