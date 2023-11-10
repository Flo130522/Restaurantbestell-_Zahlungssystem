import tkinter as tk
from menu_manager import MenuManager
from order_manager import OrderManager

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.menu_manager = MenuManager(root)
        self.order_manager = OrderManager(root)

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()
