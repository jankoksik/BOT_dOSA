from asyncio.windows_events import NULL
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.popup import Popup


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
    def ClickedConf1(self):
        print("button on conf 1")

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
    popupWindow = Popup(title="App1", content=show, size_hint=(0.8,0.8) )
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