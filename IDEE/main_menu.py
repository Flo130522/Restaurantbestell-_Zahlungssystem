import tkinter as tk
from tkinter import ttk, simpledialog
import pandas as pd
from datetime import datetime

class MainMenu:
    def __init__(self, root, menu_file="speisekarte.csv"):
        self.root = root
        self.root.title("Golden Seagull - Hauptmenü")
        self.menu = self.load_menu(menu_file)
        self.create_menu_ui()
        self.create_order_ui()
        self.tischnummer = None
        self.tip_percentage = 0
        self.order_items = {}
        self.cart = {}
        self.create_payment_ui()

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

        self.cart_text_var = tk.StringVar()  # StringVar to manage the content of the cart_text
        self.cart_text = tk.Text(self.cart_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        self.cart_text.grid(row=1, column=0, padx=5, pady=5)

        self.total_label = tk.Label(self.cart_frame, text="Gesamtsumme: 0.00 €")
        self.total_label.grid(row=2, column=0, padx=5, pady=5)

    def create_order_ui(self):
        self.order_frame = ttk.LabelFrame(self.root, text="Bestellung")
        self.order_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.selected_dish = None

    def add_to_cart(self, event):
        selected_item = self.menu_tree.selection()
        if selected_item:
            dish_id = selected_item[0]
            print(f"Adding dish to cart: {dish_id}")
            if dish_id in self.cart:
                self.cart[dish_id] += 1
            else:
                self.cart[dish_id] = 1
            print(f"Cart after adding: {self.cart}")
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
                order = self.create_order(dish_id, quantity)
                if order:
                    self.orders = pd.concat([self.orders, order], ignore_index=True)

            self.cart = {}
            self.update_invoice()

        elif self.selected_dish:
            if self.selected_dish["Name"] not in self.order_items:
                self.order_items[self.selected_dish["Name"]] = {
                    "Name": self.selected_dish["Name"],
                    "Beschreibung": self.selected_dish["Beschreibung"],
                    "Preis": self.selected_dish["Preis"],
                    "Menge": 1
                }
            else:
                self.order_items[self.selected_dish["Name"]]["Menge"] += 1
            self.update_invoice()

    def update_invoice(self):
        invoice = self.generate_invoice()

        # Set the text widget to normal state before updating
        self.cart_text.config(state=tk.NORMAL)

        # Delete the existing content in the text widget
        self.cart_text.delete(1.0, tk.END)

        # Insert the new content into the text widget
        self.cart_text.insert(tk.END, invoice)

        # Disable the text widget to prevent user modification
        self.cart_text.config(state=tk.DISABLED)

        total_price = sum(
            self.menu.loc[dish_id, "Preis"] * quantity if dish_id in self.menu.index else 0
            for dish_id, quantity in self.cart.items()
        )
        self.total_label.config(text=f"Gesamtsumme: {total_price:.2f} €")

    def generate_invoice(self):
        total = 0
        invoice_text = ""
        net_price = 0
        tax_rate = 0.19

        for dish_id, quantity in self.cart.items():
            dish_data = self.menu_tree.item(dish_id, "values")
            name = dish_data[1]
            beschreibung = dish_data[2]
            preis = dish_data[3]

            try:
                price_float = float(preis.split(" €")[0])
                total += price_float * quantity
                net_price += price_float * quantity
                invoice_text += f"{name} x{quantity}: {beschreibung} ({preis})\n"
            except ValueError:
                print(f"Invalid 'preis' value for {name}: {preis}")

        # Calculate tax amount
        tax_amount = total * tax_rate

        # Add tip to the total if provided
        total_price = total + tax_amount
        if self.tip_percentage > 0:
            total_price += self.tip_percentage

        # Construct the invoice text
        invoice_text += "-----------------------------\n"
        invoice_text += f"Gesamtpreis: {total:.2f} €\n"
        if self.tip_percentage > 0:
            invoice_text += f"Trinkgeld: {self.tip_percentage:.2f} €\n"
        invoice_text += f"Nettopreis: {net_price:.2f} €\n"
        invoice_text += f"MwSt.: {tax_amount:.2f} €\n"
        invoice_text += f"Bruttopreis: {total_price:.2f} €"

        return invoice_text



    def create_order(self, speiseID, menge):
        if self.validate_order({speiseID: menge}):
            order = pd.DataFrame(columns=["ID", "Datum", "SpeiseID", "Menge", "Status"])
            order = order.append({"ID": len(self.orders) + 1, "Datum": datetime.now(), "SpeiseID": speiseID,
                                  "Menge": menge, "Status": "offen"}, ignore_index=True)
            self.orders = pd.concat([self.orders, order], ignore_index=True)
            return order
        else:
            return None

    def validate_order(self, order_details):
        for item_id in order_details.keys():
            if item_id not in self.menu.index:
                return False
        return True

    def cancel_order(self, order_id):
        self.orders.loc[self.orders["ID"] == order_id, "Status"] = "storno"

    def set_tischnummer(self):
        self.tischnummer = simpledialog.askinteger("Tischnummer", "Bitte geben Sie die Tischnummer ein:", parent=self.root)
    
    def set_tip_percentage(self):
        self.tip_percentage = simpledialog.askfloat("Trinkgeld", "Bitte geben Sie das Trinkgeld ein:", parent=self.root)
    
    def create_payment_ui(self):  # Neu hinzugefügte Funktion
        self.payment_frame = ttk.LabelFrame(self.root, text="Bezahlung")
        self.payment_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.pay_button = ttk.Button(self.payment_frame, text="Bezahlen", command=self.process_payment)
        self.pay_button.grid(row=0, column=0, pady=5)

    def process_payment(self):  # Neu hinzugefügte Funktion
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Zahlung")

        tip_label = tk.Label(payment_window, text="Möchten Sie Trinkgeld geben?")
        tip_label.grid(row=0, column=0, padx=10, pady=10)

        tip_options = [5, 10, 15]
        tip_var = tk.StringVar(payment_window, value=0)
        tip_dropdown = ttk.Combobox(payment_window, values=tip_options, textvariable=tip_var)
        tip_dropdown.grid(row=0, column=1, padx=10, pady=10)

        custom_tip_entry = ttk.Entry(payment_window)
        custom_tip_entry.grid(row=0, column=2, padx=10, pady=10)

        confirm_button = ttk.Button(payment_window, text="Bestätigen", command=lambda: self.complete_payment(payment_window, tip_var, custom_tip_entry))
        confirm_button.grid(row=1, column=0, columnspan=3, pady=10)

    def complete_payment(self, payment_window, tip_var, custom_tip_entry):  # Neu hinzugefügte Funktion
        if tip_var.get():
            self.tip_percentage = float(tip_var.get())
        elif custom_tip_entry.get():
            self.tip_percentage = float(custom_tip_entry.get())

        payment_window.destroy()

        if self.tip_percentage > 0:
            tip_message = f"Vielen Dank für Ihr Trinkgeld von {self.tip_percentage:.2f} €!\n\n"
        else:
            tip_message = ""

        confirmation_message = f"Ihre Bestellung wurde erfolgreich bezahlt.\n{tip_message}Wählen Sie eine Zahlungsmethode:"

        payment_result = simpledialog.askstring("Bezahlung abgeschlossen", confirmation_message)


        if payment_result:
            self.display_order_status(payment_result)
        else:
            print("Zahlung storniert.")

    def display_order_status(self, payment_method):  # Neu hinzugefügte Funktion
        status_window = tk.Toplevel(self.root)
        status_window.title("Bestellstatus")

        status_label = tk.Label(status_window, text=f"Ihre Bestellung wurde {payment_method}.")
        status_label.pack()
        
if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()

