import subprocess
import sys
from sys import argv
def main():
    status,host, port = argv
    exe = ("iperf3.exe iperf3"+ status + host + port+ "--logfile iperf.log")###-c speedtest.serverius.net -p5002
    act = subprocess.run(exe)

    subprocess.run("notepad iperf.log")
if __name__ == '__main__':
    main()