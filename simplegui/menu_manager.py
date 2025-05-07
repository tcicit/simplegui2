import tkinter as tk

class MenuManager:
    def __init__(self, root):
        # Initialize the menu bar and store the root window
        self.menubar = tk.Menu(root)
        self.root = root

    def build_menu(self, menu_structure):
        """
        Build the menu bar from a given menu structure dictionary.

        Args:
            menu_structure (dict): Dictionary where keys are menu names and values are lists of menu items.
        """
        for menu_name, items in menu_structure.items():
            menu = tk.Menu(self.menubar, tearoff=0)
            for item in items:
                if item == "separator":
                    # Add a separator line to the menu
                    menu.add_separator()
                else:
                    label = item.get("label", "Item")
                    command = item.get("command")
                    # Check if the command is callable before assigning
                    if callable(command):
                        menu.add_command(label=label, command=command)
                    else:
                        # If not callable, add the item as disabled or with no action
                        menu.add_command(label=label, command=None)
            # Add the constructed menu to the menu bar
            self.menubar.add_cascade(label=menu_name, menu=menu)
        # Set the menu bar for the root window
        self.root.config(menu=self.menubar)
