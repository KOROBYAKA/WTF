#!/usr/bin/python3
import iperf_tester
import open_socket
import socket

import subprocess
import sys
from sys import argv
import platform
import os.path
import argparse


def main():
    UDP_PORT_NUMBER = 0
    IP_ADDR = socket.gethostbyname(socket.gethostname())
    UDP_SOCKET = open_socket.open_UDP(UDP_PORT_NUMBER, IP_ADDR)


















if __name__ == '__main__':
    main()