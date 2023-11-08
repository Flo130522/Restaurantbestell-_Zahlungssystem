# region Modulimporte
from datetime import datetime
import pandas as pd
# endregion Modulimporte

# region Speisekarte laden
def load_menu(menu_file, encoding="utf-8", index_col="id"):
    menu = pd.read_csv(menu_file, encoding=encoding)
    return menu

menu_file = r"speisekarte.csv"
restaurant_menu = load_menu(menu_file)
print(restaurant_menu)
#endregion Speisekarte laden

# region Bestellungen erstellen und Bestellliste anzeigen
bestellungen = pd.DataFrame(columns=["ID", "Datum", "Tischnummer", "SpeiseID", "Menge", "Status"])

def create_order(speiseID, menge, tischnummer):
    global bestellungen
    bestellungen = bestellungen.append({"ID": len(bestellungen) + 1,
                                        "Datum": datetime.now(),
                                        "Tischnummer": tischnummer,
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

def generate_invoice(order, menu, tip=0):
    total = calculate_total(order, menu)
    net_price = total
    tax_rate = 0.19  # Beispiel: 19% Mehrwertsteuer
    tax_amount = total * tax_rate
    total_price = total + tax_amount
    if tip > 0:
        total_price += tip

    invoice = {
        "Gerichte": order,
        "Nettopreis": net_price,
        "MwSt.": tax_amount,
        "Bruttopreis": total_price,
        "Trinkgeld": tip
    }
    return invoice
# endregion Bezahlen und Rechnung erstellen

