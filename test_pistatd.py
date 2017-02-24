## Author:  Hao Gu
## File:    test_pistatd.py
## Date:    02/24/2017
## Purpose: This file is to test the functionality of pistatd.py
# !/usr/bin/env python3

from pistatd import CPU

def test_cpu_parse_stat():
    a = CPU()
    list = a.parse_stat
    print('The list is ', list)

def test_calculate_util():
    a = CPU()
    a.calculate_util()


def main():
    test_cpu_parse_stat()
    test_calculate_util()

main()