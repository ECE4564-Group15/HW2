## Author:  Hao Gu
## File:    test_pistatd.py
## Date:    02/24/2017
## Purpose: This file is to test the functionality of pistatd.py
# !/usr/bin/env python3

from pistatd import CPU

def test_print_util():
    a = CPU()
    a.print_util()


def main():
    test_print_util()

main()