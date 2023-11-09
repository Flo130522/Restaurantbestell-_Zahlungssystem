# region Modulimporte
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import pandas as pd
from datetime import datetime
# endregion Modulimporte

class MainMenu:
    def __init__(self, root, menu_file="speisekarte.csv"):
        self.root = root
        self.root.title("Golden Seagull - Hauptmenü")
        self.menu = self.load_menu(menu_file)
        self.create_menu_ui()
        self.tischnummer = None
        self.tip_percentage = 0  
        self.order_items = {}
        self.cart = {}
        self.cart_frame = ttk.LabelFrame(self.root, text="Warenkorb")
        self.cart_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.order_button = ttk.Button(self.cart_frame, text="Bestellen", command=self.place_order)
        self.order_button.grid(row=0, column=0, pady=5)
    
    def ask_tip_percentage(self):
        options = ["5%", "10%", "15%", "Eigener Betrag"]
        result = simpledialog.askstring("Trinkgeld", "Wählen Sie den Trinkgeldbetrag:", initialvalue="5%", parent=self.root, options=options)
        
        if result == "Eigener Betrag":
            custom_tip = simpledialog.askfloat("Trinkgeld", "Geben Sie den gewünschten Trinkgeldbetrag ein:", parent=self.root)
            if custom_tip is not None:
                self.tip_percentage = custom_tip / 100
            else:
                self.tip_percentage = 0
        elif result:
            self.tip_percentage = float(result.strip('%')) / 100
        else:
            self.tip_percentage = 0
        
        self.generate_invoice()

    def load_menu(self, menu_file, encoding="utf-8"):
        try:
            menu = pd.read_csv(menu_file, encoding=encoding, index_col="ID")
            menu["Preis"] = menu["Preis"].map("{:.2f} €".format)
            pd.set_option('display.max_colwidth', None)  # Beschreibung vollständig anzeigen
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

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14))  # Schriftgröße für Überschriften
        style.configure("Treeview", font=("Arial", 11))  # Schriftgröße für den Inhalt

        self.menu_tree.tag_configure("Beschreibung", font=("Arial", 11))  # Schriftgröße für die Spalte "Beschreibung"

        self.menu_tree.column("#2", width=300, anchor="center")  # Breite der Beschreibung anpassen
        self.menu_tree.column("#3", width=100, anchor="center")  # Breite der Preis-Spalte anpassen
        self.menu_tree.column("#3", anchor="center")  # Preis zentrieren

        self.menu_tree.bind("<ButtonRelease-1>", self.select_dish)

    def create_order_ui(self):
        self.order_frame = ttk.LabelFrame(self.root, text="Bestellung")
        self.order_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.selected_dish = None

    def select_dish(self, event):
        selected_item = self.menu_tree.selection()
        if selected_item:
            item_values = self.menu_tree.item(selected_item[0], "values")
            self.selected_dish = {
                "ID": selected_item[0],
                "Name": item_values[0],
                "Beschreibung": item_values[1],
                "Preis": float(item_values[2].replace(" €", ""))
            }

    def add_to_cart(self):
        if self.selected_dish:
            dish_id = self.selected_dish["ID"]
            if dish_id in self.cart:
                self.cart[dish_id] += 1
            else:
                self.cart[dish_id] = 1
            self.update_invoice()

    def remove_from_cart(self):
        if self.selected_dish:
            dish_id = self.selected_dish["ID"]
            if dish_id in self.cart:
                if self.cart[dish_id] > 1:
                    self.cart[dish_id] -= 1
                else:
                    del self.cart[dish_id]
                self.update_invoice()

    def place_order(self):
        if self.cart:
            for dish_id, quantity in self.cart.items():
                # Erstellen Sie die Bestellung und fügen Sie sie zur Gesamtbestellung hinzu
                order = self.create_order(dish_id, quantity)
                if order:
                    self.orders = pd.concat([self.orders, order], ignore_index=True)
            
            # Leeren Sie den Warenkorb
            self.cart = {}
            self.update_invoice()

    def update_invoice(self):
        invoice = self.generate_invoice()
        self.invoice_text.delete(1.0, "end")
        self.invoice_text.insert("end", invoice)
        cart_text = "Warenkorb:\n"
        for dish_id, quantity in self.cart.items():
            dish_name = self.menu_tree.item(dish_id, "values")[0]
            cart_text += f"{dish_name} x{quantity}\n"
        self.cart_text.delete(1.0, "end")
        self.cart_text.insert("end", cart_text)
        
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

    def create_order(self, speiseID, menge):
        if self.validate_order({speiseID: menge}):
            order = pd.DataFrame(columns=["ID", "Datum", "SpeiseID", "Menge", "Status"])
            order = order.append({"ID": len(self.orders) + 1, "Datum": datetime.now(), "SpeiseID": speiseID, "Menge": menge, "Status": "offen"}, ignore_index=True)
            self.orders = pd.concat([self.orders, order], ignore_index=True)
            return order
        else:
            return None  # Die Bestellung ist nicht gültig

    def validate_order(self, order_details):
        for item_id in order_details.keys():
            if item_id not in self.menu.index:
                return False
        return True

    def cancel_order(self, order_id):
        self.orders.loc[self.orders["ID"] == order_id, "Status"] = "storno"

    def set_tischnummer(self):
        self.tischnummer = simpledialog.askinteger("Tischnummer", "Bitte geben Sie die Tischnummer ein:", parent=self.root)

class Restaurant:
    def __init__(self, name, menu_file="speisekarte.csv", encoding="utf-8"):
        self.name = name
        self.menu = self.load_menu(menu_file, encoding)
        
    def load_menu(self, menu_file, encoding):
        menu = pd.read_csv(menu_file, encoding=encoding, index_col="ID")
        return menu

    def get_id_by_name(self, name):
        for index, row in self.menu.iterrows():
            if row["Name"] == name:
                return index
        return None
    
class Order:
    def __init__(self, table_number):
        self.table_number = table_number
        self.order_items = pd.DataFrame(columns=["ID", "SpeiseID", "Menge"])
        
    def add_item(self, speiseID, menge):
        order_item = pd.DataFrame({"ID": [len(self.order_items) + 1], "SpeiseID": [speiseID], "Menge": [menge]})
        self.order_items = pd.concat([self.order_items, order_item], ignore_index=True)

    def generate_invoice(self, restaurant, tip=0):
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
        if tip > 0:
            total_price += tip

        invoice_text += "-----------------------------\n"
        invoice_text += f"Gesamtpreis: {total:.2f} €\n"
        invoice_text += f"Trinkgeld: {tip:.2f} €\n"
        invoice_text += f"Nettopreis: {net_price:.2f} €\n"
        invoice_text += f"MwSt.: {tax_amount:.2f} €\n"
        invoice_text += f"Bruttopreis: {total_price:.2f} €"

        return invoice_text
   
if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()
