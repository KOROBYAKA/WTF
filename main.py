#!/usr/bin/python3
import asyncio
import tomllib
import time



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
    time.sleep(0.1)


async def main():
    with open("conf.toml", mode="rb") as fp:
        config = tomllib.load(fp)

    options = check_defaults(config["defaults"])
    print(options)


    '''isAP = wifi_capabilities.AP_check(wifi_iface)#check if our interface is Wi-Fi AP
    ch_num = 36
    channel = wifi_channels[ch_num]
    i = 0
    bw = 0
    while isAP:
        if (channel[-1] == bw):
            ch_num += 4
            channel = wifi_channels[ch_num]
            i = 0
            bw = 0
        bw = channel[i]
        i += 1
        wifi_capabilities.set_signal(wifi_iface,ch_num,bw)
        time.sleep(300)
        client.status = client.check_client()
        if(client.status):
            client.run_client()
            






            #TODO
            #add logic that skip channel settings after 4 failed reconnects'''



asyncio.run(main())