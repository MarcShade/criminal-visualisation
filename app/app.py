import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from visualisations import Plot


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x1000")
        self.title("Criminality Visualisation")

        self.plot = Plot()

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

        self.bottom_bar = tk.Frame(self, bg="#2b2b2b", height=80)
        self.bottom_bar.pack_propagate(False)

        self.hist_option = tk.StringVar(value="Weight")

        self.hist_dropdown_btn = tk.Button(
            self.bottom_bar,
            textvariable=self.hist_option,
            font=("Segoe UI", 11, "bold"),
            bg="#3c3f41",
            fg="white",
            activebackground="#4b6eaf",
            activeforeground="white",
            relief="flat",
            bd=0,
            width=16,
            height=2,
            command=self.show_hist_menu
        )
        self.hist_dropdown_btn.pack(pady=20)

        self.hist_menu = tk.Menu(
            self,
            tearoff=0,
            bg="#3c3f41",
            fg="white",
            activebackground="#4b6eaf",
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 11)
        )

        for option in [
            "Weight",
            "Nationality",
            "Sex",
            "Country of Birth",
            "Languages Spoken",
            "Height",
            "Eye color"
        ]:
            self.hist_menu.add_command(
                label=option,
                command=lambda v=option: self.set_hist_option(v)
            )


        self.show_histogram()
        self.mainloop()

    def clear_plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def show_histogram(self):
        self.clear_plot()
        self.bottom_bar.pack(side="bottom", fill="x")


        selected = self.hist_option.get()
        fig = self.plot.make_histogram(selected)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_world(self):
        self.clear_plot()
        self.bottom_bar.pack_forget()

        fig = self.plot.make_world_map()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_hist_menu(self):
        x = self.hist_dropdown_btn.winfo_rootx()
        y = self.hist_dropdown_btn.winfo_rooty() + self.hist_dropdown_btn.winfo_height()
        self.hist_menu.tk_popup(x, y)

    def set_hist_option(self, value):
        self.hist_option.set(value)
        self.show_histogram()

