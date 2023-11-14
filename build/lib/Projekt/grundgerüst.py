import pandas as pd
from datetime import datetime
import sys
import traceback

sys.excepthook = traceback.print_exception


class Restaurant:
    def __init__(self, name, menu_file="speisekarte.csv", encoding="utf-8"):
        self.name = name
        self.menu = self.load_menu(menu_file, encoding)
        self.orders = pd.DataFrame(columns=["ID", "Datum", "SpeiseID", "Menge", "Status"])

    def load_menu(self, menu_file, encoding):
        menu = pd.read_csv(menu_file, encoding=encoding, index_col="id")
        return menu

    def create_order(self, speiseID, menge):
        order = pd.DataFrame(columns=["ID", "Datum", "SpeiseID", "Menge", "Status"])
        order = order.append({"ID": len(self.orders) + 1, "Datum": datetime.now(), "SpeiseID": speiseID, "Menge": menge, "Status": "offen"}, ignore_index=True)
        self.orders = pd.concat([self.orders, order], ignore_index=True)
        return order

    def validate_order(self, order_details):
        for item_id in order_details.keys():
            if item_id not in self.menu.index:
                return False
        return True

    def cancel_order(self, order_id):
        self.orders.loc[self.orders["ID"] == order_id, "Status"] = "storno"

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
        tax_rate = 0.19  # Beispiel: 19% Mehrwertsteuer
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


