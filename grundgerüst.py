import pandas as pd
import os
print(os.getcwd())
os.chdir(r"c:/Users/User/Documents/Thorsten/GitHub/gastro")
print(os.getcwd())
def load_menu(menu_file, encoding="utf-8"):
    menu = pd.read_csv(menu_file, encoding=encoding)
    return menu

menu_file = r"speisekarte.csv"
restaurant_menu = load_menu(menu_file)

print(restaurant_menu)

def bestellung_pruefen(speisekarte, bestellung):
    for gericht in bestellung:
        if gericht not in speisekarte:
            return False  # Falls ein Gericht in der Bestellung nicht auf der Speisekarte ist, ist die Bestellung ungültig
    return True  # Alle Gerichte in der Bestellung sind auf der Speisekarte

# Beispiel für die Speisekarte und eine Bestellung
speisekarte = ['Schnitzel mit Pommes,Frisches Schweineschnitzel mit knusprigen Pommes frites', 
               'Spaghetti Bolognese,Italienische Spaghetti mit herzhafter Bolognesesauce', 
               'Caesar Salat,Gemischter Salat mit Caesar-Dressing und Croutons', 
               'Pizza Margherita,Klassische Pizza mit Tomaten & Mozzarella und Basilikum', 
               'Fischfilet mit Gemüse,Gebratenes Fischfilet mit saisonalem Gemüse',
               "Fruchtsalat,Bunter Fruchtsalat mit frischen Früchten"]

bestellung_1 = ['Pizza', 'Salat', 'Burger']
bestellung_2 = ['Pasta', 'Suppe', 'Dessert']

# Überprüfung der Bestellungen
if bestellung_pruefen(speisekarte, bestellung_1):
    print("Bestellung 1 ist gültig.")
else:
    print("Bestellung 1 enthält Gerichte, die nicht auf der Speisekarte sind.")

if bestellung_pruefen(speisekarte, bestellung_2):
    print("Bestellung 2 ist gültig.")
else:
    print("Bestellung 2 enthält Gerichte, die nicht auf der Speisekarte sind.")

import pandas as pd
from datetime import datetime

# Erstellen des leeren DataFrame für die Bestellungen
bestellungen_gesamt = pd.DataFrame(columns=['ID', 'Datum', 'Tischnummer', 'SpeiseID', 'Menge', 'Status'])

# Die Funktion zum Hinzufügen einer neuen Bestellung
def neue_bestellung_generieren(tischnummer, speisen):
    global bestellungen_gesamt  # Verwende die globale Variable
    
    neue_id = len(bestellungen_gesamt) + 1
    datum = datetime.now().strftime("%Y-%m-%d")
    
    neue_bestellung = pd.DataFrame({
        'ID': [neue_id] * len(speisen),
        'Datum': [datum] * len(speisen),
        'Tischnummer': [tischnummer] * len(speisen),
        'SpeiseID': speisen.keys(),
        'Menge': speisen.values(),
        'Status': 'offen'
    })
    
    bestellungen_gesamt = pd.concat([bestellungen_gesamt, neue_bestellung], ignore_index=True)
    return bestellungen_gesamt

# Beispielaufruf der Funktion für eine neue Bestellung
neue_bestellung = neue_bestellung_generieren(5, {'1': 2, '3': 1, '5': 3})
print(neue_bestellung)

# Annahme: bestellungen_gesamt als globales DataFrame definiert
bestellungen_gesamt = pd.DataFrame(columns=['ID', 'Datum', 'Tischnummer', 'SpeiseID', 'Menge', 'Status'])

def bestellung_stornieren(bestellungs_id):
    global bestellungen_gesamt
    
    if bestellungs_id in bestellungen_gesamt['ID'].tolist():
        bestellungen_gesamt.loc[bestellungen_gesamt['ID'] == bestellungs_id, 'Status'] = 'storno'
        print(f"Bestellung {bestellungs_id} wurde storniert.")
    else:
        print(f"Bestellung {bestellungs_id} nicht gefunden.")

# Beispielaufruf der Stornierungs-Funktion
bestellung_stornieren(3)  # Annahme: Die Bestellung mit der ID 3 soll storniert werden