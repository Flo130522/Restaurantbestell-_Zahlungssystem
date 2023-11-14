import tkinter as tk

class WelcomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Willkommen bei Golden Seagull")

        label = tk.Label(root, text="Willkommen bei Golden Seagull", font=("Arial", 20))
        label.grid()

        button = tk.Button(root, text="Jetzt bestellen!", font=("Arial", 15), command=self.open_main_menu)
        button.grid()

    def open_main_menu(self):
        from grundgerüst import MainMenu
        main_menu = MainMenu(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    welcome_window = WelcomeWindow(root)
    root.mainloop()
