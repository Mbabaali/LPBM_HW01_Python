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
from kivy.uix.vkeyboard import VKeyboard

from kivy.config import Config

from kivy.event import EventDispatcher

from kivy.base import runTouchApp
from kivy.lang import Builder



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
from multiprocessing import Process

global alarmawake

# On défini le clavier comme étant le clavier virtuel
Config.set('kivy', 'keyboard_mode', 'systemandmulti')


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

file5='/data_dut_1_Graph_'
file6='/data_dut_2_Graph_'
file7='/data_dut_3_Graph_'
file8='/data_dut_4_Graph_'
file555='/data_dut_5_Graph_'
file666='/data_dut_6_Graph_'


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
print((";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out1)
print((";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out2)
print((";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out3)
print((";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out4)
print((";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out55)
print((";".join(["date-time", "Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out66)

print((";".join(["date-time","Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out5)
print((";".join(["date-time","Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out6)
print((";".join(["date-time","Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out7)
print((";".join(["date-time","Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out8)
print((";".join(["date-time","Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out555)
print((";".join(["date-time","Value", "Unit", "Power cosumption", "Unit", "Box state", "Alarm"])), file=out666)

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


def process_graph(list_argument_graph):
    chemin=list_argument_graph[0]
    low_min=list_argument_graph[1]
    low_max=list_argument_graph[2]
    high_min=list_argument_graph[3]
    high_max=list_argument_graph[4]
    taille=list_argument_graph[5]

    Logger.warning('process_graph: chemin : {}  ;  low_min : {} ; low_max : {}  ; high_min : {} ; high_max : {}  ; taille : {} '.format(chemin, low_min, low_max, high_min, high_max, taille))
    GenGraph.generer_graph(chemin=chemin, y_low_min=low_min, y_low_max=low_max, y_high_min=high_min, y_high_max=high_max, format_graph=taille)

class graph:
    """
    contient les paramètres à définir lors de la generation d'un graphe
    """
    def __init__(self):
        self.y_low_min_uA=0
        self.y_low_max_uA=200
        self.y_low_min=0
        self.y_low_max=0.200
        self.y_high_min=10
        self.y_high_max=1500
        self.flagGraph=True
        self.setTaille=0


class Dut:
    """
    un objet par DUT. les objets DUTs seronts stocké dans une liste 
    """
    def __init__(self, fic, fic_err):
        self.U=0
        self.A=0.0
        self.W=0.0
        self.A_mA=0.0
        self.W_mA=0.0
        self.AoffMax=0
        self.WoffMax=0
        self.AonMax=0
        self.WonMax=0
        self.cptalarmeoff=0
        self.cptalarmeon=0
        self.fic=fic
        self.fic_err=fic_err

    def set_AonMax(self, currentOnRead):
        if(currentOnRead>self.AonMax):
            self.AonMax = currentOnRead
        else:
            pass
    
    def set_AoffMax(self,currentOffRead):
        if(currentOffRead>self.AoffMax):
            self.AoffMax = currentOffRead
        else:
            pass


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
    nb_screen_param_param=0

    flag_alamarOff_init=False

    timer_acquisition=time.time()


    graph1=graph()
    dut=[]
    dut.append(Dut(out1, out5))
    dut.append(Dut(out2, out6))
    dut.append(Dut(out3, out7))
    dut.append(Dut(out4, out8))
    dut.append(Dut(out55, out555))
    dut.append(Dut(out66, out666))

    cycles_saved = []
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
        flag_ecriture_fic=False
        if(passerelle.start_stop == 1):
            # A1_mA, A2_mA, A3_mA, A4_mA=0,0,0,0
            # W1_mA, W2_mA, W3_mA, W4_mA=0,0,0,0
            A1_mA, A2_mA, A3_mA, A4_mA, A5_mA, A6_mA = 0,0,0,0,0,0
            W1_mA, W2_mA, W3_mA, W4_mA, W5_mA, W6_mA =0,0,0,0,0,0
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            ####################################################################################
            #Récupération des données Serial
            ####################################################################################
            if arduino1.inWaiting()>0:
                inbox_code = arduino1.readline()
                inbox = inbox_code.decode()
                inbox =str(inbox)
                flag_ecriture_fic=True

                if(inbox.count(':')!=19):
                    statut, U1,W1,A1, U2,W2,A2, U3,W3,A3, U4,W4,A4, U5,W5,A5, U6,W6,A6 ,bullshit= 0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0
                    Logger.warning("timer: Bug du double bus")
                    Logger.warning("timer : {}".format(inbox))
                elif (inbox[0]=='d'):
                    statut, U1,W1,A1, U2,W2,A2, U3,W3,A3, U4,W4,A4, U5,W5,A5, U6,W6,A6,bullshit = 0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0
                    Logger.warning("debug arduino: {}".format(inbox))
                else:   
                    statut, U1,W1,A1, U2,W2,A2, U3,W3,A3, U4,W4,A4, U5,W5,A5, U6,W6,A6, bullshit = inbox.split(":")
                    passerelle.dut[0].U,passerelle.dut[0].W,passerelle.dut[0].A = U1,W1,A1
                    passerelle.dut[1].U,passerelle.dut[1].W,passerelle.dut[1].A = U2,W2,A2
                    passerelle.dut[2].U,passerelle.dut[2].W,passerelle.dut[2].A = U3,W3,A3
                    passerelle.dut[3].U,passerelle.dut[3].W,passerelle.dut[3].A = U4,W4,A4
                    passerelle.dut[4].U,passerelle.dut[4].W,passerelle.dut[4].A = U5,W5,A5
                    passerelle.dut[5].U,passerelle.dut[5].W,passerelle.dut[5].A = U6,W6,A6
                    
                                  
                    Logger.info("debug arduino: {}".format(inbox))

            ####################################################################################
            ####Conversion de la mesure en mA pour pouvoir la comparer aux alarmes sleep et awake
            ####################################################################################
            alarm_awake_mA=passerelle.alarm_awake*1000
            alarm_sleep_mA=float(passerelle.alarm_sleep)/1000
            #Logger.warning('alarme awake : {} mA ; alarme sleep : {} '.format(alarm_awake_mA, alarm_sleep_mA))

            for i in passerelle.dut :
                #Pour chaque DUT, on check l'unité (A, mA ou uA, et on initialise A_mA et W_mA en fonction)
                if(i.U=='0'):
                    i.A_mA=float(i.A)/1000
                    i.W_mA=((float(i.A)) * 12)/1000
                elif(i.U=='1'):
                    i.A_mA=float(i.A)
                    i.W_mA=((float(i.A)) * 12)
                elif(i.U=='2'):
                    i.A_mA=float(i.A)*1000
                    i.W_mA=((float(i.A)) * 12)
                else:
                   i.A_mA=0
                   i.W_mA=0
            

################################################################################################################################################
######################################REGLAGE DE L'ALARME#######################################################################################
################################################################################################################################################
            if(statut=='0' and passerelle.flag_alamarOff_init==False):

                Logger.info('init : initialisé')
                passerelle.flag_alamarOff_init=True
                passerelle.timer_delai_init=time.time()


            if(passerelle.flag_seuil==False and statut == '0' and passerelle.flag_alamarOff_init==True):
                a=time.time()-passerelle.timer_delai_init

                if((passerelle.dut[0].A_mA<alarm_sleep_mA) and (passerelle.dut[1].A_mA<alarm_sleep_mA) and (passerelle.dut[2].A_mA<alarm_sleep_mA) and (passerelle.dut[3].A_mA<alarm_sleep_mA)
                and (passerelle.dut[4].A_mA<alarm_sleep_mA) and (passerelle.dut[5].A_mA<alarm_sleep_mA)):
                    Logger.warning('passerelle.dut[0].A_mA<alarm_sleep_mA')
                    timer_print=time.time()-passerelle.timer_delai_init
                    Logger.warning('timer delai: {}'.format(timer_print) )
                    passerelle.flag_seuil=True
                    #Si tous les Duts sont en dessous de la valeur de l'alarme, on active le flag seuil

                if((a>25) and (statut=='0')):
                    passerelle.flag_seuil=True
                    Logger.warning('delai depassé (25 secondes)')

            if passerelle.flag_seuil==True and statut=='0':
                #Logger.warning('On commence à verifier les valeurs pour l alarme off')
                flag_cpt_off=[False, False, False, False, False, False]

                for i in passerelle.dut:
                     if(i.A_mA>alarm_sleep_mA):
                        Logger.warning("alarme: seuil dépassé")
                        i.cptalarmeoff+=1
                        flag_cpt_off[passerelle.dut.index(i)]=True

                if(flag_cpt_off[0]==True):
                    self.cptalarmeoff1.text=str(passerelle.dut[0].cptalarmeoff)
                    flag_cpt_off[0]=False

                if(flag_cpt_off[1]==True):
                    self.cptalarmeoff2.text=str(passerelle.dut[1].cptalarmeoff)
                    flag_cpt_off[1]=False

                if(flag_cpt_off[2]==True):
                    self.cptalarmeoff3.text=str(passerelle.dut[2].cptalarmeoff)
                    #Logger.warning("maj : channel 3")
                    flag_cpt_off[2]=False

                if(flag_cpt_off[3]==True):
                    self.cptalarmeoff4.text=str(passerelle.dut[3].cptalarmeoff)
                    #Logger.warning("maj : channel 4")
                    flag_cpt_off[3]=False
                
                if(flag_cpt_off[4]==True):
                    self.cptalarmeoff5.text=str(passerelle.dut[4].cptalarmeoff)
                    #Logger.warning("maj : channel 4")
                    flag_cpt_off[4]=False
                
                if(flag_cpt_off[5]==True):
                    self.cptalarmeoff6.text=str(passerelle.dut[5].cptalarmeoff)
                    #Logger.warning("maj : channel 4")
                    flag_cpt_off[5]=False


            if(statut=='1'):

                if(passerelle.flag_seuil==True):
                    passerelle.flag_seuil=False
                if(passerelle.flag_alamarOff_init==True):
                    passerelle.flag_alamarOff_init=False

                flag_cpt_on=[False, False, False, False, False, False]


                for i in passerelle.dut:
                    if(i.A_mA>alarm_awake_mA):
                        i.cptalarmeon+=1
                        Logger.warning('index : {}'.format(passerelle.dut.index(i)))
                        flag_cpt_on[passerelle.dut.index(i)]=True
                #         Logger.warning("Ecriture dans le fichier error i.A_mA>alarm_awake_mA")

                Logger.warning("flag cpt_on : {}".format(flag_cpt_on))
                if(flag_cpt_on[0]==True):
                    self.cptalarmeon1.text=str(passerelle.dut[0].cptalarmeon)
                    # Logger.warning("maj : channel 1")
                    flag_cpt_on[0]=False

                if(flag_cpt_on[1]==True):
                    self.cptalarmeon2.text=str(passerelle.dut[1].cptalarmeon)
                    # Logger.warning("maj : channel 2")
                    flag_cpt_on[1]=False

                if(flag_cpt_on[2]==True):
                    self.cptalarmeon3.text=str(passerelle.dut[2].cptalarmeon)
                    # Logger.warning("maj : channel 3")
                    flag_cpt_on[2]=False

                if(flag_cpt_on[3]==True):
                    self.cptalarmeon4.text=str(passerelle.dut[3].cptalarmeon)
                    # Logger.warning("maj : channel 4")
                    flag_cpt_on[2]=False
                
                if(flag_cpt_on[4]==True):
                    self.cptalarmeon5.text=str(passerelle.dut[2].cptalarmeon)
                    # Logger.warning("maj : channel 5")
                    flag_cpt_on[4]=False

                if(flag_cpt_on[5]==True):
                    self.cptalarmeon6.text=str(passerelle.dut[5].cptalarmeon)
                    # Logger.warning("maj : channel 6")
                    flag_cpt_on[5]=False

            if(passerelle.dut[0].U =='0'):
                self.courant1.text = passerelle.dut[0].A + "  µA"
            
            if(passerelle.dut[1].U=='0'):    
                self.courant2.text = passerelle.dut[1].A + "  µA"

            if(passerelle.dut[2].U=='0'):    
                self.courant3.text = passerelle.dut[2].A + "  µA"
            
            if(passerelle.dut[3].U=='0'):    
                self.courant4.text = passerelle.dut[3].A + "  µA"
            
            if(passerelle.dut[4].U=='0'):    
                self.courant5.text = passerelle.dut[4].A + "  µA"
            
            if(passerelle.dut[5].U=='0'):    
                self.courant6.text = passerelle.dut[5].A + "  µA"



            if(passerelle.dut[0].U == '1'):
                self.courant1.text = passerelle.dut[0].A + "  mA"

            if(passerelle.dut[1].U=='1'):        
                self.courant2.text = passerelle.dut[1].A + "  mA"

            if(passerelle.dut[2].U=='1'):    
                self.courant3.text = passerelle.dut[2].A + "  mA"

            if(passerelle.dut[3].U=='1'):    
                self.courant4.text = passerelle.dut[3].A + "  mA"
            
            if(passerelle.dut[4].U=='1'):    
                self.courant5.text = passerelle.dut[4].A + "  mA"
            
            if(passerelle.dut[5].U=='1'):    
                self.courant6.text = passerelle.dut[5].A + "  mA"
                



            if(passerelle.dut[0].U == '2'):
                self.courant1.text = passerelle.dut[0].A + "  A"

            
            if(passerelle.dut[1].U == '2'):    
                self.courant2.text = passerelle.dut[1].A + "  A"

            
            if(passerelle.dut[2].U == '2'):    
                self.courant3.text = passerelle.dut[2].A + "  A"

            
            if(passerelle.dut[3].U == '2'):    
                self.courant4.text = passerelle.dut[3].A + "  A"
            
            if(passerelle.dut[4].U == '2'):    
                self.courant5.text = passerelle.dut[4].A + "  A"

            
            if(passerelle.dut[5].U == '2'):    
                self.courant6.text = passerelle.dut[5].A + "  A"

            flag_timer=time.time()-passerelle.timer_acquisition
            #flag_timer+=0.331 #leger offset observé lors de l'acquisition des données, on le modifie 'en dur'
            #Logger.warning('622: flag_timer : {}'.format(flag_timer))

            #if flag_ecriture_fic==True: #and flag_timer>=passerelle.f_acquisition :
            #if flag_timer>=passerelle.f_acquisition :
                #Si on a bien reçu une valeur pendat ce tour de boucle, et que la période correspond à celle voulu par l'user, alors on écrit dans les fichiers
            if flag_ecriture_fic==True and flag_timer>=passerelle.f_acquisition :
                Logger.info('timer: ecriture dans les fichiers ')
                for i in passerelle.dut :
                    if(statut == '0'):
                        Logger.info('timer:  statut = 0')
                        print((";".join([date, str(i.A_mA).replace('.' ,','), "mA", str(i.W_mA).replace('.' ,','), "mW","Sleep"])), file=(i.fic))
                        Logger.info('timer:  ifich ')
                        print((";".join([date, str(i.A_mA), "mA", str(i.W_mA), "mW","Sleep"])), file=(i.fic_err))
                        Logger.info('timer:  ifich_Graph')
                    if(statut == '1'):
                        Logger.info('timer: statut = 1')
                        print((";".join([date, str(i.A_mA).replace('.' ,','), "mA", str(i.W_mA).replace('.' ,','), "mW","Awake"])),  file=(i.fic))
                        Logger.warning('timer: ifich ')
                        print((";".join([date, str(i.A_mA), "mA", str(i.W_mA), "mW","Awake"])), file=(i.fic_err))
                        Logger.info('timer: ifich_graph ')
                passerelle.timer_acquisition=time.time()
                Logger.info('timer: fin de la boucle for i in passerelle.dut :')


           

            # if(passerelle.update_alarm == 1):           
            #     self.alarmeon1.text = (str(passerelle.alarm_awake)+" A")
            #     self.alarmeoff1.text = (str(passerelle.alarm_sleep)+" µA")
            #     self.alarmeon2.text = (str(passerelle.alarm_awake)+" A")
            #     self.alarmeoff2.text = (str(passerelle.alarm_sleep)+" µA")
            #     self.alarmeon3.text = (str(passerelle.alarm_awake)+" A")
            #     self.alarmeoff3.text = (str(passerelle.alarm_sleep)+" µA")
            #     self.alarmeon4.text = (str(passerelle.alarm_awake)+" A")
            #     self.alarmeoff4.text = (str(passerelle.alarm_sleep)+" µA")
            #     self.alarmeon5.text = (str(passerelle.alarm_awake)+" A")
            #     self.alarmeoff5.text = (str(passerelle.alarm_sleep)+" µA")
            #     self.alarmeon6.text = (str(passerelle.alarm_awake)+" A")
            #     self.alarmeoff6.text = (str(passerelle.alarm_sleep)+" µA")
            #     passerelle.update_alarm = 0

            if(statut=='0'):

                for i in passerelle.dut:
                    if(i.AoffMax<i.A_mA):
                        i.AoffMax=i.A_mA
                        i.WoffMax=i.W_mA
                        passerelle.updateMax=True         

            if(statut=='1'):
                for i in passerelle.dut:
                    if(i.A_mA>i.AonMax):
                        i.AonMax=i.A_mA
                        i.WonMax=i.W_mA
                        passerelle.updateMax=True
        


            #Affichage des Max
            if(passerelle.updateMax):
                self.maxAOn1.text=(str(passerelle.dut[0].AonMax)+" mA")
                self.maxAOn2.text=(str(passerelle.dut[1].AonMax)+" mA")
                self.maxAOn3.text=(str(passerelle.dut[2].AonMax)+" mA")
                self.maxAOn4.text=(str(passerelle.dut[3].AonMax)+" mA")
                self.maxAOn5.text=(str(passerelle.dut[4].AonMax)+" mA")
                self.maxAOn6.text=(str(passerelle.dut[5].AonMax)+" mA")

                self.maxAoff1.text=(str(passerelle.dut[0].AoffMax)+" mA")
                self.maxAoff2.text=(str(passerelle.dut[1].AoffMax)+" mA")
                self.maxAoff3.text=(str(passerelle.dut[2].AoffMax)+" mA")
                self.maxAoff4.text=(str(passerelle.dut[3].AoffMax)+" mA")
                self.maxAoff5.text=(str(passerelle.dut[4].AoffMax)+" mA")
                self.maxAoff6.text=(str(passerelle.dut[5].AoffMax)+" mA")



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

        chemin_screen=adresseUSB+date_titre+'_'+str(passerelle.nb_screen_param_param)+".png"
        Logger.warning(chemin_screen)

        self.export_to_png(chemin_screen)
        passerelle.nb_screen_param_param+=1
    
        
                


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
        Logger.warning('startacq: valeur de time_awake  1: {}'.format(passerelle.cycle1.time_awake))
        Logger.warning('startacq: valeur de time_sleep  1: {}'.format(passerelle.cycle1.time_sleep))

        Logger.warning('startacq: valeur de time_awake  2: {}'.format(passerelle.cycle2.time_awake))
        Logger.warning('startacq: valeur de time_sleep  2: {}'.format(passerelle.cycle2.time_sleep))

        Logger.warning('startacq: valeur de time_awake  3: {}'.format(passerelle.cycle3.time_awake))
        Logger.warning('startacq: valeur de time_sleep  3: {}'.format(passerelle.cycle3.time_sleep))

        Logger.warning('startacq: valeur de time_awake  4: {}'.format(passerelle.cycle4.time_awake))
        Logger.warning('startacq: valeur de time_sleep  4: {}'.format(passerelle.cycle4.time_sleep))

        Logger.warning('startacq: valeur de time_awake 5 : {}'.format(passerelle.cycle5.time_awake))
        Logger.warning('startacq: valeur de time_sleep  5: {}'.format(passerelle.cycle5.time_sleep))


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

        #On cherche à envoyer la trame à l'arduino. le time_awake et time_sleep doivent être composé de 6 chiffre, pour cela, on vérifie le 
        # la longueur de chaque, et on insere des 0 à gauche tant que différent de 6 : exemple : 12 devient 000012 
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
                  passerelle.timer_acquisition=time.time()-passerelle.f_acquisition
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
    
    def fermerBanc_schedule(self, *args):
        '''
    	permet de "multithreader" l'application : avant de lancer "fermer banc" (qui peut mettre une 30aine de secondes à s'executer suivant la taille du graphe)
    	on affiche à l'écran une image pour éviter la sensation de "freeze" du programme par l'user.
    	'''
        with self.canvas:
            self.loading_screen = Rectangle(pos=(0, 0),size=(1280,800),source="images/loading_screen.jpg")
            
        Clock.schedule_once(lambda dt: self.fermerBanc(self, *args), 0)

    def fermerBanc(self, dt):  

        # self.msgAlarm = Label(text="Merci de Patienter", font_size='60sp', size=(100, 50), pos=(-335, -175))
        # self.add_widget(self.msgAlarm)


        passerelle.start_stop = 0


        Logger.warning('stopacq: simulation arreté ')
        pause_code = "p\n"
        pause = pause_code.encode()

        arduino1.write(pause)

        Logger.warning('FERMETURE DES FICHIERS')
        out1.close()
        out2.close()
        out3.close()
        out4.close()
        out55.close()
        out66.close()

        out5.close()
        out6.close()
        out7.close()
        out8.close()
        out555.close()
        out666.close()

        
        Logger.warning('FICHIERS FERMES')

        Logger.warning('y low min : {}'.format(passerelle.graph1.y_low_min))
        Logger.warning('y low max : {}'.format(passerelle.graph1.y_low_max))
        Logger.warning('y high min : {}'.format(passerelle.graph1.y_high_min))
        Logger.warning('y high max : {}'.format(passerelle.graph1.y_high_max))


        
        list_argument_graph=[]
        list_argument_graph.append(passerelle.graph1.y_low_min)
        list_argument_graph.append(passerelle.graph1.y_low_max)
        list_argument_graph.append(passerelle.graph1.y_high_min)
        list_argument_graph.append(passerelle.graph1.y_high_max)
        list_argument_graph.append(passerelle.graph1.setTaille)

        list_argument_graph_1=list(list_argument_graph)
        list_argument_graph_1.insert(0, chemin5)

        list_argument_graph_2=list(list_argument_graph)
        list_argument_graph_2.insert(0, chemin6)

        list_argument_graph_3=list(list_argument_graph)
        list_argument_graph_3.insert(0, chemin7)

        list_argument_graph_4=list(list_argument_graph)
        list_argument_graph_4.insert(0, chemin8)

        list_argument_graph_5=list(list_argument_graph)
        list_argument_graph_5.insert(0, chemin555)

        list_argument_graph_6=list(list_argument_graph)
        list_argument_graph_6.insert(0, chemin666)




        if(passerelle.graph1.flagGraph):
            p1 = Process(target=process_graph, args=(list_argument_graph_1,))
            p2 = Process(target=process_graph, args=(list_argument_graph_2,))
            p3 = Process(target=process_graph, args=(list_argument_graph_3,))
            p4 = Process(target=process_graph, args=(list_argument_graph_4,))
            p5 = Process(target=process_graph, args=(list_argument_graph_5,))
            p6 = Process(target=process_graph, args=(list_argument_graph_6,))

            p1.start()   
            p2.start()
            p3.start()
            p4.start()
            p5.start()
            p6.start()
            
            p1.join()
            p2.join()
            p3.join()
            p4.join()
            p5.join()
            p6.join()

        os.remove(chemin5)
        os.remove(chemin6)
        os.remove(chemin7)
        os.remove(chemin8)
        os.remove(chemin555)
        os.remove(chemin666)

        exit()



class Graph(Screen):
    def __init__(self, **kwargs):
        super(Graph, self).__init__(**kwargs)



        self.label_y_low_min_uA = Label(text="0", font_size='25sp', size=(100, 50), pos_hint={'center_x': 0.3, 'center_y':0.9})
        self.add_widget(self.label_y_low_min_uA)

        self.label_y_low_max_uA = Label(text="200", font_size='25sp', size=(100, 50), pos_hint={'center_x': 0.3, 'center_y':0.6})
        self.add_widget(self.label_y_low_max_uA)

        self.label_y_high_min = Label(text="10", font_size='25sp', size=(100, 50), pos_hint={'center_x': 0.3, 'center_y':0.4})
        self.add_widget(self.label_y_high_min)

        self.label_y_high_max = Label(text="1500", font_size='25sp', size=(100, 50), pos_hint={'center_x': 0.3, 'center_y':0.2})
        self.add_widget(self.label_y_high_max)


    def increment_y_low_min(self):
        if(passerelle.graph1.y_low_min_uA<3000):
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
            passerelle.graph1.y_low_min_uA =3000
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

    def setSize(self, a):
        passerelle.graph1.setTaille=a


            
class Apropos(Screen):
    pass

class Manuel(Screen):
    pass

class Setup2(Screen):
    pass

class afficherParametres(Screen):

    def __init__(self, **kwargs):
        super(afficherParametres, self).__init__(**kwargs)
        

        self.label_sec_awake_1 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-35, 250))
        self.add_widget(self.label_sec_awake_1)

        self.label_min_awake_1 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-105, 250))
        self.add_widget(self.label_min_awake_1)

        self.label_h_awake_1 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-175, 250))
        self.add_widget(self.label_h_awake_1)
        
        self.label_sec_sleep_1 = Label(text="25", font_size='25sp', size=(100, 50), pos=(-35, 225))
        self.add_widget(self.label_sec_sleep_1)

        self.label_min_sleep_1 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-105, 225))
        self.add_widget(self.label_min_sleep_1)

        self.label_h_sleep_1 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-175, 225))
        self.add_widget(self.label_h_sleep_1)



        self.label_sec_awake_2 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-35, 150))
        self.add_widget(self.label_sec_awake_2)

        self.label_min_awake_2 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-105, 150))
        self.add_widget(self.label_min_awake_2)

        self.label_h_awake_2 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-175, 150))
        self.add_widget(self.label_h_awake_2)

        self.label_sec_sleep_2 = Label(text="25", font_size='25sp', size=(100, 50), pos=(-35, 125))
        self.add_widget(self.label_sec_sleep_2)

        self.label_min_sleep_2 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-105, 125))
        self.add_widget(self.label_min_sleep_2)

        self.label_h_sleep_2 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-175, 125))
        self.add_widget(self.label_h_sleep_2)



        self.label_sec_awake_3 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-35, 50))
        self.add_widget(self.label_sec_awake_3)

        self.label_min_awake_3 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-105, 50))
        self.add_widget(self.label_min_awake_3)

        self.label_h_awake_3 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-175, 50))
        self.add_widget(self.label_h_awake_3)

        self.label_sec_sleep_3 = Label(text="25", font_size='25sp', size=(100, 50), pos=(-35, 25))
        self.add_widget(self.label_sec_sleep_3)

        self.label_min_sleep_3 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-105, 25))
        self.add_widget(self.label_min_sleep_3)

        self.label_h_sleep_3 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-175, 25))
        self.add_widget(self.label_h_sleep_3)





        self.label_sec_awake_4 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-35, -50))
        self.add_widget(self.label_sec_awake_4)

        self.label_min_awake_4 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-105, -50))
        self.add_widget(self.label_min_awake_4)

        self.label_h_awake_4 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-175, -50))
        self.add_widget(self.label_h_awake_4)

        self.label_sec_sleep_4 = Label(text="25", font_size='25sp', size=(100, 50), pos=(-35, -75 ))
        self.add_widget(self.label_sec_sleep_4)

        self.label_min_sleep_4 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-105, -75 ))
        self.add_widget(self.label_min_sleep_4)

        self.label_h_sleep_4 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-175, -75 ))
        self.add_widget(self.label_h_sleep_4)



        self.label_sec_awake_5 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-35, -175))
        self.add_widget(self.label_sec_awake_5)

        self.label_min_awake_5 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-105, -175))
        self.add_widget(self.label_min_awake_5)

        self.label_h_awake_5 = Label(text="N/A", font_size='25sp', size=(100, 50), pos=(-175, -175))
        self.add_widget(self.label_h_awake_5)

        self.label_sec_sleep_5 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-35, -200 ))
        self.add_widget(self.label_sec_sleep_5)

        self.label_min_sleep_5 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-105, -200 ))
        self.add_widget(self.label_min_sleep_5)

        self.label_h_sleep_5 = Label(text="0", font_size='25sp', size=(100, 50), pos=(-175, -200 ))
        self.add_widget(self.label_h_sleep_5)


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

        self.label_nb_rep_cycle4=Label(text="N/A4", font_size='25sp', size=(100, 50), pos=(330, -250))
        self.add_widget(self.label_nb_rep_cycle4)

        self.label_nb_rep_cycle5=Label(text="N/A5", font_size='25sp', size=(100, 50), pos=(330, -300))
        self.add_widget(self.label_nb_rep_cycle5)



               


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




        self.label_sec_awake_4.text=str(passerelle.cycle4.time_awake_s)+" s."
        self.label_min_awake_4.text=str(passerelle.cycle4.time_awake_m)+" m."
        self.label_h_awake_4.text=str(passerelle.cycle4.time_awake_h)+" h."

        self.label_sec_sleep_4.text=str(passerelle.cycle4.time_sleep_s)+" s."
        self.label_min_sleep_4.text=str(passerelle.cycle4.time_sleep_m)+" m."
        self.label_h_sleep_4.text=str(passerelle.cycle4.time_sleep_h)+" h."



        self.label_sec_awake_5.text=str(passerelle.cycle5.time_awake_s)+" s."
        self.label_min_awake_5.text=str(passerelle.cycle5.time_awake_m)+" m."
        self.label_h_awake_5.text=str(passerelle.cycle5.time_awake_h)+" h."

        self.label_sec_sleep_5.text=str(passerelle.cycle5.time_sleep_s)+" s."
        self.label_min_sleep_5.text=str(passerelle.cycle5.time_sleep_m)+" m."
        self.label_h_sleep_5.text=str(passerelle.cycle5.time_sleep_h)+" h."


        

        self.label_alarm_awake.text=str(passerelle.alarm_awake)+" A"
        self.label_alarm_sleep.text=str(passerelle.alarm_sleep)+" uA"

        self.label_s_frequency.text=str(passerelle.f_acquisition)+ " S."

        self.label_nb_rep_cycle1.text=str(passerelle.cycle1.nb_repetition)+" rep"
        self.label_nb_rep_cycle2.text=str(passerelle.cycle2.nb_repetition)+" rep"
        self.label_nb_rep_cycle3.text=str(passerelle.cycle3.nb_repetition)+" rep"
        self.label_nb_rep_cycle4.text=str(passerelle.cycle4.nb_repetition)+" rep"
        self.label_nb_rep_cycle5.text=str(passerelle.cycle5.nb_repetition)+" rep"


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



# class Keyboard1(VKeyboard): 
#     player = VKeyboard()



class SaveCycle(Screen):
    cycles_name = ObjectProperty(None)
    #Keyboard1.docked = False

    Logger.warning('Keyboard1.docked = False')

    def do_login(self, loginText):
        app = App.get_running_app()

        app.username = loginText
        self.manager.current = 'saveCycle'

        app.config.read(app.get_application_config())
        app.config.write()

        passerelle.cycles_saved.append(loginText)

        Logger.warning('passerelle.cycles_saved.append(loginText)')
        

        for k in range(0, len(passerelle.cycles_saved))
            Logger.info('Cycles saved {} '.format(passerelle.cycles_saved[k]))

    def resetForm(self):
        self.ids['login'].text = ""

    def reset(self):
        self.cycles_name.text = ""


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