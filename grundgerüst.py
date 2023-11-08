import pandas as pd

def load_menu(menu_file):
    food_menu = pd.read_csv(menu_file, index_col=0)
    return food_menu

menu_file = r"C:\Users\Admin\source\repos\Flo130522\gastro\speisekarte.csv"
food_menu = load_menu(menu_file)
print(food_menu)