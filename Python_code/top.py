import tkinter as tk
import os

class Top:
    def __init__(self):
        self.__dcolor = "#383838"

    def draw(self, parent_widget):
        self.__top = tk.Frame(parent_widget, bg = self.__dcolor, width = parent_widget.winfo_reqwidth(), height = 40)
        self.__top.pack_propagate(False)
        
        self.__photo = tk.PhotoImage(file = os.getcwd() + "/" + "prom_racing_logo_resized.png") # You have to store it to a variable, because local variables are going to be deleted after end of function execution
        label = tk.Label(self.__top, bg = self.__dcolor, image = self.__photo)
        label.pack(side = tk.TOP)

        self.__top.pack(side = tk.TOP)


    def return_frame(self):
        return self.__top
