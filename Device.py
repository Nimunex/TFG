#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:05:12 2020

@author: pi
"""

from bluepy import btle
from bluepy.btle import Peripheral, DefaultDelegate
import EnvironmentService
from EnvironmentService import EnvironmentService

## Thingy52 Definition

class Device(Peripheral):
    ##Thingy:52 module. Instance the class and enable to get access to the Thingy:52 Sensors.
    #The addr of your device has to be know, or can be found by using the hcitool command line 
    #tool, for example. Call "> sudo hcitool lescan" and your Thingy's address should show up.
    
    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType="random")

         #Thingy configuration service not implemented
        #self.battery = BatterySensor(self)
        self.environment = EnvironmentService(self)
        #self.ui = UserInterfaceService(self)
        #self.motion = MotionService(self)
        #self.sound = SoundService(self)
        
        
    
