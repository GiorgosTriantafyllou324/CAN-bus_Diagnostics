import tkinter as tk
from scrollable_frame import *


class LabelExtended(tk.Label):   # Label extended stores text and the ID in hex, dec and bin form

    def __init__(self, parent, hex_id, dec_id, bin_id, node_name, *args, **kwargs):  
        super().__init__(parent, *args, **kwargs)
        self.__hex_id = hex_id
        self.__dec_id = dec_id
        self.__bin_id = bin_id
        self.__node_name = node_name

    def get_hex_id(self):
        return self.__hex_id

    def get_dec_id(self):
        return self.__dec_id

    def get_bin_id(self):
        return self.__bin_id

    def get_node_name(self):
        return self.__node_name

    


class IdPanel:

    def __init__(self, parent_class, mapping):

        self.number_system = '' # number system takes the values: HEX, DEC, BIN. 

        self.__parent = parent_class # The reference to the caller class

        self.__fontsize = 12
        self.__back_color = "white"
        self.__error_color = "#f51d1d"  # red

        self.__selected = None

        self.__map = mapping
        self.__frame = tk.Frame() # self.__frame needs to be initialized when an OptionsPanel object is created
        self.__id_has_error = {}  # Boolean


    def unselect(self):
        self.__selected = None


    def draw(self, parent_w, _width, _height):
        self.__outer_frame = ScrollableFrame(parent_w, width = _width, height = _height)
        self.__outer_frame.pack_propagate(False)

        self.__frame = self.__outer_frame.return_inner_frame()  
        self.__canvas = self.__outer_frame.return_canvas()
        self.__canvas.config(bg = "white")

        self.__outer_frame.pack(side = tk.LEFT)


    def return_frame(self):  
        return self.__frame    


    def clear_panel(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()
        self.__frame.config(bg = self.__back_color) # Redraw color because it may have been deleted

        self.__id_has_error.clear()


    def append_id(self, hex_id_str, dec_id_num, bin_id_num):
        self.__id_has_error[hex_id_str] = False
        
        f = tk.Frame(self.__frame, bg = self.__back_color, width = self.__frame.winfo_reqwidth(), height = 40, borderwidth = 1, relief = "solid")  
        f.pack_propagate(False)
        f.bind("<Enter>", self.mouseover)
        f.bind("<Leave>", self.mouseout)
        f.bind("<Button-1>", self.mouseclick)
        f.bind("<MouseWheel>", self.scroll)

        
        f.pack(side = tk.TOP)

        id_to_write = hex_id_str
        if hex_id_str in self.__map:
            if self.number_system == "HEX":
                label_text = self.__map[hex_id_str] + " (" + hex_id_str + ")"
            elif self.number_system == "DEC":
                label_text = self.__map[hex_id_str] + " (" + str(dec_id_num) + ")"
            else:  # Number system is binary
                label_text = self.__map[hex_id_str] + " (" + bin_id_num + ")"
                
        
        l = LabelExtended(f, hex_id = hex_id_str, dec_id = dec_id_num, bin_id = bin_id_num, node_name = self.__map[hex_id_str],
                          text = label_text, padx = 30, bg = self.__back_color, font = ("Arial", self.__fontsize))
        l.pack(side = tk.LEFT)

    def display_ids(self, mapping):
        for hex_id_str in mapping:
            dec_id_num = int(hex_id_str, 16)
            bin_id_str = bin(dec_id_num)[2:]
            self.append_id(hex_id_str, dec_id_num, bin_id_str)


    # Checks if the id of the new message is active in the window, so as to print the new data
    # Returns True is this id's window is active
    def is_id_window_active(self, hex_id):
        if self.__selected != None:
            try:
                if self.__selected.winfo_children()[0].get_hex_id() == hex_id:
                    return True
            except tk.TclError as e:
                 pass
        return False
    

    def mouseover(self, event):
        if event.widget != self.__selected:
            if self.__id_has_error[event.widget.winfo_children()[0].get_hex_id()]:
                event.widget.config(bg = "#ff8a8a")  # pink
                event.widget.winfo_children()[0].config(bg = "#ff8a8a")
            else:
                event.widget.config(bg = "#b3f0fc")  # light blue
                event.widget.winfo_children()[0].config(bg = "#b3f0fc")
    
    def mouseout(self, event):
        if event.widget != self.__selected:
            if self.__id_has_error[event.widget.winfo_children()[0].get_hex_id()]:
                event.widget.config(bg = self.__error_color)
                event.widget.winfo_children()[0].config(bg = self.__error_color)
            else:
                event.widget.config(bg = self.__back_color)
                event.widget.winfo_children()[0].config(bg = self.__back_color)


    def mouseclick(self, event):
        if self.__selected != None:
            if self.__id_has_error[self.__selected.winfo_children()[0].get_hex_id()]:
                self.__selected.config(bg = self.__error_color)
                self.__selected.winfo_children()[0].config(bg = self.__error_color)
            else:    
                self.__selected.config(bg = self.__back_color)
                self.__selected.winfo_children()[0].config(bg = self.__back_color)

        if self.__selected != None and self.__selected.winfo_children()[0].get_hex_id() != event.widget.winfo_children()[0].get_hex_id():
            self.__parent.clear_data_panel()
            self.__parent.clear_error_panel()

        if self.__selected != event.widget:                
            self.__parent.print_previous_data(event.widget.winfo_children()[0].get_hex_id())
            self.__parent.print_previous_errors(event.widget.winfo_children()[0].get_hex_id())

        if self.__id_has_error[event.widget.winfo_children()[0].get_hex_id()]:
            event.widget.config(bg = "#b80000") # dark red
            event.widget.winfo_children()[0].config(bg = "#b80000")
        else:    
            event.widget.config(bg = "#007991") # dark blue
            event.widget.winfo_children()[0].config(bg = "#007991")
        
        self.__selected = event.widget


    def scroll(self, event):
        self.__canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def handle_error(self, hex_id_str):
        
        for frame in self.__frame.winfo_children():
            try:
                if frame.winfo_children()[0].get_hex_id() == hex_id_str:
                    if self.__selected != frame and self.__id_has_error[hex_id_str] == False:
                        self.__id_has_error[hex_id_str] = True
                        frame.config(bg = self.__error_color)
                        frame.winfo_children()[0].config(bg = self.__error_color)
                    elif self.__id_has_error[hex_id_str] == False:
                        self.__id_has_error[hex_id_str] = True
                        frame.config(bg = "#b80000")   # dark red
                        frame.winfo_children()[0].config(bg = "#b80000")
            except tk.TclError as e:
                pass




        
