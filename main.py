#!/usr/bin/python3
import iperf_tester
import wifi_capabilities


import subprocess
import sys
from sys import argv
import platform
import os.path
import argparse


def main():
    wifi_if = 'wlp1s0'
    isAP = wifi_capabilities.AP_check(wifi_if)#check if our interface is Wi-Fi AP



















if __name__ == '__main__':
    main()