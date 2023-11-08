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
