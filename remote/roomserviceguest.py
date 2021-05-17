import socket
import gi
gi.require_version('Gst', '1.0')
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.graphics.texture import Texture
from kivy.core.camera import Camera
from kivy.graphics import *
from kivy.base import runTouchApp
import time
from datetime import datetime
import os
import hashlib
from pathlib import Path
import struct
import threading
import pickle
from cryptography.fernet import Fernet
Builder.load_file('RMS.kv')

updatemsg = ''
host_name = socket.gethostname()
myip = socket.gethostbyname(host_name + ".local")
logid = "tshmachineclone" +":"+ "192.168.1.100"

logmsg = ''
logclock = ''
action = False
state = '0 0 0 0'
state_update = False
msg = ''
instruction = ''

def clocking():
    global logclock
    now = datetime.now()
    logclock = now.strftime("%H:%M:%S")

clockthread = threading.Thread(target = clocking)

def instructor():
    global logmsg, logid , current_time, state, instruction
    machine1_address = '192.168.1.106'

    while True:
        try:            
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
            s2.connect(('192.168.1.106', 2532))
            while True:
                msg = s2.recv(100)  
                print(msg.decode("utf-8"))
                if msg.decode("utf-8") != '':
                    state = msg.decode("utf-8")
                    instruction = state
                    logmsg = logclock + "|" + logid + "|" + logmsg+"-stroot/"+ state    
                if msg.decode("utf-8") == '':
                    print("breaking")
                    s2.close()                   
                    break                   
        except:
            logmsg = ''
instructor_thread = threading.Thread(target = instructor)


def logformaster():
    global state, state_update, logmsg, logclock, logid, action, msg
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind(('192.168.1.100', 2932))
    s2.listen(10)
    while True:
        clientsocket, address = s2.accept()

        while True:                
                if action == True and logmsg !='':
                    print(logid + " "+ logmsg + " at "+logclock + " focus")   
                    packet =  logclock + "|" + logid + "|" + logmsg+"-st/"+state  
                    print(action)       
                    clientsocket.send(bytes(packet, 'utf-8'))
                    logmsg = ''
                    logclock = ''
                    packet = ''
                    action = False

                elif state_update == True:
                    clientsocket.send(bytes( logclock+ "|" + logid + "|" + " connected "+ "-st/"+state, 'utf-8'))
                    state_update = False


logmasterthread = threading.Thread(target = logformaster)

class liscencescreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.liscence.text = "-Band 1: ..............\n\n-Band 2: ..............\n\n-Band 3: ..............\n\n-Band 4: .............. \n\n-Band 5: .............. \n\n-Band 6: .............. \n\n-Band 7: .............. \n\n-Band 8: .............. \n\n-Band 9: .............. \n\n-Band 10: .............. \n\n-Band 11: .............. \n\n-Band 12: .............. \n\n-Band 13: .............. \n\n-Band 14: .............. \n\n-Band 15: .............. \n\n-Band 16: .............. \n\n-Band 17: .............. \n\n-Band 18: .............. \n\n-Band 19: .............. \n\n -Band 20: .............. \n\n-Band 21: .............. "
    def Agreedliscence(self):

        RMS.screenm.current = "login screen"

    def Declineliscence(self):
        quit()

class loginscreen(Widget):
    nfc = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        Clock.schedule_interval(self.nfcscan, 0.1)

    def nfcscan(self, dt):
        self.ids.nfc.text = '00010001'
        self.nfc = self.ids.nfc.text


    def login(self):
       RMS.screenm.current = "main screen" 

class mainscreen(Widget):
    firstsource = StringProperty()
    firstlamp_msg = StringProperty()
    secondsource = StringProperty()
    secondlamp_msg = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global action, state, state_update
        state_update = True
        ### shoud be detected on login with the time log
        self.firstsource = 'on1.png'
        state = '1 ' + '1 ' +state.split(' ')[2]+ ' ' +state.split(' ')[3]
        self.firstlamp_msg = ' '
        self.secondsource = 'on2.png'
        state = state.split(' ')[0]+ ' ' + state.split(' ')[1]+ ' 1' + ' 1'
        self.secondlamp_msg = ' '

############## state_update make sure sent at first connect
        Clock.schedule_interval(self.timeandlog, 0.1)

    def timeandlog(self, dt):
        global logclock, instruction
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.ids.time.text = current_time
        logclock = current_time
        if instruction != '':
            print(instruction)
            if instruction.split(' ')[0] == '1':
                self.firstsource = 'on1.png'
                self.firstlamp_msg = 'first-lamp-is-on'
            elif instruction.split(' ')[0] == '0':
                self.firstsource = 'off1.png'
                self.firstlamp_msg = 'first-lamp-is-off'
            if instruction.split(' ')[3] == '1':
                self.secondsource = 'on2.png'
                self.secondlamp_msg = 'second-lamp-is-on'
            elif instruction.split(' ')[3] == '0':
                self.secondsource = 'off2.png'
                self.secondlamp_msg = 'second-lamp-is-off'
            instruction = ''
            
        



    def logout(self):
        RMS.screenm.current = "login screen"

    def firstlamponoff(self):
        global logmsg, action, state, state_update
        if self.firstsource == 'off1.png':
            action = True
            self.firstsource = 'on1.png'
            self.firstlamp_msg = 'first-lamp-is-on'
            state = '1 ' + '1 ' + state.split(' ')[2]+ ' ' +state.split(' ')[3]
            logmsg = ' notiffication '+self.firstlamp_msg
            
        elif self.firstsource == 'on1.png':
            action = True
            self.firstsource = 'off1.png'
            self.firstlamp_msg = 'first-lamp-is-off'
            state = '0 ' + '0 '+state.split(' ')[2]+ ' ' +state.split(' ')[3]
            logmsg = ' notification '+self.firstlamp_msg
            

    def secondlamponoff(self):
        global logmsg, action,state, state_update
        if self.secondsource == 'off2.png':
            action = True
            self.secondsource = 'on2.png'
            self.secondlamp_msg = 'second-lamp-is-on'
            state =  state.split(' ')[0]+ ' ' + state.split(' ')[1]+ ' 1' + ' 1'
            logmsg = ' notification '+self.secondlamp_msg
            
        elif self.secondsource == 'on2.png':
            action = True
            self.secondsource = 'off2.png'
            self.secondlamp_msg = 'second-lamp-is-off'
            state =  state.split(' ')[0]+ ' ' + state.split(' ')[1]+ ' 0' + ' 0'
            logmsg = ' notification '+self.secondlamp_msg
            
        


class RMS(App):
    def build(self):
        self.screenm = ScreenManager()

        self.liscencescreen = liscencescreen()
        screen = Screen(name="liscence screen ")
        screen.add_widget(self.liscencescreen)
        self.screenm.add_widget(screen)

        self.loginscreen = loginscreen()
        screen = Screen(name="login screen")
        screen.add_widget(self.loginscreen)
        self.screenm.add_widget(screen)

        self.mainscreen = mainscreen()
        screen = Screen(name="main screen")
        screen.add_widget(self.mainscreen)
        self.screenm.add_widget(screen)


        return self.screenm


if __name__ == "__main__":
    RMS = RMS()
    logmasterthread.start()
    clockthread.start()
    instructor_thread.start()
    threading.Thread(target = RMS.run())
