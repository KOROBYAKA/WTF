#!/usr/bin/python3
import asyncio

import iperf_tester
import wifi_capabilities
import client_side
from client_side import Client
import time
import subprocess
import sys
import platform
import os.path
import argparse


wifi_channels = {
    36: [20, 40, 80, 160],
    40: [20, 40, 80, 160],
    44: [20, 40, 80, 160],
    48: [20, 40, 80, 160],
    52: [20, 40, 80, 160],
    56: [20, 40, 80, 160],
    60: [20, 40, 80, 160],
    64: [20, 40, 80, 160],
    100: [20, 40, 80, 160],
    104: [20, 40, 80, 160],
    108: [20, 40, 80, 160],
    112: [20, 40, 80, 160],
    116: [20, 40, 80, 160],
    120: [20, 40, 80, 160],
    124: [20, 40, 80, 160],
    128: [20, 40, 80, 160],
    132: [20, 40, 80, 160],
    136: [20, 40, 80, 160],
    140: [20, 40, 80, 160],
    144: [20, 40, 80],
    149: [20, 40, 80, 160],
    153: [20, 40, 80, 160],
    157: [20, 40, 80, 160],
    161: [20, 40, 80, 160],
    165: [20, 40, 80],
    169: [20, 40],
    173: [20, 40]
}







def run_cmd(cmd:str):
    print(f"#{cmd}")
    time.sleep(0.05)


async def main():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Wi-Fi interface and IP addresses for AP and client")
    parser.add_argument("--interface", "-i", help="Access Point interface", type=str, required=True)
    parser.add_argument("--client", "-c", help="Client device IP address", type=str, required=True)
    parser.add_argument("--AP_IP", "-B", help="Access Point interface IP address", type=str, required=True)
    parser.add_argument("--special_mode","-sm",help = "Specify bandwidth to be tested on all channels(optional)",
                        type=str)
    parser.add_argument("--client_user","-usr", help = "Specify client device user to run throughput util",
                        type = str, required=True)
    parser.add_argument("--client_passwd", '-passwd', help = "Specify the password of client to be used",
                         type=str, required=True)
    args = parser.parse_args()

    wifi_iface = args.interface
    client_IP = args.client
    AP_IP = args.AP_IP
    special_mode = args.special_mode
    client = Client(ip=args.client,passwd=args.client_passwd,usr_name=args.client_user)
    client.status = client.check_client()
    isAP = wifi_capabilities.AP_check(wifi_iface)#check if our interface is Wi-Fi AP


#TODO
 #add test logic


            #TODO
            #add logic that skip channel settings after 4 failed reconnects



asyncio.run(main())