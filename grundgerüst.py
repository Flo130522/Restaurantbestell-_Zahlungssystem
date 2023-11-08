import pandas as pd

def load_menu(menu_file):
    speisekarte = pd.read_csv(menu_file, index_col=0)
    return speisekarte

menu_file = r"C:\Users\Admin\source\repos\Flo130522\gastro\speisekarte.csv"
speisekarte = load_menu(menu_file)
print(speisekarte)