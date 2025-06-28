#!/usr/bin/python3
import asyncio
import tomllib
import subprocess
from client_side import Client


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
    final_result = {}
    with open("conf.toml", mode="rb") as fp:
        config = tomllib.load(fp)
    AP = Client(*[value for key,value in config["AP_info"].items()])

    wifi_channels,ht_modes =  await AP.get_wifi_capabilities()
    print("Starting tests")

    for channel in wifi_channels:
        final_result[channel] = {}
        for htmode in ht_modes:
            print(f"Setting channel:{channel} and htmode: {htmode}")
            if config["AP_info"]["os"]: await AP.set_wifi_capabilities_OpenWrt(channel,htmode)
            await asyncio.sleep(1)
            skip = False
            for x in range(0,4,1):
                if AP.connection_status():
                    break
                else:
                    if x == 3:
                        print(f"Reconnect tries are gone, probably AP is not capable to work on channel {channel} with htmode {htmode}.\nHint: "
                              f"if you are sure that AP is capable to work with this physical signal configuration increase the timeout time")
                        skip = True
                    else:
                        print("AP is offline, waiting for set up time")
                    await asyncio.sleep(1)
            if skip: continue
            result = await AP.getter(config["locals"]["wifi_ip"],config["defaults"]["timeout"])
            await asyncio.sleep(int(config["defaults"]["timeout"]))
            final_result[channel][htmode] = result
            print(final_result)

    print(final_result)




asyncio.run(main())
