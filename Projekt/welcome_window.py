import tkinter as tk
from grundgerüst import MainMenu  # Make sure MainMenu is defined in grundgerüst module

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
        # Destroy the welcome window before creating the main menu
        self.root.destroy()

        # Create an instance of the MainMenu class
        main_menu_root = tk.Tk()
        main_menu = MainMenu(main_menu_root)
        main_menu_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    welcome_window = WelcomeWindow(root)
    root.mainloop()
