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

