import tkinter as tk
from tkinter import ttk
from tkinter import *
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from visualisations import Plot

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.open_apps = {}

        self.geometry('1000x1000')
        self.resizable(0, 0)
        self.title("Criminality Visualisation")

        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True)


        self.show_plot()
        self.mainloop()


    def show_plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # fig = Plot.make_example_plot("Age")
        fig = Plot.make_histogram("")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()

        canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        toolbar.pack()