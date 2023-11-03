import time
import datetime
from general_programmer_class import *

class Brake(CANNodeHandler):

    def __init__(self, parent, hex_id, time_delay, depth, group):   # timee_delay: maximum time period between 2 consecutive messages
        super().__init__(parent, hex_id, time_delay, depth, group)

             
    # Data is an array of bytes
    def _give_output_message(self, data):
            
        if len(data) != 6:
            self.give_error("CAN bus sent " + str(len(data)) + " bytes, expected 6 bytes")
            message = "incorrect number of bytes"
        else:
            int1 = data[0]
            dummy1 = data[1]
            int2 = data[2]
            dummy2 = data[3]
            steering_angle = data[4]
            steering_sign = data[5]
                
            if steering_angle > 95:
                self.give_error("Steering angle is: " + str(steering_angle) + ". Expected value <= 95")

            if steering_sign == 0:
                turn = "right"
            elif steering_sign == 1:
                turn = "left"
            else:
                self.give_error("Steering sign message is: " + str(steering_sign) + ". Expected 0 or 1")
                
            dec1 = self.__find_decimal(dummy1)
            dec2 = self.__find_decimal(dummy2)
            brake_pressure1 = int1 + dec1
            brake_pressure2 = int2 + dec2
            
            if abs(brake_pressure1 - brake_pressure2) > 5:
                self.give_error("Front Brake Pressure: " + str(round(brake_pressure1, 3)) + " bar, Rear Brake Pressure: " + str(round(brake_pressure2, 3)) + " bar. They differ by " + str(round(abs(brake_pressure1 - brake_pressure2), 3)) + " > 5.")

            message = "Front Brake Pressure: " + str(round(brake_pressure1, 3)) + " bar, Rear Brake Pressure: " + str(round(brake_pressure2, 3)) + " bar. Steering: " + str(steering_angle) + " degrees " + turn

        return message

            
    def __find_decimal(self, decimal):  
        binary = []
        result = 0
        while decimal > 0:
            binary.append(decimal % 2) # binary array has the number in binary form from LSB to MSB
            decimal = decimal // 2
        for i in range(1, len(binary)):
            result += binary[len(binary) - i] * pow(1/2, i + 8 - len(binary)) # 8 is the number of bits in a byte
        return result
