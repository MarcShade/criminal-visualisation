import tkinter as tk
from tkinter import *
from tkinter import messagebox

class App:
    def __init__(self):
        self.open_apps = {}

        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.title("Criminality Visualisation")

        self.button_frame = tk.Frame(self.root, width=1000, height=800)

        for btn in self.button_frame.winfo_children():
            btn.pack(pady=5, fill=X)

        for frame in self.root.winfo_children():
            frame.pack(padx=45, pady=30)

        self.root.mainloop()