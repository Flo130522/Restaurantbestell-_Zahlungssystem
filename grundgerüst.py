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

