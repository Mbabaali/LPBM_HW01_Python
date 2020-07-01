#!/usr/bin/env python
# -*- coding: utf-8 -

#soft banc de test version : dev (version à indiquer)
from __future__ import division
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.graphics import Line
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.uix.popup import Popup

from kivy.event import EventDispatcher

from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty

import glob,os
import serial
import sys
import string
import time
from datetime import datetime
import subprocess
import signal 
import inspect
import GenGraph

global alarmawake






date = str(datetime.now())


# Création des fichiers csv dans clé USB
date_titre=str(datetime.now().year)+'-'+str(datetime.now().month)+'-'+str(datetime.now().day)+'-'+str(datetime.now().hour)+'-'+str(datetime.now().minute)+'-'+str(datetime.now().second)
#adresseUSB='/media/pi/DATA3/' #utiliser une expression régulière ? * sinon voir ou est tout le temps monté la clé usb ls usb -> liste tous les ports
# autre solution : démonter tous avant l'insertion de la clé usb puis remonter tous
adresseUSB=str(os.popen("mount | grep /media/pi").readlines())
try:
    adresseUSB=adresseUSB.split(" ")[2]+'/'
except IndexError:
    Logger.warning('adresseUSB: impossible d\'accéder au chemin de la clé USB :  vérifier que la clé USB est bien branché')
    exit()
Logger.warning('adresseUSB: {}'.format(adresseUSB))
try:
    os.mkdir(adresseUSB+date_titre)
except OSError:
    Logger.warning('fichier: impossible de créer un fichier à l adresse selectionné : vérifier que la clé USB est bien branché')
    exit()

#date au format que l'on souhaite avoir dans le titre 
file1='/data_dut_1_'
file2='/data_dut_2_'
file3='/data_dut_3_'
file4='/data_dut_4_'
file55='/data_dut_5_'
file66='/data_dut_6_'

file5='/data_dut_1_err_'
file6='/data_dut_2_err_'
file7='/data_dut_3_err_'
file8='/data_dut_4_err_'
file555='/data_dut_5_err_'
file666='/data_dut_6_err_'


extension='.csv'

chemin1=adresseUSB+date_titre+file1+date_titre+extension
chemin2=adresseUSB+date_titre+file2+date_titre+extension
chemin3=adresseUSB+date_titre+file3+date_titre+extension
chemin4=adresseUSB+date_titre+file4+date_titre+extension
chemin55=adresseUSB+date_titre+file55+date_titre+extension
chemin66=adresseUSB+date_titre+file66+date_titre+extension

chemin5=adresseUSB+date_titre+file5+date_titre+extension
chemin6=adresseUSB+date_titre+file6+date_titre+extension
chemin7=adresseUSB+date_titre+file7+date_titre+extension
chemin8=adresseUSB+date_titre+file8+date_titre+extension
chemin555=adresseUSB+date_titre+file555+date_titre+extension
chemin666=adresseUSB+date_titre+file666+date_titre+extension


try :   
    out1 = open(chemin1, 'w')
    out2 = open(chemin2, 'w')
    out3 = open(chemin3, 'w')
    out4 = open(chemin4, 'w')
    out55= open(chemin55, 'w')
    out66= open(chemin66, 'w')

    out5   = open(chemin5, 'w')
    out6   = open(chemin6, 'w')
    out7   = open(chemin7, 'w')
    out8   = open(chemin8, 'w')
    out555 = open(chemin555, 'w')
    out666 = open(chemin666, 'w')
    
    Logger.info('ouverture fichier: fichier ouvert')
except IOError :
    Logger.warning('ouverture fichier: impossible d\'ouvrir les fichiers')  

# Récupération de l'heure
date = str(datetime.now())

# Ecriture label colonne ficher excel        
print(";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"]), file=out1)
print(";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"]), file=out2)
print(";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"]), file=out3)
print(";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"]), file=out4)
print(";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"]), file=out55)
print(";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"]), file=out66)

print(";".join(["date-time","Value", "Unit", "State"]), file=out5)
print(";".join(["date-time","Value", "Unit", "State"]), file=out6)
print(";".join(["date-time","Value", "Unit", "State"]), file=out7)
print(";".join(["date-time","Value", "Unit", "State"]), file=out8)
print(";".join(["date-time","Value", "Unit", "State"]), file=out555)
print(";".join(["date-time","Value", "Unit", "State"]), file=out666)

class cycle:
    def __init__(self, time_awake, time_awake_s, time_awake_m, time_awake_h, time_sleep, time_sleep_s, time_sleep_m, time_sleep_h):
        self.time_awake=time_awake
        self.time_awake_s=time_awake_s
        self.time_awake_m=time_awake_m
        self.time_awake_h=time_awake_h
        self.time_sleep=time_sleep
        self.time_sleep_s=time_sleep_s
        self.time_sleep_m=time_sleep_m
        self.time_sleep_h=time_sleep_h
        self.nb_repetition=1

class graph:
    def __init__(self):
        self.y_low_min_uA=60
        self.y_low_max_uA=120
        self.y_low_min=0
        self.y_low_max=0
        self.y_high_min=600
        self.y_high_max=1000
        self.flagGraph=True


        


# Classe de transition pour variable global
class passerelle(Screen):
    cycle1=cycle(0, 25, 0, 0, 0, 25, 0, 0)
    cycle2=cycle(0,0,0,0,0,0,0,0)
    cycle3=cycle(0,0,0,0,0,0,0,0)
    cycle4=cycle(0,0,0,0,0,0,0,0)
    cycle5=cycle(0,0,0,0,0,0,0,0)

    alarm_awake = 1.1 #seuil en amper qui activera l'alarme lorsque que l'équipement sera allumé
    alarm_sleep = 200 #seuil en uA qui active l'alarme à l'état sleep

    amperage_max = 2.0
    update_amperage_max=0

    # Nombre de cycle d"fini par l'utilisateur
    nobmre_de_cycle = 1
    update_nobmre_de_cycle=0
    
    time_awake = 0 #duréée en secondes pendant lequel l'équipement est allumé

    time_awake_m=0
    time_awake_h=0
    time_sleep = 0 # "" éteint
    time_sleep_s=25
    time_sleep_m=0
    time_sleep_h=0
    update_alarm = 0 #
    start_stop = 0 #
    
    cptalarmondut1 = 0 #
    cptalarmoffdut1 = 0 #

    cptalarmondut2 = 0 #
    cptalarmoffdut2 = 0 #

    cptalarmondut3 = 0 #
    cptalarmoffdut3 = 0 #

    cptalarmondut4 = 0 # 
    cptalarmoffdut4 = 0#

    cptalarmondut5 = 0 # 
    cptalarmoffdut5 = 0#

    cptalarmondut6 = 0 # 
    cptalarmoffdut6 = 0#

    amperageMax = 0.0
    
    A1onMax=0
    W1onMax=0
    U1onMax=0

    A2onMax=0
    W2onMax=0
    U2onMax=0

    A3onMax=0
    W3onMax=0
    U3onMax=0

    A4onMax=0
    W4onMax=0
    U4onMax=0

    A5onMax=0
    W5onMax=0
    U5onMax=0

    A6onMax=0
    W6onMax=0
    U6onMax=0

    A1offMax=0
    W1offMax=0
    U1offMax=0

    A2offMax=0
    W2offMax=0
    U2offMax=0

    A3offMax=0
    W3offMax=0
    U3offMax=0

    A4offMax=0
    W4offMax=0
    U4offMax=0

    A5offMax=0
    W5offMax=0
    U5offMax=0

    A6offMax=0
    W6offMax=0
    U6offMax=0

    updateMax=False

    etat_start=1 #prends true lorsque que l'on commence l'acquistion avec l'acc à 12v false si l'on commence l'acquisition avec l'acc à 0 v
    f_acquisition=1 #frequence d'acquisition de l'équiepement mesuré 

    flag_seuil=False
    flag_delai=False
    timer_delai_init=0
    nb_screen=0


    graph1=graph()
    # uA1=0
    # uW1=0
    # uA2=0
    # uW2=0
    # uA3=0
    # uW3=0
    # uA4=0
    # uW4=0
    



# Classe écran d'accueil    
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.callNext, 5)


    # Fonction d'appel d'une autre classe    
    def callNext(self,dt):
        self.manager.current = 'voie1234'

# Classe principal d'affichage information Duts
class Voie1234(Screen):
    
    def __init__(self, **kwargs):
        super(Voie1234, self).__init__(**kwargs)
        # Mise en place du timer pour le rafraichissemnt de l'écran
        refresh_time = 0.1
        Clock.schedule_interval(self.timer, refresh_time)

################################################################################################
        # Labels courant et conso Dut1
        self.courant1 = Label(text="0 A", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.24, 'center_y':0.88})
        self.add_widget(self.courant1)
        # self.puissance1 = Label(text="puissance1", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.24, 'center_y':0.80})
        # self.add_widget(self.puissance1)
        
        # Labels courant et conso Dut2
        self.courant2 = Label(text="0 A", font_size='30sp', size=(100, 50),  pos_hint={'center_x': 0.57, 'center_y':0.88})
        self.add_widget(self.courant2)
        # self.puissance2 = Label(text="puissance2", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.57, 'center_y':0.80})
        # self.add_widget(self.puissance2)

        # Labels courant et conso Dut3
        self.courant3 = Label(text="0 A", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.9, 'center_y':0.88})
        self.add_widget(self.courant3)
        # self.puissance3 = Label(text="puissance3", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.9, 'center_y':0.80})
        # self.add_widget(self.puissance3)

        # Labels courant et conso Dut4
        self.courant4 = Label(text="0 A", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.24, 'center_y':0.43})
        self.add_widget(self.courant4)
        # self.puissance4 = Label(text="puissance4", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.24, 'center_y':0.35})
        # self.add_widget(self.puissance4)

        # Labels courant et conso Dut5
        self.courant5 = Label(text="0 A", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.57, 'center_y':0.43})
        self.add_widget(self.courant5)
        # self.puissance5 = Label(text="puissance5", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.57, 'center_y':0.35})
        # self.add_widget(self.puissance5)

        # Labels courant et conso Dut6
        self.courant6 = Label(text="0 A", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.9, 'center_y':0.43})
        self.add_widget(self.courant6)
        # self.puissance6 = Label(text="puissance6", font_size='30sp', size=(100, 50), pos_hint={'center_x': 0.9, 'center_y':0.35})
        # self.add_widget(self.puissance6)

        
        
################################################################################################
        # Labels update des alarmes.
        # Alarme Channel 1
        # self.alarmeon1 = Label(text="1.1A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.25, 'center_y':0.623})
        # self.add_widget(self.alarmeon1)
        # self.alarmeoff1 = Label(text="111uA", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.305, 'center_y':0.623})
        # self.add_widget(self.alarmeoff1)
        
        #Label compteur alarme Channel 1
        self.cptalarmeon1 = Label(text="0", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.05+0.03, 'center_y':0.52})
        self.add_widget(self.cptalarmeon1)
        self.cptalarmeoff1 = Label(text="0", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.305-0.045, 'center_y':0.52})
        self.add_widget(self.cptalarmeoff1)

        
        # # Alarme Channel 2
        # self.alarmeon2 = Label(text="2.2A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.585, 'center_y':0.623})
        # self.add_widget(self.alarmeon2)
        # self.alarmeoff2 = Label(text="222uA", font_size='20sp', pos_hint={'center_x': 0.640, 'center_y':0.623})
        # self.add_widget(self.alarmeoff2)
        
        #Label compteur alarme Channel 2
        self.cptalarmeon2 = Label(text="0", font_size='20sp', pos_hint={'center_x': 0.39+0.03, 'center_y':0.52})
        self.add_widget(self.cptalarmeon2)
        self.cptalarmeoff2 = Label(text="0", font_size='20sp', pos_hint={'center_x': 0.640-0.045, 'center_y':0.52})
        self.add_widget(self.cptalarmeoff2)


        # # Alarme Channel 3
        # self.alarmeon3 = Label(text="3.3A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.917, 'center_y':0.623})
        # self.add_widget(self.alarmeon3)
        # self.alarmeoff3 = Label(text="333uA", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.980, 'center_y':0.623})
        # self.add_widget(self.alarmeoff3)
        
        #Label compteur alarme Channel 3
        self.cptalarmeon3 = Label(text="0", font_size='20sp', size=(100, 50),  pos_hint={'center_x': 0.73+0.03, 'center_y':0.52})
        self.add_widget(self.cptalarmeon3)
        self.cptalarmeoff3 = Label(text="0", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.980-0.045, 'center_y':0.52})
        self.add_widget(self.cptalarmeoff3)

        # # Alarme Channel 4
        # self.alarmeon4 = Label(text="4.4A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.25, 'center_y':0.15})
        # self.add_widget(self.alarmeon4)
        # self.alarmeoff4 = Label(text="444uA", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.305, 'center_y':0.15})
        # self.add_widget(self.alarmeoff4)
        
        #Label compteur alarme Channel 4
        self.cptalarmeon4 = Label(text="0", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.05+0.03, 'center_y':0.05})
        self.add_widget(self.cptalarmeon4)
        self.cptalarmeoff4 = Label(text="0", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.305-0.045, 'center_y':0.05})
        self.add_widget(self.cptalarmeoff4)

        # # Alarme Channel 5
        # self.alarmeon5 = Label(text="5.5A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.585, 'center_y':0.15})
        # self.add_widget(self.alarmeon5)
        # self.alarmeoff5 = Label(text="444uA", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.640, 'center_y':0.15})
        # self.add_widget(self.alarmeoff5)
        
        #Label compteur alarme Channel 5
        self.cptalarmeon5 = Label(text="0", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.39+0.03, 'center_y':0.05})
        self.add_widget(self.cptalarmeon5)
        self.cptalarmeoff5 = Label(text="0", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.640-0.045, 'center_y':0.05})
        self.add_widget(self.cptalarmeoff5)

        # # Alarme Channel 6
        # self.alarmeon6 = Label(text="6.6A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.917, 'center_y':0.15})
        # self.add_widget(self.alarmeon6)
        # self.alarmeoff6 = Label(text="666uA", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.980, 'center_y':0.15})
        # self.add_widget(self.alarmeoff6)
        
        #Label compteur alarme Channel 6
        self.cptalarmeon6 = Label(text="0", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.73+0.03, 'center_y':0.05})
        self.add_widget(self.cptalarmeon6)
        self.cptalarmeoff6 = Label(text="0", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.980-0.045, 'center_y':0.05})
        self.add_widget(self.cptalarmeoff6)

        #Label value max channel 1
        self.maxAOn1 = Label(text="0A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.05+0.03, 'center_y':0.623})
        self.add_widget(self.maxAOn1)
        # self.maxWOn1 = Label(text="1W", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.05, 'center_y':0.52})
        # self.add_widget(self.maxWOn1)
        self.maxAoff1 = Label(text="0mA", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.16+0.1, 'center_y':0.623})
        self.add_widget(self.maxAoff1)
        # self.maxWoff1 = Label(text="1mW", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.16, 'center_y':0.52})
        # self.add_widget(self.maxWoff1)

        #Label value max channel 2
        self.maxAOn2 = Label(text="0A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.39+0.03, 'center_y':0.623})
        self.add_widget(self.maxAOn2)
        # self.maxWOn2 = Label(text="2W", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.39, 'center_y':0.52})
        # self.add_widget(self.maxWOn2)
        self.maxAoff2 = Label(text="0mA", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.5+0.1, 'center_y':0.623})
        self.add_widget(self.maxAoff2)
        # self.maxWoff2 = Label(text="2MW", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.5, 'center_y':0.52})
        # self.add_widget(self.maxWoff2)

        #Label value max channel 3
        self.maxAOn3 = Label(text="0A", font_size='20sp', size=(100, 50),  pos_hint={'center_x': 0.73+0.03, 'center_y':0.623})
        self.add_widget(self.maxAOn3)
        # self.maxWOn3 = Label(text="3W", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.73, 'center_y':0.52})
        # self.add_widget(self.maxWOn3)
        self.maxAoff3 = Label(text="0mA", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.84+0.1, 'center_y':0.623})
        self.add_widget(self.maxAoff3)
        # self.maxWoff3 = Label(text="3mW", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.84, 'center_y':0.52})
        # self.add_widget(self.maxWoff3)

        #Label value max channel 4
        self.maxAOn4 = Label(text="0A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.05+0.03, 'center_y':0.15})
        self.add_widget(self.maxAOn4)
        # self.maxWOn4 = Label(text="4W", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.05, 'center_y':0.05})
        # self.add_widget(self.maxWOn4)
        self.maxAoff4 = Label(text="0mA", font_size='20sp', size=(100, 50),  pos_hint={'center_x': 0.16+0.1, 'center_y':0.15})
        self.add_widget(self.maxAoff4)
        # self.maxWoff4 = Label(text="4mW", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.16, 'center_y':0.05})
        # self.add_widget(self.maxWoff4)

        #Label value max channel 5
        self.maxAOn5 = Label(text="0A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.39+0.03, 'center_y':0.15})
        self.add_widget(self.maxAOn5)
        # self.maxWOn5 = Label(text="5W", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.39, 'center_y':0.05})
        # self.add_widget(self.maxWOn5)
        self.maxAoff5 = Label(text="0mA", font_size='20sp', size=(100, 50),  pos_hint={'center_x': 0.5+0.1, 'center_y':0.15})
        self.add_widget(self.maxAoff5)
        # self.maxWoff5 = Label(text="5mW", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.5, 'center_y':0.05})
        # self.add_widget(self.maxWoff5)

        #Label value max channel 6
        self.maxAOn6 = Label(text="0A", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.73+0.03, 'center_y':0.15})
        self.add_widget(self.maxAOn6)
        # self.maxWOn6 = Label(text="6W", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.73, 'center_y':0.05})
        # self.add_widget(self.maxWOn6)
        self.maxAoff6 = Label(text="0mA", font_size='20sp', size=(100, 50),  pos_hint={'center_x': 0.84+0.1, 'center_y':0.15})
        self.add_widget(self.maxAoff6)
        # self.maxWoff6 = Label(text="6mW", font_size='20sp', size=(100, 50), pos_hint={'center_x': 0.84, 'center_y':0.05})
        # self.add_widget(self.maxWoff6)


       

        # Création de l'affiche dynamique de l'état de chaque équipements testés
        # Led rouge/verte-sleep/awake
        with self.canvas:
            self.rect_dut_1 = Rectangle(pos=(135,640),size=(30,30),source="images/ledred.png")
            self.rect_dut_2 = Rectangle(pos=(560,640),size=(30,30),source="images/ledred.png")
            self.rect_dut_3 = Rectangle(pos=(985,640),size=(30,30),source="images/ledred.png")
            self.rect_dut_4 = Rectangle(pos=(135,280),size=(30,30),source="images/ledred.png")
            self.rect_dut_5 = Rectangle(pos=(560,280),size=(30,30),source="images/ledred.png")
            self.rect_dut_6 = Rectangle(pos=(985,280),size=(30,30),source="images/ledred.png")
##############################################################################################
            
    def timer(self, dt): 
        statut=0
        if(passerelle.start_stop == 1):
            # A1_mA, A2_mA, A3_mA, A4_mA=0,0,0,0
            # W1_mA, W2_mA, W3_mA, W4_mA=0,0,0,0
            A1_mA, A2_mA, A3_mA, A4_mA, A5_mA, A6_mA = 0,0,0,0,0,0
            W1_mA, W2_mA, W3_mA, W4_mA, W5_mA, W6_mA =0,0,0,0,0,0
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            ####################################################################################
            #Récupération des données Serial
            ####################################################################################
            inbox_code = arduino1.readline()
            inbox = inbox_code.decode()
            inbox =str(inbox)
            #Logger.warning('timer: valeur : {}'.format(inbox))
            #Logger.warning('timer: nombre de deux points : {}'.format(inbox.count(':')))
            # if(inbox.count(':')!=13):
            #     statut,U1,W1,A1,U2,W2,A2,U3,W3,A3,U4,W4,A4,bullshit=0,0,0,0,0,0,0,0,0,0,0,0,0,0
            #     Logger.warning("timer: Bug du double bus")
            #     Logger.warning("timer : {}".format(inbox))
            # elif (inbox[0]=='d'):
            #     statut,U1,W1,A1,U2,W2,A2,U3,W3,A3,U4,W4,A4,bullshit=0,0,0,0,0,0,0,0,0,0,0,0,0,0
            #     Logger.warning("debug arduino: {}".format(inbox))
            # else:   
            #     statut,U1,W1,A1,U2,W2,A2,U3,W3,A3,U4,W4,A4,bullshit = inbox.split(":")
            if(inbox.count(':')!=19):
                statut, U1,W1,A1, U2,W2,A2, U3,W3,A3, U4,W4,A4, U5,W5,A5, U6,W6,A6 ,bullshit= 0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0
                Logger.warning("timer: Bug du double bus")
                Logger.warning("timer : {}".format(inbox))
            elif (inbox[0]=='d'):
                statut, U1,W1,A1, U2,W2,A2, U3,W3,A3, U4,W4,A4, U5,W5,A5, U6,W6,A6,bullshit = 0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0
                Logger.warning("debug arduino: {}".format(inbox))
            else:   
                statut, U1,W1,A1, U2,W2,A2, U3,W3,A3, U4,W4,A4, U5,W5,A5, U6,W6,A6, bullshit = inbox.split(":")
                Logger.info("debug arduino: {}".format(inbox))

            ####################################################################################
            ####Conversion de la mesure en mA pour pouvoir la comparer aux alarmes sleep et awake
            ####################################################################################
            alarm_awake_mA=passerelle.alarm_awake*1000
            alarm_sleep_mA=float(passerelle.alarm_sleep)/1000
            #Logger.warning('alarme awake : {} mA ; alarme sleep : {} '.format(alarm_awake_mA, alarm_sleep_mA))

            if(U1=='0'):
                A1_mA=float(A1)/1000
                W1_mA=float(W1)/1000
            elif(U1=='1'):
                A1_mA=float(A1)
                W1_mA=float(W1)
            elif(U1=='2'):
                A1_mA=float(A1)*1000
                W1_mA=float(W1)*1000
            else:
                A1_mA=0
                W1_mA=0
                Logger.warning("conversion mA: Problème de conversion : valeur de U1 : {}".format(U1))

            if(U2=='0'):
                A2_mA=float(A2)/1000
                W2_mA=float(W2)/1000
            elif(U2=='1'):
                A2_mA=float(A2)
                W2_mA=float(W2)
            elif(U2=='2'):
                A2_mA=float(A2)*1000
                W2_mA=float(W2)*1000
            else:
                A2_mA=0
                W2_mA=0
                Logger.warning("conversion mA: Problème de conversion valeur de U2 : {}".format(U2))
            
            if(U3=='0'):
                A3_mA=float(A3)/1000
                W3_mA=float(W3)/1000
            elif(U3=='1'):
                A3_mA=float(A3)
                W3_mA=float(W3)
            elif(U3=='2'):
                A3_mA=float(A3)*1000
                W3_mA=float(W3)*1000
            else:
                A3_mA=0
                W3_mA=0
                Logger.warning("conversion mA: Problème de conversion valeur de U3 : {}".format(U3))
            
            if(U4=='0'):
                A4_mA=float(A4)/1000
                W4mA=float(W4)/1000
            elif(U4=='1'):
                A4_mA=float(A4)
                W4_mA=float(W4)
            elif(U4=='2'):
                A4_mA=float(A4)*1000
                W4_mA=float(W4)*1000
            else:
                A4_mA=0
                W4_mA=0
                Logger.warning("conversion mA: Problème de conversion valeur de U4 : {}".format(U4))

            if(U5=='0'):
                A5_mA=float(A5)/1000
                W5_mA=float(W5)/1000
            elif(U5=='1'):
                A5_mA=float(A5)
                W5_mA=float(W5)
            elif(U5=='2'):
                A5_mA=float(A5)*1000
                W5_mA=float(W5)*1000
            else:
                A5_mA=0
                W5_mA=0
                Logger.warning("conversion mA: Problème de conversion valeur de U5 : {}".format(U5))
            
            if(U6=='0'):
                A6_mA=float(A6)/1000
                W6mA=float(W6)/1000
            elif(U6=='1'):
                A6_mA=float(A6)
                W6_mA=float(W6)
            elif(U6=='2'):
                A6_mA=float(A6)*1000
                W6_mA=float(W6)*1000
            else:
                A6_mA=0
                W6_mA=0
                Logger.warning("conversion mA: Problème de conversion valeur de U6 : {}".format(U6))

            ####################################

           

            #Logger.warning("conversion mA: valeur de A1_m1 : {}  ;  A2_MA : {} ;   A3_mA : {} ;  A4_mA : {} ; ".format(A1_mA, A2_mA, A3_mA, A4_mA))

            ##################################################################################################
            ######INCREMENTATION DES ALARMES DE DEPASSEMENT DE SEUIL ET ECRITURE DANS LE FICHIER ASSOCIE######
            ##################################################################################################

            #Logger.warning('ligne n°{}: statut : {}   flag_seuil : {}'.format(inspect.currentframe().f_lineno, statut, passerelle.flag_seuil))


            # if(statut=='0'):
            #     Logger.warning('ligne n°{}: statut ok'.format(inspect.currentframe().f_lineno))

            # if(passerelle.flag_seuil==False):
            #     Logger.warning('ligne n°{}: flag_seuil ok'.format(inspect.currentframe().f_lineno))

            # if(passerelle.flag_seuil==0):
            #     Logger.warning('test: test')

            if((passerelle.flag_seuil==False) and (statut=='0')):
                a=time.time()-passerelle.timer_delai_init

                #Logger.warning('ligne n°{}: temps écoulé depuis passage off : {}   statut : {}'.format(inspect.currentframe().f_lineno, a, statut))

                if((A1_mA<alarm_sleep_mA) and (A2_mA<alarm_sleep_mA) and (A3_mA<alarm_sleep_mA) and (A4_mA<alarm_sleep_mA)):

                    timer_print=time.time()-passerelle.timer_delai_init
                    Logger.warning('timer delai: {}'.format(timer_print) )
                    passerelle.flag_seuil=True

                if((a>25) and (statut=='0')):
                    Logger.warning('ligne n°{}: 25 secondes ecoulé depuis passage off'.format(inspect.currentframe().f_lineno))



            if((statut=='0') and (passerelle.flag_delai==False)):

                Logger.warning('init : initialisé')
                passerelle.flag_delai=True
                passerelle.timer_delai_init=time.time()
                Logger.warning('init: timer_init : {}'.format(passerelle.timer_delai_init))


            if((statut=='0') and (passerelle.flag_seuil==True)):
                if (A1_mA>alarm_sleep_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmoffdut1=passerelle.cptalarmoffdut1+1
                    Logger.warning("alarme: valeur de cptalarmoffdut1 : {}".format(passerelle.cptalarmoffdut1))
                    self.cptalarmeoff1.text=str(passerelle.cptalarmoffdut1)
                    print >> out5, ";".join([date, str(A1_mA), "mA", "Sleep"])

                if(A2_mA>alarm_sleep_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmoffdut2=passerelle.cptalarmoffdut2+1
                    Logger.warning("alarme: valeur de cptalarmoffdut2 : {}".format(passerelle.cptalarmoffdut2))
                    self.cptalarmeoff2.text=str(passerelle.cptalarmoffdut2)
                    print >> out6, ";".join([date, str(A2_mA), "mA", "Sleep"])

                if(A3_mA>alarm_sleep_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmoffdut3=passerelle.cptalarmoffdut3+1
                    Logger.warning("alarme: valeur de cptalarmoffdut3 : {}".format(passerelle.cptalarmoffdut3))
                    self.cptalarmeoff3.text=str(passerelle.cptalarmoffdut3)
                    print >> out7, ";".join([date, str(A3_mA), "mA", "Sleep"])
                

                if(A4_mA>alarm_sleep_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmoffdut4=passerelle.cptalarmoffdut4+1
                    Logger.warning("alarme: valeur de cptalarmoffdut4 : {}".format(passerelle.cptalarmoffdut4))
                    self.cptalarmeoff4.text=str(passerelle.cptalarmoffdut4)
                    print >> out8, ";".join([date, str(A4_mA), "mA", "Sleep"])
                    Logger.warning("écriture dans le ficheir ")

                if(A5_mA>alarm_sleep_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmoffdut5=passerelle.cptalarmoffdut5+1
                    Logger.warning("alarme: valeur de cptalarmoffdut5 : {}".format(passerelle.cptalarmoffdut5))
                    self.cptalarmeoff5.text=str(passerelle.cptalarmoffdut5)
                    print >> out555, ";".join([date, str(A5_mA), "mA", "Sleep"])
                    Logger.warning("écriture dans le ficheir ")

                
                if(A6_mA>alarm_sleep_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmoffdut6=passerelle.cptalarmoffdut6+1
                    Logger.warning("alarme: valeur de cptalarmoffdut6 : {}".format(passerelle.cptalarmoffdut6))
                    self.cptalarmeoff6.text=str(passerelle.cptalarmoffdut6)
                    print >> out666, ";".join([date, str(A6_mA), "mA", "Sleep"])
                    Logger.warning("écriture dans le ficheir ")

            if(statut=='1'):

                if(passerelle.flag_seuil==True):
                    passerelle.flag_seuil=False
                if(passerelle.flag_delai==True):
                    passerelle.flag_delai=False


                if(A1_mA>alarm_awake_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmondut1=passerelle.cptalarmondut1+1
                    Logger.warning("alarme: valeur de cptalarmondut1 : {}".format(passerelle.cptalarmondut1))
                    self.cptalarmeon1.text=str(passerelle.cptalarmondut1)
                    print >> out5, ";".join([date, str(A1_mA), "mA", "Awake"])

                if(A2_mA>alarm_awake_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmondut2=passerelle.cptalarmondut2+1
                    Logger.warning("alarme: valeur de cptalarmondut2 : {}".format(passerelle.cptalarmondut2))
                    self.cptalarmeon2.text=str(passerelle.cptalarmondut2)
                    print >> out6, ";".join([date, str(A2_mA), "mA", "Awake"])

                if(A3_mA>alarm_awake_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmondut3=passerelle.cptalarmondut3+1
                    Logger.warning("alarme: valeur de cptalarmondut3 : {}".format(passerelle.cptalarmondut3))
                    self.cptalarmeon3.text=str(passerelle.cptalarmondut3)
                    print >> out7, ";".join([date, str(A3_mA), "mA", "Awake"])

    
                if(A4_mA>alarm_awake_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmondut4=passerelle.cptalarmondut4+1
                    Logger.warning("alarme: valeur de cptalarmondut4 : {}".format(passerelle.cptalarmondut4))
                    self.cptalarmeon4.text=str(passerelle.cptalarmondut4)
                    print >> out8, ";".join([date, str(A4_mA), "mA", "Awake"])
                
                if(A5_mA>alarm_awake_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmondut5=passerelle.cptalarmondut5+1
                    Logger.warning("alarme: valeur de cptalarmondut5 : {}".format(passerelle.cptalarmondut5))
                    self.cptalarmeon5.text=str(passerelle.cptalarmondut5)
                    print >> out555, ";".join([date, str(A5_mA), "mA", "Awake"])

                
                if(A6_mA>alarm_awake_mA):
                    Logger.warning("alarme: seuil dépassé")
                    passerelle.cptalarmondut4=passerelle.cptalarmondut6+1
                    Logger.warning("alarme: valeur de cptalarmondut6 : {}".format(passerelle.cptalarmondut6))
                    self.cptalarmeon6.text=str(passerelle.cptalarmondut6)
                    print >> out666, ";".join([date, str(A6_mA), "mA", "Awake"])
                    
                    
            


            if(U1 == '1'):
                self.courant1.text = A1 + "  mA"
                # W11 = W1.replace(".",",")
                # A11 = A1.replace(".",",")
                # if(statut == '0'):
                #     print >> out1, ";".join([date, A11, "mA", W11, "mW", "Sleep"])
                # if(statut == '1'):
                #     print >> out1, ";".join([date, A11, "mA", W11, "mW", "Awake"])

            if(U2=='1'):        
                self.courant2.text = A2 + "  mA"
                # W22 = W2.replace(".",",")
                # A22 = A2.replace(".",",")
                # if(statut == '0'):
                #     print >> out2, ";".join([date, A22, "mA", W22, "mW", "Sleep"])
                # if(statut == '1'):
                #     print >> out2, ";".join([date, A22, "mA", W22, "mW", "Awake"])

            if(U3=='1'):    
                self.courant3.text = A3 + "  mA"
                # W33 = W3.replace(".",",")
                # A33 = A3.replace(".",",")
                # if(statut == '0'):
                #     print >> out3, ";".join([date, A33, "mA", W33, "mW", "Sleep"])
                # if(statut == '1'):
                #     print >> out3, ";".join([date, A33, "mA", W33, "mW", "Awake"])

            if(U4=='1'):    
                self.courant4.text = A4 + "  mA"
                # W44 = W4.replace(".",",")
                # A44 = A4.replace(".",",")
                # if(statut == '0'):
                #     print >> out4, ";".join([date, A44, "mA", W44, "mW", "Sleep"])
                # if(statut == '1'):
                #     print >> out4, ";".join([date, A44, "mA", W44, "mW", "Awake"])
            
            if(U5=='1'):    
                self.courant5.text = A5 + "  mA"
            
            if(U6=='1'):    
                self.courant6.text = A6 + "  mA"

            if(U1 == '0'):
                self.courant1.text = A1 + "  µA"
                #Logger.warning('Ecriture Fichier: valeur de A1 avant castage : {}'.format(A1))
                # A1 = float(A1)
                # #Logger.warning('Ecriture Fichier: valeur de A1 après castage : {}'.format(A1))
                # W11 = W1.replace(".",",")
                # A11 = str(A1).replace(".",",")
                # #Logger.warning('Ecriture Fichier: valeur écrite : {}'.format(A11))
                # if(statut == '0'):
                #     print >> out1, ";".join([date, A11, "uA", W11, "uW", "Sleep"])
                # if(statut == '1'):
                #     print >> out1, ";".join([date, A11, "uA", W11, "uW", "Awake"])
            
            if(U2=='0'):    
                self.courant2.text = A2 + "  µA"
                # A2 = float(A2)
                # W22 = W2.replace(".",",")
                # A22 = str(A2).replace(".",",")
                # if(statut == '0'):
                #     print >> out2, ";".join([date, A22, "uA", W22,"uW", "Sleep"])
                # if(statut == '1'):
                #     print >> out2, ";".join([date, A22, "uA", W22, "uW","Awake"])

            if(U3=='0'):    
                self.courant3.text = A3 + "  µA"
                # A3 = float(A3)
                # W33 = W3.replace(".",",")
                # A33 = str(A3).replace(".",",")
                # if(statut == '0'):
                #     print >> out3, ";".join([date, A33, "uA", W33, "uW","Sleep"])
                # if(statut == '1'):
                #     print >> out3, ";".join([date, A33, "uA", W33,"uW", "Awake"])
            
            if(U4=='0'):    
                self.courant4.text = A4 + "  µA"
                # A4 = float(A4)
                # W44 = W4.replace(".",",")
                # A44 = str(A4).replace(".",",")
                # if(statut == '0'):
                #     print >> out4, ";".join([date, A44, "uA", W44, "uW","Sleep"])
                # if(statut == '1'):
                #     print >> out4, ";".join([date, A44, "uA", W44, "uW","Awake"])

            if(U5=='0'):    
                self.courant5.text = A5 + "  µA"

            if(U6=='0'):    
                self.courant6.text = A6 + "  µA"

            if(U1 == '2'):
                self.courant1.text = A1 + "  A"
                # A1 = float(A1)
                # W11 = W1.replace(".",",")
                # A11 = str(A1).replace(".",",")
                # if(statut == '0'):
                #     print >> out1, ";".join([date, A11, "A", W11, "W","Sleep"])
                # if(statut == '1'):
                #     print >> out1, ";".join([date, A11, "A", W11, "W","Awake"])
            
            if(U2 == '2'):    
                self.courant2.text = A2 + "  A"
                # A2 = float(A2)
                # W22 = W2.replace(".",",")
                # A22 = str(A2).replace(".",",")
                # if(statut == '0'):
                #     print >> out2, ";".join([date, A22, "A", W22, "W","Sleep"])
                # if(statut == '1'):
                #     print >> out2, ";".join([date, A22, "A", W22, "W","Awake"])
            
            if(U3 == '2'):    
                self.courant3.text = A3 + "  A"
                # A3 = float(A3)
                # W33 = W3.replace(".",",")
                # A33 = str(A3).replace(".",",")
                # if(statut == '0'):
                #     print >> out3, ";".join([date, A33, "A", W33, "W","Sleep"])
                # if(statut == '1'):
                #     print >> out3, ";".join([date, A33, "A", W33, "W","Awake"])
            
            if(U4 == '2'):    
                self.courant4.text = A4 + "  A"
                # A4 = float(A4)
                # W44 = W4.replace(".",",")
                # A44 = str(A4).replace(".",",")
                # if(statut == '0'):
                #     print >> out4, ";".join([date, A44, "A", W44, "W","Sleep"])
                # if(statut == '1'):
                #     print >> out4, ";".join([date, A44, "A", W44, "W","Awake"])

            if(U5 == '2'):    
                self.courant5.text = A5 + "  A"

            if(U6 == '2'):    
                self.courant6.text = A6 + "  A"

            A11=str(A1_mA).replace(".",",")
            W11=str(W1_mA).replace(".",",")

            A22=str(A2_mA).replace(".",",")
            W22=str(W2_mA).replace(".",",")

            A33=str(A3_mA).replace(".",",")
            W33=str(W3_mA).replace(".",",")

            A44=str(A4_mA).replace(".",",")
            W44=str(W4_mA).replace(".",",")

            A55=str(A5_mA).replace(".",",")
            W55=str(W5_mA).replace(".",",")

            A66=str(A6_mA).replace(".",",")
            W66=str(W6_mA).replace(".",",")

            # if(statut == '0'):
            #     print >> out1, ";".join([date, A11, "mA", W11, "mW","Sleep"])
            # if(statut == '1'):
            #     print >> out1, ";".join([date, A11, "mA", W11, "mW","Awake"])

            # if(statut == '0'):
            #     print >> out2, ";".join([date, A22, "mA", W22, "mW","Sleep"])
            # if(statut == '1'):
            #     print >> out2, ";".join([date, A22, "mA", W22, "mW","Awake"])

            # if(statut == '0'):
            #     print >> out3, ";".join([date, A33, "mA", W33, "mW","Sleep"])
            # if(statut == '1'):
            #     print >> out3, ";".join([date, A33, "mA", W33, "mW","Awake"])

            # if(statut == '0'):
            #     print >> out4, ";".join([date, A44, "mA", W44, "mW","Sleep"])
            # if(statut == '1'):
            #     print >> out4, ";".join([date, A44, "mA", W44, "mW","Awake"])

            # if(statut == '0'):
            #     print >> out55, ";".join([date, A55, "mA", W55, "mW","Sleep"])
            # if(statut == '1'):
            #     print >> out55, ";".join([date, A55, "mA", W55, "mW","Awake"])

            # if(statut == '0'):
            #     print >> out66, ";".join([date, A66, "mA", W66, "mW","Sleep"])
            # if(statut == '1'):
            #     print >> out66, ";".join([date, A66, "mA", W66, "mW","Awake"])

            if(statut == '0'):
                print((";".join([date, A11, "mA", W11, "mW","Sleep"])), file=out1)
            if(statut == '1'):
                print((";".join([date, A11, "mA", W11, "mW","Awake"])), file=out1)

            if(statut == '0'):
                print((";".join([date, A22, "mA", W22, "mW","Sleep"])), file=out2)
            if(statut == '1'):
                print((";".join([date, A22, "mA", W22, "mW","Awake"])), file=out2)

            if(statut == '0'):
                print((";".join([date, A33, "mA", W33, "mW","Sleep"])), file=out3)
            if(statut == '1'):
                print((";".join([date, A33, "mA", W33, "mW","Awake"])), file=out3)

            if(statut == '0'):
                print((";".join([date, A44, "mA", W44, "mW","Sleep"])), file=out4)
            if(statut == '1'):
                print((";".join([date, A44, "mA", W44, "mW","Awake"])), file=out4)

            if(statut == '0'):
                print((";".join([date, A55, "mA", W55, "mW","Sleep"])), file=out55)
            if(statut == '1'):
                print((";".join([date, A55, "mA", W55, "mW","Awake"])), file=out55)

            if(statut == '0'):
                print((";".join([date, A66, "mA", W66, "mW","Sleep"])), file=out66)
            if(statut == '1'):
                print((";".join([date, A66, "mA", W66, "mW","Awake"])), file=out66)


            #Logger.warning('test format log: date : {} ; ligne n°{}: test format log'.format(str(datetime.now()),inspect.currentframe().f_lineno))
     
           

            if(passerelle.update_alarm == 1):           
                # self.alarmeon1.text = (str(passerelle.alarm_awake)+" A")
                # self.alarmeoff1.text = (str(passerelle.alarm_sleep)+" µA")
                # self.alarmeon2.text = (str(passerelle.alarm_awake)+" A")
                # self.alarmeoff2.text = (str(passerelle.alarm_sleep)+" µA")
                # self.alarmeon3.text = (str(passerelle.alarm_awake)+" A")ddddd
                # self.alarmeoff3.text = (str(passerelle.alarm_sleep)+" µA")
                # self.alarmeon4.text = (str(passerelle.alarm_awake)+" A")
                # self.alarmeoff4.text = (str(passerelle.alarm_sleep)+" µA")
                # self.alarmeon5.text = (str(passerelle.alarm_awake)+" A")
                # self.alarmeoff5.text = (str(passerelle.alarm_sleep)+" µA")
                # self.alarmeon6.text = (str(passerelle.alarm_awake)+" A")
                # self.alarmeoff6.text = (str(passerelle.alarm_sleep)+" µA")
                passerelle.update_alarm = 0
            
            U1 = int(U1)
            U2 = int(U2)
            U3 = int(U3)
            U4 = int(U4)
            U5 = int(U5)
            U6 = int(U6)

            A1 = float(A1)
            A2 = float(A2)
            A3 = float(A3)
            A4 = float(A4)
            A5 = float(A5)
            A6 = float(A6)

            W1 = float(W1)
            W2 = float(W2)
            W3 = float(W3)
            W4 = float(W4)
            W5 = float(W5)
            W6 = float(W6)


            if(statut=='0'):
                if(passerelle.U1offMax<U1):
                    passerelle.U1offMax=U1
                    passerelle.A1offMax=A1
                    passerelle.W1offMax=W1
                    passerelle.updateMax=True

                else :
                    if((passerelle.A1offMax<A1) and (passerelle.U1offMax==U1)):
                        passerelle.A1offMax=A1
                        passerelle.updateMax=True
                    if((passerelle.W1offMax<W1) and (passerelle.U1offMax==U1)) :
                        passerelle.W1offMax=W1
                        passerelle.updateMax=True

                if(passerelle.U2offMax<U2):
                    passerelle.U2offMax=U2
                    passerelle.A2offMax=A2
                    passerelle.W2offMax=W2
                    passerelle.updateMax=True
                else:
                    if((passerelle.A2offMax<A2) and (passerelle.U2offMax==U2)):
                        passerelle.A2offMax=A2
                        passerelle.updateMax=True
                    if((passerelle.W2offMax<W2) and (passerelle.U2offMax==U2)):
                        passerelle.W2offMax=W2
                        passerelle.updateMax=True

                if(passerelle.U3offMax<U3):
                    passerelle.U3offMax=U3
                    passerelle.A3offMax=A3
                    passerelle.W3offMax=W3
                    passerelle.updateMax=True
                else:
                    if((passerelle.A3offMax<A3) and (passerelle.U3offMax==U3)):
                        passerelle.A3offMax=A3
                        passerelle.updateMax=True
                    if((passerelle.W3offMax<W3) and (passerelle.U3offMax==U3)):
                        passerelle.W3offMax=W3
                        passerelle.updateMax=True  

                if(passerelle.U4offMax<U4):
                    passerelle.U4offMax=U4
                    passerelle.A4offMax=A4
                    passerelle.W4offMax=W4
                    passerelle.updateMax=True
                else:
                    if((passerelle.A4offMax<A4) and (passerelle.U4offMax==U4)):
                        passerelle.A4offMax=A4
                        passerelle.updateMax=True
                    if((passerelle.W4offMax<W4) and (passerelle.U4offMax==U4)):
                        passerelle.W4offMax=W4
                        passerelle.updateMax=True   

                if(passerelle.U5offMax<U5):
                    passerelle.U5offMax=U5
                    passerelle.A5offMax=A5
                    passerelle.W5offMax=W5
                    passerelle.updateMax=True
                else:
                    if((passerelle.A5offMax<A5) and (passerelle.U5offMax==U5)):
                        passerelle.A5offMax=A5
                        passerelle.updateMax=True
                    if((passerelle.W4offMax<W5) and (passerelle.U5offMax==U5)):
                        passerelle.W5offMax=W5
                        passerelle.updateMax=True   

                if(passerelle.U6offMax<U6):
                    passerelle.U6offMax=U6
                    passerelle.A6offMax=A6
                    passerelle.W6offMax=W6
                    passerelle.updateMax=True
                else:
                    if((passerelle.A6offMax<A6) and (passerelle.U6offMax==U6)):
                        passerelle.A6offMax=A6
                        passerelle.updateMax=True
                    if((passerelle.W6offMax<W6) and (passerelle.U6offMax==U6)):
                        passerelle.W6offMax=W6
                        passerelle.updateMax=True       


            if(statut=='1'):
                if(passerelle.U1onMax<U1):
                    passerelle.U1onMax=U1
                    passerelle.A1onMax=A1
                    passerelle.W1onMax=W1
                    passerelle.updateMax=True
                else :
                    if((passerelle.A1onMax<A1) and (passerelle.U1onMax==U1)):
                        passerelle.A1onMax=A1
                        passerelle.updateMax=True
                    if((passerelle.W1onMax<W1) and (passerelle.U1onMax==U1)):
                        passerelle.W1onMax=W1
                        passerelle.updateMax=True

                if(passerelle.U2onMax<U2):
                    passerelle.U2onMax=U2
                    passerelle.A2onMax=A2
                    passerelle.W2onMax=W2
                    passerelle.updateMax=True
                else:
                    if((passerelle.A2onMax<A2) and (passerelle.U2onMax==U2)):
                        passerelle.A2onMax=A2
                        passerelle.updateMax=True
                    if((passerelle.W2onMax<W2) and (passerelle.U2onMax==U2)):
                        passerelle.W2onMax=W2
                        passerelle.updateMax=True

                if(passerelle.U3onMax<U3):
                    passerelle.U3onMax=U3
                    passerelle.A3onMax=A3
                    passerelle.W3onMax=W3
                    passerelle.updateMax=True
                else:
                    if((passerelle.A3onMax<A3) and (passerelle.U3onMax==U3)):
                        passerelle.A3onMax=A3
                        passerelle.updateMax=True
                    if((passerelle.W3onMax<W3) and (passerelle.U3onMax==U3)):
                        passerelle.W3onMax=W3
                        passerelle.updateMax=True  

                if(passerelle.U4onMax<U4):
                    passerelle.U4onMax=U4
                    passerelle.A4onMax=A4
                    passerelle.W4onMax=W4
                    passerelle.updateMax=True
                else:
                    if((passerelle.A4onMax<A4) and (passerelle.U4onMax==U4)):
                        passerelle.A4onMax=A4
                        passerelle.updateMax=True
                    if((passerelle.W4onMax<W4) and (passerelle.U4onMax==U4)):
                        passerelle.W4onMax=W4
                        passerelle.updateMax=True      

                if(passerelle.U5onMax<U5):
                    passerelle.U5onMax=U5
                    passerelle.A5onMax=A5
                    passerelle.W5onMax=W5
                    passerelle.updateMax=True
                else:
                    if((passerelle.A5onMax<A5) and (passerelle.U5onMax==U5)):
                        passerelle.A5onMax=A5
                        passerelle.updateMax=True
                    if((passerelle.W5onMax<W5) and (passerelle.U5onMax==U5)):
                        passerelle.W5onMax=W5
                        passerelle.updateMax=True   

                if(passerelle.U6onMax<U6):
                    passerelle.U6onMax=U6
                    passerelle.A6onMax=A6
                    passerelle.W6onMax=W6
                    passerelle.updateMax=True
                else:
                    if((passerelle.A6onMax<A6) and (passerelle.U6onMax==U6)):
                        passerelle.A6onMax=A6
                        passerelle.updateMax=True
                    if((passerelle.W6onMax<W6) and (passerelle.U6onMax==U6)):
                        passerelle.W6onMax=W6
                        passerelle.updateMax=True         


            #Affichage des Max
            if(passerelle.updateMax):

                if(passerelle.U1onMax=='0'):
                    self.maxAOn1.text=(str(passerelle.A1onMax)+ " uA")
                    self.maxWOn1.text=(str(passerelle.W1onMax)+" uW")
                elif(passerelle.U1onMax=='1'):  
                    self.maxAOn1.text=(str(passerelle.A1onMax)+ " mA") 
                    self.maxWOn1.text=(str(passerelle.W1onMax)+" mW") 
                elif(passerelle.U1onMax=='2'):  
                    self.maxAOn1.text=(str(passerelle.A1onMax)+ " A")
                    self.maxWOn1.text=(str(passerelle.W1onMax)+" W")  

                if(passerelle.U2onMax=='0'):
                    self.maxAOn2.text=(str(passerelle.A2onMax)+ " uA")
                    self.maxWOn2.text=(str(passerelle.W2onMax)+" uW")
                elif(passerelle.U2onMax=='1'):  
                    self.maxAOn2.text=(str(passerelle.A2onMax)+ " mA") 
                    self.maxWOn2.text=(str(passerelle.W2onMax)+" mW") 
                elif(passerelle.U2onMax=='2'):  
                    self.maxAOn2.text=(str(passerelle.A2onMax)+ " A")
                    self.maxWOn2.text=(str(passerelle.W2onMax)+" W")

                if(passerelle.U3onMax=='0'):
                    self.maxAOn3.text=(str(passerelle.A3onMax)+ " uA")
                    self.maxWOn3.text=(str(passerelle.W3onMax)+" uW")
                elif(passerelle.U3onMax=='1'):  
                    self.maxAOn3.text=(str(passerelle.A3onMax)+ " mA") 
                    self.maxWOn3.text=(str(passerelle.W3onMax)+" mW") 
                elif(passerelle.U3onMax=='2'):  
                    self.maxAOn3.text=(str(passerelle.A3onMax)+ " A")
                    self.maxWOn3.text=(str(passerelle.W3onMax)+" W")

                if(passerelle.U4onMax=='0'):
                    self.maxAOn4.text=(str(passerelle.A4onMax)+ " uA")
                    self.maxWOn4.text=(str(passerelle.W4onMax)+" uW")
                elif(passerelle.U4onMax=='1'):  
                    self.maxAOn4.text=(str(passerelle.A4onMax)+ " mA") 
                    self.maxWOn4.text=(str(passerelle.W4onMax)+" mW") 
                elif(passerelle.U4onMax=='2'):  
                    self.maxAOn4.text=(str(passerelle.A4onMax)+ " A")
                    self.maxWOn4.text=(str(passerelle.W4onMax)+" W") 

                if(passerelle.U5onMax=='0'):
                    self.maxAOn5.text=(str(passerelle.A5onMax)+ " uA")
                    self.maxWOn5.text=(str(passerelle.W5onMax)+" uW")
                elif(passerelle.U5onMax=='1'):  
                    self.maxAOn5.text=(str(passerelle.A5onMax)+ " mA") 
                    self.maxWOn5.text=(str(passerelle.W5onMax)+" mW") 
                elif(passerelle.U5onMax=='2'):  
                    self.maxAOn5.text=(str(passerelle.A4onMax)+ " A")
                    self.maxWOn5.text=(str(passerelle.W4onMax)+" W") 

                if(passerelle.U6onMax=='0'):
                    self.maxAOn6.text=(str(passerelle.A6onMax)+ " uA")
                    self.maxWOn6.text=(str(passerelle.W6onMax)+" uW")
                elif(passerelle.U6onMax=='1'):  
                    self.maxAOn6.text=(str(passerelle.A6onMax)+ " mA") 
                    self.maxWOn6.text=(str(passerelle.W6onMax)+" mW") 
                elif(passerelle.U6onMax=='2'):  
                    self.maxAOn6.text=(str(passerelle.A6onMax)+ " A")
                    self.maxWOn6.text=(str(passerelle.W6onMax)+" W") 

                if(passerelle.U1offMax=='0'):
                    self.maxAoff1.text=(str(passerelle.A1offMax)+ " uA")
                    self.maxWoff1.text=(str(passerelle.W1offMax)+" uW")
                elif(passerelle.U1offMax=='1'):  
                    self.maxAoff1.text=(str(passerelle.A1offMax)+ " mA") 
                    self.maxWoff1.text=(str(passerelle.W1offMax)+" mW") 
                elif(passerelle.U1offMax=='2'):  
                    self.maxAoff1.text=(str(passerelle.A1offMax)+ " A")
                    self.maxWoff1.text=(str(passerelle.W1offMax)+" W")  

                if(passerelle.U2offMax=='0'):
                    self.maxAoff2.text=(str(passerelle.A2offMax)+ " uA")
                    self.maxWoff2.text=(str(passerelle.W2offMax)+" uW")
                elif(passerelle.U2offMax=='1'):  
                    self.maxAoff2.text=(str(passerelle.A2offMax)+ " mA") 
                    self.maxWoff2.text=(str(passerelle.W2offMax)+" mW") 
                elif(passerelle.U2offMax=='2'):  
                    self.maxAoff2.text=(str(passerelle.A2offMax)+ " A")
                    self.maxWoff2.text=(str(passerelle.W2offMax)+" W")

                if(passerelle.U3offMax=='0'):
                    self.maxAoff3.text=(str(passerelle.A3offMax)+ " uA")
                    self.maxWoff3.text=(str(passerelle.W3offMax)+" uW")
                elif(passerelle.U3offMax=='1'):  
                    self.maxAoff3.text=(str(passerelle.A3offMax)+ " mA") 
                    self.maxWoff3.text=(str(passerelle.W3offMax)+" mW") 
                elif(passerelle.U3offMax=='2'):  
                    self.maxAoff3.text=(str(passerelle.A3offMax)+ " A")
                    self.maxWoff3.text=(str(passerelle.W3offMax)+" W")

                if(passerelle.U4offMax=='0'):
                    self.maxAoff4.text=(str(passerelle.A4offMax)+ " uA")
                    self.maxWoff4.text=(str(passerelle.W4offMax)+" uW")
                elif(passerelle.U4offMax=='1'):  
                    self.maxAoff4.text=(str(passerelle.A4offMax)+ " mA") 
                    self.maxWoff4.text=(str(passerelle.W4offMax)+" mW") 
                elif(passerelle.U4offMax=='2'):  
                    self.maxAoff4.text=(str(passerelle.A4offMax)+ " A")
                    self.maxWoff4.text=(str(passerelle.W4offMax)+" W")   

                if(passerelle.U5offMax=='0'):
                    self.maxAoff5.text=(str(passerelle.A5offMax)+ " uA")
                    self.maxWoff5.text=(str(passerelle.W5offMax)+" uW")
                elif(passerelle.U5offMax=='1'):  
                    self.maxAoff5.text=(str(passerelle.A5offMax)+ " mA") 
                    self.maxWoff5.text=(str(passerelle.W5offMax)+" mW") 
                elif(passerelle.U5offMax=='2'):  
                    self.maxAoff5.text=(str(passerelle.A5offMax)+ " A")
                    self.maxWoff5.text=(str(passerelle.W5offMax)+" W")  
                
                if(passerelle.U6offMax=='0'):
                    self.maxAoff6.text=(str(passerelle.A6offMax)+ " uA")
                    self.maxWoff6.text=(str(passerelle.W6offMax)+" uW")
                elif(passerelle.U6offMax=='1'):  
                    self.maxAoff6.text=(str(passerelle.A6offMax)+ " mA") 
                    self.maxWoff6.text=(str(passerelle.W6offMax)+" mW") 
                elif(passerelle.U6offMax=='2'):  
                    self.maxAoff6.text=(str(passerelle.A6offMax)+ " A")
                    self.maxWoff6.text=(str(passerelle.W6offMax)+" W")  

                passerelle.updateMax=False
        if(statut == '0'):
                self.rect_dut_1.source = "images/ledred.png"
                self.rect_dut_2.source = "images/ledred.png"
                self.rect_dut_3.source = "images/ledred.png"
                self.rect_dut_4.source = "images/ledred.png"
                self.rect_dut_5.source = "images/ledred.png"
                self.rect_dut_6.source = "images/ledred.png"
                
        if(statut == '1'):
                self.rect_dut_1.source = "images/ledgreen.png"
                self.rect_dut_2.source = "images/ledgreen.png"
                self.rect_dut_3.source = "images/ledgreen.png"
                self.rect_dut_4.source = "images/ledgreen.png"
                self.rect_dut_5.source = "images/ledgreen.png"
                self.rect_dut_6.source = "images/ledgreen.png"



    def printscreen(self):

        chemin_screen=adresseUSB+date_titre+'_'+str(passerelle.nb_screen)+".png"
        Logger.warning(chemin_screen)

        self.export_to_png(chemin_screen)
        passerelle.nb_screen+=1
    
        
                


    def startacq(self):
        passerelle.start_stop = 1

        passerelle.flag_seuil=False
        passerelle.flag_delai=False
        passerelle.timer_delai_init=0

        passerelle.cycle1.time_awake=passerelle.cycle1.time_awake_s+passerelle.cycle1.time_awake_m*60+passerelle.cycle1.time_awake_h*3600
        passerelle.cycle1.time_sleep=passerelle.cycle1.time_sleep_s+passerelle.cycle1.time_sleep_m*60+passerelle.cycle1.time_sleep_h*3600

        passerelle.cycle2.time_awake=passerelle.cycle2.time_awake_s+passerelle.cycle2.time_awake_m*60+passerelle.cycle2.time_awake_h*3600
        passerelle.cycle2.time_sleep=passerelle.cycle2.time_sleep_s+passerelle.cycle2.time_sleep_m*60+passerelle.cycle2.time_sleep_h*3600

        passerelle.cycle3.time_awake=passerelle.cycle3.time_awake_s+passerelle.cycle3.time_awake_m*60+passerelle.cycle3.time_awake_h*3600
        passerelle.cycle3.time_sleep=passerelle.cycle3.time_sleep_s+passerelle.cycle3.time_sleep_m*60+passerelle.cycle3.time_sleep_h*3600

        passerelle.cycle4.time_awake=passerelle.cycle3.time_awake_s+passerelle.cycle3.time_awake_m*60+passerelle.cycle3.time_awake_h*3600
        passerelle.cycle3.time_sleep=passerelle.cycle3.time_sleep_s+passerelle.cycle3.time_sleep_m*60+passerelle.cycle3.time_sleep_h*3600

        passerelle.cycle4.time_awake=passerelle.cycle4.time_awake_s+passerelle.cycle4.time_awake_m*60+passerelle.cycle4.time_awake_h*3600
        passerelle.cycle4.time_sleep=passerelle.cycle4.time_sleep_s+passerelle.cycle4.time_sleep_m*60+passerelle.cycle4.time_sleep_h*3600

        passerelle.cycle5.time_awake=passerelle.cycle5.time_awake_s+passerelle.cycle5.time_awake_m*60+passerelle.cycle4.time_awake_h*3600
        passerelle.cycle5.time_sleep=passerelle.cycle5.time_sleep_s+passerelle.cycle5.time_sleep_m*60+passerelle.cycle5.time_sleep_h*3600



        Logger.warning('startacq: lancement acquisition avec comme setup')
        Logger.warning('startacq: valeur de time_awake 1 : {}'.format(passerelle.cycle1.time_awake))
        Logger.warning('startacq: valeur de time_sleep  1: {}'.format(passerelle.cycle1.time_sleep))

        Logger.warning('startacq: valeur de time_awake 2 : {}'.format(passerelle.cycle2.time_awake))
        Logger.warning('startacq: valeur de time_sleep  2: {}'.format(passerelle.cycle2.time_sleep))

        Logger.warning('startacq: valeur de time_awake 3 : {}'.format(passerelle.cycle3.time_awake))
        Logger.warning('startacq: valeur de time_sleep  3: {}'.format(passerelle.cycle3.time_sleep))


        time_awake_list_1 = list(str(passerelle.cycle1.time_awake))
        time_sleep_list_1 = list(str(passerelle.cycle1.time_sleep))  

        time_awake_list_2 = list(str(passerelle.cycle2.time_awake))
        time_sleep_list_2 = list(str(passerelle.cycle2.time_sleep))  

        time_awake_list_3 = list(str(passerelle.cycle3.time_awake))
        time_sleep_list_3 = list(str(passerelle.cycle3.time_sleep))   

        time_awake_list_4 = list(str(passerelle.cycle4.time_awake))
        time_sleep_list_4 = list(str(passerelle.cycle4.time_sleep))   

        time_awake_list_5 = list(str(passerelle.cycle5.time_awake))
        time_sleep_list_5 = list(str(passerelle.cycle5.time_sleep))   

        f_acquisition_list=list(str(passerelle.f_acquisition))

        nb_rep_list_1=list(str(passerelle.cycle1.nb_repetition))
        nb_rep_list_2=list(str(passerelle.cycle2.nb_repetition))
        nb_rep_list_3=list(str(passerelle.cycle3.nb_repetition))
        nb_rep_list_4=list(str(passerelle.cycle4.nb_repetition))
        nb_rep_list_5=list(str(passerelle.cycle5.nb_repetition))

        amperage_max_list = list(str(passerelle.amperage_max))


        while(len(time_awake_list_1)!=6):
            time_awake_list_1.insert(0,0)
        while(len(time_sleep_list_1)!=6):
            time_sleep_list_1.insert(0,0)

        while(len(time_awake_list_2)!=6):
            time_awake_list_2.insert(0,0)
        while(len(time_sleep_list_2)!=6):
            time_sleep_list_2.insert(0,0)

        while(len(time_awake_list_3)!=6):
            time_awake_list_3.insert(0,0)
        while(len(time_sleep_list_3)!=6):
            time_sleep_list_3.insert(0,0)

        while(len(time_awake_list_4)!=6):
            time_awake_list_4.insert(0,0)
        while(len(time_sleep_list_4)!=6):
            time_sleep_list_4.insert(0,0)

        while(len(time_awake_list_5)!=6):
            time_awake_list_5.insert(0,0)
        while(len(time_sleep_list_5)!=6):
            time_sleep_list_5.insert(0,0)       

        while(len(f_acquisition_list)!=3):
            f_acquisition_list.insert(0,0)
        
        while(len(nb_rep_list_1)!=2):
            nb_rep_list_1.insert(0,0)

        while(len(nb_rep_list_2)!=2):
            nb_rep_list_2.insert(0,0)

        while(len(nb_rep_list_3)!=2):
            nb_rep_list_3.insert(0,0)
        
        while(len(nb_rep_list_4)!=2):
            nb_rep_list_4.insert(0,0)
        
        while(len(nb_rep_list_5)!=2):
            nb_rep_list_5.insert(0,0)
        
        

        Logger.warning('startacq: time_awake 1 : {}'.format(time_awake_list_1))
        Logger.warning('startacq: time_sleep 1 : {}'.format(time_sleep_list_1))

        Logger.warning('startacq: time_awake 2 : {}'.format(time_awake_list_2))
        Logger.warning('startacq: time_sleep 2 : {}'.format(time_sleep_list_2))

        Logger.warning('startacq: time_awake 3 : {}'.format(time_awake_list_3))
        Logger.warning('startacq: time_sleep 3 : {}'.format(time_sleep_list_3))

        Logger.warning('startacq: time_awake 3 : {}'.format(time_awake_list_4))
        Logger.warning('startacq: time_sleep 3 : {}'.format(time_sleep_list_4))

        Logger.warning('startacq: time_awake 3 : {}'.format(time_awake_list_5))
        Logger.warning('startacq: time_sleep 3 : {}'.format(time_sleep_list_5))

        Logger.warning('startacq: amperage_max  : {}'.format(amperage_max_list))
        
        #envoi de la trame
        #arduino1.write(str("s"))
        trame_bus=''
        trame_bus+='s'
        #Logger.warning("bus: s")

        for chiffre in time_awake_list_1:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))

        for chiffre in time_sleep_list_1:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))

        for chiffre in time_awake_list_2:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))

        for chiffre in time_sleep_list_2:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))

        for chiffre in time_awake_list_3:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))

        for chiffre in time_sleep_list_3:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))
        
        for chiffre in time_awake_list_4:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))

        for chiffre in time_sleep_list_4:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))

        for chiffre in time_awake_list_5:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))

        for chiffre in time_sleep_list_5:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))

        # for chiffre in f_acquisition_list:
        #     #arduino1.write(str(chiffre))
        #     trame_bus+=str(chiffre)
        #     #Logger.warning('bus: {}'.format(chiffre))


        #arduino1.write(str(passerelle.etat_start))
        trame_bus+=str(passerelle.etat_start)
        Logger.warning('bus: {}'.format(passerelle.etat_start))

        for chiffre in nb_rep_list_1:
            trame_bus+=str(chiffre)

        for chiffre in nb_rep_list_2:
            trame_bus+=str(chiffre)

        for chiffre in nb_rep_list_3:
            trame_bus+=str(chiffre)

        for chiffre in nb_rep_list_4:
            trame_bus+=str(chiffre)
        
        for chiffre in nb_rep_list_5:
            trame_bus+=str(chiffre)


        for chiffre in amperage_max_list:
            #arduino1.write(str(chiffre))
            trame_bus+=str(chiffre)
            #Logger.warning('bus: {}'.format(chiffre))
            

        # arduino1.write(str("\n"))
        # Logger.warning('bus: /n')
        trame_bus+=str('\n')

        arduino1.write(trame_bus.encode())

        Logger.warning('trame envoyé: {}'.format(trame_bus))

        #Logger.warning('test : ligne n°{}: Vérfif '.format(inspect.currentframe().f_lineno))
        cpt_erreur=0
        ok=False
        msg_encode ="rien reçu"
        while(ok==False):
          while(arduino1.inWaiting()):
              msg_encode = arduino1.readline()
              msg = msg_encode.decode()
              msg = str(msg)

              if (msg =='ok\n'):
                  Logger.warning('liaison à l\'arduino : communication ok')
                  ok=True
              else : 
                  Logger.warning('liaison à l\'arduino: en attente de la communication...')
                  Logger.warning('startacq: date : {} ; ligne n°{}: valeur de msg : {}'.format(str(datetime.now()),inspect.currentframe().f_lineno, msg))
                  ok=False
                  cpt_erreur+=1
                  if cpt_erreur>5:
                    Logger.warning('l544: pb, renvoie de la trame')
                    arduino1.write(trame_bus.encode())
        #       #Logger.warning('message: msg : {}'.format(msg))        

        
    def stopacq(self):
        passerelle.start_stop = 0
        Logger.warning('stopacq: simulation arreté ')
        pause = "p\n"
        pause_encode = pause.encode()
        arduino1.write(pause_encode)
        statut=0

        self.rect_dut_1.source = "images/ledred.png"
        self.rect_dut_2.source = "images/ledred.png"
        self.rect_dut_3.source = "images/ledred.png"
        self.rect_dut_4.source = "images/ledred.png"
        self.rect_dut_5.source = "images/ledred.png"
        self.rect_dut_6.source = "images/ledred.png"

        self.courant1.text = "0  A"
        self.courant2.text = "0  A"
        self.courant3.text = "0  A"
        self.courant4.text = "0  A"
        self.courant5.text = "0  A"
        self.courant6.text = "0  A"

        

        ok=False
        while(ok==False):
          while(arduino1.inWaiting()):
              msg_code = arduino1.readline()
              msg = msg_code.decode()

              if (msg=='ok\n'):
                  Logger.warning('liaison à l\'arduino : communication ok, acquisition stopé')
                  ok=True
              else : 
                  Logger.warning('liaison à l\'arduino: en attente de la communication...')
              #Logger.warning('message: msg : {}'.format(msg)) fff 

    def fermerBanc(self):  

        self.msgAlarm = Label(text="Merci de Patienter", font_size='60sp', size=(100, 50), pos=(-335, -175))
        self.add_widget(self.msgAlarm)


        passerelle.start_stop = 0


        Logger.warning('stopacq: simulation arreté ')
        pause_code = "p\n"
        pause = pause_code.encode()

        arduino1.write(pause)
        out1.close()
        Logger.warning('fermerBanc: out1 fermé')
        out2.close()
        Logger.warning('fermerBanc: out2 fermé')
        out3.close()
        Logger.warning('fermerBanc: out3 fermé')
        out4.close()
        Logger.warning('fermerBanc: out4 fermé')

        Logger.warning('y low min : {}'.format(passerelle.graph1.y_low_min))
        Logger.warning('y low max : {}'.format(passerelle.graph1.y_low_max))
        Logger.warning('y high min : {}'.format(passerelle.graph1.y_high_min))
        Logger.warning('y high max : {}'.format(passerelle.graph1.y_high_max))


        if(passerelle.graph1.flagGraph):
            try:
                GenGraph.generer_graph(chemin=chemin1, y_low_min=passerelle.graph1.y_low_min, y_low_max=passerelle.graph1.y_low_max, y_high_min=passerelle.graph1.y_high_min, y_high_max=passerelle.graph1.y_high_max )
              
            except AttributeError:
                Logger.warning('fermerBanc: impossible de generer un graph, fichier vide')

            try:
                GenGraph.generer_graph(chemin=chemin2, y_low_min=passerelle.graph1.y_low_min, y_low_max=passerelle.graph1.y_low_max, y_high_min=passerelle.graph1.y_high_min, y_high_max=passerelle.graph1.y_high_max )
              
            except AttributeError:
                Logger.warning('fermerBanc: impossible de generer un graph, fichier vide')

            try:
                GenGraph.generer_graph(chemin=chemin3, y_low_min=passerelle.graph1.y_low_min, y_low_max=passerelle.graph1.y_low_max, y_high_min=passerelle.graph1.y_high_min, y_high_max=passerelle.graph1.y_high_max )
              
            except AttributeError:
                Logger.warning('fermerBanc: impossible de generer un graph, fichier vide')

            try:
                GenGraph.generer_graph(chemin=chemin4, y_low_min=passerelle.graph1.y_low_min, y_low_max=passerelle.graph1.y_low_max, y_high_min=passerelle.graph1.y_high_min, y_high_max=passerelle.graph1.y_high_max )
              
            except AttributeError:
                Logger.warning('fermerBanc: impossible de generer un graph, fichier vide')
            


        







        #   os.popen('umount')
        # except Exception as e:
        #   raise e
        exit()


        
class Graph(Screen):
    def __init__(self, **kwargs):
        super(Graph, self).__init__(**kwargs)



        self.label_y_low_min_uA = Label(text="60", font_size='25sp', size=(100, 50), pos_hint={'center_x': 0.3, 'center_y':0.750})
        self.add_widget(self.label_y_low_min_uA)

        self.label_y_low_max_uA = Label(text="120", font_size='25sp', size=(100, 50), pos_hint={'center_x': 0.3, 'center_y':0.580})
        self.add_widget(self.label_y_low_max_uA)

        self.label_y_high_min = Label(text="600", font_size='25sp', size=(100, 50), pos_hint={'center_x': 0.3, 'center_y':0.380})
        self.add_widget(self.label_y_high_min)

        self.label_y_high_max = Label(text="1000", font_size='25sp', size=(100, 50), pos_hint={'center_x': 0.3, 'center_y':0.18})
        self.add_widget(self.label_y_high_max)


    def increment_y_low_min(self):
        if(passerelle.graph1.y_low_min_uA<1000):
            passerelle.graph1.y_low_min_uA += 10
            self.label_y_low_min_uA.text = str(passerelle.graph1.y_low_min_uA)
        else : 
            passerelle.graph1.y_low_min_uA =0
            self.label_y_low_min_uA.text = str(passerelle.graph1.y_low_min_uA)

        passerelle.graph1.y_low_min=float(passerelle.graph1.y_low_min_uA/1000)
        Logger.warning('y_low min : {}'.format(passerelle.graph1.y_low_min))
        Logger.warning('y_low min_uA : {}'.format(passerelle.graph1.y_low_min_uA))
        

    def decrement_y_low_min(self):
        if(passerelle.graph1.y_low_min_uA>0):
            passerelle.graph1.y_low_min_uA -= 10
            self.label_y_low_min_uA.text = str(passerelle.graph1.y_low_min_uA)
        else : 
            passerelle.graph1.y_low_min_uA =1000
            self.label_y_low_min_uA.text = str(passerelle.graph1.y_low_min_uA)

        passerelle.graph1.y_low_min=float(passerelle.graph1.y_low_min_uA/1000)
        Logger.warning('{}'.format(passerelle.graph1.y_low_min))
        Logger.warning('y_low min_uA : {}'.format(passerelle.graph1.y_low_min_uA))
        


    def increment_y_low_max(self):
        if(passerelle.graph1.y_low_max_uA<1000):
            passerelle.graph1.y_low_max_uA += 10
            self.label_y_low_max_uA.text = str(passerelle.graph1.y_low_max_uA)
        else : 
            passerelle.graph1.y_low_max_uA =0
            self.label_y_low_max_uA.text = str(passerelle.graph1.y_low_max_uA)
        passerelle.graph1.y_low_max=float(passerelle.graph1.y_low_max_uA/1000)

    def decrement_y_low_max(self):
        if(passerelle.graph1.y_low_max_uA>0):
            passerelle.graph1.y_low_max_uA -= 10
            self.label_y_low_max_uA.text = str(passerelle.graph1.y_low_max_uA)
        else : 
            passerelle.graph1.y_low_max_uA =1000
            self.label_y_low_max_uA.text = str(passerelle.graph1.y_low_max_uA)
        passerelle.graph1.y_low_max=float(passerelle.graph1.y_low_max_uA/1000)




    def increment_y_high_min(self):
        if(passerelle.graph1.y_high_min<1500):
            passerelle.graph1.y_high_min += 20
            self.label_y_high_min.text = str(passerelle.graph1.y_high_min)
        else : 
            passerelle.graph1.y_high_min =0
            self.label_y_high_min.text = str(passerelle.graph1.y_high_min)

    def decrement_y_high_min(self):
        if(passerelle.graph1.y_high_min>=20):
            passerelle.graph1.y_high_min -= 20
            self.label_y_high_min.text = str(passerelle.graph1.y_high_min)
        else : 
            passerelle.graph1.y_high_min =1500
            self.label_y_high_min.text = str(passerelle.graph1.y_high_min)

    def increment_y_high_max(self):
        if(passerelle.graph1.y_high_max<1500):
            passerelle.graph1.y_high_max += 20
            self.label_y_high_max.text = str(passerelle.graph1.y_high_max)
        else : 
            passerelle.graph1.y_high_max =0
            self.label_y_high_max.text = str(passerelle.graph1.y_high_max)

    def decrement_y_high_max(self):
        if(passerelle.graph1.y_high_max>=20):
            passerelle.graph1.y_high_max -= 20
            self.label_y_high_max.text = str(passerelle.graph1.y_high_max)
        else : 
            passerelle.graph1.y_high_max =1500
            self.label_y_high_max.text = str(passerelle.graph1.y_high_max)

    def graphOn(self):
        passerelle.graph1.flagGraph=True
        
    def graphOff(self):
        passerelle.graph1.flagGraph=False




            
class Apropos(Screen):
    pass

class Manuel(Screen):
    pass

class Setup2(Screen):
    pass

class afficherParametres(Screen):

    def __init__(self, **kwargs):
        super(afficherParametres, self).__init__(**kwargs)
        

        self.label_sec_awake_1 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-35, 120))
        self.add_widget(self.label_sec_awake_1)

        self.label_min_awake_1 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-105, 120))
        self.add_widget(self.label_min_awake_1)

        self.label_h_awake_1 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-175, 120))
        self.add_widget(self.label_h_awake_1)
        
        self.label_sec_sleep_1 = Label(text="25", font_size='25sp', size=(100, 50), pos=(-35, 75))
        self.add_widget(self.label_sec_sleep_1)

        self.label_min_sleep_1 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-105, 75))
        self.add_widget(self.label_min_sleep_1)

        self.label_h_sleep_1 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-175, 75))
        self.add_widget(self.label_h_sleep_1)



        self.label_sec_awake_2 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-35, -5))
        self.add_widget(self.label_sec_awake_2)

        self.label_min_awake_2 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-105, -5))
        self.add_widget(self.label_min_awake_2)

        self.label_h_awake_2 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-175, -5))
        self.add_widget(self.label_h_awake_2)

        self.label_sec_sleep_2 = Label(text="25", font_size='25sp', size=(100, 50), pos=(-35, -50))
        self.add_widget(self.label_sec_sleep_2)

        self.label_min_sleep_2 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-105, -50))
        self.add_widget(self.label_min_sleep_2)

        self.label_h_sleep_2 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-175, -50))
        self.add_widget(self.label_h_sleep_2)



        self.label_sec_awake_3 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-35, -130))
        self.add_widget(self.label_sec_awake_3)

        self.label_min_awake_3 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-105, -130))
        self.add_widget(self.label_min_awake_3)

        self.label_h_awake_3 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-175, -130))
        self.add_widget(self.label_h_awake_3)

        self.label_sec_sleep_3 = Label(text="25", font_size='25sp', size=(100, 50), pos=(-35, -175))
        self.add_widget(self.label_sec_sleep_3)

        self.label_min_sleep_3 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-105, -175))
        self.add_widget(self.label_min_sleep_3)

        self.label_h_sleep_3 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-175, -175))
        self.add_widget(self.label_h_sleep_3)


        self.label_alarm_awake = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(180, 120))
        self.add_widget(self.label_alarm_awake)
        self.label_alarm_sleep = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(180, 75))
        self.add_widget(self.label_alarm_sleep)

        self.label_f_text=Label(text='Fréquence d\'acquisition : ', font_size='25sp', size=(100,50), pos=(160, 0))
        self.label_s_frequency=Label(text="N/A", font_size='25sp', size=(100, 50), pos=(330, 0))
        self.add_widget(self.label_f_text)
        self.add_widget(self.label_s_frequency)

        self.label_etat_init_text=Label(text='Etat initial: ', font_size='25sp', size=(100,50), pos=(160, -70))
        self.label_etat_init=Label(text="N/A", font_size='25sp', size=(100, 50), pos=(330, -70))
        self.add_widget(self.label_etat_init_text)
        self.add_widget(self.label_etat_init)

        self.label_nb_rep_cycle1=Label(text="N/A1", font_size='25sp', size=(100, 50), pos=(330, -100))
        self.add_widget(self.label_nb_rep_cycle1)

        self.label_nb_rep_cycle2=Label(text="N/A2", font_size='25sp', size=(100, 50), pos=(330, -150))
        self.add_widget(self.label_nb_rep_cycle2)

        self.label_nb_rep_cycle3=Label(text="N/A3", font_size='25sp', size=(100, 50), pos=(330, -200))
        self.add_widget(self.label_nb_rep_cycle3)



               


        Logger.warning('test: test __init__')

    def refresh(self):
        self.label_sec_awake_1.text=str(passerelle.cycle1.time_awake_s)+" s."
        self.label_min_awake_1.text=str(passerelle.cycle1.time_awake_m)+" m."
        self.label_h_awake_1.text=str(passerelle.cycle1.time_awake_h)+" h."

        self.label_sec_sleep_1.text=str(passerelle.cycle1.time_sleep_s)+" s."
        self.label_min_sleep_1.text=str(passerelle.cycle1.time_sleep_m)+" m."
        self.label_h_sleep_1.text=str(passerelle.cycle1.time_sleep_h)+" h."



        self.label_sec_awake_2.text=str(passerelle.cycle2.time_awake_s)+" s."
        self.label_min_awake_2.text=str(passerelle.cycle2.time_awake_m)+" m."
        self.label_h_awake_2.text=str(passerelle.cycle2.time_awake_h)+" h."

        self.label_sec_sleep_2.text=str(passerelle.cycle2.time_sleep_s)+" s."
        self.label_min_sleep_2.text=str(passerelle.cycle2.time_sleep_m)+" m."
        self.label_h_sleep_2.text=str(passerelle.cycle2.time_sleep_h)+" h."



        self.label_sec_awake_3.text=str(passerelle.cycle3.time_awake_s)+" s."
        self.label_min_awake_3.text=str(passerelle.cycle3.time_awake_m)+" m."
        self.label_h_awake_3.text=str(passerelle.cycle3.time_awake_h)+" h."

        self.label_sec_sleep_3.text=str(passerelle.cycle3.time_sleep_s)+" s."
        self.label_min_sleep_3.text=str(passerelle.cycle3.time_sleep_m)+" m."
        self.label_h_sleep_3.text=str(passerelle.cycle3.time_sleep_h)+" h."

        self.label_alarm_awake.text=str(passerelle.alarm_awake)+" A"
        self.label_alarm_sleep.text=str(passerelle.alarm_sleep)+" uA"

        self.label_s_frequency.text=str(passerelle.f_acquisition)+ " S."

        self.label_nb_rep_cycle1.text=str(passerelle.cycle1.nb_repetition)+" rep"
        self.label_nb_rep_cycle2.text=str(passerelle.cycle2.nb_repetition)+" rep"
        self.label_nb_rep_cycle3.text=str(passerelle.cycle3.nb_repetition)+" rep"


        if(passerelle.etat_start==1):
            self.label_etat_init.text="On"
        elif(passerelle.etat_start==0):
            self.label_etat_init.text="Off"
        else:
            self.label_etat_init.text="ERREUR"
        Logger.warning('test: test on start')

class SetCycle1(Screen):
    alarmawake = NumericProperty(1.1)
    alarmsleep = NumericProperty(200)
    timeacq = NumericProperty(150)
    
    def __init__(self, **kwargs):
        super(SetCycle1, self).__init__(**kwargs)
        

        self.label_sec_awake = Label(text="25", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.4, 'center_y':0.63})
        self.add_widget(self.label_sec_awake)

        self.label_min_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.25, 'center_y':0.63})
        self.add_widget(self.label_min_awake)

        self.label_h_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.1, 'center_y':0.63})
        self.add_widget(self.label_h_awake)
        
        self.label_sec_sleep = Label(text="25", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.9, 'center_y':0.63})
        self.add_widget(self.label_sec_sleep)

        self.label_min_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.75, 'center_y':0.63})
        self.add_widget(self.label_min_sleep)

        self.label_h_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.6, 'center_y':0.63})
        self.add_widget(self.label_h_sleep)

        self.label_nb_cycle = Label(text="1", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.37, 'center_y':0.24})
        self.add_widget(self.label_nb_cycle)

        self.label_s_frequency = Label(text="1", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.09, 'center_y':0.24})
        self.add_widget(self.label_s_frequency)
        

    def incrementtimeawake_s(self):
        if(passerelle.cycle1.time_awake_s<60):
            passerelle.cycle1.time_awake_s += 5
            self.label_sec_awake.text = str(passerelle.cycle1.time_awake_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle1.time_awake_s =0
            self.label_sec_awake.text = str(passerelle.cycle1.time_awake_s)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_s(self):
        if(passerelle.cycle1.time_awake_s>0):
            passerelle.cycle1.time_awake_s -= 5
            self.label_sec_awake.text = str(passerelle.cycle1.time_awake_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle1.time_awake_s =60
            self.label_sec_awake.text = str(passerelle.cycle1.time_awake_s)
            passerelle.update_alarm = 1

    def incrementtimeawake_min(self):
        if(passerelle.cycle1.time_awake_m<60):
            passerelle.cycle1.time_awake_m += 1
            self.label_min_awake.text = str(passerelle.cycle1.time_awake_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle1.time_awake_m =0
            self.label_min_awake.text = str(passerelle.cycle1.time_awake_m)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_min(self):
        if(passerelle.cycle1.time_awake_m>0):
            passerelle.cycle1.time_awake_m -= 1
            self.label_min_awake.text = str(passerelle.cycle1.time_awake_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle1.time_awake_m =60
            self.label_min_awake.text = str(passerelle.cycle1.time_awake_m)
            passerelle.update_alarm = 1

    def incrementtimeawake_h(self):
        if(passerelle.cycle1.time_awake_h<50):
            passerelle.cycle1.time_awake_h += 1
            self.label_h_awake.text = str(passerelle.cycle1.time_awake_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle1.time_awake_h =0
            self.label_h_awake.text = str(passerelle.cycle1.time_awake_h)
            passerelle.update_alarm = 1

    def decrementtimeawake_h(self):
        if(passerelle.cycle1.time_awake_h>0):
            passerelle.cycle1.time_awake_h -= 1
            self.label_h_awake.text = str(passerelle.cycle1.time_awake_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle1.time_awake_h =50
            self.label_h_awake.text = str(passerelle.cycle1.time_awake_h)
            passerelle.update_alarm = 1
        
    def incrementtimesleep_s(self):
        if(passerelle.cycle1.time_sleep_s<60):
            passerelle.cycle1.time_sleep_s += 5
            self.label_sec_sleep.text = str(passerelle.cycle1.time_sleep_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle1.time_sleep_s =0
            self.label_sec_sleep.text = str(passerelle.cycle1.time_sleep_s)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_s(self):
        if(passerelle.cycle1.time_sleep_s>0):
            passerelle.cycle1.time_sleep_s -= 5
            self.label_sec_sleep.text = str(passerelle.cycle1.time_sleep_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle1.time_sleep_s =60
            self.label_sec_sleep.text = str(passerelle.cycle1.time_sleep_s)
            passerelle.update_alarm = 1

    def incrementtimesleep_min(self):
        if(passerelle.cycle1.time_sleep_m<60):
            passerelle.cycle1.time_sleep_m += 1
            self.label_min_sleep.text = str(passerelle.cycle1.time_sleep_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle1.time_sleep_m =0
            self.label_min_sleep.text = str(passerelle.cycle1.time_sleep_m)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_min(self):
        if(passerelle.cycle1.time_sleep_m>0):
            passerelle.cycle1.time_sleep_m -= 1
            self.label_min_sleep.text = str(passerelle.cycle1.time_sleep_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle1.time_sleep_m =60
            self.label_min_sleep.text = str(passerelle.cycle1.time_sleep_m)
            passerelle.update_alarm = 1

    def incrementtimesleep_h(self):
        if(passerelle.cycle1.time_sleep_h<50):
            passerelle.cycle1.time_sleep_h += 1
            self.label_h_sleep.text = str(passerelle.cycle1.time_sleep_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle1.time_sleep_h =0
            self.label_h_sleep.text = str(passerelle.cycle1.time_sleep_h)
            passerelle.update_alarm = 1

    def decrementtimesleep_h(self):
        if(passerelle.cycle1.time_sleep_h>0):
            passerelle.cycle1.time_sleep_h -= 1
            self.label_h_sleep.text = str(passerelle.cycle1.time_sleep_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle1.time_sleep_h =50
            self.label_h_sleep.text = str(passerelle.cycle1.time_sleep_h)
            passerelle.update_alarm = 1

    def begin_sleep(self):
        passerelle.etat_start=0
    def begin_awake(self):
        passerelle.etat_start=1

    def incrementfacq(self):
        if(passerelle.f_acquisition<120):
            if(passerelle.f_acquisition==1):
                passerelle.f_acquisition=5
            else:    
                passerelle.f_acquisition+=5
            self.label_s_frequency.text=str(passerelle.f_acquisition)

    def decrementfacq(self):
        if(passerelle.f_acquisition>=5):
            if(passerelle.f_acquisition==5):
                passerelle.f_acquisition=1
            else:
                passerelle.f_acquisition-=5
            self.label_s_frequency.text=str(passerelle.f_acquisition)

    def incrementnbrep(self):
        if(passerelle.cycle1.nb_repetition<99):
            passerelle.cycle1.nb_repetition+=1
        else:
            passerelle.cycle1.nb_repetition=1
        self.label_nb_cycle.text=str(passerelle.cycle1.nb_repetition) 

    def decrementnbrep(self):
        if(passerelle.cycle1.nb_repetition>1):
            passerelle.cycle1.nb_repetition-=1
        else:
            passerelle.cycle1.nb_repetition=99
        self.label_nb_cycle.text=str(passerelle.cycle1.nb_repetition)
    
    def validationCycle1(self):
        if (passerelle.nobmre_de_cycle != 1):
            self.manager.current = 'setCycle2'
        else:
            self.manager.current = 'setCourantMax'

class SetCycle2(Screen):
    alarmawake = NumericProperty(1.1)
    alarmsleep = NumericProperty(200)
    timeacq = NumericProperty(150)
    
    def __init__(self, **kwargs):
        super(SetCycle2, self).__init__(**kwargs)
        

        self.label_sec_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.35, 'center_y': 0.63})
        self.add_widget(self.label_sec_awake)

        self.label_min_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.2, 'center_y': 0.63})
        self.add_widget(self.label_min_awake)

        self.label_h_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.05, 'center_y': 0.63})
        self.add_widget(self.label_h_awake)
        
        self.label_sec_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.85, 'center_y': 0.63})
        self.add_widget(self.label_sec_sleep)

        self.label_min_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.7, 'center_y': 0.63})
        self.add_widget(self.label_min_sleep)

        self.label_h_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.55, 'center_y': 0.63})
        self.add_widget(self.label_h_sleep)
        
        self.label_nb_cycle = Label(text="1", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.37, 'center_y':0.24})
        self.add_widget(self.label_nb_cycle)

    def incrementtimeawake_s(self):
        if(passerelle.cycle2.time_awake_s<60):
            passerelle.cycle2.time_awake_s += 5
            self.label_sec_awake.text = str(passerelle.cycle2.time_awake_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle2.time_awake_s =0
            self.label_sec_awake.text = str(passerelle.cycle2.time_awake_s)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_s(self):
        if(passerelle.cycle2.time_awake_s>0):
            passerelle.cycle2.time_awake_s -= 5
            self.label_sec_awake.text = str(passerelle.cycle2.time_awake_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle2.time_awake_s =60
            self.label_sec_awake.text = str(passerelle.cycle2.time_awake_s)
            passerelle.update_alarm = 1

    def incrementtimeawake_min(self):
        if(passerelle.cycle2.time_awake_m<60):
            passerelle.cycle2.time_awake_m += 1
            self.label_min_awake.text = str(passerelle.cycle2.time_awake_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle2.time_awake_m =0
            self.label_min_awake.text = str(passerelle.cycle2.time_awake_m)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_min(self):
        if(passerelle.cycle2.time_awake_m>0):
            passerelle.cycle2.time_awake_m -= 1
            self.label_min_awake.text = str(passerelle.cycle2.time_awake_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle2.time_awake_m =60
            self.label_min_awake.text = str(passerelle.cycle2.time_awake_m)
            passerelle.update_alarm = 1

    def incrementtimeawake_h(self):
        if(passerelle.cycle2.time_awake_h<50):
            passerelle.cycle2.time_awake_h += 1
            self.label_h_awake.text = str(passerelle.cycle2.time_awake_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle2.time_awake_h =0
            self.label_h_awake.text = str(passerelle.cycle2.time_awake_h)
            passerelle.update_alarm = 1

    def decrementtimeawake_h(self):
        if(passerelle.cycle2.time_awake_h>0):
            passerelle.cycle2.time_awake_h -= 1
            self.label_h_awake.text = str(passerelle.cycle2.time_awake_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle2.time_awake_h =50
            self.label_h_awake.text = str(passerelle.cycle2.time_awake_h)
            passerelle.update_alarm = 1
        
    def incrementtimesleep_s(self):
        if(passerelle.cycle2.time_sleep_s<60):
            passerelle.cycle2.time_sleep_s += 5
            self.label_sec_sleep.text = str(passerelle.cycle2.time_sleep_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle2.time_sleep_s =0
            self.label_sec_sleep.text = str(passerelle.cycle2.time_sleep_s)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_s(self):
        if(passerelle.cycle2.time_sleep_s>0):
            passerelle.cycle2.time_sleep_s -= 5
            self.label_sec_sleep.text = str(passerelle.cycle2.time_sleep_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle2.time_sleep_s =60
            self.label_sec_sleep.text = str(passerelle.cycle2.time_sleep_s)
            passerelle.update_alarm = 1

    def incrementtimesleep_min(self):
        if(passerelle.cycle2.time_sleep_m<60):
            passerelle.cycle2.time_sleep_m += 1
            self.label_min_sleep.text = str(passerelle.cycle2.time_sleep_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle2.time_sleep_m =0
            self.label_min_sleep.text = str(passerelle.cycle2.time_sleep_m)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_min(self):
        if(passerelle.cycle2.time_sleep_m>0):
            passerelle.cycle2.time_sleep_m -= 1
            self.label_min_sleep.text = str(passerelle.cycle2.time_sleep_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle2.time_sleep_m =60
            self.label_min_sleep.text = str(passerelle.cycle2.time_sleep_m)
            passerelle.update_alarm = 1

    def incrementtimesleep_h(self):
        if(passerelle.cycle2.time_sleep_h<50):
            passerelle.cycle2.time_sleep_h += 1
            self.label_h_sleep.text = str(passerelle.cycle2.time_sleep_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle2.time_sleep_h =0
            self.label_h_sleep.text = str(passerelle.cycle2.time_sleep_h)
            passerelle.update_alarm = 1

    def decrementtimesleep_h(self):
        if(passerelle.cycle2.time_sleep_h>0):
            passerelle.cycle2.time_sleep_h -= 1
            self.label_h_sleep.text = str(passerelle.cycle2.time_sleep_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle2.time_sleep_h =50
            self.label_h_sleep.text = str(passerelle.cycle2.time_sleep_h)
            passerelle.update_alarm = 1
    
    def incrementnbrep(self):
        if(passerelle.cycle2.nb_repetition<99):
            passerelle.cycle2.nb_repetition+=1
        else:
            passerelle.cycle2.nb_repetition=1
        self.label_nb_cycle.text=str(passerelle.cycle2.nb_repetition) 

    def decrementnbrep(self):
        if(passerelle.cycle2.nb_repetition>1):
            passerelle.cycle2.nb_repetition-=1
        else:
            passerelle.cycle2.nb_repetition=99
        self.label_nb_cycle.text=str(passerelle.cycle2.nb_repetition)
    
    def validationCycle2(self):
        if (passerelle.nobmre_de_cycle != 2):
            self.manager.current = 'setCycle3'
        else:
            self.manager.current = 'setCourantMax'

class SetCycle3(Screen):
    alarmawake = NumericProperty(1.1)
    alarmsleep = NumericProperty(200)
    timeacq = NumericProperty(150)
    
    def __init__(self, **kwargs):
        super(SetCycle3, self).__init__(**kwargs)
        

        self.label_sec_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.35, 'center_y': 0.63})
        self.add_widget(self.label_sec_awake)

        self.label_min_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.2, 'center_y': 0.63})
        self.add_widget(self.label_min_awake)

        self.label_h_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.05, 'center_y': 0.63})
        self.add_widget(self.label_h_awake)
        
        self.label_sec_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.85, 'center_y': 0.63})
        self.add_widget(self.label_sec_sleep)

        self.label_min_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.7, 'center_y': 0.63})
        self.add_widget(self.label_min_sleep)

        self.label_h_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.55, 'center_y': 0.63})
        self.add_widget(self.label_h_sleep)

        self.label_nb_cycle = Label(text="1", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.37, 'center_y':0.24})
        self.add_widget(self.label_nb_cycle)

    def incrementtimeawake_s(self):
        if(passerelle.cycle3.time_awake_s<60):
            passerelle.cycle3.time_awake_s += 5
            self.label_sec_awake.text = str(passerelle.cycle3.time_awake_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle3.time_awake_s =0
            self.label_sec_awake.text = str(passerelle.cycle3.time_awake_s)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_s(self):
        if(passerelle.cycle3.time_awake_s>0):
            passerelle.cycle3.time_awake_s -= 5
            self.label_sec_awake.text = str(passerelle.cycle3.time_awake_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle3.time_awake_s =60
            self.label_sec_awake.text = str(passerelle.cycle3.time_awake_s)
            passerelle.update_alarm = 1

    def incrementtimeawake_min(self):
        if(passerelle.cycle3.time_awake_m<60):
            passerelle.cycle3.time_awake_m += 1
            self.label_min_awake.text = str(passerelle.cycle3.time_awake_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle3.time_awake_m =0
            self.label_min_awake.text = str(passerelle.cycle3.time_awake_m)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_min(self):
        if(passerelle.cycle3.time_awake_m>0):
            passerelle.cycle3.time_awake_m -= 1
            self.label_min_awake.text = str(passerelle.cycle3.time_awake_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle3.time_awake_m =60
            self.label_min_awake.text = str(passerelle.cycle3.time_awake_m)
            passerelle.update_alarm = 1

    def incrementtimeawake_h(self):
        if(passerelle.cycle3.time_awake_h<50):
            passerelle.cycle3.time_awake_h += 1
            self.label_h_awake.text = str(passerelle.cycle3.time_awake_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle3.time_awake_h =0
            self.label_h_awake.text = str(passerelle.cycle3.time_awake_h)
            passerelle.update_alarm = 1

    def decrementtimeawake_h(self):
        if(passerelle.cycle3.time_awake_h>0):
            passerelle.cycle3.time_awake_h -= 1
            self.label_h_awake.text = str(passerelle.cycle3.time_awake_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle3.time_awake_h =50
            self.label_h_awake.text = str(passerelle.cycle3.time_awake_h)
            passerelle.update_alarm = 1
        
    def incrementtimesleep_s(self):
        if(passerelle.cycle3.time_sleep_s<60):
            passerelle.cycle3.time_sleep_s += 5
            self.label_sec_sleep.text = str(passerelle.cycle3.time_sleep_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle3.time_sleep_s =0
            self.label_sec_sleep.text = str(passerelle.cycle3.time_sleep_s)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_s(self):
        if(passerelle.cycle3.time_sleep_s>0):
            passerelle.cycle3.time_sleep_s -= 5
            self.label_sec_sleep.text = str(passerelle.cycle3.time_sleep_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle3.time_sleep_s =60
            self.label_sec_sleep.text = str(passerelle.cycle3.time_sleep_s)
            passerelle.update_alarm = 1

    def incrementtimesleep_min(self):
        if(passerelle.cycle3.time_sleep_m<60):
            passerelle.cycle3.time_sleep_m += 1
            self.label_min_sleep.text = str(passerelle.cycle3.time_sleep_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle3.time_sleep_m =0
            self.label_min_sleep.text = str(passerelle.cycle3.time_sleep_m)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_min(self):
        if(passerelle.cycle3.time_sleep_m>0):
            passerelle.cycle3.time_sleep_m -= 1
            self.label_min_sleep.text = str(passerelle.cycle3.time_sleep_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle3.time_sleep_m =60
            self.label_min_sleep.text = str(passerelle.cycle3.time_sleep_m)
            passerelle.update_alarm = 1

    def incrementtimesleep_h(self):
        if(passerelle.cycle3.time_sleep_h<50):
            passerelle.cycle3.time_sleep_h += 1
            self.label_h_sleep.text = str(passerelle.cycle3.time_sleep_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle3.time_sleep_h =0
            self.label_h_sleep.text = str(passerelle.cycle3.time_sleep_h)
            passerelle.update_alarm = 1

    def decrementtimesleep_h(self):
        if(passerelle.cycle3.time_sleep_h>0):
            passerelle.cycle3.time_sleep_h -= 1
            self.label_h_sleep.text = str(passerelle.cycle3.time_sleep_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle3.time_sleep_h =50
            self.label_h_sleep.text = str(passerelle.cycle3.time_sleep_h)
            passerelle.update_alarm = 1

    def incrementnbrep(self):
        if(passerelle.cycle3.nb_repetition<99):
            passerelle.cycle3.nb_repetition+=1
        else:
            passerelle.cycle3.nb_repetition=1
        self.label_nb_cycle.text=str(passerelle.cycle3.nb_repetition) 

    def decrementnbrep(self):
        if(passerelle.cycle3.nb_repetition>1):
            passerelle.cycle3.nb_repetition-=1
        else:
            passerelle.cycle3.nb_repetition=99
        self.label_nb_cycle.text=str(passerelle.cycle3.nb_repetition)
    
    def validationCycle3(self):
        if (passerelle.nobmre_de_cycle != 3):
            self.manager.current = 'setCycle4'
        else:
            self.manager.current = 'setCourantMax'


class SetCycle4(Screen):
    alarmawake = NumericProperty(1.1)
    alarmsleep = NumericProperty(200)
    timeacq = NumericProperty(150)
    
    def __init__(self, **kwargs):
        super(SetCycle4, self).__init__(**kwargs)
        

        self.label_sec_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.35, 'center_y': 0.63})
        self.add_widget(self.label_sec_awake)

        self.label_min_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.2, 'center_y': 0.63})
        self.add_widget(self.label_min_awake)

        self.label_h_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.05, 'center_y': 0.63})
        self.add_widget(self.label_h_awake)
        
        self.label_sec_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.85, 'center_y': 0.63})
        self.add_widget(self.label_sec_sleep)

        self.label_min_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.7, 'center_y': 0.63})
        self.add_widget(self.label_min_sleep)

        self.label_h_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.55, 'center_y': 0.63})
        self.add_widget(self.label_h_sleep)

        self.label_nb_cycle = Label(text="1", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.37, 'center_y':0.24})
        self.add_widget(self.label_nb_cycle)

    def incrementtimeawake_s(self):
        if(passerelle.cycle4.time_awake_s<60):
            passerelle.cycle4.time_awake_s += 5
            self.label_sec_awake.text = str(passerelle.cycle4.time_awake_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle4.time_awake_s =0
            self.label_sec_awake.text = str(passerelle.cycle4.time_awake_s)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_s(self):
        if(passerelle.cycle4.time_awake_s>0):
            passerelle.cycle4.time_awake_s -= 5
            self.label_sec_awake.text = str(passerelle.cycle4.time_awake_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle4.time_awake_s =60
            self.label_sec_awake.text = str(passerelle.cycle4.time_awake_s)
            passerelle.update_alarm = 1

    def incrementtimeawake_min(self):
        if(passerelle.cycle4.time_awake_m<60):
            passerelle.cycle4.time_awake_m += 1
            self.label_min_awake.text = str(passerelle.cycle4.time_awake_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle4.time_awake_m =0
            self.label_min_awake.text = str(passerelle.cycle4.time_awake_m)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_min(self):
        if(passerelle.cycle4.time_awake_m>0):
            passerelle.cycle4.time_awake_m -= 1
            self.label_min_awake.text = str(passerelle.cycle4.time_awake_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle4.time_awake_m =60
            self.label_min_awake.text = str(passerelle.cycle4.time_awake_m)
            passerelle.update_alarm = 1

    def incrementtimeawake_h(self):
        if(passerelle.cycle4.time_awake_h<50):
            passerelle.cycle4.time_awake_h += 1
            self.label_h_awake.text = str(passerelle.cycle4.time_awake_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle4.time_awake_h =0
            self.label_h_awake.text = str(passerelle.cycle4.time_awake_h)
            passerelle.update_alarm = 1

    def decrementtimeawake_h(self):
        if(passerelle.cycle4.time_awake_h>0):
            passerelle.cycle4.time_awake_h -= 1
            self.label_h_awake.text = str(passerelle.cycle4.time_awake_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle4.time_awake_h =50
            self.label_h_awake.text = str(passerelle.cycle4.time_awake_h)
            passerelle.update_alarm = 1
        
    def incrementtimesleep_s(self):
        if(passerelle.cycle4.time_sleep_s<60):
            passerelle.cycle4.time_sleep_s += 5
            self.label_sec_sleep.text = str(passerelle.cycle4.time_sleep_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle4.time_sleep_s =0
            self.label_sec_sleep.text = str(passerelle.cycle4.time_sleep_s)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_s(self):
        if(passerelle.cycle4.time_sleep_s>0):
            passerelle.cycle4.time_sleep_s -= 5
            self.label_sec_sleep.text = str(passerelle.cycle4.time_sleep_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle4.time_sleep_s =60
            self.label_sec_sleep.text = str(passerelle.cycle4.time_sleep_s)
            passerelle.update_alarm = 1

    def incrementtimesleep_min(self):
        if(passerelle.cycle4.time_sleep_m<60):
            passerelle.cycle4.time_sleep_m += 1
            self.label_min_sleep.text = str(passerelle.cycle4.time_sleep_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle4.time_sleep_m =0
            self.label_min_sleep.text = str(passerelle.cycle4.time_sleep_m)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_min(self):
        if(passerelle.cycle4.time_sleep_m>0):
            passerelle.cycle4.time_sleep_m -= 1
            self.label_min_sleep.text = str(passerelle.cycle4.time_sleep_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle4.time_sleep_m =60
            self.label_min_sleep.text = str(passerelle.cycle4.time_sleep_m)
            passerelle.update_alarm = 1

    def incrementtimesleep_h(self):
        if(passerelle.cycle4.time_sleep_h<50):
            passerelle.cycle4.time_sleep_h += 1
            self.label_h_sleep.text = str(passerelle.cycle4.time_sleep_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle4.time_sleep_h =0
            self.label_h_sleep.text = str(passerelle.cycle4.time_sleep_h)
            passerelle.update_alarm = 1

    def decrementtimesleep_h(self):
        if(passerelle.cycle4.time_sleep_h>0):
            passerelle.cycle4.time_sleep_h -= 1
            self.label_h_sleep.text = str(passerelle.cycle4.time_sleep_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle4.time_sleep_h =50
            self.label_h_sleep.text = str(passerelle.cycle4.time_sleep_h)
            passerelle.update_alarm = 1

    def incrementnbrep(self):
        if(passerelle.cycle4.nb_repetition<99):
            passerelle.cycle4.nb_repetition+=1
        else:
            passerelle.cycle4.nb_repetition=1
        self.label_nb_cycle.text=str(passerelle.cycle4.nb_repetition) 

    def decrementnbrep(self):
        if(passerelle.cycle4.nb_repetition>1):
            passerelle.cycle4.nb_repetition-=1
        else:
            passerelle.cycle4.nb_repetition=99
        self.label_nb_cycle.text=str(passerelle.cycle4.nb_repetition)
    
    def validationCycle4(self):
        if (passerelle.nobmre_de_cycle != 4):
            self.manager.current = 'setCycle5'
        else:
            self.manager.current = 'setCourantMax'


class SetCycle5(Screen):
    alarmawake = NumericProperty(1.1)
    alarmsleep = NumericProperty(200)
    timeacq = NumericProperty(150)
    
    def __init__(self, **kwargs):
        super(SetCycle5, self).__init__(**kwargs)
        

        self.label_sec_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.35, 'center_y': 0.63})
        self.add_widget(self.label_sec_awake)

        self.label_min_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.2, 'center_y': 0.63})
        self.add_widget(self.label_min_awake)

        self.label_h_awake = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.05, 'center_y': 0.63})
        self.add_widget(self.label_h_awake)
        
        self.label_sec_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.85, 'center_y': 0.63})
        self.add_widget(self.label_sec_sleep)

        self.label_min_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.7, 'center_y': 0.63})
        self.add_widget(self.label_min_sleep)

        self.label_h_sleep = Label(text="0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.55, 'center_y': 0.63})
        self.add_widget(self.label_h_sleep)

        self.label_nb_cycle = Label(text="1", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.37, 'center_y':0.24})
        self.add_widget(self.label_nb_cycle)

    def incrementtimeawake_s(self):
        if(passerelle.cycle5.time_awake_s<60):
            passerelle.cycle5.time_awake_s += 5
            self.label_sec_awake.text = str(passerelle.cycle5.time_awake_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle5.time_awake_s =0
            self.label_sec_awake.text = str(passerelle.cycle5.time_awake_s)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_s(self):
        if(passerelle.cycle5.time_awake_s>0):
            passerelle.cycle5.time_awake_s -= 5
            self.label_sec_awake.text = str(passerelle.cycle5.time_awake_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle5.time_awake_s =60
            self.label_sec_awake.text = str(passerelle.cycle5.time_awake_s)
            passerelle.update_alarm = 1

    def incrementtimeawake_min(self):
        if(passerelle.cycle5.time_awake_m<60):
            passerelle.cycle5.time_awake_m += 1
            self.label_min_awake.text = str(passerelle.cycle5.time_awake_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle5.time_awake_m =0
            self.label_min_awake.text = str(passerelle.cycle5.time_awake_m)
            passerelle.update_alarm = 1
        
    def decrementtimeawake_min(self):
        if(passerelle.cycle5.time_awake_m>0):
            passerelle.cycle5.time_awake_m -= 1
            self.label_min_awake.text = str(passerelle.cycle5.time_awake_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle5.time_awake_m =60
            self.label_min_awake.text = str(passerelle.cycle5.time_awake_m)
            passerelle.update_alarm = 1

    def incrementtimeawake_h(self):
        if(passerelle.cycle5.time_awake_h<50):
            passerelle.cycle5.time_awake_h += 1
            self.label_h_awake.text = str(passerelle.cycle5.time_awake_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle5.time_awake_h =0
            self.label_h_awake.text = str(passerelle.cycle5.time_awake_h)
            passerelle.update_alarm = 1

    def decrementtimeawake_h(self):
        if(passerelle.cycle5.time_awake_h>0):
            passerelle.cycle5.time_awake_h -= 1
            self.label_h_awake.text = str(passerelle.cycle5.time_awake_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle5.time_awake_h =50
            self.label_h_awake.text = str(passerelle.cycle5.time_awake_h)
            passerelle.update_alarm = 1
        
    def incrementtimesleep_s(self):
        if(passerelle.cycle5.time_sleep_s<60):
            passerelle.cycle5.time_sleep_s += 5
            self.label_sec_sleep.text = str(passerelle.cycle5.time_sleep_s)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle5.time_sleep_s =0
            self.label_sec_sleep.text = str(passerelle.cycle5.time_sleep_s)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_s(self):
        if(passerelle.cycle5.time_sleep_s>0):
            passerelle.cycle5.time_sleep_s -= 5
            self.label_sec_sleep.text = str(passerelle.cycle5.time_sleep_s)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle5.time_sleep_s =60
            self.label_sec_sleep.text = str(passerelle.cycle5.time_sleep_s)
            passerelle.update_alarm = 1

    def incrementtimesleep_min(self):
        if(passerelle.cycle5.time_sleep_m<60):
            passerelle.cycle5.time_sleep_m += 1
            self.label_min_sleep.text = str(passerelle.cycle5.time_sleep_m)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle5.time_sleep_m =0
            self.label_min_sleep.text = str(passerelle.cycle5.time_sleep_m)
            passerelle.update_alarm = 1
        
    def decrementtimesleep_min(self):
        if(passerelle.cycle5.time_sleep_m>0):
            passerelle.cycle5.time_sleep_m -= 1
            self.label_min_sleep.text = str(passerelle.cycle5.time_sleep_m)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle5.time_sleep_m =60
            self.label_min_sleep.text = str(passerelle.cycle5.time_sleep_m)
            passerelle.update_alarm = 1

    def incrementtimesleep_h(self):
        if(passerelle.cycle5.time_sleep_h<50):
            passerelle.cycle5.time_sleep_h += 1
            self.label_h_sleep.text = str(passerelle.cycle5.time_sleep_h)
            passerelle.update_alarm = 1
        else : 
            passerelle.cycle5.time_sleep_h =0
            self.label_h_sleep.text = str(passerelle.cycle5.time_sleep_h)
            passerelle.update_alarm = 1

    def decrementtimesleep_h(self):
        if(passerelle.cycle5.time_sleep_h>0):
            passerelle.cycle5.time_sleep_h -= 1
            self.label_h_sleep.text = str(passerelle.cycle5.time_sleep_h)
            passerelle.update_alarm = 1
        else :
            passerelle.cycle5.time_sleep_h =50
            self.label_h_sleep.text = str(passerelle.cycle5.time_sleep_h)
            passerelle.update_alarm = 1

    def incrementnbrep(self):
        if(passerelle.cycle5.nb_repetition<99):
            passerelle.cycle5.nb_repetition+=1
        else:
            passerelle.cycle5.nb_repetition=1
        self.label_nb_cycle.text=str(passerelle.cycle5.nb_repetition) 

    def decrementnbrep(self):
        if(passerelle.cycle5.nb_repetition>1):
            passerelle.cycle5.nb_repetition-=1
        else:
            passerelle.cycle5.nb_repetition=99
        self.label_nb_cycle.text=str(passerelle.cycle5.nb_repetition)
    
    def validationCycle5(self):
        self.manager.current = 'setCourantMax'


class SetAlarm(Screen):
    alarmawake = NumericProperty(1.1)
    alarmsleep = NumericProperty(200)
    timeacq = NumericProperty(150)
    
    def __init__(self, **kwargs):
        super(SetAlarm, self).__init__(**kwargs)
        
        self.label_alarm_awake = Label(text="1.2", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.22, 'center_y':0.5})
        self.add_widget(self.label_alarm_awake)

        self.label_alarm_sleep = Label(text="200", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.72, 'center_y':0.5})
        self.add_widget(self.label_alarm_sleep)

    def incrementalarmawake(self):
        passerelle.alarm_awake += 0.1
        self.label_alarm_awake.text = str(passerelle.alarm_awake)
        passerelle.update_alarm = 1
        
    def decrementalarmawake(self):
        if(passerelle.alarm_awake>=0.1):
            passerelle.alarm_awake -= 0.1
            self.label_alarm_awake.text = str(passerelle.alarm_awake)
            passerelle.update_alarm = 1
    def incrementalarmsleep(self):
        passerelle.alarm_sleep += 10
        self.label_alarm_sleep.text = str(passerelle.alarm_sleep)
        passerelle.update_alarm = 1
        
    def decrementalarmsleep(self):
        if(passerelle.alarm_sleep>=10):
            passerelle.alarm_sleep -= 10
            self.label_alarm_sleep.text = str(passerelle.alarm_sleep)
            passerelle.update_alarm = 1

class SetCourantMax(Screen):
    amperagemax = NumericProperty(2)
    timeacq = NumericProperty(150)
    
    def __init__(self, **kwargs):
        super(SetCourantMax, self).__init__(**kwargs)
        
        self.label_courant_max = Label(text="2.0", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.48, 'center_y':0.5})
        self.add_widget(self.label_courant_max)

       

    def incrementCourantMax(self):
        if(passerelle.amperage_max < 10.5):
            passerelle.amperage_max += 0.5
            self.label_courant_max.text = str(passerelle.amperage_max)
            passerelle.update_amperage_max = 1
        
    def decrementCourantMax(self):
        if(passerelle.amperage_max>0.5):
            passerelle.amperage_max -= 0.5
            self.label_courant_max.text = str(passerelle.amperage_max)
            passerelle.update_amperage_max = 1


class SetNombreDeCycle(Screen):
    nobmre_de_cycle = NumericProperty(2)
    timeacq = NumericProperty(150)
    
    def __init__(self, **kwargs):
        super(SetNombreDeCycle, self).__init__(**kwargs)
        
        self.label_nobmre_de_cycle = Label(text="1", font_size='40sp', size=(100, 50), pos_hint={'center_x': 0.48, 'center_y':0.5})
        self.add_widget(self.label_nobmre_de_cycle)

       

    def incrementCycle(self):
        if(passerelle.nobmre_de_cycle < 5):
            passerelle.nobmre_de_cycle += 1
            self.label_nobmre_de_cycle.text = str(passerelle.nobmre_de_cycle)
            passerelle.update_nobmre_de_cycle = 1
        
    def decrementCycle(self):
        if(passerelle.nobmre_de_cycle>1):
            passerelle.nobmre_de_cycle -= 1
            self.label_nobmre_de_cycle.text = str(passerelle.nobmre_de_cycle)
            passerelle.update_nobmre_de_cycle = 1


            
class RootScreen(ScreenManager):
    pass



class MainApp(App):
    def build(self):
        return RootScreen()


if __name__ == "__main__":
    Logger.warning('DATE ET HEURE DE LANCEMENT DE L ACQUISITION: {}'.format((datetime.now())))
    try:
        arduino1 = serial.Serial('/dev/ttyACM0',115200,timeout = 10)
        Logger.warning('arduino: Communication lancé')

    except:
        print ("Failed to connect à l'arduino")
        exit()


    MainApp().run()

    arduino1.close()

