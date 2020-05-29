#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 17:30:34 2020

@author: pi
"""
##Mac: FD:88:50:58:E7:45

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
#import json

## MAC address Device device
global MAC

## Definition of all UUID used by Device

CCCD_UUID = 0x2902

HUMIDITY_CHAR_UUID = "ef830203-9b35-4933-9B10-52FFA9740042"

##  Notification handles used in notification delegate

humidity_handle = None

## Useful functions


def _str_to_int(self, s):
   ## Transform hex str into int. 
   i = int(s, 16)
   if i >= 2**7:
       i -= 2**8
   return i    

def getTimeStamp():
    ts = time.time()
    ts_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return ts_str

## Notifications /Indications Handler

class DeviceDelegate(DefaultDelegate):

    def handleNotification(self, hnd, data):
        if (hnd == humidity_handle):
            teptep = binascii.b2a_hex(data)
            humidity_value = format(self._str_to_int(teptep))
            
#            timestamp = getTimeStamp()
            print("A notification was received -> Humidity: ", humidity_value, "  %")

class EnvironmentService():
    
    ##Environment service module. Instance the class and enable to get access to the Environment interface.
    


    def __init__(self, periph):
        self.periph = periph
        self.environment_service = None
        self.humidity_char = None
        self.humidity_cccd = None


    def enable(self):
        ##Enables the class by finding the service and its characteristics. 

        global humidity_handle


        if self.environment_service is None:
            self.environment_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.humidity_char is None:
            self.humidity_char = self.environment_service.getCharacteristics(self.humidity_char_uuid)[0]
            humidity_handle = self.humidity_char.getHandle()
            self.humidity_cccd = self.humidity_char.getDescriptors(forUUID=CCCD_UUID)[0]
  

    def set_humidity_notification(self, state):
        ## Enable/Disable Humidity Notifications
        if self.humidity_cccd is not None:
            if state == True:
                self.humidity_cccd.write(b"\x01\x00", True)
            else:
                self.humidity_cccd.write(b"\x00\x00", True)    
    
    def disable(self):
        ## Disable Humidity Notifications
        self.set_humidity_notification(False)


## Thingy52 Definition

class Thingy52(Peripheral):
    """
    Thingy:52 module. Instance the class and enable to get access to the Thingy:52 Sensors.
    The addr of your device has to be know, or can be found by using the hcitool command line 
    tool, for example. Call "> sudo hcitool lescan" and your Thingy's address should show up.
    """
    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType="random")

        # Thingy configuration service not implemented
#        self.battery = BatterySensor(self)
        self.environment = EnvironmentService(self)
#        self.ui = UserInterfaceService(self)
#        self.motion = MotionService(self)
#        self.sound = SoundService(self)


## Main

if __name__ == "__main__":
    MAC = str(sys.argv[1])
#    print("Initializing DB...")
#    GluMonDA_MongoDBInit()
#    print("Initialized DB...")
#    print("Connecting to " + MAC)
#    device = Device(MAC)
#    print("Connected...")
#    print("Bonding...")
    Thingy52.setSecurityLevel("medium")
    print("Bonded...")
    print("Enabling Humidity Services...")
    Thingy52.EnvironmentService.enable()
#    device.health_thermometer.enable()
    Thingy52.setDelegate(DeviceDelegate())
    print('Services Enabled...')
#    print('Heart Rate Body Sensor Location: ' + device.heart_rate.bsl_read())
#    print('Health Thermometer Temperature Type: ' + device.health_thermometer.type_read())
    Thingy52.EnvironmentService.set_humidity_notification(True)
#    Thingy52.health_thermometer.set_ht_meas_indication(True)

    try:
        while True:
            if Thingy52.waitForNotifications(20.0):
                # handleNotification() was called
                continue
            print("Waiting...")                
                
    except KeyboardInterrupt:     
        print("Disabling Notifications and Indications...")
        Thingy52.EnvironmentService.disable()
#        device.heart_rate.disable()
#        device.health_thermometer.disable()
        print("Notifications and Indications Disabled...")
        print("Device Session Finished...")
            


