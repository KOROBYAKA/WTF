import subprocess
from wave import Error

import asyncssh
import asyncio


class Client():
    def __init__(self,ap_user:str,ap_user_password:str,ap_ip_control:str,uci_ap_iface:str,ap_wifi_iface:str,
                ap_phy:str,ap_wifi_ip:str,os:str):
        self.usr_name = ap_user
        self.passwd = ap_user_password
        self.ip =  ap_ip_control
        self.ip_ap = ap_wifi_ip
        self.ap_iface = ap_wifi_iface
        self.uci_ap = uci_ap_iface
        self.ap_phy = ap_phy
        self.os = os


    def print(self):
        for key,value in self.__dict__.items():
            print(f"{key}: {value}")

    async def credentials_check(self):
        async with asyncssh.connect(self.ip, username=self.usr_name, password=self.passwd) as conn:
            print("AP SSH CONNECTION STATUS:OK\r")
            return True

    async def get_wifi_capabilities(self):
        wifi_channels_list = []
        async with asyncssh.connect(self.ip, username=self.usr_name, password=self.passwd) as conn:
            ht_modes = await conn.run(f"iwinfo {self.ap_phy} htmodelist")
            wifi_channels = await conn.run(f"iwinfo {self.ap_phy} freq")
            for line in wifi_channels.stdout.split("\n"):
                try:
                    wifi_channels_list.append(line.strip("*()/").split()[6].strip("()/*"))
                except:
                    continue
            return wifi_channels_list,ht_modes.stdout.split()





    def connection_status(self):
        cmd = [f"ping {self.ip} -c 1 -W 0.1"]
        print("#"," ".join(cmd))
        ping_res_ip = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        if ping_res_ip.returncode == 0:
            print('CONNECTION STATUS: Client device is reachable')
        else:
            print('Client is offline')
            return False
        cmd = [f"ping {self.ip_ap} -c 1 -W 0.5"]
        print("#"," ".join(cmd))
        ping_res_ap = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        if ping_res_ap.returncode == 0:
            print("CONNECTION STATUS: AP's IP address is reachable")
            return True
        else:
            print('AP is not reachable')
            return False

    async def set_wifi_capabilities_OpenWrt(self,channel:int, ht_mode:str):
        #Due to the target OS is an OpenWRT, UCI configuration interface
        #is used to set up desirable Wi-Fi Capabilities
        #If you want use it on another
        cmds = [f"uci set wireless.{self.uci_ap}.channel='{channel}'",
                f"uci set wireless.{self.uci_ap}.htmode='{ht_mode}'",
                "uci commit",
                "wifi reload"]
        for cmd in cmds:
            async with asyncssh.connect(self.ip, username=self.usr_name, password=self.passwd) as conn:
                await conn.create_process(cmd)

    async def getter(self, ip, timeout):
        iface_path = f"/sys/class/net/{self.ap_iface}/statistics/"
        args = ['tx_bytes', 'rx_bytes', 'tx_packets', 'rx_packets']
        result1 = {}
        result2 = {}
        delta = {}
        cmd = f'cat {iface_path}'
        async with asyncssh.connect(self.ip, username=self.usr_name, password=self.passwd) as conn:
            for x in args:
                res = await conn.create_process(f'{cmd}{x}')
                stdout = await res.stdout.read()
                result1[x] = stdout
        await self.run_test(ip,timeout)
        await asyncio.sleep(timeout)
        async with asyncssh.connect(self.ip, username=self.usr_name, password=self.passwd) as conn:
            for x in args:
                res = await conn.create_process(f'{cmd}{x}')
                stdout = await res.stdout.read()
                result2[x] = stdout
        for key in result1.keys():
            delta[key] = int(result2[key].strip())-int(result1[key].strip())
        print(delta)
        return delta

    async def ap_status(self):
        cmd = f"uci show.wireless.{self.uci_ap}.disabled"
        async with asyncssh.connect(self.ip, username=self.usr_name, password=self.passwd) as conn:
            result = await conn.run(cmd)
            print(result.stdout)
            if not "uci: Entry not found" in result.stdout:
                return True
            else:
                return False

    async def run_test(self, ip, timeout):
        await self.run_iperf()
        cmd = f"iperf3 -c {self.ip_ap} -B {ip} -b 0 -t {timeout}"
        print(f"#{cmd}")
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.DEVNULL)
        await proc.wait()
        await self.kill_iperf()


    async def run_iperf(self):
        async with asyncssh.connect(self.ip, username = self.usr_name,password = self.passwd) as conn:
            result = await conn.run(f"iperf3 -s -B {self.ip_ap} -D",check = True)
            print('Running iperf3 server on client')

    async def kill_iperf(self):
        async with asyncssh.connect(self.ip, username = self.usr_name,password = self.passwd) as conn:
            res = await conn.run('killall iperf3')
            #print("I'm done, boss")




