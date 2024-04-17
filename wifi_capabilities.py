import subprocess

def AP_check(wifi_interface):#check if our desirable interface exists and is Wi-Fi AP

    try:
        cmd = [f"iw  {wifi_interface}  info | grep type"]
        result = subprocess.check_output(cmd,shell = True, text = True)
        if result.stdout == 'type ap':
            return True
        else:
            raise TypeError(f"Wi-Fi type should be ap, instead of {result.stdout}")
        print(result)
    except:
        print(f'Some error occured while {cmd}')

    return False



def set_BW(wifiIF,ch,BW):
    try:
        cmd = f'iw dev {wifiIF} set channel {ch} HT{BW}'
        subprocess.run(cmd, shell = True, text = True)
    except:
        raise TypeError(f"""Error happened while changing bandwidth with "{cmd}" """)