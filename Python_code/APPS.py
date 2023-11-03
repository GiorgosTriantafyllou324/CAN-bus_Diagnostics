import time
import datetime
from general_programmer_class import *

class APPS(CANNodeHandler):

    def __init__(self, parent, hex_id, time_delay, depth, group):   # timee_delay: maximum time period between 2 consecutive messages
        super().__init__(parent, hex_id, time_delay, depth, group)
        
             
    # Data is an array of bytes
    def _give_output_message(self, data):
            
        if len(data) != 2:
            self.give_error("CAN bus sent " + str(len(data)) + " bytes, expected 2 bytes")
            message = "incorrect number of bytes"
        else:
            app1 = data[0]
            app2 = data[1]
            if app1 < 5: # TESTING
                self.give_warning("Test warning")
            if app1 == 255:
                self.give_error("Left APPS message received: 255")
            elif app1 < 0 or app1 > 100:  
                self.give_error("Left APPS message received: " + str(app1) + "% (out of bounds)")
            if app2 == 255:
                self.give_error("Right APPS message received: 255")
            elif app2 < 0 or app2 > 100:
                self.give_error("Right APPS message received: " + str(app2) + "%  (out of bounds)")

            if abs(app1 - app2) > 5:
                self.give_error("Right APPS: " + str(app2) + ", Left APPS: " + str(app1) + ". They differ by " + str(abs(app1 - app2)) + " > 5.")
            
            message = "Left APPS: " + str(app1) + ",   Right APPS: " + str(app2) + " %"
        return message


            

            
