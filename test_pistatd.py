## Author:  Hao Gu
## File:    test_pistatd.py
## Date:    02/24/2017
## Purpose: This file is to test the functionality of pistatd.py
# !/usr/bin/env python3

from pistatd import Util

def test_print_util():
    a = Util()
    a.print_util()


def main():
    test_print_util()

main()