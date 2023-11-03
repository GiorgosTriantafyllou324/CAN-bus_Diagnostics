import time
import datetime

class CANNodeHandler:

    def __init__(self, parent, hex_id, time_delay, depth, group):

        self._output_list = []
        
        # Stores errors and warnings:
        self._error_msg_list = []

        self._hex_id = hex_id
        self._parent = parent
        self._time_delay = time_delay
        
        self._depth = depth             
        self._group = group             

        self._prev_msg_arrival = time.time()  # time when the previous message arrived


    def return_new_message(self, data):
        new_msg = self._give_output_message(data) + "\nTime of arrival: " + self.__timestamp()
        
        self._output_list.append(new_msg)
        if len(self._output_list) > 2:
            self._output_list.pop(0)

        # Check if message took too long to arrive
        if isinstance(self._time_delay, float):
            if time.time() - self._prev_msg_arrival > self._time_delay:  
                self.give_error("Message needed " + str(round(time.time() - self._prev_msg_arrival, 2)) + " seconds to arrive, expected max " + str(self._time_delay) + " seconds")
        self._prev_msg_arrival = time.time()

        if len(self._error_msg_list) > 50:
            self._error_msg_list.pop(0)

        return new_msg    
 
            
    # Data is an array of bytes
    # Only this method is overriden by the derived classes
    def _give_output_message(self, data):
        return str(data)


    def give_output(self):
        return self._output_list


    def return_errors(self):       
        return self._error_msg_list


    def return_can_group(self):
        return self._group


    def run_diagnostics(self, time_interval):
        if time.time() - self._prev_msg_arrival > time_interval:
            self.give_error("No message received for over " + str(time_interval) + " seconds")


    def give_error(self, error_msg):
        # Create timestamp to the error message  
        error_msg += "\nTime of error: " + self.__timestamp()

        self._error_msg_list.append([error_msg, "error"])
        if len(self._error_msg_list) > self._depth:
            self._error_msg_list.pop(0)
        self._parent.new_error(self._hex_id, error_msg)


    def give_warning(self, warning_msg):
        # Create timestamp to the warning message  
        warning_msg += "\nTime of warning: " + self.__timestamp()

        self._error_msg_list.append([warning_msg, "warning"])
        self._parent.new_warning(self._hex_id, warning_msg)    


    def __timestamp(self):
        hour = time.localtime(time.time()).tm_hour
        minute = time.localtime(time.time()).tm_min
        sec = time.localtime(time.time()).tm_sec

        hour_str = str(time.localtime(time.time()).tm_hour)
        minute_str = str(time.localtime(time.time()).tm_min)
        sec_str = str(time.localtime(time.time()).tm_sec)
        if hour < 10:
            hour_str = '0' + hour_str 
        if minute < 10:
            minute_str = '0' + minute_str
        if sec < 10:
            sec_str = '0' + sec_str

        return hour_str + ":" + minute_str + ":" + sec_str


    def is_msg_sent_once(self):   # Messages sent once have no time_delay
        return self._time_delay == '-'
        

    def reset(self):
        self._output_list = []
        self._error_msg_list = []
        self._prev_msg_arrival = time.time()
