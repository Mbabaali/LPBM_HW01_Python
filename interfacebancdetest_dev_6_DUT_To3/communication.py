# -*- coding: utf8 -*-

import serial

if __name__ == "__main__":
    try:
        arduino1 = serial.Serial('/dev/ttyACM0',115200,timeout = 10)
        

    except:
        print"Failed to connect à l'arduino"