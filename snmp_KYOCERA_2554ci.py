from colorama import init, Fore, Style

from pysnmp.hlapi import *


init()
black_3050 = '1.3.6.1.2.1.43.11.1.1.8.1.1'
black = '1.3.6.1.2.1.43.11.1.1.9.1.4'
cyan = '1.3.6.1.2.1.43.11.1.1.9.1.1'
blue = '1.3.6.1.2.1.43.11.1.1.9.1.2'
yellow = '1.3.6.1.2.1.43.11.1.1.9.1.3'
public = 'public'
snmp_password = '******************'

ip_list = ['PRINTERS_IP']

def get_color_2554(oid, ip):
        info = getCmd(SnmpEngine(), CommunityData(dev), UdpTransportTarget((ip, 161)),
                      ContextData(),
                      ObjectType(ObjectIdentity(oid)))
        errorIndication, errorStatus, errorIndex, varBinds = next(info)

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                #print(varBind[1])
                if oid == black:
                    print(Fore.WHITE + 'Уровень черного тонера = {}%'.format(str(int(varBind[1]) / 250)))
                    return varBind[1]
                elif oid == cyan:
                    print(Fore.MAGENTA + 'Уровень пурпурного тонера = {}% на'.format(str(int(varBind[1]) / 120)))
                    return varBind[1]
                elif oid == blue:
                    print(Fore.BLUE + 'Уровень голубого тонера = {}%'.format(str(int(varBind[1]) / 120)))
                    return varBind[1]
                else:
                    print(Fore.YELLOW + 'Уровень желтого тонера = {}%'.format(str(int(varBind[1]) / 120)))
                    return varBind[1]


def get_color_5526(oid):
    info = getCmd(SnmpEngine(), CommunityData(public), UdpTransportTarget(('192.168.33.122', 161)),
                  ContextData(),
                  ObjectType(ObjectIdentity(oid)))
    errorIndication, errorStatus, errorIndex, varBinds = next(info)

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(varBind[1])
            if oid == black:
                print('Уровень черного тонера = {}%'.format(str(int(varBind[1]) / 12)))
                return varBind[1]
            elif oid == cyan:
                print(Fore.MAGENTA + 'Уровень пурпурного тонера = {}%'.format(str(int(varBind[1]) / 12)))
                return varBind[1]
            elif oid == blue:
                print(Fore.BLUE + 'Уровень голубого тонера = {}%'.format(str(int(varBind[1]) / 12)))
                return varBind[1]
            else:
                print(Fore.YELLOW + 'Уровень желтого тонера = {}%'.format(str(int(varBind[1]) / 12)))
                return varBind[1]


for ip in ip_list:
    get_color_2554(black, ip)
    get_color_2554(blue, ip)
    get_color_2554(cyan, ip)
    get_color_2554(yellow, ip)
    print(Fore.WHITE + 'Адрес принтера: {}\n--------------------------------------'.format(ip), Style.RESET_ALL)
