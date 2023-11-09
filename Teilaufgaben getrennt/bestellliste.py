import pandas as pd
from datetime import datetime

bestellungen = pd.DataFrame(columns=["ID", "Datum", "SpeiseID", "Menge", "Status"])

def create_order(speiseID, menge):
    global bestellungen
    bestellungen = bestellungen.append({"ID": len(bestellungen) + 1,
                                        "Datum": datetime.now(),
                                        "SpeiseID": speiseID,
                                        "Menge": menge,
                                        "Status": "offen"}, ignore_index=True)
    
    return bestellungen
