import pandas as pd

def load_menu(speisekarte):
    speisekarte = pd.read_csv("speisekarte.csv", index_col=1)
    return speisekarte

load_menu()