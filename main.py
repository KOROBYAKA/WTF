import subprocess
import sys
from sys import argv
import platform
import os.path
import argparse
def main():
    sys = platform.system()
    parser = argparse.ArgumentParser()
    parser.add_argument('-host','--host',help = '''Host's IP address''')
    parser.add_argument('-BW','-bw','--bandwidth', default = 0, help = 'Bandwidth optional argument(default 0)')
    parser.add_argument('-p','--port',default = 5201, help = 'Port for connection to server')
    args = parser.parse_args()
    port = args.port
    host = args.host
    bw = args.bandwidth



    x = 1
    xstr = str(x)
    fn = ["iperf_test_N.", xstr, ".log"]
    chk = 1

    while chk == 1 :

        file = "".join(fn)
        file_check = os.path.isfile(file)
        if file_check == True:
            x += 1
            xstr = str(x)
            fn = ["iperf_test_N.", xstr, ".log"]
        elif file_check == False:
            chk = 0
    crt = open(file,"w")
    crt.close()

    if sys == 'Windows':
        cfg = (f"iperf3.exe  iperf3 -c {host} -p{port} {bw} --length 6472 -u --bytes 1342177280 -logfile {file}")
    elif sys = 'Linux':
        

    act = subprocess.run(cfg)



    subprocess.run("notepad "+file)
if __name__ == '__main__':
    main()