from random import Random
from socket import timeout
from sys import flags
from tabnanny import verbose
import threading
import ipaddress
import math
from time import sleep
from turtle import delay
import netifaces

from threading import Thread
from scapy.all import *
from scapy.all import IP, ICMP, TCP, sr, sr1
from netaddr import IPAddress



target_hosts = []


def get_network_info():

    netifaces.gateways()
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
    netmask =netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['netmask']
    network = ipaddress.IPv4Network(ip+'/'+netmask, strict=False).network_address
    iterator = math.pow(2,(32-IPAddress(netmask).netmask_bits()))-2

    return iface,ip,netmask,network,iterator




def send_ping_multi_thread(target_ip,hosts):
 
    resp = sr(IP(dst=target_ip)/ICMP(),timeout=1,verbose=0, multi= True)
    answered = str(resp[0])
    print(target_ip)
    print(answered)
    print(answered.split()[3].split(":",1)[1])
    if(int(answered.split()[3].split(":",1)[1]) == 1):
        hosts.append(target_ip)


def scan_network_multi_thread(target_network, iterator):
   
    hosts = []
    threads = []
 
    for i in range(0,int(iterator)):
        target_ip = str(target_network + i)
        thread = threading.Thread(target = send_ping_multi_thread,args = [target_ip,hosts])
        sleep(0.2)
        thread.start()
        threads.append(thread)
 
    for t in threads:
        t.join()

    return hosts
    

def send_ping(target_ip):

    resp = sr(IP(dst=target_ip)/ICMP(),timeout=1,verbose=0)
    answered = str(resp[0])
    print(target_ip)
    print(answered)
    print(answered.split()[3].split(":",1)[1])
    if(int(answered.split()[3].split(":",1)[1]) == 1):
        return True

    else:
        return False



def scan_network_single_thread(target_network, iterator):
   
    hosts = []

    for i in range(0,int(iterator)):
        target_ip = str(target_network+ i)
        result = send_ping(target_ip)
        if(result == True):
            hosts.append(target_ip)

    return hosts


def scan_port_multi_thread(dst_ip, dst_port,ports):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.5)

    result = s.connect_ex((dst_ip,dst_port))
    if(result == 0):
        ports.append(dst_port)
        print("Port " +  str(dst_port) + " found open")
    else:
        print("Port " +  str(dst_port) + " closed")
            

def scan_host_ports_multi_thread(dst_ip):

    ports = []
    threads = []

    for port in range(0,1024):
        thread = threading.Thread(target = scan_port_multi_thread, args = [dst_ip,port,ports])
        sleep(0.1)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
    
    return ports


def scan_port(dst_ip, dst_port):
    s_port = RandShort()
    packet = IP(dst =dst_ip )/ TCP(sport = s_port, dport = dst_port, flags='S')
    resp = sr1(packet,timeout=1,verbose=0)
    if(str(type(resp))== "<type 'NoneType'>"):
        print("Port " +  str(dst_port) + " closed")
        return False
    elif(resp.haslayer(TCP)):
        if(resp.getlayer(TCP).flags == 0x12):
            print("Port " +  str(dst_port) + " found open")
            return True




def scan_host_ports_single_thread(dst_ip):
    ports = []
    for i in range(0,1023):
        res = scan_port(dst_ip,i)
        if(res == True):
            ports.append(i)
    
    return ports


if __name__ == '__main__':
    net_info = get_network_info()
    print(net_info)
    #print(net_info[0])
    #print(str(net_info[3]))
    #print(str(net_info[4]))

    #result = scan_network_multi_thread(net_info[3],net_info[4])
    #result  = scan_network_single_thread(net_info[3],net_info[4])
    #print(result)

    #print(scan_port("192.168.0.31",135))
    #print(scan_host_ports("192.168.0.31"))
    res = []
    res = scan_host_ports_multi_thread("192.168.0.31")
    print(res)
   

    
    