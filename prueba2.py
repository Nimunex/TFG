

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

ENVIRONMENT_SERVICE_UUID = "ef680200-9b35-4933-9B10-52FFA9740042"
HUMIDITY_CHAR_UUID = "ef680203-9b35-4933-9B10-52FFA9740042"
TEMPERATURE_CHAR_UUID = "ef680201-9b35-4933-9B10-52FFA9740042"
GAS_CHAR_UUID = "ef680204-9b35-4933-9B10-52FFA9740042"
COLOR_CHAR_UUID = "ef680205-9b35-4933-9B10-52FFA9740042"
PRESSURE_CHAR_UUID = "ef680202-9b35-4933-9B10-52FFA9740042"

##  Notification handles used in notification delegate

humidity_handle = None
temperature_handle = None
gas_handle = None
color_handle = None
pressure_handle = None

## Useful functions



def getTimeStamp():
    ts = time.time()
    ts_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return ts_str

## Notifications /Indications Handler

class DeviceDelegate(DefaultDelegate):

    def handleNotification(self, hnd, data):
        if (hnd == humidity_handle):
#            teptep = binascii.b2a_hex(data)
            data = bytearray(data)
            humidity =int.from_bytes(data, byteorder='big', signed=False)
            #            humidity_value = format(self._str_to_int(teptep))
            
#            timestamp = getTimeStamp()
            print("A notification was received -> Humidity: ", humidity, "  %")

        elif (hnd == temperature_handle):
            #data = bytearray(data)
            #temperature_value =int.from_bytes(data, byteorder='big', signed=False) 
            teptep = binascii.b2a_hex(data)
            print('Notification: Temp received:  {}.{} degCelcius'.format(
                        self._str_to_int(teptep[:-2]), int(teptep[-2:], 16)))
            
        elif (hnd == gas_handle):
            eco2, tvoc = self._extract_gas_data(data)
            print('Notification: Gas received: eCO2 ppm: {}, TVOC ppb: {} %'.format(eco2, tvoc))

        elif (hnd == color_handle):
            teptep = binascii.b2a_hex(data)
            print('Notification: Color: {}'.format(teptep))   
            
        elif (hnd == pressure_handle):
            pressure_int, pressure_dec = self._extract_pressure_data(data)
            print('Notification: Press received: {}.{} hPa'.format(
                        pressure_int, pressure_dec))
                        
                        
                        
        
    def _str_to_int(self, s):
        """ Transform hex str into int. """
        i = int(s, 16)
        if i >= 2**7:
            i -= 2**8
        return i    

    def _extract_pressure_data(self, data):
        """ Extract pressure data from data string. """
        teptep = binascii.b2a_hex(data)
        pressure_int = 0
        for i in range(0, 4):
                pressure_int += (int(teptep[i*2:(i*2)+2], 16) << 8*i)
        pressure_dec = int(teptep[-2:], 16)
        return (pressure_int, pressure_dec)

    def _extract_gas_data(self, data):
        """ Extract gas data from data string. """
        teptep = binascii.b2a_hex(data)
        eco2 = int(teptep[:2]) + (int(teptep[2:4]) << 8)
        tvoc = int(teptep[4:6]) + (int(teptep[6:8]) << 8)
        return eco2, tvoc
            
             


class EnvironmentService():
    
    ##Environment service module. Instance the class and enable to get access to the Environment interface.
    serviceUUID  = ENVIRONMENT_SERVICE_UUID
    humidity_char_uuid  = HUMIDITY_CHAR_UUID
    temperature_char_uuid  = TEMPERATURE_CHAR_UUID
    gas_char_uuid  = GAS_CHAR_UUID
    color_char_uuid  = COLOR_CHAR_UUID
    pressure_char_uuid  = PRESSURE_CHAR_UUID

    def __init__(self, periph):
        self.periph = periph
        self.environment_service = None
        self.humidity_char = None
        self.humidity_cccd = None
        self.pressure_char = None
        self.pressure_cccd = None
        self.temperature_char = None
        self.temperature_cccd = None
        self.gas_char = None
        self.gas_cccd = None
        self.color_char = None
        self.color_cccd = None


    def enable(self):
        ##Enables the class by finding the service and its characteristics. 

        global humidity_handle
        global temperature_handle
        global gas_handle
        global color_handle
        global pressure_handle

        
        if self.environment_service is None:
            self.environment_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.temperature_char is None:
            self.temperature_char = self.environment_service.getCharacteristics(self.temperature_char_uuid)[0]
            temperature_handle = self.temperature_char.getHandle()
            self.temperature_cccd = self.temperature_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.pressure_char is None:
            self.pressure_char = self.environment_service.getCharacteristics(self.pressure_char_uuid)[0]
            pressure_handle = self.pressure_char.getHandle()
            self.pressure_cccd = self.pressure_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.humidity_char is None:
            self.humidity_char = self.environment_service.getCharacteristics(self.humidity_char_uuid)[0]
            humidity_handle = self.humidity_char.getHandle()
            self.humidity_cccd = self.humidity_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.gas_char is None:
            self.gas_char = self.environment_service.getCharacteristics(self.gas_char_uuid)[0]
            gas_handle = self.gas_char.getHandle()
            self.gas_cccd = self.gas_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.color_char is None:
            self.color_char = self.environment_service.getCharacteristics(self.color_char_uuid)[0]
            color_handle = self.color_char.getHandle()
            self.color_cccd = self.color_char.getDescriptors(forUUID=CCCD_UUID)[0]
  


    def set_temperature_notification(self, state):
        ## Enable/Disable Temperature Notifications
        if self.temperature_cccd is not None:
            if state == True:
                self.temperature_cccd.write(b"\x01\x00", True)
            else:
                self.temperature_cccd.write(b"\x00\x00", True)
    
    def set_pressure_notification(self, state):
        ## Enable/Disable Pressure Notifications
        if self.pressure_cccd is not None:
            if state == True:
                self.pressure_cccd.write(b"\x01\x00", True)
            else:
                self.pressure_cccd.write(b"\x00\x00", True)
                
    def set_humidity_notification(self, state):
        ## Enable/Disable Humidity Notifications
        if self.humidity_cccd is not None:
            if state == True:
                self.humidity_cccd.write(b"\x01\x00", True)
            else:
                self.humidity_cccd.write(b"\x00\x00", True)    
    
    def set_gas_notification(self, state):
        ## Enable/Disable Gas Notifications
        if self.gas_cccd is not None:
            if state == True:
                self.gas_cccd.write(b"\x01\x00", True)
            else:
                self.gas_cccd.write(b"\x00\x00", True)

    def set_color_notification(self, state):
        ## Enable/Disable Color Notifications
        if self.color_cccd is not None:
            if state == True:
                self.color_cccd.write(b"\x01\x00", True)
            else:
                self.color_cccd.write(b"\x00\x00", True)
    
    def disable(self):
        ## Disable Humidity Notifications
        self.set_temperature_notification(False)
        self.set_humidity_notification(False)
        self.set_gas_notification(False)
        self.set_color_notification(False)
        self.set_pressure_notification(False)


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
    print("Connecting to " + MAC)
    Device1 = Thingy52(MAC)
    print("Connected...")
    print("Bonding...")
    Device1.setSecurityLevel("medium")
    print("Bonded...")
    print("Enabling Humidity Services...")
    Device1.environment.enable()
    Device1.setDelegate(DeviceDelegate())
    print('Services Enabled...')
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
            
