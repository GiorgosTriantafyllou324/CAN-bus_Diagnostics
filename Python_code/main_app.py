import tkinter as tk
import time
from id_panel import *
from data_panel import *
from error_panel import *
from top import *
from options_panel import *
from mapping import *
from general_programmer_class import *
import os

import platform
import subprocess
#if platform.system() == 'Linux':
#    subprocess.run('sudo ip link set can0 up type can bitrate 1000000')
from can_reader import *



class App:
    def __init__(self):
        
        self.__ids_encountered = {}

        self.__can_group = ''
        self.__last_error_check = time.time()
        
        self.__root = tk.Tk()
        self.__fullscreen = True
        self.__root.attributes("-fullscreen", True)
        self.__root.title("Can diagnostics")
        self.__root.bind("<Escape>", self.fullscreen)
        self.__root.update() # It is needed for the correct calculations of dimensions

        self.__started = False

        # Initialization of all the classes needed
        self.__top = Top()
        self.__map = Mapping(self)
        self.__id_panel = IdPanel(self, self.__map.return_mapping())
        self.__options_panel = OptionsPanel(self)
        self.__data_panel = DataPanel(self)
        self.__error_panel = ErrorPanel(self)


        # Mapping process
        file = open(os.getcwd() + "/" + "mapping_txt.txt", "r")
        self.__map.make_mapping(file.read())    
        file.close()

        self.__draw_main()

        self.__root.mainloop()

    def __draw_main(self):
        
        self.__main = tk.Frame(self.__root, bg = "#383838", width = self.__root.winfo_width(), height = self.__root.winfo_height())
        self.__main.pack_propagate(False)

        # Create the logo
        self.__top.draw(self.__main)

        # Create the options panel
        self.__options_panel.draw(self.__main, self.__id_panel)
        self.__options_panel.draw_hex_id()
        self.__options_panel.change_fs_btn_text(self.__fullscreen)

        # Create the CAN group label
        self.__can_group_label = tk.Label(self.__main, font = ("Arial", 15),
                                            width = self.__main.winfo_reqwidth(), bg = "#383838", fg = "#ff6f21")
        self.__can_group_label.pack(side = tk.TOP)

        # Create the Id panel - data panel - error panel
        _height = self.__main.winfo_reqheight() - self.__top.return_frame().winfo_reqheight() - self.__options_panel.return_frame().winfo_reqheight() - self.__can_group_label.winfo_reqheight() - 5
        self.__panels_fr = tk.Frame(self.__main, width = self.__main.winfo_reqwidth() - 50, height = _height)
        self.__panels_fr.pack_propagate(False)
        self.__panels_fr.pack(side = tk.TOP)
            
        self.__id_panel.draw(self.__panels_fr, round(self.__panels_fr.winfo_reqwidth() * 2/5), self.__panels_fr.winfo_reqheight())
        self.__id_panel.display_ids(self.__map.return_mapping())
            
        # right_fr is the frame of the data and error panel    
        self.__right_fr = tk.Frame(self.__panels_fr, width = round(self.__panels_fr.winfo_reqwidth() *3/5), height = self.__panels_fr.winfo_reqheight())
        self.__right_fr.pack_propagate(False)
        self.__right_fr.pack(side  = tk.LEFT)

        self.__message_label = tk.Label(self.__right_fr, width = self.__right_fr.winfo_reqwidth(), height = 1,
                                          fg = "white", bg = "#1f1f1c", text = "Message:", font = ("Arial", 13))
        self.__message_label.pack(side = tk.TOP)

        self.__data_panel.draw(self.__right_fr, self.__right_fr.winfo_reqwidth(), _height = 100) # Testing

        self.__error_label = tk.Label(self.__right_fr, width = self.__right_fr.winfo_reqwidth(), height = 1,
                                          fg = "white", bg = "#1f1f1c", text = "Errors / Warnings:", font = ("Arial", 13))
        self.__error_label.pack(side = tk.TOP)

        error_height = self.__right_fr.winfo_reqheight() - self.__data_panel.return_frame().winfo_reqheight() - self.__error_label.winfo_reqheight() - self.__message_label.winfo_reqheight()                
        self.__error_panel.draw(self.__right_fr, _width = self.__right_fr.winfo_reqwidth(), _height = error_height)

        self.__main.pack(side = tk.TOP)

        # Start CAN bus
        if not self.__started:
            thread_ = CANBusHandler(self)
            thread_.start()
            self.__started = True


    
    def draw_map(self):
        self.__main.pack_forget()
        
        self.__map_main = tk.Frame(self.__root, bg = "#383838", width = self.__root.winfo_width(), height = self.__root.winfo_height())
        self.__map_main.pack_propagate(False)

        # Create the logo
        self.__top = Top()
        self.__top.draw(self.__map_main)

        # Create the map frame
        _height = self.__map_main.winfo_reqheight() - self.__top.return_frame().winfo_reqheight() - 25
        self.__map_fr = tk.Frame(self.__map_main, width = self.__map_main.winfo_reqwidth() - 50, height = _height)
        self.__map_fr.pack_propagate(False)
          
        self.__map.draw(self.__map_fr) 

        self.__map_fr.pack(side = tk.TOP)

        self.__map_main.pack(side = tk.TOP)


    def new_msg(self, msg):
        hex_id_str = hex(msg.get_dec_id())
        data = msg.get_data()
        
        if hex_id_str in self.__map.return_mapping() and hex_id_str not in self.__ids_encountered:
            self.__ids_encountered[hex_id_str] = []
            self.__ids_encountered[hex_id_str].append(data)

        # If a mistake has been made in mapping:
        if hex_id_str not in self.__map.return_mapping():
            self.__map.return_mapping()[hex_id_str] = "????"
            self.__map.return_id_class_handlers()[hex_id_str] = CANNodeHandler(self, hex_id_str, time_delay = 1, depth = 5, group = '')
            self.__id_panel.append_id(hex_id_str, int(hex_id_str, 16), bin(int(hex_id_str, 16)))
            self.__map.return_id_class_handlers()[hex_id_str].give_error("Node with id: " + hex_id_str + " was not found in mappping file")
            
        # Handle new message: send the new data to the class handler
        new_msg = self.__map.return_id_class_handlers()[hex_id_str].return_new_message(data)
        if self.__id_panel.is_id_window_active(hex_id_str):
            self.__data_panel.append_data(new_msg)

        # Define the CAN bus group of the sensors
        if self.__can_group == '':
            self.__can_group = self.__map.return_id_class_handlers()[hex_id_str].return_can_group()
            self.__can_group_label.config(text = "CAN Group: " + self.__can_group)
        elif self.__can_group != self.__map.return_id_class_handlers()[hex_id_str].return_can_group():
            if self.__map.return_id_class_handlers()[hex_id_str].return_can_group() == '':    # Node is not in mapping file
                self.__map.return_id_class_handlers()[hex_id_str].give_error("Node with id: " + hex_id_str + " was not found in mappping file")
            else:    
                self.__map.return_id_class_handlers()[hex_id_str].give_error("CAN group of " + hex_id_str + " (" + self.__map.return_id_class_handlers()[hex_id_str].return_can_group() + ") is not " + self.__can_group)
        

        # Run diagnostics every time_interval = 2s
        time_interval = 2
        if time.time() - self.__last_error_check > time_interval:
            for i in list(self.__map.return_id_class_handlers()):
                if self.__map.return_id_class_handlers()[i].return_can_group() == self.__can_group:
                    if not self.__map.return_id_class_handlers()[i].is_msg_sent_once():  # not all messages are sent continuously
                        self.__map.return_id_class_handlers()[i].run_diagnostics(time_interval)
            self.__last_error_check = time.time()

      


    def new_error(self, str_hex_id, error_msg):
        self.__id_panel.handle_error(str_hex_id)
        if self.__id_panel.is_id_window_active(str_hex_id):
           self.__error_panel.append_error(error_msg)


    def new_warning(self, str_hex_id, warning_msg):
        self.__id_panel.handle_error(str_hex_id)
        if self.__id_panel.is_id_window_active(str_hex_id):
           self.__error_panel.append_warning(warning_msg)        
  

    def exit_mapping(self):
        self.__map_main.destroy()        
        self.__id_panel.number_system = ''
        self.__draw_main()
    
    
    def clear_data_panel(self):
        self.__data_panel.clear_panel()


    def clear_error_panel(self):
        self.__error_panel.clear_panel()
        

    def __clear_id_panel(self):
        self.__id_panel.clear_panel()
        self.__ids_encountered.clear()



    def __clear_unmapped_ids(self):
        map_dict = self.__map.return_mapping()
        map_dict = {k: v for k, v in map_dict.items() if v  != '????'}


    def print_previous_data(self, id_num):
        output = self.__map.return_id_class_handlers()[id_num].give_output()
        if len(output) > 0:
            self.__data_panel.append_data(output[0])


    def print_previous_errors(self, id_num):
        errors = self.__map.return_id_class_handlers()[id_num].return_errors()
        for i in range(len(errors)):
            if errors[i][1] == "error":
                self.__error_panel.append_error(errors[i][0])
            else:
                self.__error_panel.append_warning(errors[i][0])
                if errors[i][1] != "warning":  # TESTING 
                    raise Exception(errors[i][1] + " is not warning")

    def fullscreen(self, event):
        if self.__fullscreen:
            self.__root.attributes("-fullscreen", False)
            self.__root.geometry("800x500")
            self.__options_panel.change_fs_btn_text(False)
            self.__fullscreen = False
        else:
            self.__root.attributes("-fullscreen", True)
            self.__options_panel.change_fs_btn_text(True)
            self.__fullscreen = True


    def reset(self):   
        self.__map.reset_class_handlers()
        self.__clear_unmapped_ids()
        self.clear_data_panel() 
        self.__clear_id_panel()
        self.clear_error_panel()
        self.__last_error_check = time.time()
        self.__can_group = ''
        self.__id_panel.display_ids(self.__map.return_mapping())
        self.__can_group_label.config(text = "")
        self.__id_panel.unselect()




app = App()
