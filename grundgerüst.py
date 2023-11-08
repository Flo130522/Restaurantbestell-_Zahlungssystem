# region Modulimporte
from datetime import datetime
import pandas as pd
# endregion Modulimporte

# region Speisekarte laden
restaurant_name = "Golden Seagull"
def load_menu(menu_file, encoding="utf-8", index_col="id"):
    menu = pd.read_csv(menu_file, encoding=encoding)
    return menu

menu_file = r"speisekarte.csv"
restaurant_menu = load_menu(menu_file)
print(restaurant_menu)
#endregion Speisekarte laden

# region Bestellungen erstellen und Bestellliste anzeigen
bestellungen = pd.DataFrame(columns=["ID", "Datum", "SpeiseID", "Menge", "Status"])

def create_order(speiseID, menge):
    global bestellungen
    bestellungen = bestellungen.append({"ID": len(bestellungen) + 1,
                                        "Datum": datetime.now(),
                                        "SpeiseID": speiseID,
                                        "Menge": menge,
                                        "Status": "offen"}, ignore_index=True)
    
    return bestellungen
# endregion Bestellungen erstellen und Bestellliste anzeigen

# region Datenvalidierung
def validate_order(menu, order_details):
    for item_id in order_details.keys():
        if item_id not in menu.index:
            return False
    return True
# endregion Datenvalidierung

# region Storno
def cancel_order(order_list, order_id):
    order_list.loc[order_list["ID"] == order_id, "Status"] = "storno"
    
    return order_list
# endregion Storno

# region Bezahlen und Rechnung erstellen
def calculate_total(order, menu):
    total = 0
    for i, row in order.iterrows():
        item_id = row["SpeiseID"]
        quantity = row["Menge"]
        price = menu.loc[item_id, "Preis"]
        total += price * quantity
    return total

def generate_invoice(order, menu, tip=0, restaurant_name=""):
    total = calculate_total(order, menu)
    net_price = total
    tax_rate = 0.19  # Beispiel: 19% Mehrwertsteuer
    tax_amount = total * tax_rate
    total_price = total + tax_amount
    if tip > 0:
        total_price += tip

    invoice = f"Restaurant: {restaurant_name}\n"
    invoice += "-----------------------------\n"
    invoice += order.to_string(index=False) + "\n"
    invoice += "-----------------------------\n"
    invoice += f"Gesamtpreis: {total:.2f} €\n"
    invoice += f"Trinkgeld: {tip:.2f} €\n"
    invoice += f"Nettopreis: {net_price:.2f} €\n"
    invoice += f"MwSt.: {tax_amount:.2f} €\n"
    invoice += f"Bruttopreis: {total_price:.2f} €\n"

    return invoice

# endregion Bezahlen und Rechnung erstellen

if __name__ == "__main__":
    menu_file = "speisekarte.csv"
    menu = load_menu(menu_file)

    order_list = pd.DataFrame(columns=["ID", "Datum", "Tischnummer", "SpeiseID", "Menge", "Status"])

    order_details = {
        1: 2,  # Beispiel: SpeiseID und Menge
        3: 1
    }

    if validate_order(menu, order_details):
        order_list = create_order(order_list, table_number=1, menu=menu, order_details=order_details)
    else:
        print("Ungültige Bestellung.")

    order_id_to_cancel = 1  # Beispiel: Bestellung stornieren
    cancel_order(order_list, order_id_to_cancel)

    tip_amount = 5  # Beispiel: Trinkgeld
    invoice = generate_invoice(order_list, menu, tip_amount)
    print(invoice)