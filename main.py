##Main

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
import DeviceDelegate
from DeviceDelegate import DeviceDelegate

##Mac: FD:88:50:58:E7:45

## MAC address Device device
global MAC

if __name__ == "__main__":
    MAC = str(sys.argv[1])
#    print("Initializing DB...")
#    GluMonDA_MongoDBInit()
#    print("Initialized DB...")
    print("Connecting to " + MAC)
    Device1 = Device(MAC)
    print("Connected...")
    print("Bonding...")
    Device1.setSecurityLevel("medium")
    print("Bonded...")
    select = input("Select the service (1)-Temperature (2)-Pressure (3)-Humidity (4)-Gas (5)-Color (6)-All: ")
    
    print("Enabling Environment Services...")
    Device1.environment.enable()
    Device1.setDelegate(DeviceDelegate())
    print('Services Enabled...')
    if (select == 1):
        Device1.environment.set_temperature_notification(True)
    elif (select == 2):    
        Device1.environment.set_pressure_notification(True)
    elif (select == 3):
        Device1.environment.set_humidity_notification(True)
    elif (select == 4):
        Device1.environment.set_gas_notification(True)
    elif (select == 5):
        Device1.environment.set_color_notification(True)
    elif (select == 6):
        Device1.environment.set_temperature_notification(True)
        Device1.environment.set_pressure_notification(True)
        Device1.environment.set_humidity_notification(True)
        Device1.environment.set_gas_notification(True)
        Device1.environment.set_color_notification(True)
    


    try:
        while True:
            if Device1.waitForNotifications(20.0):
                # handleNotification() was called
                continue
            print("Waiting...")                
                
    except KeyboardInterrupt:     
        print("Disabling Notifications and Indications...")
        Device1.environment.disable()
        print("Notifications and Indications Disabled...")
        print("Device Session Finished...")
            
