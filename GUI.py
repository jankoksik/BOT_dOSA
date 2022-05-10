from asyncio.base_futures import _FINISHED
from asyncio.windows_events import NULL
from threading import Thread
from time import sleep

from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.popup import Popup


import modules.auxilliary


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
        self.ids.ClickedConf1_port.disabled=False
    

    def ClickedConf1_port(self):
        res = []
        res = modules.auxilliary.scan_host_ports_multi_thread(self.ids.spinner_id_port.text)
        print(res)
        P1.finished = True
        #TODO: FINISH

    def SearchForHosts(self):
        net_info = self.Dane.get_network_info()
        print(net_info)
        result = self.Dane.scan_network_multi_thread(net_info[3],net_info[4])
        print(result)
        P1.finished = True
        print("[INFO] succesfully closed threads")
        modules.auxilliary.dane.JOINED=False
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

      
        
        

    

class P2(FloatLayout):
    def ClickedConf2(self):
        print("button on conf 2")

class P3(FloatLayout):
    def ClickedConf3(self):
        print("button on conf 3")

class P4(FloatLayout):
    def ClickedConf4(self):
        print("button on conf 4")
    

def showPopUp1():
    show = P1()
    popupWindow = Popup(title="Wifi DOS Conf", content=show, size_hint=(0.8,0.8) )
    popupWindow.open()

def showPopUp2():
    show = P2()
    popupWindow = Popup(title="App2", content=show, size_hint=(0.8,0.8) )
    popupWindow.open()

def showPopUp3():
    show = P3()
    popupWindow = Popup(title="App3", content=show, size_hint=(0.8,0.8) )
    popupWindow.open()

def showPopUp4():
    show = P4()
    popupWindow = Popup(title="App4", content=show, size_hint=(0.8,0.8) )
    popupWindow.open()


if __name__ == '__main__':
    MyApp().run()
