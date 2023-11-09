import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk, simpledialog

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant App")
        self.restaurant = Restaurant("Golden Seagull")
        self.current_table = 1  # Aktueller Tisch
        self.current_order = None
        self.create_menu_ui()
        self.create_order_ui()
        self.create_invoice_ui()
        self.tip_percentage = 0  # Trinkgeldbetrag


        self.create_order_ui()
        self.welcome_label = tk.Label(self.order_frame, text="Willkommen bei Golden Seagull")
        self.welcome_label.grid(row=0, column=0, columnspan=2)


        self.label = tk.Label(root, text="Möchten Sie bestellen?")
        self.label.grid(row=0, column=0)

        self.order_button = tk.Button(root, text="Bestellen", command=self.place_order)
        self.order_button.grid(row=1, column=0)

        self.pay_button = tk.Button(root, text="Bezahlen", command=self.ask_tip_percentage, state=tk.DISABLED)
        self.pay_button.grid(row=2, column=0)
        
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

    def create_order_ui(self):
        self.order_frame = ttk.LabelFrame(self.root, text="Bestellung")
        self.order_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.selected_dish = None

    def select_dish(self, event):
        selected_item = self.menu_tree.selection()
        if selected_item:
            item_values = self.menu_tree.item(selected_item[0], "values")
            self.selected_dish = {
                "Name": item_values[0],
                "Beschreibung": item_values[1],
                "Preis": item_values[2]
            }

    def place_order(self):
        if self.selected_dish:
            speiseID = self.restaurant.get_id_by_name(self.selected_dish["Name"])
            menge = 1
            if self.current_order is None:
                self.current_order = Order(self.current_table)
            self.current_order.add_item(speiseID, menge)
            self.update_invoice()
            self.order_button["state"] = tk.DISABLED
            self.pay_button["state"] = tk.NORMAL

    def update_invoice(self):
        invoice = self.current_order.generate_invoice(self.restaurant, self.tip_percentage)
        self.invoice_text.delete(1.0, "end")
        self.invoice_text.insert("end", invoice)

    def create_invoice_ui(self):
        self.invoice_frame = ttk.LabelFrame(self.root, text="Rechnung")
        self.invoice_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.invoice_text = tk.Text(self.invoice_frame, height=10, width=40)
        self.invoice_text.grid(row=0, column=0)

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
        for i, row in self.order_items.iterrows():
            item_id = row["SpeiseID"]
            quantity = row["Menge"]
            price = restaurant.menu.loc[item_id, "Preis"]
            total += price * quantity
        net_price = total
        tax_rate = 0.19
        tax_amount = total * tax_rate
        total_price = total + tax_amount
        if tip > 0:
            total_price += tip

        invoice = f"Restaurant: {restaurant.name}\n"
        invoice += f"Tischnummer: {self.table_number}\n"
        invoice += "-----------------------------\n"
        invoice += self.order_items.to_string(index=False) + "\n"
        invoice += "-----------------------------\n"
        invoice += f"Gesamtpreis: {total:.2f} €\n"
        invoice += f"Trinkgeld: {tip:.2f} €\n"
        invoice += f"Nettopreis: {net_price:.2f} €\n"
        invoice += f"MwSt.: {tax_amount:.2f} €\n"
        invoice += f"Bruttopreis: {total_price:.2f} €\n"

        return invoice

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()
