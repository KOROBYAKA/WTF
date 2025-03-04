import subprocess
import asyncssh
import time

class Client():
    def __init__(self,ip:str,passwd:str,usr_name:str):
        self.ip = ip
        self.passwd = passwd
        self.usr_name = usr_name
        self.status = False # If status is False, then client is offline

    def check_client(self):
        cmd = [f"ping {self.ip} -c 1"]
        print("#"," ".join(cmd))
        ping_res = subprocess.run(cmd, shell=True, text=True)
        if ping_res.returncode == 0:
            print('Client is online')
            self.status = True
        else:
            print('Client is offline')
            self.status = False



        async def run_client(client:Client):
            async with asyncssh.connect(client.ip, username = client.usr_name,password = client.passwd) as conn:
                result = await conn.run(f"iperf3 -s -B {client.ip}",check = True)
                print('Running iperf3 server on client')

    async def kill_iperf(client):
        async with asyncssh.connect(client.ip, username = client.usr_name,password = client.passwd) as conn:
            res = await conn.run('killall iperf3', check=True)
            print("I'm done, boss")




    def wait_for_client(client):
        failed_reconnects_in_row = 0
        while True:
            client.status = client.check_client()
            print('30 sec to reconnect the client')
            time.sleep(30)
            failed_reconnects_in_row += 1
            if failed_reconnects_in_row >= 3:
                return False
            elif client.status:
                return True

