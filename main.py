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
import Services
from Services import EnvironmentService, BatterySensor, UserInterfaceService, MotionService, DeviceDelegate
import Device
from Device import Device


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
    #select = input("Select the service (1)-Temperature (2)-Pressure (3)-Humidity (4)-Gas (5)-Color (6)-All: ")
    
    print("Enabling Services...")
    Device1.battery.enable()
    Device1.environment.enable()
    Device1.ui.enable()
    Device1.motion.enable()
    
    Device1.setDelegate(DeviceDelegate())
    print('Services Enabled...')

    print('Battery Level: ', Device1.battery.b_read(), '%')
    
    #~ led = int(raw_input("Select the mode (1)-Off (2)-Constant (3)-Breathe (4)- One shot: "))
    #~ if (led) == 1
        #~ Device1.ui.set_led_mode_off()
    #~ elif (led) == 2
        #~ red = input("Red[0-255]: ")
        #~ green = input("Green[0-255]: ")
        #~ blue = input(Blue[0-255]: ")
        #~ Device1.ui.set_led_mode_constant(red, green, blue)
    #~ elif (led) == 3
        #~ color = input("Color(use 0x0X)[1(Red)-2(Green)-3(Yellow)-4(Blue)-5(Purple)-6(Cyan)-7(White)]: ")
        #~ intensity = input("Intensity(%)[1-100]: ")
        #~ delay = input(Delay[50ms-10s]: ")
        #~ Device1.ui.set_led_mode_breathe(color, intensity, delay)
    #~ elif (led) == 4
        #~ color = input("Color(use 0x0X)[1(Red)-2(Green)-3(Yellow)-4(Blue)-5(Purple)-6(Cyan)-7(White)]: ")
        #~ intensity = input("Intensity(%)[1-100]: ")
        #~ Device1.ui.set_led_mode_one_shot(color, intensity)
    
    #~ Device1.ui.set_led_mode_breathe(0x03, 50, 1000)
    #~ Device1.battery.set_battery_notification(True)
    #~ Device1.environment.set_temperature_notification(True)
    #~ Device1.environment.configure(temp_int=1000)
    #~ Device1.environment.set_pressure_notification(True)
    #~ Device1.environment.set_humidity_notification(True)
    #~ Device1.environment.set_gas_notification(True)
    #~ Device1.environment.set_color_notification(True)
    #~ Device1.ui.set_button_notification(True)
    #~ Device1.motion.set_tap_notification(True)
    #~ Device1.motion.set_orient_notification(True)
    #~ Device1.motion.set_quaternion_notification(True)
    #~ Device1.motion.set_stepcount_notification(True)
    #~ Device1.motion.set_rawdata_notification(True)
    Device1.motion.set_euler_notification(True)
    #~ Device1.motion.set_rotation_notification(True)
    #~ Device1.motion.set_heading_notification(True)
    #~ Device1.motion.set_gravity_notification(True)
    


    try:
        while True:
            if Device1.waitForNotifications(20.0):
                # handleNotification() was called
                continue
            print("Waiting...")                
                
    except KeyboardInterrupt:     
        print("Disabling Notifications and Indications...")
        Device1.environment.disable()
        Device1.battery.disable()
        Device1.ui.disable()
        Device1.motion.disable()
        print("Notifications and Indications Disabled...")
        print("Device Session Finished...")
            
