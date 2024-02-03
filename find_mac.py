import json
import subprocess

from scapy.all import *


def find_mac(ip):
        #res, unans = sr(IP(dst="192.168.39.241")/ TCP(flags="S", dport=(1, 443)))
        #res.nsummary( lfilter=lambda s, r: (r.haslayer(TCP) and (r.getlayer(TCP).flags & 2)))

        ip_gw = conf.route.route("0.0.0.0")[2]

        apr_requests = ARP(pdst=ip)
        broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_pack = broadcast / apr_requests
        #print(hexdump(arp_pack))
        answered_list = srp(arp_pack, timeout=5, verbose=False)[0]
        for element in answered_list:
            if str(element[1].hwsrc) == '24:5a:4c:4e:fa:39':
                print(element[1].psrc)
            else:
                pass


def local_scan(ip):
    ip_gw = conf.route.route("0.0.0.0")[2]

    apr_requests = ARP(pdst=ip)
    broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_pack = broadcast / apr_requests
    # print(hexdump(arp_pack))
    answered_list = srp(arp_pack, timeout=5, verbose=False)[0]
    for element in answered_list:
        try:
            print(element[1].psrc + '\t\t' + element[1].hwsrc)
        except Exception as e:
            pass


def get_mac(target_ip):
        arp_request = ARP(pdst=target_ip)
        broadcast = Ether(dst="00:25:0b:02:58:d2")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=5, verbose=False)[0]
        #print(answered_list)
        return answered_list[0][1].hwsrc


def main():
    find_mac('192.168.32.0/24')
    find_mac('192.168.33.0/24')
    find_mac('192.168.34.0/24')
    find_mac('192.168.35.0/24')
    find_mac('192.168.36.0/24')
    find_mac('192.168.37.0/24')
    find_mac('192.168.38.0/24')
    find_mac('192.168.39.0/24')
    #local_scan('192.168.39.106')


if __name__ == "__main__":
    main()

































