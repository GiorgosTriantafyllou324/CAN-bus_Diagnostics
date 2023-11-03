import tkinter as tk
from mapping import *
import time


class OptionsPanel:
    def __init__(self, parent_class):
        self.__parent_class = parent_class 

        self.__dcolor = "#383838"


    def draw(self, parent_widget, id_panel_class):
        self.__id_panel_class = id_panel_class
        
        self.__opt = tk.Frame(parent_widget, bg = self.__dcolor, width = parent_widget.winfo_reqwidth(), height = 60)
        self.__opt.columnconfigure([0, 1, 2, 3, 4, 5, 6], weight = 1)
        self.__opt.rowconfigure(0, weight = 1)
        self.__opt.pack_propagate(False)

        # Basic fuction of change_mapping_btn is to change the arguments of CANBusHandler Classes
        self.__change_mapping_btn = tk.Button(self.__opt, text = "Change Mapping", bg = "#ff6f21", font = ("Arial", 11), command = self.__parent_class.draw_map) 
        self.__change_mapping_btn.grid(row = 0, column = 0, pady = 10)

        #self.__logic_analyzer_btn = tk.Button(self.__opt, text = "Logic Analyzer", bg = "#ff6f21", font = ("Arial", 11), command = self.__parent_class.draw_logic_analyzer)
        #self.__logic_analyzer_btn.grid(row = 0, column = 1, pady = 10, sticky = "w")

        self.__hex_id_btn = tk.Button(self.__opt, text = "Hexadecimal ID", bg = "red", font = ("Arial", 11), command = self.draw_hex_id) 
        self.__hex_id_btn.grid(row = 0, column = 2, pady = 10, sticky = "e")
        
        self.__dec_id_btn = tk.Button(self.__opt, text = "Decimal ID", bg = "red", font = ("Arial", 11), command = self.draw_dec_id)  
        self.__dec_id_btn.grid(row = 0, column = 3, pady =10)

        self.__bin_id_btn = tk.Button(self.__opt, text = "Binary ID", bg = "red", font = ("Arial", 11), command = self.draw_bin_id) 
        self.__bin_id_btn.grid(row = 0, column = 4, pady = 10, sticky = "w")                                          

        self.__reset_btn = tk.Button(self.__opt, text = "Reset", bg = "#ff6f21", font = ("Arial", 11), command = self.__parent_class.reset)
        self.__reset_btn.grid(row = 0, column = 5, pady = 10, sticky = "e")

        self.__fullscreen_btn = tk.Button(self.__opt, text = "Exit", bg = "#ff6f21", font = ("Arial", 11))
        self.__fullscreen_btn.bind("<Button-1>", self.__parent_class.fullscreen)
        self.__fullscreen_btn.grid(row = 0, column = 6, pady = 10)
        
        self.__opt.pack(side = tk.TOP, fill = "both")


    def change_fs_btn_text(self, is_fullscreen):
        if is_fullscreen:
            self.__fullscreen_btn.configure(text = "Exit")
        else:
            self.__fullscreen_btn.configure(text = "Fullscreen")


    def draw_hex_id(self):                  
        if self.__id_panel_class.number_system != "HEX":  
            self.__hex_id_btn.configure(bg = "yellow")
            self.__dec_id_btn.configure(bg = "red")
            self.__bin_id_btn.configure(bg = "red")
            self.__id_panel_class.number_system = "HEX"  
            frames_list = self.__id_panel_class.return_frame().winfo_children()             
            for i in range(len(frames_list)):
                label = frames_list[i].winfo_children()[0] # label is LabelExtended
                hex_id = label.get_hex_id()
                node_name = label.get_node_name()
                label.config(text = node_name + " (" + hex_id + ")")
        

    def draw_dec_id(self):                  
        if self.__id_panel_class.number_system != "DEC":  
            self.__hex_id_btn.configure(bg = "red")
            self.__dec_id_btn.configure(bg = "yellow")
            self.__bin_id_btn.configure(bg = "red")
            self.__id_panel_class.number_system = "DEC"  

            frames_list = self.__id_panel_class.return_frame().winfo_children()         
            for i in range(len(frames_list)):
                label = frames_list[i].winfo_children()[0] # label is LabelExtended
                dec_id = label.get_dec_id()
                node_name = label.get_node_name()
                label.config(text = node_name + " (" + str(dec_id) + ")")
            

    def draw_bin_id(self):                       
        if self.__id_panel_class.number_system != "BIN":  
            self.__hex_id_btn.configure(bg = "red")
            self.__dec_id_btn.configure(bg = "red")
            self.__bin_id_btn.configure(bg = "yellow")
            self.__id_panel_class.number_system = "BIN" 

            frames_list = self.__id_panel_class.return_frame().winfo_children()          
            for i in range(len(frames_list)):
                label = frames_list[i].winfo_children()[0] # label is LabelExtended
                bin_id = label.get_bin_id()
                node_name = label.get_node_name()
                label.config(text = node_name + " (" + bin_id + ")")


    def return_frame(self):
        return self.__opt

            
