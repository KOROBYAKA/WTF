


import subprocess


def main():
    cfg = ("iperf3.exe")
    act = subprocess.run(cfg, input("iperf3 -c speedtest.hostkey.ru -p5202"))



if __name__ == '__main__':
    main()