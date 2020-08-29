#####################################################################
# BLE devices handler                                               #
# A new subprocess is created for each preregistered device in:     #
# ./devices.mac                                                     #
#####################################################################

import subprocess
import time 

#~ mac_file = open('devices.mac', 'r')

#~ for mac_address in mac_file:
		#~ subprocess.call(['gnome-terminal', '-e', 'python3 main.py ' + mac_address])
		#~ time.sleep(10)

subprocess.call(['gnome-terminal', '-e', 'python3 main.py FD:88:50:58:E7:45' ])
time.sleep(20)
subprocess.call(['gnome-terminal', '-e', 'python3 mainMotion.py E4:F6:C5:F7:03:39' ])
