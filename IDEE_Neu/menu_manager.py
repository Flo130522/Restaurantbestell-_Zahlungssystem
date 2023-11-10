import tkinter as tk
from tkinter import ttk
import pandas as pd

class MenuManager:
    def __init__(self, root, menu_file="speisekarte.csv"):
        self.root = root
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

        if not hasattr(self, 'menu_tree'):
            self.menu_tree = ttk.Treeview(self.menu_frame, columns=("Name", "Beschreibung", "Preis"))
            self.menu_tree.heading("#1", text="Name")
            self.menu_tree.heading("#2", text="Beschreibung")
            self.menu_tree.heading("#3", text="Preis")
            self.menu_tree.grid(row=0, column=0)

            for index, row in self.menu.iterrows():
                self.menu_tree.insert("", "end", values=(index, row["Name"], row["Beschreibung"], row["Preis"]))

            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Arial", 14))  # Schriftgröße für Überschriften
            style.configure("Treeview", font=("Arial", 11))  # Schriftgröße für den Inhalt

            self.menu_tree.tag_configure("Beschreibung", font=("Arial", 11))  # Schriftgröße für die Spalte "Beschreibung"

            self.menu_tree.column("#2", width=300, anchor="center")  # Breite der Beschreibung anpassen
            self.menu_tree.column("#3", width=100, anchor="center")  # Breite der Preis-Spalte anpassen
            self.menu_tree.column("#3", anchor="center")  # Preis zentrieren

            self.menu_tree.bind("<Double-1>", self.add_to_cart)

        if not hasattr(self, 'order_button'):
            self.order_button = ttk.Button(self.menu_frame, text="Jetzt bestellen", command=self.place_order)
            self.order_button.grid(row=1, column=0, pady=5)

        # Warenkorb-Anzeige
        self.cart_frame = ttk.LabelFrame(self.root, text="Warenkorb")
        self.cart_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.cart_text = tk.Text(self.cart_frame, height=10, width=40, wrap=tk.WORD)
        self.cart_text.grid(row=1, column=0, padx=5, pady=5)

        self.total_label = tk.Label(self.cart_frame, text="Gesamtsumme: 0.00 €")
        self.total_label.grid(row=2, column=0, padx=5, pady=5)
        pass

    def add_to_cart(self, event):
        if self.selected_dish:
            dish_id = self.selected_dish["ID"]
            print(f"Adding dish to cart: {dish_id}")
            if dish_id in self.cart:
                self.cart[dish_id] += 1
            else:
                self.cart[dish_id] = 1
            print(f"Cart after adding: {self.cart}")
            self.update_invoice()
            pass

    def update_invoice(self):
        invoice = self.generate_invoice()
        self.cart_text.delete(1.0, "end")
        self.cart_text.insert("end", invoice)

        total_price = sum(
            self.menu.loc[dish_id, "Preis"] * quantity
            for dish_id, quantity in self.cart.items()
        )
        self.total_label.config(text=f"Gesamtsumme: {total_price:.2f} €")
        pass

    def generate_invoice(self):
        total = 0
        invoice_text = ""
        for dish_id, quantity in self.cart.items():
            dish_data = self.menu_tree.item(dish_id, "values")
            name = dish_data[0]
            beschreibung = dish_data[1]
            preis = dish_data[2]
            total += float(preis.split(" €")[0]) * quantity
            invoice_text += f"{name} x{quantity}: {beschreibung} ({preis})\n"

        net_price = total
        tax_rate = 0.19
        tax_amount = total * tax_rate
        total_price = total + tax_amount
        if self.tip_percentage > 0:
            total_price += self.tip_percentage

        invoice_text += "-----------------------------\n"
        invoice_text += f"Gesamtpreis: {total:.2f} €\n"
        invoice_text += f"Trinkgeld: {self.tip_percentage:.2f} €\n"
        invoice_text += f"Nettopreis: {net_price:.2f} €\n"
        invoice_text += f"MwSt.: {tax_amount:.2f} €\n"
        invoice_text += f"Bruttopreis: {total_price:.2f} €"

        return invoice_text
    pass
