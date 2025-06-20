#!/usr/bin/python3
import asyncio
import tomllib
import subprocess
from client_side import Client


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
    132: [20, 40, 80],
    136: [20, 40, 80],
    140: [20, 40, 80],
    144: [20, 40, 80],
    149: [20, 40, 80, 160],
    153: [20, 40, 80, 160],
    157: [20, 40, 80, 160],
    161: [20, 40, 80, 160],
    165: [20, 40, 80],
    169: [20, 40],
    173: [20, 40]
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
    print(config)
    #options = check_defaults(config["defaults"])
    print(config["AP_info"])
    AP = Client(*[value for key,value in config["AP_info"].items()])
    AP.print()
    run_cmd("iperf3 -s -D")
    #Initial check for AP accessibility
    if not AP.connection_status():
        print("FAILED: AP.connection_status()")
        return 0
    if not await AP.ap_status():
        print("FAILED: AP.ap_status()")
        return 0
    if not await AP.credentials_check():
        print("FAILED: AP.ap_status()")
        return 0

    await asyncio.sleep(1)
    print("Starting tests")
    for channel, freq in wifi_channels.items():
            for width in freq:
                print(f"Setting channel and bandwidth: {channel}:{width}MHz")
                if config["AP_info"]["os"]: await AP.set_wifi_capabilities_OpenWrt(channel,width)
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
                result = await AP.getter(config["locals"]["wifi_ip"],config["locals"]["timeout"])
                await asyncio.sleep(int(config["defaults"]["timeout"]))
                final_result.append(result)
                print(result)
                print(final_result)


    print(final_result)




asyncio.run(main())
