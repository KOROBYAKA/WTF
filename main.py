import subprocess
import sys
from sys import argv
import os.path
def main():
    try:
        script, host, port,bw = argv
        port = "-p"+port
        data = [host,port]
        xx = " ".join(data)

    except ValueError:
        pass
        print('''Give arguments or use manual config or test for test''')
        xx = input('''For example "*host IP* -p*port number* *bandwidth*" \n -->>''')

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

    if xx != "manual" and xx != "test":
        xx = xx.split(" ")
        xx[-1] = "--bandwidth" + xx[-1]
        xx = "".join(xx)
        cfg = ("iperf3.exe iperf3 -c " + xx + " --length 6472 -u --bytes 1342177280  --logfile " + file)
    if xx == "manual":
        xx = input("Give Iperf3 startup config: ")
        cfg = ("iperf3.exe iperf3 " + xx)
    if xx == "test":
        cfg = ("iperf3.exe iperf3 -c iperf.eenet.ee -p5201 --logfile iperf_test.log")
        file = "iperf_test.log"


    act = subprocess.run(cfg)



    subprocess.run("notepad "+file)
if __name__ == '__main__':
    main()