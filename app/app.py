import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from visualisations import Plot

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x1000")
        self.resizable(False, False)
        self.title("Criminality Visualisation")

        self.top_bar = tk.Frame(self, bg="#2b2b2b", height=120)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        btn_style = {
            "font": ("Segoe UI", 11, "bold"),
            "bg": "#3c3f41",
            "fg": "white",
            "activebackground": "#4b6eaf",
            "activeforeground": "white",
            "relief": "flat",
            "bd": 0,
            "width": 16,
            "height": 2
        }

        self.button_container = tk.Frame(self.top_bar, bg="#2b2b2b")
        self.button_container.pack(expand=True)

        self.btn_hist = tk.Button(
            self.button_container,
            text="Histogram",
            command=self.show_histogram,
            **btn_style
        )
        self.btn_hist.grid(row=0, column=0, padx=40)

        self.btn_world = tk.Button(
            self.button_container,
            text="World",
            command=self.show_world,
            **btn_style
        )
        self.btn_world.grid(row=0, column=1, padx=40)

        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True)

        self.show_histogram()
        self.mainloop()

    def clear_plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def show_histogram(self):
        self.clear_plot()
        plot = Plot()
        fig = plot.make_histogram("weight")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_world(self):
        self.clear_plot()
        label = ttk.Label(
            self.plot_frame,
            text="WORLD GRAPH GOES HERE",
            font=("Segoe UI", 18)
        )
        label.pack(expand=True)
