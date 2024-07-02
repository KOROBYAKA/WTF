import subprocess

def AP_check(wifi_interface):#check if our desirable interface exists and is Wi-Fi AP

    try:
        cmd = [f"iw  {wifi_interface}  info | grep type"]
        result = subprocess.check_output(cmd,shell = True, text = True)
        if result == 'type ap':
            return True
        else:
            raise TypeError(f"Wi-Fi module should be at the AP mode, instead of {result}")
    except:
        print(f'Some error occured while {cmd}')

    return False



def set_BW(wifi_iface:str,ch:int,BW:int):
    try:
        cmd = f'iw dev {wifi_iface} set channel {ch} HT{BW}'
        subprocess.run(cmd, shell = True, text = True)
    except:
        raise TypeError(f"""Error happened while changing bandwidth with "{cmd}" """)