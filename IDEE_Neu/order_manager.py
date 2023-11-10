import tkinter as tk
from tkinter import ttk, simpledialog
from datetime import datetime
import pandas as pd

class OrderManager:
    def __init__(self, root):
        self.root = root
        self.tischnummer = None
        self.tip_percentage = 0
        self.order_items = {}
        self.cart = {}
        self.create_order_ui()

    def create_order_ui(self):
        self.order_frame = ttk.LabelFrame(self.root, text="Bestellung")
        self.order_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.selected_dish = None
        pass

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
            pass

    def create_payment_ui(self):
        self.payment_frame = ttk.LabelFrame(self.root, text="Bezahlung")
        self.payment_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.pay_button = ttk.Button(self.payment_frame, text="Bezahlen", command=self.process_payment)
        self.pay_button.grid(row=0, column=0, pady=5)
        pass

    def process_payment(self):
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
        pass

    def complete_payment(self, payment_window, tip_var, custom_tip_entry):
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

        payment_result = simpledialog.askstring("Bezahlung abgeschlossen", confirmation_message, parent=self.root,
                                                prompt="Barzahlung, EC-Karte, Kreditkarte")

        if payment_result:
            self.display_order_status(payment_result)
        else:
            print("Zahlung storniert.")
            pass

    def display_order_status(self, payment_method):
        status_window = tk.Toplevel(self.root)
        status_window.title("Bestellstatus")

        status_label = tk.Label(status_window, text=f"Ihre Bestellung wurde {payment_method}.")
        status_label.pack()
        pass
