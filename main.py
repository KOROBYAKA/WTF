#!/usr/bin/python3
import tomllib
import subprocess
import time
from test_logic import Ap
import json
from datetime import datetime


def save_output(final_result):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"test_results_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(final_result, f, indent=4)

    print(f"Saved test results to {output_file}")

def print_results(final_result, htmodes, channels, timeout):
    for channel in channels:
        ht = []
        tx_res = []
        rx_res = []
        print(f"Test channel: {channel}")
        for htmode in htmodes:
            try:
                ht.append( f" {htmode:^13} ")
                value = final_result[channel][htmode]['rx_bytes'] / (timeout * 1024)
                formatted = f"{value:.2f}kB/s"
                rx_res.append(f" {formatted:^13} ")
                value = final_result[channel][htmode]['tx_bytes'] / (timeout * 1024)
                formatted = f"{value:.2f}kB/s"
                tx_res.append(f" {formatted:^13} ")
            except:
                continue
        print("HT MODE  |","|".join(ht))
        print("TX BYTES |","|".join(tx_res))
        print("RX BYTES |","|".join(rx_res))


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

def main():
    final_result = {}
    with open("conf.toml", mode="rb") as fp:
        config = tomllib.load(fp)

    AP = Ap(
    uci_ap_iface=config["ap_conf"]["uci_ap_iface"],
    ap_wifi_iface=config["ap_conf"]["ap_wifi_iface"],
    ap_phy=config["ap_conf"]["ap_phy"],
    ap_wifi_ip=config["ap_conf"]["ap_wifi_ip"],
    ip_client=config["client_conf"]["wifi_ip"]
    )
    if not AP.ap_status():
        print("Access Point software interface is disabled (check UCI)")
        exit()
    wifi_channels,ht_modes = AP.get_wifi_capabilities()
    #wifi_channels = ['1','2']
    #ht_modes = ['HT20','HT40']
    print("Starting tests")
    for channel in wifi_channels:
        final_result[channel] = {}
        for htmode in ht_modes:
            print(f"Setting channel:{channel} and htmode: {htmode}")
            AP.set_wifi_capabilities_OpenWrt(channel,htmode)
            time.sleep(5)
            skip = False
            for x in range(0,4,1):
                if AP.connection_status() and AP.ap_link_status():
                    break
                else:
                    if x == 3:
                        print(f"Reconnect tries are gone, probably AP is not capable to work on channel {channel} with htmode {htmode}.\nHint: "
                              f"if you are sure that AP is capable to work with this physical signal configuration increase the timeout time")
                        skip = True
                    else:
                        print("AP is offline, waiting for set up time")
                        time.sleep(5+x*5)
            if skip: continue
            result = AP.getter(config["defaults"]["timeout"])
            final_result[channel][htmode] = result

    print_results(final_result,ht_modes,wifi_channels,config["defaults"]["timeout"])
    save_output(final_result)




if __name__ == "__main__":
    main()
