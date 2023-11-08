import pandas as pd

def load_menu(menu_file):
    food_menu = pd.read_csv(menu_file, index_col=0)
    return food_menu

# "C:\Users\User\Documents\GitHub\gastro\speisekarte.csv" ## Georg's PC
# "C:\Users\Admin\source\repos\Flo130522\gastro\speisekarte.csv ## Florian's PC
# "C:\Users\User\Documents\Thorsten\GitHub\gastro\speisekarte.csv ## Thorsten's PC
menu_file = r"C:\Users\User\Documents\GitHub\gastro\speisekarte.csv"

food_menu = load_menu(menu_file)
print(food_menu)