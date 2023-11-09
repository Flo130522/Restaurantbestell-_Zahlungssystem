import tkinter as tk
from tkinter import font

class WelcomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Willkommen bei Golden Seagull")

        # Schriftart und Größe für die Willkommensnachricht
        custom_font = font.nametofont("TkDefaultFont")
        custom_font.configure(size=20)  # Ändere die Schriftgröße hier nach Bedarf

        # Willkommensnachricht mit angepasster Schriftgröße
        label = tk.Label(root, text="Willkommen bei Golden Seagull", font=("Arial", 20))
        label.grid()

        button = tk.Button(root, text="Weiter", command=self.open_main_menu)
        button.grid()

    def open_main_menu(self):
        from main_menu import MainMenu
        main_menu = MainMenu(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    welcome_window = WelcomeWindow(root)
    root.mainloop()
