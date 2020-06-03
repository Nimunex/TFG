

from bluepy import btle
from bluepy.btle import Peripheral, DefaultDelegate
#import pymongo
#from pymongo import MongoClient
import os.path
import struct
import binascii
import sys
import datetime
import time
import EnvironmentService
from EnvironmentService import EnvironmentService
import Device
from Device import Device

## Useful functions



def getTimeStamp():
    ts = time.time()
    ts_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return ts_str

## Notifications /Indications Handler

class DeviceDelegate(DefaultDelegate):

    def handleNotification(self, hnd, data):
        
        if (hnd == temperature_handle):
            data = bytearray(data)
            temperature_value =int.from_bytes(data, byteorder='big', signed=False) 
            ##teptep = binascii.b2a_hex(data)
            print("A notification was received -> Temperature: ", temperature_value, "C")
        
        elif (hnd == pressure_handle):
            data = bytearray(data)
            pressure_value =int.from_bytes(data, byteorder='big', signed=False) 
            ##pressure_int, pressure_dec = self._extract_pressure_data(data)
            print("A notification was received -> Pressure: ", pressure_value, "  hPa")
        
        elif (hnd == humidity_handle):
            data = bytearray(data)
            humidity_value =int.from_bytes(data, byteorder='big', signed=False)                  
#            timestamp = getTimeStamp()
            print("A notification was received -> Humidity: ", humidity_value, "  %")
        
        elif (hnd == gas_handle):
            eco2, tvoc = self._extract_gas_data(data)
            print("A notification was received -> Gas: ", humidity_value, "  %")

        elif (hnd == e_color_handle):
            teptep = binascii.b2a_hex(data)
            print("A notification was received -> Color: ", humidity_value, "  %")
            
            
            
            
            
            
