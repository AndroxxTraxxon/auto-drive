import tkinter as tk

class ResizingCanvas(tk.Canvas):

    def __init__(self, parent, highlightthickness=0, **kwargs):
        super().__init__(parent, highlightthickness=highlightthickness ,**kwargs)
        self.bind('<Configure>', self.on_configure)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_configure(self, event):

        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height

        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height = self.height)
        self.scale("all", 0,0,wscale, hscale)