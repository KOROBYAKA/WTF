import subprocess

def AP_check(wifi_interface:str):#check if our desirable interface exists and is Wi-Fi AP
    cmd = f"iw  {wifi_interface} info | grep type"
    try:
        result = subprocess.check_output(cmd,shell = True, text = True)
        if any(ap in ['AP','ap'] for ap in result):
            return True
        else:
            raise TypeError(f"Wi-Fi module should be at the AP mode, instead of {result}")
    except:
        print(f'Some error occured while {cmd}')
        return False



def set_signal(wifi_iface:str,ch:int,BW:int):
    cmd = f'iw dev {wifi_iface} set channel {ch} HE{BW}'
    try:

        subprocess.run(cmd, shell = True, text = True)
    except:
        raise TypeError(f"""Error happened while changing bandwidth with "{cmd}" """)


