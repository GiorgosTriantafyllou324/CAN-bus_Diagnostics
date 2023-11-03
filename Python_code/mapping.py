import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

from general_programmer_class import *
import sys
sys.path.append(os.getcwd() + "/" + "CAN_Node_Handler_Classes")
from APPS import *   
from Brake import *



class MappingException(Exception):
    pass



class Mapping:
    def __init__(self, parent_class):
        self.__parent_class = parent_class   # parent_class is App()
        
        self.__dcolor = "#383838"
        
        self.__id_class_handlers = {}  
        self.__mapping = {}
        

    def draw(self, parent_w):
        _width = parent_w.winfo_reqwidth()
        _height = parent_w.winfo_reqheight()

        self.__map_fr = tk.Frame(parent_w, bg = self.__dcolor, width = _width, height = _height)       
        self.__map_fr.pack_propagate(False)
        
        self.__map_top_frame = tk.Frame(self.__map_fr, bg = self.__dcolor, width = _width, height = 50)
        self.__map_top_frame.columnconfigure([0, 1, 2], weight = 1)
        self.__map_top_frame.rowconfigure(0, weight = 1)
        self.__map_top_frame.pack_propagate(False)

        self.__apply_btn = tk.Button(self.__map_top_frame, text = "Apply", bg = "#ff6f21", font = ("Arial", 13), command = self.__apply)
        self.__apply_btn.grid(row = 0, column = 0, pady = 10)

        self.__map_title = tk.Label(self.__map_top_frame, bg = self.__dcolor, text = "Chage mapping / sensor parameters", fg = "white", font = ("Arial", 16))
        self.__map_title.grid(row = 0, column = 1, pady = 10)

        self.__exit_btn = tk.Button(self.__map_top_frame, text = "Exit", bg = "#ff6f21", font = ("Arial", 13), command = self.__exit)
        self.__exit_btn.grid(row = 0, column = 2, pady = 10)

        self.__map_top_frame.pack(side = tk.TOP, fill = "both")

        #this label displays the syntax error messages 
        self.__error_frame = tk.Frame(self.__map_fr, bg = self.__dcolor, width = _width, height = 50)
        self.__error_frame.pack_propagate(False)
        self.__error_label = tk.Label(self.__error_frame, bg = self.__dcolor, fg = "red", text = "", font = ("Arial", 16))
        self.__error_label.pack(side = tk.TOP)
        self.__error_frame.pack(side = tk.TOP)

        horizontal_scrollbar = tk.Scrollbar(self.__map_fr, orient = 'horizontal')
        vertical_scrollbar = tk.Scrollbar(self.__map_fr, orient = 'vertical')

        horizontal_scrollbar.pack(side = tk.BOTTOM, fill = 'x')
        vertical_scrollbar.pack(side = tk.RIGHT, fill = 'y')
        
        self.__text = tk.Text(self.__map_fr, wrap = tk.NONE, width = 40, height = 10,
                              xscrollcommand = horizontal_scrollbar.set,
                              yscrollcommand = vertical_scrollbar.set, bd = 20,
                              font = ("Arial",12), bg = "black", fg = "white")       
        self.__text.config(insertbackground = "red")
        self.__text.pack(fill = "both", expand = True)

        horizontal_scrollbar.config(command = self.__text.xview)
        vertical_scrollbar.config(command = self.__text.yview)

        #Load the mapping file
        with open(os.getcwd() + "/" + "mapping_txt.txt", "r") as input_file:
            text = input_file.read()
            self.__text.insert(tk.END, text)


        self.__map_fr.pack(side = tk.TOP, fill = "both")     
        
        
    def __exit(self):
        self.__parent_class.reset() 
        self.__parent_class.exit_mapping()


    def __apply(self):

        # try to make mapping and check for syntax errors
        try:
            # mapping from the text widget
            self.make_mapping(self.__text.get(1.0, tk.END)) 

            # save the changes
            with open(os.getcwd() + "/" + "mapping_txt.txt", "w") as output_file:
                text_output = self.__text.get(1.0, tk.END)
                if text_output[-1] == "\n":
                    text_output = text_output[:-1] # if the last character is \n, remove it
                output_file.write(text_output)
                output_file.close()

            # resets so the new changes will be applied  
            self.__parent_class.reset()

            self.__parent_class.exit_mapping()

        except MappingException as e:
            self.__error_label.config(text = "ERROR: " + str(e))


    def make_mapping(self, text):

        # First it checks for syntax errors
        lines = text.splitlines()  # lines is an array of lines
        line_counter = 1           # helps to spot syntax errors when exception is raised
        for line in lines:
            hex_str_id = ""
            node_str = ""
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.replace('\t', '')

            # Comments can be made using '#'
            i = line.find('#')
            if i != -1:       #  '#' symbol was found at the line
                line = line[:i]

            if line == "":
                line_counter += 1
                continue
            if ':' not in line:
                raise MappingException("Forgot ':' in line " + str(line_counter))    
            i = 0
            while line[i] != ":":
                hex_str_id += line[i]
                i += 1
            i += 1
            hex_str_id = hex_str_id.lower()
            if hex_str_id[0:2] != '0x':
                raise MappingException("ID should start with '0x' in line " + str(line_counter))
            try:
                int(hex_str_id[2:], 16)
            except ValueError:
                raise MappingException("Expected hexadecimal after '0x' in line " + str(line_counter))

            if ',' not in line:
                raise MappingException("Forgot ',' in line " + str(line_counter))
            while line[i] != ',':
                i += 1
            i += 1
            line_remaining = line[i:]

            time_delay = self.__find_num_value(line_remaining, "time delay", line_counter) # finds the value of float time delay in string: line
            depth = self.__find_num_value(line_remaining, "depth", line_counter)
            group = self.__find_string_value(line_remaining, "CAN group", line_counter)    # finds the value of string CAN group in: line
            if not (depth).is_integer():
                raise MappingException("depth must be integer, in line " + str(line_counter))
            if depth <= 0:
                raise MappingException("depth must be positive, in line " + str(line_counter))
            if isinstance(time_delay, float) and time_delay <= 0: # time_delay might be '-' 
                raise MappingException("time delay must be >0, in line " + str(line_counter))
            if group == '':
                raise MappingException("CAN group is blank, in line " + str(line_counter))

            line_counter += 1  
        
        # Then it creates the mapping
        self.__mapping.clear()
        line_counter = 1      # helps to spot syntax errors when exception is raised
        for line in lines:
            hex_str_id = ""
            node_str = ""
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.replace('\t', '')

            # Comments can be made using '#'
            i = line.find('#')
            if i != -1:       #  '#' symbol was found at the line
                line = line[:i]

            if line == "":
                line_counter += 1
                continue
   
            i = 0
            while line[i] != ":":
                hex_str_id += line[i]
                i += 1
            i += 1
            hex_str_id = hex_str_id.lower()

            while line[i] != ',':
                node_str += line[i]
                i += 1
            i += 1
            line_remaining = line[i:]

            time_delay = self.__find_num_value(line_remaining, "time delay", line_counter) # finds the value of float time delay in string: line
            depth = self.__find_num_value(line_remaining, "depth", line_counter)
            group = self.__find_string_value(line_remaining, "CAN group", line_counter)    # finds the value of string CAN group in: line

            self.__mapping[hex_str_id] = node_str

            # if a CanNodeHandler class has already been instantiated, it is destroyed automatically before a new one is created
            if hex_str_id == "0x301":
                self.__id_class_handlers[hex_str_id] = APPS(self.__parent_class, hex_str_id, time_delay, depth, group)
            elif hex_str_id == "0x303":
                self.__id_class_handlers[hex_str_id] = Brake(self.__parent_class, hex_str_id, time_delay, depth, group)
            else:    
                self.__id_class_handlers[hex_str_id] = CANNodeHandler(self.__parent_class, hex_str_id, time_delay, depth, group) # Create a new instance of the handler

            line_counter += 1
        

    def __find_string_value(self, line, string, line_counter):
        substring = string.replace(' ', '')
        substring = substring.replace('\t', '')
        if substring not in line:
            raise MappingException("No " + string + " in line " + str(line_counter))
        i = line.find(substring)
        i += len(substring)
        if len(line) <= i or line[i] != '=':
            raise MappingException("No '=' after " + string + " in line " +str(line_counter))
        i += 1
        if len(line) <= i:
            raise MappingException("No value after " + string + " in line " + str(line_counter))
        rest_of_the_line = line[i:]
        if ',' not in rest_of_the_line:
            raise MappingException("Forgot ',' after " + string + " in line " + str(line_counter))
        string_value = ""
        while line[i] != ',':
            string_value += line[i]
            i += 1
        return string_value

            
    def __find_num_value(self, line, string, line_counter):
        try:
            string_value = self.__find_string_value(line, string, line_counter)
            if string.replace(' ', '').replace('\t', '') == 'timedelay' and string_value == '-':  # if a message is only sent once, a dash is used in time delay
                return '-'
            float_value = float(string_value)
        except ValueError:
            if string.replace(' ', '').replace('\t', '') == 'timedelay':
                raise MappingException("No '-' or unable to convert " + string_value + " to float after time delay in line " + str(line_counter))
            raise MappingException("Cannot convert " + string_value + " to float in line " + str(line_counter))

        return float_value


    def return_id_class_handlers(self):
        return self.__id_class_handlers


    def return_mapping(self):
        return self.__mapping


    def reset_class_handlers(self):
        for i in self.__id_class_handlers:
            self.__id_class_handlers[i].reset()

