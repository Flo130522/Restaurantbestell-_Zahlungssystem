import tkinter as tk
import pandas as pd
from tkinter import ttk

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Golden Seagull - Hauptmenü")

        self.menu = self.load_menu("speisekarte.csv")
        self.create_menu_ui()

    def load_menu(self, menu_file, encoding="utf-8"):
        menu = pd.read_csv(menu_file, encoding=encoding, index_col="ID")
        menu["Preis"] = menu["Preis"].map("{:.2f} €".format)
        pd.set_option('display.max_colwidth', None)
        menu_file = r"speisekarte.csv"
        return menu
    
    def create_menu_ui(self):
        self.menu_frame = ttk.LabelFrame(self.root, text="Speisekarte")
        self.menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.menu_tree = ttk.Treeview(self.menu_frame, columns=("Name", "Beschreibung", "Preis"))
        self.menu_tree.heading("#1", text="Name")
        self.menu_tree.heading("#2", text="Beschreibung")
        self.menu_tree.heading("#3", text="Preis")
        self.menu_tree.grid(row=0, column=0)

        for index, row in self.restaurant.menu.iterrows():
            self.menu_tree.insert("", "end", values=(row["Name"], row["Beschreibung"], row["Preis"]))

        self.menu_tree.bind("<ButtonRelease-1>", self.select_dish)