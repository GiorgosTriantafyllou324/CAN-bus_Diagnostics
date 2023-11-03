import tkinter as tk
from scrollable_frame import *

class DataPanel:
    def __init__(self, parent_class):
        self.__parent = parent_class # The reference to the caller class

        self.__fontsize = 12
        self.__back_color = "white"

        self.__selected = None


    def draw(self, parent_widget, _width, _height):
        self.__outer_frame = ScrollableFrame(parent_widget, width = _width, height = _height)
        self.__outer_frame.pack_propagate(False)

        self.__frame = self.__outer_frame.return_inner_frame()
        self.__canvas = self.__outer_frame.return_canvas()
        self.__canvas.config(bg = self.__back_color)

        self.__outer_frame.pack(side = tk.TOP)


    def append_data(self, data):
        try:
            if len(self.__frame.winfo_children()) == 0:
                f = tk.Frame(self.__frame, bg = self.__back_color, width = self.__frame.winfo_reqwidth(), height = 40, borderwidth = 1, relief = "solid")
                f.pack_propagate(False)
                f.bind("<MouseWheel>", self.scroll)

                l = tk.Label(f, text = str(data), padx = 30, bg = self.__back_color, font = ("Arial", self.__fontsize), justify = "left")
                l.pack(side = tk.LEFT)

            else:
                f = self.__frame.winfo_children()[0]
                l = f.winfo_children()[0]
            f.pack(side = tk.TOP)
            l.configure(text = str(data))
        except tk.TclError as e:
            pass


    def clear_panel(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()
        self.__frame.config(bg = self.__back_color) # Redraw color because it may have been deleted


    def scroll(self, event):
        self.__canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        

    def return_frame(self):
        return self.__outer_frame
