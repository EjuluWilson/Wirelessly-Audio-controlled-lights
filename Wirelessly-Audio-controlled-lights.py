
"""
Created on Wed Mar 18 14:04:42 2020

@author: Ejulu Wilson and Agnes Nakalembe
"""

#kivy
from kivymd.app import MDApp
from kivy.lang import Builder

#audio
import speech_recognition as sr
r = sr.Recognizer() 


import pyfirmata
import time
br1 = 57600
br2 = 9600
port = 'COM12'
my_board = pyfirmata.Arduino(port, baudrate = br2)
time.sleep(1) #allow the board to synchronise with pyfirmata


class led():

    def __init__(self,pin_configuration):
        self.led = my_board.get_pin(pin_configuration)
        
    def on(self,brighness_level = 1):
        self.led.write(brighness_level)
        
    def off(self):
        self.led.write(0)
        
    def blink(self,blink_times =1,on_time = 1,off_time = 1,brighness_level=1):
        #blink_times:- how many times the led should blink
        #on_time:- how long the led should stay on in a single blink
        #off_time:- how long the led should stay off in a single blink
        i = 0
        while i < blink_times:
            self.led.write(brighness_level)
            time.sleep(on_time)
            self.led.write(0)
            time.sleep(off_time)
            i +=1
            

            #creating led instances/objects
leaving = led('d:11:p') #leaving_room light
bath = led('d:9:p') #bathroom_light
security = led('d:6:p') #security_light

#'d:13:p':d(digital pin),13(pin number) and p(PWM pin)
'''
*PWM stands for pulse width modulation. These pins allow for voltage variation 
from (0-1)v in python, which is equivalent to (0-5)v in reality or (0-1024)v 
in arduino code.
*on an arduino UNO, PWM is only possible with digital pins 3,5,6, 9,10 and 11

'''
#definig a disco light function
def disco():
    while True:
        #blink_times =1,on_time = 1,off_time = 1,brighness_level=1
        #x = random_number
        leaving.blink()
        bath.blink()
        security.blink()
#lights on function(turns all lights on)        
def lights_on():
        leaving.on()
        bath.on()
        security.on()
        
#lights off function(turns all lights off)     
def lights_out():
        leaving.off()
        bath.off()
        security.off() 

        
def leaving_on():
        leaving.on()
        bath.off()
        security.off()
 
def security_on():
        leaving.off()
        bath.off()
        security.on()

def bath_on():
        leaving.off()
        bath.on()
        security.off()        

#lights controller using audio
def smartlights(text):
    if "all lights" in text and "on" in text:#all lights on
        lights_on()
        
    elif "living" in text and "on" in text:#all lights on
        leaving_on()
        
    elif "lights" in text and "out" in text:#all lights on
        lights_out()
        
    elif "bath" in text and "on" in text: #all lights on
        bath_on()
        
    elif "Security" in text and "on" in text: #all lights on
        security_on()
        
    elif "security" in text and "on" in text: #all lights on
        security_on()

#definig a speech to text function

def audio_text():
    try:
        with sr.Microphone() as source:                # use the default microphone as the audio source
            print("wait...")
            r.adjust_for_ambient_noise(source,duration=2)
            print("talk")
            audio = r.listen(source, timeout=10) 
            # listen for the first phrase and extract it into audio data
            audio_text = r.recognize_google(audio)
            
                #print("You said " + r.recognize_sphinx(audio))
            print("You said " + audio_text)    # recognize speech using Google Speech Recognition
                             
        return audio_text
    
    except:                            # speech is unintelligible
        print("Could not understand audio")
                

kvgui =  """
Screen:
    MDLabel:
        text: "[b]Smart House[/b]"
        pos_hint: {'center_x': 0.6, 'center_y': 0.8}
        font_style: "H4"
        markup: True
        
    MDRaisedButton:
        text: 'ligt up'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_press:
            app.audiolights()
    
    MDLabel:
        text: 'wait for it'
        id: audiotext
        pos_hint: {'center_x': 1.0, 'center_y': 0.2}
        
"""
'''
class Main(MDApp):
    def build(self):
        return Builder.load_string(kvgui)
    
    def audiolights(self):
        while True:
            text = audio_text()
            smartlights(text)
            label = self.root.ids.audiotext
            label.text = text
            
            
Main().run()
  '''      