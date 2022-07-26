import subprocess
import sys
from sys import argv
import os.path
def main():
    script, host, port,bw = argv
    port = "-p"+port
    data = [host,port]
    xx = " ".join(data)

    x = 1
    xstr = str(x)
    list = ["iperf_test_N.", xstr, ".log"]
    chk = 1

    while chk == 1 :

        file = "".join(list)
        file_check = os.path.isfile(file)
        if file_check == True:
            x += 1
            xstr = str(x)
            list = ["iperf_test_N.", xstr, ".log"]
        elif file_check == False:
            chk = 0
    crt = open(file,"w")

    #xx =" -c 192.168.0.14 -p5201  --length 6472 -u --bytes 1342177280 --bandwidth 0 "
    cfg = ("iperf3.exe iperf3 -c" + xx + " --length 6472 -u --bytes 1342177280 --bandwidth " + bw + " --logfile "+file)
    #cfg = ("iperf3.exe iperf3 -c speedtest.hostkey.ru -p5202 --logfile "+file)
    print(cfg)
    act = subprocess.run(cfg)



    subprocess.run("notepad "+file)
if __name__ == '__main__':
    main()