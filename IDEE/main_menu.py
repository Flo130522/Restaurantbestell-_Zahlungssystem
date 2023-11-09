import tkinter as tk
from tkinter import ttk
import pandas as pd

class MainMenu:
    def __init__(self, root, menu_file="speisekarte.csv"):
        self.root = root
        self.root.title("Golden Seagull - Hauptmenü")
        self.menu = self.load_menu(menu_file)
        self.create_menu_ui()

    def load_menu(self, menu_file, encoding="utf-8"):
        try:
            menu = pd.read_csv(menu_file, encoding=encoding, index_col="ID")
            menu["Preis"] = menu["Preis"].map("{:.2f} €".format)
            pd.set_option('display.max_colwidth', None)
            return menu
        except FileNotFoundError:
            print(f"Die Datei '{menu_file}' wurde nicht gefunden.")
            return pd.DataFrame()

    def create_menu_ui(self):
        self.menu_frame = ttk.LabelFrame(self.root, text="Speisekarte")
        self.menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.menu_tree = ttk.Treeview(self.menu_frame, columns=("Name", "Beschreibung", "Preis"))
        self.menu_tree.heading("#1", text="Name")
        self.menu_tree.heading("#2", text="Beschreibung")
        self.menu_tree.heading("#3", text="Preis")
        self.menu_tree.grid(row=0, column=0)

        for index, row in self.menu.iterrows():
            self.menu_tree.insert("", "end", values=(row["Name"], row["Beschreibung"], row["Preis"]))

        # Ändern Sie hier die Schriftgröße für den gesamten Treeview (aller Spalten)
        self.menu_tree.configure(font=("Arial", 11))

        self.menu_tree.bind("<ButtonRelease-1>", self.select_dish)

    def select_dish(self, event):
        selected_item = self.menu_tree.selection()
        if selected_item:
            item_values = self.menu_tree.item(selected_item[0], "values")
            # Hier können Sie die ausgewählte Speise verarbeiten, z.B., Bestellung hinzufügen.

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()
