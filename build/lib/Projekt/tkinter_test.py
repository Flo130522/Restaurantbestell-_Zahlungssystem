import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant App")
        self.restaurant = Restaurant("Golden Seagull")
        self.create_menu_ui()
        self.create_order_ui()
        self.create_invoice_ui()

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
        self.order_button = ttk.Button(self.order_frame, text="Bestellen", state=tk.DISABLED, command=self.place_order)
        self.order_button.grid(row=2, column=0, columnspan=2)

    def select_dish(self, event):
        selected_item = self.menu_tree.selection()
        if selected_item:
            item_values = self.menu_tree.item(selected_item[0], "values")
            self.selected_dish = {
                "Name": item_values[0],
                "Beschreibung": item_values[1],
                "Preis": item_values[2]
            }
            self.order_button["state"] = tk.NORMAL
        else:
            self.selected_dish = None
            self.order_button["state"] = tk.DISABLED

    def place_order(self):
        if self.selected_dish:
            speiseID = self.restaurant.get_id_by_name(self.selected_dish["Name"])
            menge = 1  
            order = self.restaurant.create_order(speiseID, menge)
            self.update_invoice()

    def update_invoice(self):
        invoice = self.restaurant.generate_invoice()
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
        self.orders = pd.DataFrame(columns=["ID", "Datum", "SpeiseID", "Menge", "Status"])

    def load_menu(self, menu_file, encoding):
        menu = pd.read_csv(menu_file, encoding=encoding, index_col="ID")
        return menu

    def create_order(self, speiseID, menge):
        order = pd.DataFrame(columns=["ID", "Datum", "SpeiseID", "Menge", "Status"])
        order = order.append({"ID": len(self.orders) + 1, "Datum": datetime.now(), "SpeiseID": speiseID, "Menge": menge, "Status": "offen"}, ignore_index=True)
        self.orders = pd.concat([self.orders, order], ignore_index=True)
        return order

    def get_id_by_name(self, name):
        for index, row in self.menu.iterrows():
            if row["Name"] == name:
                return index
        return None  
    
    def calculate_total(self):
        total = 0
        for i, row in self.orders.iterrows():
            item_id = row["SpeiseID"]
            quantity = row["Menge"]
            price = self.menu.loc[item_id, "Preis"]
            total += price * quantity
        return total

    def generate_invoice(self, tip=0):
        total = self.calculate_total()
        net_price = total
        tax_rate = 0.19  
        tax_amount = total * tax_rate
        total_price = total + tax_amount
        if tip > 0:
            total_price += tip

        invoice = f"Restaurant: {self.name}\n"
        invoice += "-----------------------------\n"
        invoice += self.orders.to_string(index=False) + "\n"
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
