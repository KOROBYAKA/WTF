# WTF - Wi-Fi Test Framework

Script for test automation of speed tests on different physical capabilities of Wi-Fi signal. At this momnent designed for OpenWrt(uses UCI&SSH).

1. Run iperf3 on your Wi-Fi client machine "iperf3 -s", don't bind it to the Wi-Fi interface IP, because it might cause issues while test is running.
2. Check config accurately conf.toml and ensure it has correct data
3. Run test on your OpenWrt router/AP 

Setup on OpenWRT:
1. opkg update
2. opkg install python git
3. git clone https://github.com/KOROBYAKA/WTF.git
4. cd WTF
5. nano conf.toml #set your config
6. run: python main.py
