import threading
import time
import datetime
import random

class Message:
    # Data is an array of bytes which has length 1-8 bytes
    def __init__(self, dec_id, data):
        self.__dec_id = dec_id
        self.__data = data

    
    def get_dec_id(self):
        return self.__dec_id


    def get_data(self):
        return self.__data



class CANBusHandler(threading.Thread):
    def __init__(self, class_caller):
        threading.Thread.__init__(self, daemon = True)
        self.__parent_class = class_caller

    def run(self):

        can_group = random.randint(0, 1)
        # ID = 500 / 501 doesnt belong to a sensor - only for testing
        if can_group == 0: # Primary CAN bus
            dec_ids_list = [769, 771, 773, 784, 785, 16, 774, 776, 777, 778, 780, 1365, 256, 257, 258, 259, 261, 262, 263,
                    264, 385, 1792, 1793, 1794, 1795, 1025, 1024, 500]
        else: # Sensory CAN bus
            dec_ids_list = [1260, 1261, 1263, 1264, 1265, 1266, 1268, 1270, 1272, 1274, 1313, 1314, 501]
        
        while True:
            random_id = dec_ids_list[random.randint(0, len(dec_ids_list)-1)]
            current = time.time()
            time.sleep(0.001)
            
            data = []
            if random_id == 769: # APPS
                app1 = random.randint(0, 100)
                app2 = abs(app1 + random.randint(-5, 5))
                while app2 > 100:
                    app2 -= 1
                data.append(app1)
                data.append(app2)
            elif random_id == 771: # Brake
                bp1 = random.randint(0, 100)
                bp2 = abs(bp1 + random.randint(-4, 4))
                data.append(bp1) # Brake Pressures
                data.append(random.randint(0, 255))
                data.append(bp2)
                data.append(random.randint(0, 255))
                data.append(random.randint(0, 95))  # Steering angle
                data.append(random.randint(0, 1))   # Steering sign (0:+, 1:-)
            else:
                n = random.randint(1, 7)
                for i in range(0, n):
                    data.append(random.randint(0, 100))
            new_msg = Message(random_id, data)
            self.__parent_class.new_msg(new_msg)
