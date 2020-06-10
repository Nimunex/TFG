from bluepy import btle
from bluepy.btle import Peripheral, DefaultDelegate
import os.path
import struct
import sys

CCCD_UUID = 0x2902

BATTERY_SERVICE_UUID = "ef68180F-9b35-4933-9B10-52FFA9740042"
BATTERY_LEVEL_UUID = "ef682AF1-9b35-4933-9B10-52FFA9740042"

battery_handle = None


class DeviceDelegate(DefaultDelegate):
    

    def handleNotification(self, hnd, data):
        
        if (hnd == battery_handle):
            data = bytearray(data)
            battery_value = data[0]
            print("A notification was received -> Battery:", battery_value, "%")



class BatterySensor():
    
    ##Battery Service module. Instance the class and enable to get access to Battery interface.
    
    svcUUID = BATTERY_SERVICE_UUID  # Ref https://www.bluetooth.com/specifications/gatt/services 
    dataUUID = BATTERY_LEVEL_UUID # Ref https://www.bluetooth.com/specifications/gatt/characteristics

    def __init__(self, periph):
        self.periph = periph
        self.service = None
        self.data = None
        self.data_cccd = None

    def enable(self):
        ##Enables the class by finding the service and its characteristics. 
        
        global battery_handle
        
        if self.service is None:
            self.service = self.periph.getServiceByUUID(self.svcUUID)
        if self.data is None:
            self.data = self.service.getCharacteristics(self.dataUUID)[0]
            battery_handle = self.data.getHandle()
            self.data_cccd = self.data.getDescriptors(forUUID=CCCD_UUID)[0]

    def b_read(self):
        ## Returns the battery level in percent 
        val = ord(self.data.read())
        return val

    def set_battery_notification(self, state):
        ## Enable/Disable Battery Notifications
        if self.data_cccd is not None:
            if state == True:
                self.data_cccd.write(b"\x01\x00", True)
            else:
                self.data_cccd.write(b"\x00\x00", True)

    def disable(self):
        ## Disable Battery Notifications
        self.set_battery_notification(False)
