import time
import datetime
from general_programmer_class import *

class Charger(CANNodeHandler):

    def __init__(self, parent, hex_id, time_delay, depth, group):   # timee_delay: maximum time period between 2 consecutive messages
        super().__init__(parent, hex_id, time_delay, depth, group)

             
    # Data is an array of bytes
    def _give_output_message(self, data):
        if len(data) < 1:
            self.give_error("message has " + str(len(data)) + " bytes, expected at least 1")
        byte0 = data[0]
        binary = int(bin(data[0])[2:])
        bin_array = []
        while binary > 0:
            if binary % 2 == 0:
                bin_array.append(0)
            elif binary % 2 == 1:
                bin_array.append(1)
            else:
                self.give_error("paixthke malakia")
            binary = binary // 10
        if len(bin_array) != 8:
            self.give_error("bin_array doesnt have 8 bits")
        message = ''
        for i in range(8):
            message = message + str(bin_array[7 - i])
            if bin_array[7 - i] != 0:
                self.give_warning("bit " + str(i) + " is " + str(bin_array[7 - i]))
        return message
