import tkinter as tk
from welcome_window import WelcomeWindow
from main_window import MainWindow

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.show_welcome_window()

    def show_welcome_window(self):
        self.welcome_window = WelcomeWindow(self.root, self.show_main_window)

    def show_main_window(self):
        self.root.destroy()
        root = tk.Tk()
        main_window = MainWindow(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()
