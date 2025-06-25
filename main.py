#!/usr/bin/python3
import asyncio
import tomllib
import subprocess
from client_side import Client
import os

wifi_channels = {
    36: [20, 40, 80],
    40: [20, 40, 80],
    44: [20, 40, 80],
    48: [20, 40, 80],
    52: [20, 40, 80],
    56: [20, 40, 80],
    60: [20, 40, 80],
    64: [20, 40, 80],
    100: [20, 40, 80],
    104: [20, 40, 80],
    108: [20, 40, 80],
    112: [20, 40, 80],
    116: [20, 40, 80],
    120: [20, 40, 80],
    124: [20, 40, 80],
    128: [20, 40, 80],
    132: [20, 40, 80],
    136: [20, 40, 80],
    140: [20, 40, 80],
    144: [20, 40, 80],
    149: [20, 40, 80],
    153: [20, 40, 80],
    157: [20, 40, 80],
    161: [20, 40, 80],
    165: [20, 40, 80],
    169: [20, 40, 80],
    173: [20, 40, 80]
}


def check_defaults(defaults):
    command = [f'-t {defaults["timeout"]}']
    if "bandwidth" in defaults:
        command.append(f"-b {defaults['bandwidth']}")
    if "packet_length" in defaults:
        command.append(f"-l {defaults['packet_length']}")
    if "bidir" in defaults and defaults["bidir"] == 1:
        command.append("--bidir")
    if "fragmentation" in defaults and defaults["fragmentation"] == 0:
        command.append(f"--dont-fragment")
    if "reverse" in defaults and defaults["reverse"] == 1:
        command.append(f"--reverse")

    return ' '.join(command)


def run_cmd(cmd:str):
    print(f"#{cmd}")
    subprocess.run(cmd, shell=True)


async def main():
    final_result = []
    with open("conf.toml", mode="rb") as fp:
        config = tomllib.load(fp)
    AP = Client(*[value for key,value in config["AP_info"].items()])

    print("Starting tests")
    for channel, freq in wifi_channels.items():
            for width in freq :
                print(f"Setting channel:{channel} and bandwidth:{width}MHz")
                if config["AP_info"]["os"]: await AP.set_wifi_capabilities_OpenWrt(channel,width,config["defaults"]["ht_mode"])
                await asyncio.sleep(10)
                skip = False
                for x in range(0,4,1):
                    if AP.connection_status():
                        break
                    else:
                        if x == 3:
                            print(f"Reconnect tries are gone, probably AP is not capable to work on channel {channel} with bandwidth {width}MHz.\nHint: "
                                  f"if you are sure that AP is capable to work with this physical signal configuration increase the timeout time")
                            skip = True
                        else:
                            print("AP is offline, waiting for set up time")
                        await asyncio.sleep(30)
                if skip: continue
                result = await AP.getter(config["locals"]["wifi_ip"],config["defaults"]["timeout"])
                await asyncio.sleep(int(config["defaults"]["timeout"]))
                final_result.append(result)
                print(final_result)


    print(final_result)




asyncio.run(main())
