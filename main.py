##Main

from bluepy import btle
from bluepy.btle import Peripheral, DefaultDelegate
import os.path
import struct
import binascii
import sys
import datetime
import time
from time import time,sleep
import Services
from Services import EnvironmentService, BatterySensor, UserInterfaceService, MotionService, DeviceDelegate
import Device
from Device import Device
from urllib.request import urlopen


##Mac 1: FD:88:50:58:E7:45
##Mac 2: E4:F6:C5:F7:03:39

## MAC address Device device
global MAC


if __name__ == "__main__":
    MAC = str(sys.argv[1])

 


    print("Connecting to " + MAC)
    Device1 = Device(MAC)
    print("Connected...")
    print("Bonding...")
    Device1.setSecurityLevel("medium")
    print("Bonded...")
    print("Enabling Services...")
    Device1.battery.enable()
    Device1.environment.enable()
    Device1.ui.enable()

    
    Device1.setDelegate(DeviceDelegate())
    print('Services Enabled...')

    print('Battery Level(1): ', Device1.battery.b_read(), '%')
    

    
    #~ Device1.ui.set_led_mode_breathe(0x02, 50, 1000) 
    ##Battery sensor
    #~ Device1.battery.set_battery_notification(True)
    ##Environment Services
    #~ Device1.environment.configure(temp_int=20000)
    #~ Device1.environment.set_temperature_notification(True)
    
    #~ Device1.environment.configure(press_int=20000)
    #~ Device1.environment.set_pressure_notification(True)
    
    Device1.environment.configure(humid_int=20000)
    Device1.environment.set_humidity_notification(True)
    #~ Device1.environment.set_gas_notification(True)
    #~ Device1.environment.configure(gas_mode_int=2)
    #~ Device1.environment.set_color_notification(True)
    #~ Device1.environment.configure(color_int=20000)
    
    ##UI service
    Device1.ui.set_button_notification(True)
    
    ##Motion Services
    #~ Device1.motion.configure(motion_freq=5)
    #~ Device1.motion.set_tap_notification(True)
    #~ Device1.motion.set_orient_notification(True)
    #~ Device1.motion.set_quaternion_notification(True)
    #~ Device1.motion.set_stepcount_notification(True)
    #~ Device1.motion.set_rawdata_notification(True)
    #~ Device1.motion.set_euler_notification(True)
    #~ Device1.motion.set_rotation_notification(True)
    #~ Device1.motion.set_heading_notification(True)
    #~ Device1.motion.set_gravity_notification(True)

    
    
    


    try:
        while True:
            if Device1.waitForNotifications(20.0) :
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
            
