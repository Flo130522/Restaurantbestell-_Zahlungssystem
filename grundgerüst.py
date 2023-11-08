import pandas as pd

def load_menu(menu_file, encoding="utf-8"):
    speisekarte = pd.read_csv(menu_file, encoding=encoding)
    return speisekarte

menu_file = r"C:\Users\Admin\source\repos\Flo130522\gastro\speisekarte.csv"
speisekarte = load_menu(menu_file)