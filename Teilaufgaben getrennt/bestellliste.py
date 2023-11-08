import pandas as pd
from datetime import datetime

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
