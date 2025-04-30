import tkinter as tk

class MenuManager:
    def __init__(self, root):
        self.menubar = tk.Menu(root)
        self.root = root

    def build_menu(self, menu_structure):
        for menu_name, items in menu_structure.items():
            menu = tk.Menu(self.menubar, tearoff=0)
            for item in items:
                if item == "separator":
                    menu.add_separator()
                else:
                    label = item.get("label", "Item")
                    command = item.get("command")
                    if callable(command):  # Prüfen, ob command aufrufbar ist
                        menu.add_command(label=label, command=command)
                    else:
                        menu.add_command(label=label, command=None)
            self.menubar.add_cascade(label=menu_name, menu=menu)
        self.root.config(menu=self.menubar)
