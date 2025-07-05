import subprocess
import time

class Ap():
    def __init__(self,uci_ap_iface:str,ap_wifi_iface:str,
                ap_phy:str,ap_wifi_ip:str,ip_client:str):
        self.ip_ap = ap_wifi_ip
        self.ip_cl = ip_client
        self.ap_iface = ap_wifi_iface
        self.uci_ap = uci_ap_iface
        self.ap_phy = ap_phy

    def get_wifi_capabilities(self):
        wifi_channels_list = []
        ht_modes = subprocess.run(f"iwinfo {self.ap_phy} htmodelist", shell=True, capture_output=True, text=True)
        wifi_channels = subprocess.run(f"iwinfo {self.ap_phy} freq", shell=True, capture_output=True, text=True)
        for line in wifi_channels.stdout.split("\n"):
            try:
                wifi_channels_list.append(line.strip(" *()\\|/").split(" ")[6].strip(")"))
            except:
                continue
        return wifi_channels_list,ht_modes.stdout.split()

    def connection_status(self):
        cmd = [f"ping {self.ip_cl} -c 1 -W 1"]
        print("#"," ".join(cmd))
        ping_res_ip = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        if ping_res_ip.returncode == 0:
            print('CONNECTION STATUS: Client device is reachable')
            return True
        else:
            print('Client is offline')
            return False

    def set_wifi_capabilities_OpenWrt(self,channel:int, ht_mode:str):
        #Due to the target OS is an OpenWRT, UCI configuration interface
        #is used to set up desirable Wi-Fi Capabilities
        #If you want use it on another
        cmds = [f"uci set wireless.{self.uci_ap}.channel='{channel}'",
                f"uci set wireless.{self.uci_ap}.htmode='{ht_mode}'",
                "uci commit",
                "wifi reload"]
        for cmd in cmds:
            subprocess.run(cmd, shell=True, check=True, text=True)

    def getter(self, timeout):
        args = ['tx_bytes', 'rx_bytes', 'tx_packets', 'rx_packets']
        result1 = {}
        result2 = {}
        delta = {}
        for x in args:
            res = subprocess.run(f'cat /sys/class/net/{self.ap_iface}/statistics/{x}',
                                 shell=True, capture_output=True, text=True)
            stdout = res.stdout
            result1[x] = stdout
        self.run_test(timeout)
        time.sleep(1)
        for x in args:
            res = subprocess.run(f'cat /sys/class/net/{self.ap_iface}/statistics/{x}',
                                 shell=True, capture_output=True, text=True)
            stdout = res.stdout
            result2[x] = stdout
        for key in result1.keys():
            delta[key] = int(result2[key].strip())-int(result1[key].strip())
        return delta

    def ap_status(self):
        cmd = f"uci show.wireless.{self.uci_ap}.disabled"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if not "uci: Entry not found" in result.stdout:
            return True
        else:
            return False

    def ap_link_status(self):
        cmd = f"dmesg | tail -n 6"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout.find("link becomes ready"): return True
        return False

    def run_test(self, timeout):
        cmd = f"iperf3 -c {self.ip_cl} -B {self.ip_ap} -b 0 -t {timeout}"
        print(f"#{cmd}")
        subprocess.run(cmd,shell=True, text=True,check=True, stdout=subprocess.DEVNULL)







