import time
import os

import paramiko


mikrotik_ip = input('input ip mikrotik :  ')
username = 'admin'
password = ''


def connect():
    # connecting
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(mikrotik_ip, username=username, password=password, banner_timeout=200)


def access_point():

    # connecting
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(mikrotik_ip, username=username, password=password, banner_timeout=200)

    # add_bridge
    add_bridge = f"/interface bridge add name=bridge1"
    ssh_client.exec_command(add_bridge)
    add_wireless = f"/interface bridge port add bridge=bridge1 interface=wlan1"
    ssh_client.exec_command(add_wireless)
    add_ether_1 = f"/interface bridge port add bridge=bridge1 interface=ether1"
    ssh_client.exec_command(add_ether_1)
    add_ether_2 = f"/interface bridge port add bridge=bridge1 interface=ether2"
    ssh_client.exec_command(add_ether_2)
    add_ether_3 = f"/interface bridge port add bridge=bridge1 interface=ether3"
    ssh_client.exec_command(add_ether_3)
    add_ether_4 = f"/interface bridge port add bridge=bridge1 interface=ether4"
    ssh_client.exec_command(add_ether_4)
    print('bridge added')
    time.sleep(2)

    # add setting wireless
    add_wireless_set = f"/interface wireless set [ find default-name=wlan1 ] band=2ghz-onlyn " \
                       f"channel-width=20/40mhz-XX country=russia3 disabled=no mode=ap-bridge ssid=SC.DEFOLT"
    ssh_client.exec_command(add_wireless_set)
    add_wireless_profiles = f"/interface wireless security-profiles set [ find default=yes ] " \
                            f"supplicant-identity=MikroTik"
    ssh_client.exec_command(add_wireless_profiles)
    print('wireless added')
    time.sleep(2)

    # add client dhcp
    add_dhcp_client = f"/ip dhcp-client add dhcp-options=hostname,clientid disabled=no interface=bridge1"
    ssh_client.exec_command(add_dhcp_client)
    print('dhcp-client added')
    time.sleep(2)

    # set time
    add_time = f"/system clock set time-zone-name=Europe/Moscow"
    ssh_client.exec_command(add_time)
    print('time added')
    time.sleep(2)

    # update
    select_long_term = f"/system package update set channel=long-term"
    ssh_client.exec_command(select_long_term)
    update_long_term = f"system package update download"
    ssh_client.exec_command(update_long_term)
    time.sleep(10)
    reboot = f"system reboot"
    ssh_client.exec_command(reboot)

    # remove addresses
    remove_addresses = f"/ip address remove numbers=0"
    ssh_client.exec_command(remove_addresses)
    print('default address removed')
    time.sleep(1)
    print('+++  script completed successfully   +++\n     you will be disconnected ...     ')

    ssh_client.close()


if __name__ == "__main__":
    os.system('color a')
    access_point()
