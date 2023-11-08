import pandas as pd

def load_menu(menu_file, encoding="utf-8"):
    speisekarte = pd.read_csv(menu_file, encoding=encoding)
    return speisekarte

menu_file = r"speisekarte.csv"
speisekarte = load_menu(menu_file)

load_menu(menu_file)
print(speisekarte)