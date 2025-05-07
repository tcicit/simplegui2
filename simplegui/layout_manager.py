import tkinter as tk  # Import tkinter for menu creation
from simplegui.yaml_loader import load_yaml_layout
from simplegui.validation import Validator
from simplegui.core import SimpleGUI
import logging

def setup_layout(app, layout_file, command_mapping):
    """
    Loads the layout, maps commands, and builds the layout.

    Args:
        app (SimpleGUI): The instance of the SimpleGUI class.
        layout_file (str): Path to the YAML layout file.
        command_mapping (dict): Mapping from function names to Python functions.
    """
    # Load layout from YAML file
    layout = load_yaml_layout(layout_file)
    widget_class_mapping = SimpleGUI.get_widget_class_mapping()
    Validator.validate_layout(layout, command_mapping, widget_class_mapping)

    # Store menu data separately before modifying the layout dict
    menu_data = layout.pop("menu", None)

    # Map commands in the layout
    map_layout_commands(layout, command_mapping, app)

    # Build the main layout (grid or rows)
    app.build(layout)

    # Load the menu if present
    if menu_data:
        setup_menu(app, menu_data, command_mapping)

def map_layout_commands(layout, command_mapping, app):
    """
    Recursively walks through the layout and replaces command strings with callables.

    Args:
        layout (dict or list): The layout structure.
        command_mapping (dict): Mapping from function names to Python functions.
        app (SimpleGUI): The app instance to pass to commands.
    """
    def _recursive_map(data):
        if isinstance(data, dict):
            # Check if this dict represents a widget with a 'command'
            if "command" in data and isinstance(data["command"], str):
                command_name = data["command"]
                mapped_func = command_mapping.get(command_name)
                if mapped_func:
                    # Replace string with a lambda that calls the function with app
                    data["command"] = lambda app=app, cmd=mapped_func: cmd(app)
                else:
                    logging.warning(f"Command '{command_name}' found in layout but not in command_mapping.")
                    data["command"] = None  # Or a dummy function

            # Recursively process all values in the dictionary
            for key, value in data.items():
                # Especially for 'options' or other nested structures that may contain commands
                if isinstance(value, (dict, list)):
                    _recursive_map(value)

        elif isinstance(data, list):
            # Recursively process all items in the list
            for item in data:
                _recursive_map(item)
    _recursive_map(layout)  # Start the recursive search/replacement

def setup_menu(app, menu_data, command_mapping):
    """
    Creates a menu based on the menu structure from the YAML file.

    Args:
        app (SimpleGUI): The instance of the SimpleGUI class.
        menu_data (list): The menu structure from the YAML file.
        command_mapping (dict): Mapping from function names to Python functions.
    """
    menu_bar = tk.Menu(app.root)
    for menu in menu_data:
        menu_label = menu.get("label", "Unnamed")
        menu_items = menu.get("items", [])
        menu_dropdown = tk.Menu(menu_bar, tearoff=0)
        for item in menu_items:
            item_label = item.get("label", "Unnamed")
            command_name = item.get("command")
            item_command = command_mapping.get(command_name)

            if item_command:
                # IMPORTANT: Create a lambda that calls the function with the app instance
                menu_dropdown.add_command(
                    label=item_label,
                    command=lambda app=app, cmd=item_command: cmd(app)
                )
            else:
                # Disable the menu item if no command is found
                menu_dropdown.add_command(label=item_label, state="disabled")
        menu_bar.add_cascade(label=menu_label, menu=menu_dropdown)
    app.root.config(menu=menu_bar)