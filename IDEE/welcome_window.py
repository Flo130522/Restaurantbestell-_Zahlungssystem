import tkinter as tk
from tkinter import font

class WelcomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Willkommen bei Golden Seagull")
        
        # Willkommensnachricht
        custom_font = font.nametofont("TkDefaultFont")
        custom_font.configure(size=20)
        label = tk.Label(root, text="Willkommen bei Golden Seagull")
        label.grid(row=0, column=0)

        button = tk.Button(root, text="Weiter", command=self.open_main_menu)
        button.grid(row=1, column=0)
        
    def open_main_menu(self):
        from main_menu import MainMenu
        main_menu = MainMenu(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    welcome_window = WelcomeWindow(root)
    root.mainloop()