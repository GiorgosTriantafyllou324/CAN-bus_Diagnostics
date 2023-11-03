import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.pack_propagate(False)
        self.__canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.__canvas.yview)
        #print(self.winfo_reqwidth(), scrollbar.winfo_reqwidth())
        self.__scrollable_frame = tk.Frame(self.__canvas, width = self.winfo_reqwidth() - scrollbar.winfo_reqwidth() - 2) # The offset -2 is added to make the frame look better

        self.__scrollable_frame.bind(
            "<Configure>",
            lambda e: self.__canvas.configure(
                scrollregion=self.__canvas.bbox("all")
            )
        )

        self.__canvas.create_window((0, 0), window=self.__scrollable_frame, anchor="nw")

        self.__canvas.configure(yscrollcommand=scrollbar.set)

        self.__canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.bind("<MouseWheel>", self.on_mousewheel)


    def on_mousewheel(self, event):
        self.__canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def return_inner_frame(self):
        return self.__scrollable_frame

    def return_canvas(self):
        return self.__canvas
