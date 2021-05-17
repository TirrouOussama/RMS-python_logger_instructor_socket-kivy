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
from kivy.graphics import Color
from kivy.uix.dropdown import DropDown
from kivy.core.audio import SoundLoader
import time
from kivy.uix.scrollview import ScrollView
from datetime import datetime
import os
import hashlib
from pathlib import Path
import cv2
import struct
import threading
import pickle
from cryptography.fernet import Fernet

Builder.load_file('RMS.kv')   ################# KV file Include ##############

##################### GLOBAL #############  begin ######
host_name = socket.gethostname()
myip = socket.gethostbyname(host_name + ".local")
logid = 'root' + ":" + '192.168.1.106'
logmsg = ''
current_time = ''
rfid =''
trig = False
instruction = ''
action = True
state = 'x x x x'
minions = []
minionsfile = open('minions.txt', 'r')
minionslines = minionsfile.readlines()
for line in minionslines:
    minions.append(line.strip())
    print(minions[0].split(' ')[1])
minionsfile.close()
print(minions)
roomip = ''

##################### Globals ############# end ######################
def machine1_instructor():
    global instruction, action, roomip
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind(('192.168.1.106', 2532))
    s1.listen(10)
    while True:
        clientsocket, address = s1.accept()

        while True:                
                if action == True and instruction !='' and roomip == '192.168.1.100':
                    print(instruction, action)   
                    packet = instruction           
                    clientsocket.send(bytes(packet, 'utf-8'))
                    instruction = ''
                    packet = ''
                    action = False

                #elif state_update == True:
                #   clientsocket.send(bytes( logclock+ "|" + logid + "|" + " connected "+ "-st/"+state, 'utf-8'))
                #   state_update = False
machine1_instructorThread = threading.Thread(target = machine1_instructor) 

def machine1(): ######### MACHINE 1 SOCKET ######### begin #############
    global logmsg, current_time, minions, state, instruction, action
    machine1_address = '192.168.1.100'
    count = 0   
    for items in minions:  
        if items.split(' ')[1] == machine1_address:
        
            break
        count+=1

    while True:
        try:            
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
            s2.connect(('192.168.1.100', 2932))        
            minions[count] = minions[count].split(' ')[0] + " " + minions[count].split(' ')[1] + " " + 'up ' + '/'+ minions[count].split('/')[1]
            while True:
                msg = s2.recv(100)  
                print(msg.decode("utf-8"))
                logmsg = msg.decode("utf-8")    
                if msg.decode("utf-8") == '':
                    print("breaking")
                    s2.close()                   
                    break                   
        except:
            print()
            logmsg = current_time+' warning '+'machine:192.168.1.100|down'
            if minions[count].split(' ')[2] == 'up' or minions[count].split(' ')[2] == 'none':
                minions[count] = minions[count].split(' ')[0] + " " + minions[count].split(' ')[1] + " " + 'down '+ '/x x x x'        
            print("this is count1 " + str(count))
            print(logmsg)
            time.sleep(10) 
            ## MACHINE 1 SOCKET ###### end ############### 

logmachine1 = threading.Thread(target = machine1) ####### SOCKET THREAD ##########

def machine2_instructor():
    global instruction, action, roomip
    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s3.bind(('192.168.1.106', 3532))
    s3.listen(10)
    while True:
        clientsocket, address = s3.accept()

        while True:                
                if action == True and instruction !='' and roomip == '192.168.1.110':
                    print(instruction, action)   
                    packet = instruction           
                    clientsocket.send(bytes(packet, 'utf-8'))
                    instruction = ''
                    packet = ''
                    action = False

                #elif state_update == True:
                #   clientsocket.send(bytes( logclock+ "|" + logid + "|" + " connected "+ "-st/"+state, 'utf-8'))
                #   state_update = False

machine2_instructorThread = threading.Thread(target = machine2_instructor) 

def machine2(): ######### MACHINE 2 SOCKET ######### begin #############
    global logmsg, current_time, minions, state, instruction, action
    machine2_address = '192.168.1.110'
    count = 0   
    for items in minions:  
        if items.split(' ')[1] == machine2_address:
            
            break
        count+=1

    while True:
        try:            
            s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
            s4.connect(('192.168.1.110', 3932))        
            minions[count] = minions[count].split(' ')[0] + " " + minions[count].split(' ')[1] + " " + 'up ' + '/'+ minions[count].split('/')[1]
            while True:    
                msg = s4.recv(100)  
                print(msg.decode("utf-8"))
                logmsg = msg.decode("utf-8")    
                if msg.decode("utf-8") == '':
                    print("breaking")
                    s4.close()                   
                    break                   
        except:
            print()
            logmsg = current_time+' warning '+'machine:192.168.1.110|down'
            if minions[count].split(' ')[2] == 'up' or minions[count].split(' ')[2] == 'none':
                minions[count] = minions[count].split(' ')[0] + " " + minions[count].split(' ')[1] + " " + 'down '+ '/x x x x'        
            print("this is count2  "+ str(count))
            print(logmsg)
            time.sleep(12) 

                ## MACHINE 2 SOCKET ###### end ############### 
 
logmachine2 = threading.Thread(target = machine2)####### SOCKET THREAD ##########

class liscencescreen(Widget): ################ KIVY LISCENCE SCREEN #### begin###########
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.liscence.text = "-Band 1: ..............\n\n-Band 2: ..............\n\n-Band 3: ..............\n\n-Band 4: .............. \n\n-Band 5: .............. \n\n-Band 6: .............. \n\n-Band 7: .............. \n\n-Band 8: .............. \n\n-Band 9: .............. \n\n-Band 10: .............. \n\n-Band 11: .............. \n\n-Band 12: .............. \n\n-Band 13: .............. \n\n-Band 14: .............. \n\n-Band 15: .............. \n\n-Band 16: .............. \n\n-Band 17: .............. \n\n-Band 18: .............. \n\n-Band 19: .............. \n\n -Band 20: .............. \n\n-Band 21: .............. "
   
    def Agreedliscence(self):
        RMS.screenm.current = "login screen"

    def Declineliscence(self):
        quit()

                             ################ KIVY LISCENCE SCREEN ##### end ###########
class loginscreen(Widget):   ################ KIVY LOGIN SCREEN #### begin###########
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.wrongpass.text = "" 

    def login(self):
        self.username = self.ids.username.text
        self.password = self.ids.password.text
        self.combo = self.username+','+self.password
        self.hash = hashlib.sha3_512(self.combo.encode('utf-8')).hexdigest()
        self.loginfile = open('login.txt', 'r')
        self.loginlines = self.loginfile.readlines()    
        self.count = 0
        for line in self.loginlines:
            
            self.stringencrypted = line.strip()[:-1]
            if self.stringencrypted == self.hash:
                RMS.screenm.current = "main screen"
                if line.strip()[-1] == '1':
                    RMS.mainscreen.ids.user.text = 'Admin' + ': ' + self.username
                    RMS.Cardsscreen.ids.userCards.text = 'Admin' + ': ' + self.username
                    self.ids.username.text = ''
                    self.ids.password.text = ''
                    self.loginfile.close()
                elif line.strip()[-1] == '0':
                    RMS.mainscreen.ids.user.text = 'User' + ': ' + self.username
                    RMS.Cardsscreen.ids.userCards.text = 'User' + ': ' + self.username
                    self.ids.username.text = ''
                    self.ids.password.text = ''
                    self.loginfile.close()
            else:
                self.ids.wrongpass.text = "Wrong Username or Password, if forgotten call admin"
            self.count += 1
                 ################ KIVY LOGIN SCREEN ##### end ###########

class mainscreen(Widget):  ################ KIVY MAIN SCREEN ##### begin ###########
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.accessmsg.text = ''
        self.loaded = False
        self.old_logmsg = ""
        self.x = 0
        self.msgcolor = (1,1,1,1)
        Clock.schedule_interval(self.timeandlog, 0.1)

    def timeandlog(self, dt):
        global logid, logmsg, current_time, state, minions
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
    
        self.ids.time.text = current_time
        self.ids.logtittle.text = 'Log listning on '+ logid 
        print(minions)             
        if logmsg != '':
            ################## updating states for machines #############

            ################## updating states########## for machines ###########
            if logmsg.split(" ")[1] == "notification":
                if self.loaded == True:
                    self.notif.unload()
                self.notif = SoundLoader.load('notif.mp3')
                self.notif.play()
                self.loaded  = True             
                self.msgcolor = (0,1,0,1)
                self.count = 0
                for items in minions:
                    print(logmsg.split('|')[1])
                    print(items.split(' ')[0])

                    if logmsg.split('|')[1].split(':')[0] == items.split(' ')[0]:
                        minions[self.count] = items.split(' ')[0] + ' ' + items.split(' ')[1] + ' ' + 'up' +' /' + logmsg.split("/")[1]
                        print("timelog state updater in condition " + minions[self.count])
                        break
                    
                    self.count += 1
                self.count = 0  
                 
            elif logmsg.split(" ")[1] == "connected":

                if self.loaded == True:
                    self.notif.unload()
                self.notif = SoundLoader.load('connected.mp3')
                self.notif.play()
                self.loaded = True

                self.msgcolor = (1,0,1,1)
                self.count = 0
                for items in minions:
                    print(logmsg.split('|')[1])
                    print(items.split(' ')[0])
                    if logmsg.split('|')[1].split(':')[0] == items.split(' ')[0]:
                        minions[self.count] = items.split(' ')[0] + ' ' + items.split(' ')[1] + ' ' + 'up' +' /' + logmsg.split("/")[1]
                        print("timelog state updater in condition " + minions[self.count])
                        break
                    self.count += 1
                self.count = 0  

            elif logmsg.split(" ")[1] == "warning":
                if self.loaded == True:
                    self.notif.unload()
                self.notif = SoundLoader.load('down.mp3')
                self.notif.play()
                self.loaded = True        
                self.msgcolor = (1,0,0,1)            
            self.ids.pofchild.add_widget(Label(text=logmsg, color = self.msgcolor, pos = (10, self.x), font_size= 12, size_hint_y=None, height= 30))
            logmsg = ''
            self.x = self.x + 2
            print(self.x)

    def Cards(self):
        RMS.screenm.current = "Cards screen"

    def viewlog(self):
        pass

    def access(self):
        global minions, state, roomip
        if self.ids.room.text == '':
            self.ids.accessmsg.text = 'Enter Room IP'
   
        elif self.ids.room.text != '':
            self.count = 0   
            for items in minions:    
                if self.ids.room.text == items.split(' ')[1]:
                    if items.split(' ')[2] == 'up':

                        print(items.split('/')[1])
                        RMS.roomscreen.pointer = self.count       ######### lowers the complixity of room actions

                        if items.split('/')[1].split(' ')[0] == '1':
                            RMS.roomscreen.firstsource = 'on1.png'
                            RMS.roomscreen.firstlamp_msg = 'first-lamp-is-on'
                        elif items.split('/')[1].split(' ')[0] == '0':
                            RMS.roomscreen.firstsource = 'off1.png'
                            RMS.roomscreen.firstlamp_msg = 'first-lamp-is-off'
                        if items.split('/')[1].split(' ')[3] == '1':
                            RMS.roomscreen.secondsource = 'on2.png'
                            RMS.roomscreen.secondlamp_msg = 'second-lamp-is-on'
                        elif items.split('/')[1].split(' ')[3] == '0':
                            RMS.roomscreen.secondsource = 'off2.png'
                            RMS.roomscreen.secondlamp_msg = 'second-lamp-is-off'
                        
                        print(items.split(' ')[2])
                        RMS.roomscreen.ids.roomid.text = items.split(' ')[0]
                        print(RMS.roomscreen.ids.roomid.text)
                        RMS.screenm.current = "room screen"
                        roomip = self.ids.room.text

                    elif items.split(' ')[2] == 'down':
                        print(items.split(' ')[2])
                        self.ids.accessmsg.text = 'room is down check log'
                        self.ids.accessmsg.color = (1,0,0,1)

                    elif items.split(' ')[2] == 'none':
                        self.ids.accessmsg.text = 'not updated'

                elif self.ids.room.text != items.split(' ')[1]:
                    self.ids.accessmsg.text = 'Enter a valid room id'  



                        

                self.count +=1
            self.count = 0

        ########### should break on condition

    def Exit(self):
        pass

    def logout(self):
        RMS.screenm.current = "login screen"
                    ################ KIVY MAIN SCREEN ##### end  ###########

class Cardsscreen(Widget): ################ KIVY CARDS SCREEN ##### begin  ###########
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.timerfid, 0.1)
        self.rfidlistfile = open('rfidlist.txt', 'r')
        self.ids.rfidlist.text = self.rfidlistfile.read()  
        self.rfidlistfile.close()
    
    def timerfid(self, dt):
        global current_time, rfid
        self.ids.ctime.text = current_time
        
    def editrfid(self):
        pass

    def back(self):
        RMS.screenm.current = "main screen"
                        ################ KIVY CARDS SCREEN ##### end  ###########

class roomscreen(Widget): ################ KIVY ROOM SCREEN ##### begin  ###########
    secondlamp_msg = StringProperty()
    firstlamp_msg = StringProperty()
    secondsource = StringProperty()
    firstsource = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global instruction, action
        ### shoud be detected on login with the time log               
        Clock.schedule_interval(self.timeinstruct, 0.1)
      
    def timeinstruct(self, dt):
        global current_time, state
        self.ids.rtime.text = current_time

    def backroom(self):
        global roomip
        RMS.screenm.current = "main screen"
        roomip = ""
        self.ids.roomid.text = ""


    def firstlamponoff(self):
        global logmsg, action, state, logid, instruction, minions

        if self.firstsource == 'off1.png':
            action = True
            self.firstsource = 'on1.png'
            self.firstlamp_msg = 'first-lamp-is-on'
            state = '1 ' + '1 ' + state.split(' ')[2] + ' ' + state.split(' ')[3]
            logmsg = current_time + "|" + logid + "|" + ' notiffication '+ self.firstlamp_msg + "-st/" + state
            instruction = state
            print(logmsg)
            print(instruction)
            minions[self.pointer] = minions[self.pointer].split('/')[0] +' /'+ state

        elif self.firstsource == 'on1.png':
            action = True
            self.firstsource = 'off1.png'
            self.firstlamp_msg = 'first-lamp-is-off'
            state = '0 ' + '0 ' + state.split(' ')[2]+ ' ' + state.split(' ')[3]
            logmsg = current_time + "|" + logid + "|" + ' notification ' + self.firstlamp_msg +"-st/" + state
            instruction = state
            print(logmsg)
            print(instruction)
            minions[self.pointer] = minions[self.pointer].split('/')[0] +' /'+ state

       

    def secondlamponoff(self):
        global logmsg, action, state, logid, instruction, minions

        if self.secondsource == 'off2.png':
            action = True
            self.secondsource = 'on2.png'
            self.secondlamp_msg = 'second-lamp-is-on'
            state = state.split(' ')[0] + ' ' + state.split(' ')[1] + ' 1' + ' 1'
            logmsg = current_time + "|" + logid + "|" + ' notification ' + self.secondlamp_msg + "-st/"+ state
            instruction = state
            print(logmsg)
            print(instruction)
            minions[self.pointer] = minions[self.pointer].split('/')[0] +' /'+ state

        elif self.secondsource == 'on2.png':
            action = True
            self.secondsource = 'off2.png'
            self.secondlamp_msg = 'second-lamp-is-off'
            state =  state.split(' ')[0] + ' ' + state.split(' ')[1] + ' 0' + ' 0'
            logmsg = current_time+ "|" + logid+ "|" + ' notification ' + self.secondlamp_msg + "-st/"+ state
            instruction = state
            print(logmsg)
            print(instruction)        
            minions[self.pointer] = minions[self.pointer].split('/')[0] +' /'+ state

class RMS(App):                  ############# APP  THREADS RUNNER ######
    def build(self):
        self.screenm = ScreenManager()      

        self.liscencescreen = liscencescreen()      #  LISCENCE SCREEN
        screen = Screen(name="liscence screen ")    #
        screen.add_widget(self.liscencescreen)      #
        self.screenm.add_widget(screen)             #

        self.loginscreen = loginscreen()            #  LOGIN    SCREEN
        screen = Screen(name="login screen")        #
        screen.add_widget(self.loginscreen)         #
        self.screenm.add_widget(screen)             #

        self.mainscreen = mainscreen()              #  MIAN     SCREEN
        screen = Screen(name="main screen")         #
        screen.add_widget(self.mainscreen)          #
        self.screenm.add_widget(screen)             #

        self.Cardsscreen = Cardsscreen()            #  CARDS    SCREEN
        screen = Screen(name="Cards screen")        #
        screen.add_widget(self.Cardsscreen)         #
        self.screenm.add_widget(screen)
                     #
        self.roomscreen = roomscreen()            #  CARDS    SCREEN
        screen = Screen(name="room screen")        #
        screen.add_widget(self.roomscreen)         #
        self.screenm.add_widget(screen)

        return self.screenm
                            ################ APP THREAD RUNNER ########
if __name__ == "__main__":
    RMS = RMS()
    logmachine1.start()
    machine1_instructorThread.start()
    logmachine2.start()
    machine2_instructorThread.start()
    threading.Thread(target = RMS.run())
    