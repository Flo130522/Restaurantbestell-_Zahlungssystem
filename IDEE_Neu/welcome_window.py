import tkinter as tk
#from main_window import MainMenu  # Richtig importieren

class WelcomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Willkommen bei Golden Seagull")

        # Willkommensnachricht mit Schriftgröße 20
        label = tk.Label(root, text="Willkommen bei Golden Seagull", font=("Arial", 20))
        label.grid()

        # Button mit Schriftgröße 15 und Aktion zum Wechseln zum Hauptmenü
        button = tk.Button(root, text="Jetzt bestellen!", font=("Arial", 15), command=self.open_main_menu)
        button.grid()

    def open_main_menu(self):
        main_menu = MainMenu(self.root)  # Korrekte Instanz von MainMenu erstellen
