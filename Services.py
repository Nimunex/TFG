

from bluepy import btle
from bluepy.btle import UUID,Peripheral, DefaultDelegate
import os.path
import struct
import sys
import binascii

from urllib.request import urlopen

import bitstring
import fxpmath
from bitstring import BitArray
from fxpmath import Fxp

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
                
def getTimeStamp():
    ts = time.time()
    ts_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return ts_str


#API key for environment services
WRITE_API = "AZOKZQAG2ZC1P2Z2" 
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)

#API key for motion services
WRITE_API_2 = "L8IVUKY6GII5QP95" 
BASE_URL_2 = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API_2)


ThingSpeakPrevSec = 0
ThingSpeakInterval = 20 # 20 seconds


## Definition of all UUID used for Environment Service

CCCD_UUID = 0x2902

##Environment UUID
ENVIRONMENT_SERVICE_UUID = "ef680200-9b35-4933-9B10-52FFA9740042"
TEMPERATURE_CHAR_UUID = "ef680201-9b35-4933-9B10-52FFA9740042"
PRESSURE_CHAR_UUID = "ef680202-9b35-4933-9B10-52FFA9740042"
HUMIDITY_CHAR_UUID = "ef680203-9b35-4933-9B10-52FFA9740042"
GAS_CHAR_UUID = "ef680204-9b35-4933-9B10-52FFA9740042"
COLOR_CHAR_UUID = "ef680205-9b35-4933-9B10-52FFA9740042"
CONFIG_CHAR_UUID = "ef680206-9b35-4933-9B10-52FFA9740042"

##Battery UUID
BATTERY_SERVICE_UUID = 0x180F
BATTERY_LEVEL_UUID = 0x2A19

##UI UUID
USER_INTERFACE_SERVICE_UUID = "ef680300-9b35-4933-9B10-52FFA9740042"
LED_CHAR_UUID = "ef680301-9b35-4933-9B10-52FFA9740042"
BUTTON_CHAR_UUID = "ef680302-9b35-4933-9B10-52FFA9740042"
EXT_PIN_CHAR_UUID = "ef680303-9b35-4933-9B10-52FFA9740042"

##Motion UUID
MOTION_SERVICE_UUID = "ef680400-9b35-4933-9B10-52FFA9740042"
TAP_CHAR_UUID = "ef680402-9b35-4933-9B10-52FFA9740042"
ORIENTATION_CHAR_UUID = "ef680403-9b35-4933-9B10-52FFA9740042"
QUATERNION_CHAR_UUID = "ef680404-9b35-4933-9B10-52FFA9740042"
STEP_COUNTER_CHAR_UUID = "ef680405-9b35-4933-9B10-52FFA9740042"
RAW_DATA_CHAR_UUID = "ef680406-9b35-4933-9B10-52FFA9740042"
EULER_CHAR_UUID = "ef680407-9b35-4933-9B10-52FFA9740042"
ROTATION_MATRIX_CHAR_UUID = "ef680408-9b35-4933-9B10-52FFA9740042"
HEADING_CHAR_UUID = "ef680409-9b35-4933-9B10-52FFA9740042"
GRAVITY_VECTOR_CHAR_UUID = "ef68040A-9b35-4933-9B10-52FFA9740042"
M_CONFIG_CHAR_UUID = "ef680401-9b35-4933-9B10-52FFA9740042"

##  Notification handles used in notification delegate

##Environment handles
temperature_handle = None
pressure_handle = None
humidity_handle = None
gas_handle = None
color_handle = None

##Battery handles
battery_handle = None

##UI handles
button_handle = None

##Motion handles
tap_handle = None
orient_handle = None
quaternion_handle = None
stepcount_handle = None
rawdata_handle = None
euler_handle = None
rotation_handle = None
heading_handle = None
gravity_handle = None



## Notifications /Indications Handler

class DeviceDelegate(DefaultDelegate):
    

    def handleNotification(self, hnd, data):
     
        
        ##Environment delegate
        if (hnd == temperature_handle):
            data = bytearray(data)
            temperature_int = data[0]
            temperature_dec = data[1]
            print("A notification was received -> Temperature:", temperature_int, ',', temperature_dec, "ºC")
            
            #~ if time() - ThingSpeakPrevSec > ThingSpeakInterval:
                
                #~ ThingSpeakPrevSec = time()
            thingspeakHttp = BASE_URL + "&field1={:.2f}".format(temperature_int + temperature_dec*0.01)
            conn = urlopen(thingspeakHttp)
            print("Response: {}".format(conn.read()))
            conn.close()
            
        elif (hnd == pressure_handle):
            teptep = binascii.b2a_hex(data)
            pressure_int = 0
            for i in range(0, 4):
                    pressure_int += (int(teptep[i*2:(i*2)+2], 16) << 8*i)
            pressure_dec = int(teptep[-2:], 16)
            print("A notification was received -> Pressure: ", pressure_int,',', pressure_dec, "  hPa")
            
            #~ if time() - ThingSpeakPrevSec > ThingSpeakInterval:
                
                #~ ThingSpeakPrevSec = time()
            thingspeakHttp2 = BASE_URL + "&field2={:.2f}".format(pressure_int + pressure_dec*0.01)
            conn = urlopen(thingspeakHttp2)
            print("Response: {}".format(conn.read()))
            conn.close()
        
        elif (hnd == humidity_handle):
            data = bytearray(data)
            humidity_value =int.from_bytes(data, byteorder='big', signed=False)                  
#            timestamp = getTimeStamp()
            print("A notification was received -> Humidity: ", humidity_value, "  %")
            
            #~ if time() - ThingSpeakPrevSec > ThingSpeakInterval:
                
                #~ ThingSpeakPrevSec = time()
            thingspeakHttp3 = BASE_URL + "&field3={:.2f}".format(humidity_value)
            conn = urlopen(thingspeakHttp3)
            print("Response: {}".format(conn.read()))
            conn.close()
        
        elif (hnd == gas_handle):
            teptep = binascii.b2a_hex(data)
            eco2 = 0
            tvoc = 0
            for i in range(0, 2):
                    eco2 += (int(teptep[i*2:(i*2)+2], 16) << 8*i)
            for i in range(2, 4):
                    tvoc += (int(teptep[i*2:(i*2)+2], 16) << 8*(i-2))
            print("A notification was received -> Gas: ", eco2, "  ppm", tvoc,"ppb")
            
            #~ if time() - ThingSpeakPrevSec > ThingSpeakInterval:
                
                #~ ThingSpeakPrevSec = time()
            thingspeakHttp4 = BASE_URL + "&field3={:.2f}".format(eco2)
            conn = urlopen(thingspeakHttp4)
            print("Response: {}".format(conn.read()))
            conn.close()

        elif (hnd == color_handle):
            teptep = binascii.b2a_hex(data)
            red = 0
            green = 0
            blue = 0
            clear = 0
            for i in range(0, 2):
                    red += (int(teptep[i*2:(i*2)+2], 16) << 8*i)
            for i in range(2, 4):
                    green += (int(teptep[i*2:(i*2)+2], 16) << 8*(i-2))
            for i in range(4, 6):
                    blue += (int(teptep[i*2:(i*2)+2], 16) << 8*(i-4))
            for i in range(6, 8):
                    clear += (int(teptep[i*2:(i*2)+2], 16) << 8*(i-6))
            print("A notification was received -> Color: ", red, green, blue, clear)
            
            thingspeakHttp13 = BASE_URL + "&field5={:.2f}".format(red)
            conn = urlopen(thingspeakHttp13)
            print("Response: {}".format(conn.read()))
            conn.close()
            thingspeakHttp14 = BASE_URL + "&field6={:.2f}".format(green)
            conn = urlopen(thingspeakHttp14)
            print("Response: {}".format(conn.read()))
            conn.close()
            thingspeakHttp15 = BASE_URL + "&field7={:.2f}".format(blue)
            conn = urlopen(thingspeakHttp15)
            print("Response: {}".format(conn.read()))
            conn.close()
        
        ##Battery delegate    
        elif (hnd == battery_handle):
            data = bytearray(data)
            battery_value = data[0]
            print("A notification was received -> Battery:", battery_value, "%")
        
        ##UI delegate
        elif (hnd == button_handle):
            data = bytearray(data)
            button = data[0]
            print("A notification was received -> Button[1-> pressed]: ", button)
            
            thingspeakHttp6 = BASE_URL + "&field8={:}".format(button)
            conn = urlopen(thingspeakHttp6)
            print("Response: {}".format(conn.read()))
            conn.close()
        
        ##Motion delegate
        elif (hnd == tap_handle):
             
            data = bytearray(data)
            tap = data[0]
            count = data[1]
            if tap == 0x01:
                print("A notification was received -> TAP_X_UP, count: ", count)
            elif tap == 0x02:
                print("A notification was received -> TAP_X_DOWN, count: ", count)
            elif tap == 0x03:
                print("A notification was received -> TAP_Y_UP, count: ", count)
            elif tap == 0x04:
                print("A notification was received -> TAP_Y_DOWN, count: ", count)   
            elif tap == 0x05:
                print("A notification was received -> TAP_Z_UP, count: ", count)   
            elif tap == 0x06:
                print("A notification was received -> TAP_Z_DOWN, count: ", count)   


        elif (hnd == orient_handle):
            data = bytearray(data)
            orientation = data[0]
            if orientation == 0x00:
                print("A notification was received -> Orientation: Portrait ")
            elif orientation == 0x01:
                print("A notification was received -> Orientation: Landscape ")
            elif orientation == 0x02:
                print("A notification was received -> Orientation: Reverse Portrait ")
            elif orientation == 0x03:
                print("A notification was received -> Orientation: Reverse Landscape ")

           

        elif (hnd == quaternion_handle):
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[3] & 0x80:
                negative = True    
            result  = data[3] << 24
            result += data[2] << 16
            result += data[1] << 8
            result += data[0]
    
            w = 0.
            if negative:
                #this is negative
                result = (1 << 32) - 1 - result
                result = result+1
                w = -1. * (float(result) / 1073741823.)
            else:
                #this is positive
                w = float(result) / 1073741823.
            #~ print( "{:.4f}".format( resultF ))
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[7] & 0x80:
                negative = True    
            result  = data[7] << 24
            result += data[6] << 16
            result += data[5] << 8
            result += data[4]
    
            x = 0.
            if negative:
                #this is negative
                result = (1 << 32) - 1 - result
                result = result+1
                x = -1. * (float(result) / 1073741823.)
            else:
                #this is positive
                x = float(result) / 1073741823.
        
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[11] & 0x80:
                negative = True    
            result  = data[11] << 24
            result += data[10] << 16
            result += data[9] << 8
            result += data[8]
    
            y = 0.
            if negative:
                #this is negative
                result = (1 << 32) - 1 - result
                result = result+1
                y = -1. * (float(result) / 1073741823.)
            else:
                #this is positive
                y = float(result) / 1073741823.
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[15] & 0x80:
                negative = True    
            result  = data[15] << 24
            result += data[14] << 16
            result += data[13] << 8
            result += data[12]
    
            z = 0.
            if negative:
                #this is negative
                result = (1 << 32) - 1 - result
                result = result+1
                z = -1. * (float(result) / 1073741823.)
            else:
                #this is positive
                z = float(result) / 1073741823.
           
            print("A notification was received -> Quaternion(w,x,y,z): {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(w,x,y,z))
            

        elif (hnd == stepcount_handle):
            teptep = binascii.b2a_hex(data)
            steps = 0
            time = 0
            for i in range(0, 4):
                    steps += (int(teptep[i*2:(i*2)+2], 16) << 8*i)
            for i in range(4, 8):
                    time += (int(teptep[i*2:(i*2)+2], 16) << 8*(i-4))
            print("A notification was received -> Stepcount(steps,time): ", steps, time)
            #~ print('Notification: Step Count: {}'.format(teptep))

        elif (hnd == rawdata_handle):
     
            ##Accelerometer
             #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[1] & 0x80:
                negative = True    
            result  = data[1] << 8
            result += data[0] 
    
            ax = 0.
            if negative:
                #this is negative
                result = (1 << 16) - 1 - result
                result = result+1
                ax = -1. * (float(result) / 1023.)
            else:
                #this is positive
                ax = float(result) / 1023.
            
             #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[3] & 0x80:
                negative = True    
            result  = data[3] << 8
            result += data[2] 
    
            ay = 0.
            if negative:
                #this is negative
                result = (1 << 16) - 1 - result
                result = result+1
                ay = -1. * (float(result) / 1023.)
            else:
                #this is positive
                ay = float(result) / 1023.
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[5] & 0x80:
                negative = True    
            result  = data[5] << 8
            result += data[4] 
    
            az = 0.
            if negative:
                #this is negative
                result = (1 << 16) - 1 - result
                result = result+1
                az = -1. * (float(result) / 1023.)
            else:
                #this is positive
                az = float(result) / 1023.
          
            ##Gyroscope
             #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[7] & 0x80:
                negative = True    
            result  = data[7] << 8
            result += data[6] 
    
            gx = 0.
            if negative:
                #this is negative
                result = (1 << 16) - 1 - result
                result = result+1
                gx = -1. * (float(result) / 31.)
            else:
                #this is positive
                gx = float(result) / 31.
            
             #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[9] & 0x80:
                negative = True    
            result  = data[9] << 8
            result += data[8] 
    
            gy = 0.
            if negative:
                #this is negative
                result = (1 << 16) - 1 - result
                result = result+1
                gy = -1. * (float(result) / 31.)
            else:
                #this is positive
                gy = float(result) / 31.
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[11] & 0x80:
                negative = True    
            result  = data[11] << 8
            result += data[10] 
    
            gz = 0.
            if negative:
                #this is negative
                result = (1 << 16) - 1 - result
                result = result+1
                gz = -1. * (float(result) / 31.)
            else:
                #this is positive
                gz = float(result) / 31.
          
            ##Compass
             #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[13] & 0x80:
                negative = True    
            result  = data[13] << 8
            result += data[12] 
    
            cx = 0.
            if negative:
                #this is negative
                result = (1 << 16) - 1 - result
                result = result+1
                cx = -1. * (float(result) / 15.)
            else:
                #this is positive
                cx = float(result) / 15.
            
             #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[15] & 0x80:
                negative = True    
            result  = data[15] << 8
            result += data[14] 
    
            cy = 0.
            if negative:
                #this is negative
                result = (1 << 16) - 1 - result
                result = result+1
                cy = -1. * (float(result) / 15.)
            else:
                #this is positive
                cy = float(result) / 15.
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[17] & 0x80:
                negative = True    
            result  = data[17] << 8
            result += data[16] 
    
            cz = 0.
            if negative:
                #this is negative
                result = (1 << 16) - 1 - result
                result = result+1
                cz = -1. * (float(result) / 15.)
            else:
                #this is positive
                cz = float(result) / 15.

            print("A notification was received -> Raw data: Accelerometer(G):{:.2f}, {:.2f}, {:.2f} Gyroscope(deg/s): {:.2f}, {:.2f}, {:.2f} Compass(uT): {:.2f}, {:.2f}, {:.2f}".format(ax,ay,az,gx,gy,gz,cx,cy,cz))
        
        elif (hnd == euler_handle):
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[3] & 0x80:
                negative = True    
            result  = data[3] << 24
            result += data[2] << 16
            result += data[1] << 8
            result += data[0]
    
            roll = 0.
            if negative:
                #this is negative
                result = (1 << 32) - 1 - result
                result = result+1
                roll = -1. * (float(result) / 65535.)
            else:
                #this is positive
                roll = float(result) / 65535.
            #~ print( "{:.4f}".format( resultF ))
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[7] & 0x80:
                negative = True    
            result  = data[7] << 24
            result += data[6] << 16
            result += data[5] << 8
            result += data[4]
    
            pitch = 0.
            if negative:
                #this is negative
                result = (1 << 32) - 1 - result
                result = result+1
                pitch = -1. * (float(result) / 65535.)
            else:
                #this is positive
                pitch = float(result) / 65535.
        
            
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[11] & 0x80:
                negative = True    
            result  = data[11] << 24
            result += data[10] << 16
            result += data[9] << 8
            result += data[8]
    
            yaw = 0.
            if negative:
                #this is negative
                result = (1 << 32) - 1 - result
                result = result+1
                yaw = -1. * (float(result) / 65535.)
            else:
                #this is positive
                yaw = float(result) / 65535.
           
    
            print("A notification was received -> Euler(roll,pitch,yaw)[degrees]: {:.2f}, {:.2f}, {:.2f}".format(roll,pitch,yaw))
            
            thingspeakHttp7 = BASE_URL_2 + "&field1={:.2f}".format(roll)
            conn = urlopen(thingspeakHttp7)
            print("Response: {}".format(conn.read()))
            conn.close()
            thingspeakHttp8 = BASE_URL_2 + "&field2={:.2f}".format(pitch)
            conn = urlopen(thingspeakHttp8)
            print("Response: {}".format(conn.read()))
            conn.close()
            thingspeakHttp9 = BASE_URL_2 + "&field3={:.2f}".format(yaw)
            conn = urlopen(thingspeakHttp9)
            print("Response: {}".format(conn.read()))
            conn.close()
            

        elif (hnd == rotation_handle):
            teptep = binascii.b2a_hex(data)
            print('Notification: Rotation matrix: {}'.format(teptep))

        elif (hnd == heading_handle):
            #True if this is negative number 
            negative = False
            result = 0
            #check oldest bit
            if data[3] & 0x80:
                negative = True    
            result  = data[3] << 24
            result += data[2] << 16
            result += data[1] << 8
            result += data[0]
    
            heading = 0.
            if negative:
                #this is negative
                result = (1 << 32) - 1 - result
                result = result+1
                heading = -1. * (float(result) / 65535.)
            else:
                #this is positive
                heading = float(result) / 65535.
            print("A notification was received -> Heading(degrees): ", heading)
            

        elif (hnd == gravity_handle):
           
            d2=data[0:4]
            [gx] = struct.unpack('f', d2)
            d3=data[4:8]
            [gy] = struct.unpack('f', d3)
            d4=data[8:12]
            [gz] = struct.unpack('f', d4)
            
            print("A notification was received -> Gravity(x,y,z): {:.2f}, {:.2f}, {:.2f}".format(gx,gy,gz))
            
            thingspeakHttp10 = BASE_URL_2 + "&field1={:.2f}".format(roll)
            conn = urlopen(thingspeakHttp10)
            print("Response: {}".format(conn.read()))
            conn.close()
            thingspeakHttp11 = BASE_URL_2 + "&field2={:.2f}".format(pitch)
            conn = urlopen(thingspeakHttp11)
            print("Response: {}".format(conn.read()))
            conn.close()
            thingspeakHttp12 = BASE_URL_2 + "&field3={:.2f}".format(yaw)
            conn = urlopen(thingspeakHttp12)
            print("Response: {}".format(conn.read()))
            conn.close()
            

           
            
            
            
class EnvironmentService():
    
    ##Environment service module. Instance the class and enable to get access to the Environment interface.
    serviceUUID  = ENVIRONMENT_SERVICE_UUID
    temperature_char_uuid  = TEMPERATURE_CHAR_UUID
    pressure_char_uuid  = PRESSURE_CHAR_UUID
    humidity_char_uuid  = HUMIDITY_CHAR_UUID
    gas_char_uuid  = GAS_CHAR_UUID
    color_char_uuid  = COLOR_CHAR_UUID
    config_char_uuid = CONFIG_CHAR_UUID

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
        if self.config_char is None:
            self.config_char = self.environment_service.getCharacteristics(self.config_char_uuid)[0]

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
        ## Disable Environment Notifications
        self.set_temperature_notification(False)
        self.set_pressure_notification(False)
        self.set_humidity_notification(False)
        self.set_gas_notification(False)
        self.set_color_notification(False)
        
        
class BatterySensor():
    
    ##Battery Service module. Instance the class and enable to get access to Battery interface.
    
    svcUUID = UUID(BATTERY_SERVICE_UUID)  # Ref https://www.bluetooth.com/specifications/gatt/services 
    dataUUID = UUID(BATTERY_LEVEL_UUID) # Ref https://www.bluetooth.com/specifications/gatt/characteristics

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

class UserInterfaceService():
    """
    User interface service module. Instance the class and enable to get access to the UI interface.
    """
    serviceUUID = USER_INTERFACE_SERVICE_UUID
    led_char_uuid = LED_CHAR_UUID
    btn_char_uuid = BUTTON_CHAR_UUID
    # To be added: EXT PIN CHAR

    def __init__(self, periph):
        self.periph = periph
        self.ui_service = None
        self.led_char = None
        self.btn_char = None
        self.btn_char_cccd = None
        # To be added: EXT PIN CHAR

    def enable(self):
        """ Enables the class by finding the service and its characteristics. """
        global button_handle

        if self.ui_service is None:
            self.ui_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.led_char is None:
            self.led_char = self.ui_service.getCharacteristics(self.led_char_uuid)[0]
        if self.btn_char is None:
            self.btn_char = self.ui_service.getCharacteristics(self.btn_char_uuid)[0]
            button_handle = self.btn_char.getHandle()
            self.btn_char_cccd = self.btn_char.getDescriptors(forUUID=CCCD_UUID)[0]

    def set_led_mode_off(self):
        self.led_char.write(b"\x00", True)
        
    def set_led_mode_constant(self, r, g, b):
        teptep = "01{:02X}{:02X}{:02X}".format(r, g, b)
        self.led_char.write(binascii.a2b_hex(teptep), True)
        
    def set_led_mode_breathe(self, color, intensity, delay):
        """
        Set LED to breathe mode.
        color has to be within 0x01 and 0x07
        intensity [%] has to be within 1-100
        delay [ms] has to be within 1 ms - 10 s
        """
        teptep = "02{:02X}{:02X}{:02X}{:02X}".format(color, intensity,
                delay & 0xFF, delay >> 8)
        self.led_char.write(binascii.a2b_hex(teptep), True)
        
    def set_led_mode_one_shot(self, color, intensity):  
        """
        Set LED to one shot mode.
        color has to be within 0x01 and 0x07
        intensity [%] has to be within 1-100
        """
        teptep = "03{:02X}{:02X}".format(color, intensity)
        self.led_char.write(binascii.a2b_hex(teptep), True)

    def set_button_notification(self, state):
        if self.btn_char_cccd is not None:
            if state == True:
                self.btn_char_cccd.write(b"\x01\x00", True)
            else:
                self.btn_char_cccd.write(b"\x00\x00", True)

    def disable(self):
        set_button_notification(False)

class MotionService():
    
    ##Motion service module. Instance the class and enable to get access to the Motion interface.
    
    serviceUUID =           MOTION_SERVICE_UUID
    config_char_uuid =      M_CONFIG_CHAR_UUID
    tap_char_uuid =         TAP_CHAR_UUID
    orient_char_uuid =      ORIENTATION_CHAR_UUID
    quaternion_char_uuid =  QUATERNION_CHAR_UUID
    stepcnt_char_uuid =     STEP_COUNTER_CHAR_UUID
    rawdata_char_uuid =     RAW_DATA_CHAR_UUID
    euler_char_uuid =       EULER_CHAR_UUID
    rotation_char_uuid =    ROTATION_MATRIX_CHAR_UUID
    heading_char_uuid =     HEADING_CHAR_UUID
    gravity_char_uuid =     GRAVITY_VECTOR_CHAR_UUID

    def __init__(self, periph):
        self.periph = periph
        self.motion_service = None
        self.config_char = None
        self.tap_char = None
        self.tap_char_cccd = None
        self.orient_char = None
        self.orient_cccd = None
        self.quaternion_char = None
        self.quaternion_cccd = None
        self.stepcnt_char = None
        self.stepcnt_cccd = None
        self.rawdata_char = None
        self.rawdata_cccd = None
        self.euler_char = None
        self.euler_cccd = None
        self.rotation_char = None
        self.rotation_cccd = None
        self.heading_char = None
        self.heading_cccd = None
        self.gravity_char = None
        self.gravity_cccd = None

    def enable(self):
        ##Enables the class by finding the service and its characteristics. 
        
        global tap_handle
        global orient_handle
        global quaternion_handle
        global stepcount_handle
        global rawdata_handle
        global euler_handle
        global rotation_handle
        global heading_handle
        global gravity_handle

        if self.motion_service is None:
            self.motion_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.config_char is None:
            self.config_char = self.motion_service.getCharacteristics(self.config_char_uuid)[0]
        if self.tap_char is None:
            self.tap_char = self.motion_service.getCharacteristics(self.tap_char_uuid)[0]
            tap_handle = self.tap_char.getHandle()
            self.tap_char_cccd = self.tap_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.orient_char is None:
            self.orient_char = self.motion_service.getCharacteristics(self.orient_char_uuid)[0]
            orient_handle = self.orient_char.getHandle()
            self.orient_cccd = self.orient_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.quaternion_char is None:
            self.quaternion_char = self.motion_service.getCharacteristics(self.quaternion_char_uuid)[0]
            quaternion_handle = self.quaternion_char.getHandle()
            self.quaternion_cccd = self.quaternion_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.stepcnt_char is None:
            self.stepcnt_char = self.motion_service.getCharacteristics(self.stepcnt_char_uuid)[0]
            stepcount_handle = self.stepcnt_char.getHandle()
            self.stepcnt_cccd = self.stepcnt_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.rawdata_char is None:
            self.rawdata_char = self.motion_service.getCharacteristics(self.rawdata_char_uuid)[0]
            rawdata_handle = self.rawdata_char.getHandle()
            self.rawdata_cccd = self.rawdata_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.euler_char is None:
            self.euler_char = self.motion_service.getCharacteristics(self.euler_char_uuid)[0]
            euler_handle = self.euler_char.getHandle()
            self.euler_cccd = self.euler_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.rotation_char is None:
            self.rotation_char = self.motion_service.getCharacteristics(self.rotation_char_uuid)[0]
            rotation_handle = self.rotation_char.getHandle()
            self.rotation_cccd = self.rotation_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.heading_char is None:
            self.heading_char = self.motion_service.getCharacteristics(self.heading_char_uuid)[0]
            heading_handle = self.heading_char.getHandle()
            self.heading_cccd = self.heading_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.gravity_char is None:
            self.gravity_char = self.motion_service.getCharacteristics(self.gravity_char_uuid)[0]
            gravity_handle = self.gravity_char.getHandle()
            self.gravity_cccd = self.gravity_char.getDescriptors(forUUID=CCCD_UUID)[0]

    def set_tap_notification(self, state):
        if self.tap_char_cccd is not None:
            if state == True:
                self.tap_char_cccd.write(b"\x01\x00", True)
            else:
                self.tap_char_cccd.write(b"\x00\x00", True)

    def set_orient_notification(self, state):
        if self.orient_cccd is not None:
            if state == True:
                self.orient_cccd.write(b"\x01\x00", True)
            else:
                self.orient_cccd.write(b"\x00\x00", True)

    def set_quaternion_notification(self, state):
        if self.quaternion_cccd is not None:
            if state == True:
                self.quaternion_cccd.write(b"\x01\x00", True)
            else:
                self.quaternion_cccd.write(b"\x00\x00", True)

    def set_stepcount_notification(self, state):
        if self.stepcnt_cccd is not None:
            if state == True:
                self.stepcnt_cccd.write(b"\x01\x00", True)
            else:
                self.stepcnt_cccd.write(b"\x00\x00", True)

    def set_rawdata_notification(self, state):
        if self.rawdata_cccd is not None:
            if state == True:
                self.rawdata_cccd.write(b"\x01\x00", True)
            else:
                self.rawdata_cccd.write(b"\x00\x00", True)

    def set_euler_notification(self, state):
        if self.euler_cccd is not None:
            if state == True:
                self.euler_cccd.write(b"\x01\x00", True)
            else:
                self.euler_cccd.write(b"\x00\x00", True)

    def set_rotation_notification(self, state):
        if self.rotation_cccd is not None:
            if state == True:
                self.rotation_cccd.write(b"\x01\x00", True)
            else:
                self.rotation_cccd.write(b"\x00\x00", True)

    def set_heading_notification(self, state):
        if self.heading_cccd is not None:
            if state == True:
                self.heading_cccd.write(b"\x01\x00", True)
            else:
                self.heading_cccd.write(b"\x00\x00", True)

    def set_gravity_notification(self, state):
        if self.gravity_cccd is not None:
            if state == True:
                self.gravity_cccd.write(b"\x01\x00", True)
            else:
                self.gravity_cccd.write(b"\x00\x00", True)

    def configure(self, step_int=None, temp_comp_int=None, magnet_comp_int=None,
                        motion_freq=None, wake_on_motion=None):
        if step_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, step_int, 0)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if temp_comp_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, temp_comp_int, 1)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if magnet_comp_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, magnet_comp_int, 2)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if motion_freq is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, motion_freq, 3)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if wake_on_motion is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint8(current_config, wake_on_motion, 8)
            self.config_char.write(binascii.a2b_hex(new_config), True)

    def disable(self):
        set_tap_notification(False)
        set_orient_notification(False)
        set_quaternion_notification(False)
        set_stepcount_notification(False)
        set_rawdata_notification(False)
        set_euler_notification(False)
        set_rotation_notification(False)
        set_heading_notification(False)
        set_gravity_notification(False)






