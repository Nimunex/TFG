

from bluepy import btle
from bluepy.btle import Peripheral, DefaultDelegate
import os.path
import struct
import sys
import binascii
#import Device
#from Device import Device, DeviceDelegate


#Useful functions

def write_uint16(data, value, index):
    ## Write 16bit value into data string at index and return new string 
    data = data.decode('utf-8')  # This line is added to make sure both Python 2 and 3 works
    return '{}{:02x}{:02x}{}'.format(
                data[:index*4], 
                value & 0xFF, value >> 8, 
                data[index*4 + 4:])

def write_uint8(data, value, index):
    ## Write 8bit value into data string at index and return new string 
    data = data.decode('utf-8')  # This line is added to make sure both Python 2 and 3 works
    return '{}{:02x}{}'.format(
                data[:index*2], 
                value, 
                data[index*2 + 2:])

## Definition of all UUID used for Environment Service

CCCD_UUID = 0x2902

ENVIRONMENT_SERVICE_UUID = "ef680200-9b35-4933-9B10-52FFA9740042"
TEMPERATURE_CHAR_UUID = "ef680201-9b35-4933-9B10-52FFA9740042"
PRESSURE_CHAR_UUID = "ef680202-9b35-4933-9B10-52FFA9740042"
HUMIDITY_CHAR_UUID = "ef680203-9b35-4933-9B10-52FFA9740042"
GAS_CHAR_UUID = "ef680204-9b35-4933-9B10-52FFA9740042"
COLOR_CHAR_UUID = "ef680205-9b35-4933-9B10-52FFA9740042"
CONFIG_CHAR_UUID = "ef680206-9b35-4933-9B10-52FFA9740042"

##  Notification handles used in notification delegate

temperature_handle = None
pressure_handle = None
humidity_handle = None
gas_handle = None
color_handle = None


class EnvironmentService():
    
    ##Environment service module. Instance the class and enable to get access to the Environment interface.
    serviceUUID  = ENVIRONMENT_SERVICE_UUID
    temperature_char_uuid  = TEMPERATURE_CHAR_UUID
    pressure_char_uuid  = PRESSURE_CHAR_UUID
    humidity_char_uuid  = HUMIDITY_CHAR_UUID
    gas_char_uuid  = GAS_CHAR_UUID
    color_char_uuid  = COLOR_CHAR_UUID

    def __init__(self, periph):
        self.periph = periph
        self.environment_service = None
        self.temperature_char = None
        self.temperature_cccd = None
        self.pressure_char = None
        self.pressure_cccd = None
        self.humidity_char = None
        self.humidity_cccd = None
        self.gas_char = None
        self.gas_cccd = None
        self.color_char = None
        self.color_cccd = None
        self.config_char = None

    def enable(self):
        ##Enables the class by finding the service and its characteristics. 

        global temperature_handle
        global pressure_handle
        global humidity_handle
        global gas_handle
        global color_handle


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
        #if self.config_char is None:
            #self.config_char = self.environment_service.getCharacteristics(self.config_char_uuid)[0]

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
    
    def configure(self, temp_int=None, press_int=None, humid_int=None, gas_mode_int=None,
                        color_int=None, color_sens_calib=None):
        if temp_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, temp_int, 0)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if press_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, press_int, 1)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if humid_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, humid_int, 2)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if gas_mode_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint8(current_config, gas_mode_int, 8)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if color_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, color_int, 3)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if color_sens_calib is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint8(current_config, color_sens_calib[0], 9)
            new_config = write_uint8(current_config, color_sens_calib[1], 10)
            new_config = write_uint8(current_config, color_sens_calib[2], 11)
            self.config_char.write(binascii.a2b_hex(new_config), True)
    
    
    def disable(self):
        ## Disable All Notifications
        self.set_temperature_notification(False)
        self.set_pressure_notification(False)
        self.set_humidity_notification(False)
        self.set_gas_notification(False)
        self.set_color_notification(False)




