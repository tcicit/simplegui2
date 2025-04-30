# /home/tci/Dokumente/Entwicklung/Python/simpleGUI2/simplegui/core.py
import tkinter as tk
from tkinter import ttk
from simplegui.theme_manager import ThemeManager
# Import custom widgets including the new ColorPicker widget
from simplegui.custom_widgets import Card, InfoBox, Picture, ColorPicker # Added ColorPicker
import logging

logging.basicConfig(level=logging.INFO)

class SimpleGUI:
    # ... (init, build - unverändert) ...
    def __init__(self, root, title="SimpleGUI App", size="600x400"):
        self.root = root
        self.root.title(title)
        self.root.geometry(size)
        # Instantiate ThemeManager AFTER root is created
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_theme_to_root(root) # Apply theme to root window
        self.widgets = {}
        self.widget_vars = {} # To store associated variables (IntVar, StringVar)

    def build(self, layout):
        container = tk.Frame(self.root) # Main container frame
        container.pack(fill="both", expand=True, padx=10, pady=10)
        self.theme_manager.apply_theme_to_widget(container, "Frame") # Theme the main container

        # Use a single build_recursive function for clarity
        self._build_recursive(container, layout.get("rows", []))


    def _build_recursive(self, parent_container, rows_layout):
        """Recursively builds widgets within a given parent container."""
        for row_idx, row in enumerate(rows_layout):
            # Create a frame for each row to manage layout better
            row_frame = tk.Frame(parent_container)
            # Apply theme to row frame (optional, depends on desired look)
            self.theme_manager.apply_theme_to_widget(row_frame, "Frame")
            row_padding_y = row.get("padding_y", 5)
            row_padding_x = row.get("padding_x", 0)
            row_fill = row.get("fill", "x") # Allow row fill option
            row_expand = row.get("expand", False) # Allow row expand option
            row_frame.pack(fill=row_fill, expand=row_expand, pady=row_padding_y, padx=row_padding_x)


            for col_idx, col in enumerate(row.get("columns") or []):
                widget_type = col.get("type")
                if not widget_type:
                    logging.warning(f"Widget type missing in row {row_idx}, column {col_idx}. Skipping.")
                    continue

                widget_class = self._resolve_widget_class(widget_type)
                if not widget_class: # Check if resolving failed
                    logging.error(f"Could not resolve widget class for type '{widget_type}'. Skipping.")
                    continue

                options = col.get("options", {}).copy() # Work with a copy
                widget_name = col.get("name")
                var_key = widget_name if widget_name else f"{widget_type}_{row_idx}_{col_idx}"

                # --- Command Handling ---
                command_func = None
                command_name = col.get("command") # Get command name string from YAML
                # Map command string to function IF it's for a widget that supports it
                # Note: ColorPicker command is handled separately below
                if isinstance(command_name, str) and widget_type in ["Button", "Checkbutton", "Radiobutton", "ttk.Button", "ttk.Checkbutton", "ttk.Radiobutton"]:
                    # We assume command mapping happened before build() is called
                    # If the value in layout is still a string here, it wasn't mapped
                    logging.warning(f"Command '{command_name}' for {widget_type} '{widget_name}' seems to be a string. Ensure it was mapped to a function before calling build().")
                    # Attempt to use it anyway, might fail if not mapped
                    command_func = command_name
                elif callable(command_name): # If it was already mapped
                     command_func = command_name

                # Add mapped command to options if applicable
                if command_func and 'command' not in options and widget_type not in ["ColorPicker"]:
                    options['command'] = command_func


                # --- Variable Handling ---
                var = None
                # Handle variables for standard tk and ttk widgets
                if widget_type in ["Checkbutton", "ttk.Checkbutton"]:
                    var = tk.IntVar()
                    if 'variable' not in options: options['variable'] = var
                elif widget_type in ["Radiobutton", "ttk.Radiobutton"]:
                    group_var_name = options.pop("variable_group", f"radio_group_{row_idx}")
                    if group_var_name not in self.widget_vars:
                        self.widget_vars[group_var_name] = tk.StringVar(value=options.get('value')) # Set initial value if provided
                    var = self.widget_vars[group_var_name]
                    if 'variable' not in options: options['variable'] = var
                elif widget_type in ["Combobox", "ttk.Combobox", "Entry", "ttk.Entry", "Spinbox", "ttk.Spinbox"]:
                    var = tk.StringVar()
                    if 'textvariable' not in options: options['textvariable'] = var
                elif widget_type in ["Scale", "ttk.Scale"]:
                    var = tk.DoubleVar()
                    if 'variable' not in options: options['variable'] = var
                # Add other variable types if needed (e.g., BooleanVar for Checkbutton)

                if var and var_key:
                     self.widget_vars[var_key] = var

                # --- Special Widget Handling (Notebook, Treeview, Picture, ColorPicker) ---
                widget = None
                if widget_type == "Notebook":
                    tabs_data = options.pop("tabs", [])
                    notebook = widget_class(row_frame, **options)
                    for tab_info in tabs_data:
                        tab_title = tab_info.get("title", "Tab")
                        tab_layout = tab_info.get("layout", {})
                        tab_frame = tk.Frame(notebook)
                        self.theme_manager.apply_theme_to_widget(tab_frame, "Frame")
                        notebook.add(tab_frame, text=tab_title)
                        self._build_recursive(tab_frame, tab_layout.get("rows", []))
                    widget = notebook

                elif widget_type == "Treeview":
                    tree_container = tk.Frame(row_frame)
                    self.theme_manager.apply_theme_to_widget(tree_container, "Frame")
                    v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
                    h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal")
                    tree_options = options.copy()
                    tree_options['yscrollcommand'] = v_scrollbar.set
                    tree_options['xscrollcommand'] = h_scrollbar.set
                    columns = tree_options.pop("columns", [])
                    headings = tree_options.pop("headings", [])
                    widths = tree_options.pop("widths", {})
                    anchors = tree_options.pop("anchors", {})
                    show = tree_options.pop("show", "tree headings")
                    tree = widget_class(tree_container, **tree_options)
                    v_scrollbar.config(command=tree.yview)
                    h_scrollbar.config(command=tree.xview)
                    tree['columns'] = columns
                    tree['show'] = show
                    if 'tree' in show:
                        tree.column("#0", width=widths.get("#0", 150), anchor=anchors.get("#0", 'w'))
                        tree.heading("#0", text=headings[0] if headings else "Tree")
                    else:
                         tree.column("#0", width=0, stretch=tk.NO)
                    col_start_index = 1 if 'tree' in show else 0
                    for i, col_id in enumerate(columns):
                        col_idx_in_headings = i + col_start_index
                        heading_text = headings[col_idx_in_headings] if col_idx_in_headings < len(headings) else col_id.capitalize()
                        width = widths.get(col_id, 100)
                        anchor = anchors.get(col_id, 'w')
                        tree.column(col_id, width=width, anchor=anchor)
                        tree.heading(col_id, text=heading_text)
                    v_scrollbar.pack(side="right", fill="y")
                    h_scrollbar.pack(side="bottom", fill="x")
                    tree.pack(side="left", fill="both", expand=True)
                    widget = tree
                    pack_options = col.get("pack_options", {})
                    default_pack_options = {"side": "left", "expand": True, "fill": "both", "padx": 5, "pady": 2}
                    default_pack_options.update(pack_options)
                    tree_container.pack(**default_pack_options)


                elif widget_type == "Picture":
                    filepath = options.pop("filepath", None)
                    width = options.pop("width", None)
                    height = options.pop("height", None)
                    widget = widget_class(row_frame, filepath=filepath, width=width, height=height, **options)

                elif widget_type == "ColorPicker": # Handle ColorPicker
                    initial_color = options.pop("initial_color", "#ffffff")
                    button_text = options.pop("button_text", "Choose Color")
                    show_hex = options.pop("show_hex", True)
                    # Handle command specifically for ColorPicker
                    cp_command_func = None
                    cp_command_name = options.pop("command", None) # Get command name/func from options
                    if isinstance(cp_command_name, str):
                         # Assume it needs mapping (should have happened before build)
                         logging.warning(f"Command '{cp_command_name}' for ColorPicker '{widget_name}' seems to be a string. Ensure it was mapped.")
                         cp_command_func = cp_command_name # Pass string or mapped func
                    elif callable(cp_command_name):
                         cp_command_func = cp_command_name

                    # Pass extracted options and the rest (**options) to the constructor
                    widget = widget_class(row_frame,
                                          initial_color=initial_color,
                                          button_text=button_text,
                                          show_hex=show_hex,
                                          command=cp_command_func, # Pass the mapped command
                                          **options) # Pass remaining standard Frame options


                # --- Create Standard Widget (if not handled above) ---
                if widget is None:
                    try:
                        # Pass the mapped command_func if it exists and applicable
                        if command_func and 'command' in widget_class.__init__.__code__.co_varnames:
                             options['command'] = command_func
                        widget = widget_class(row_frame, **options)
                    except tk.TclError as e:
                         logging.error(f"Error creating widget '{widget_name}' ({widget_type}) with options {options}: {e}")
                         widget = tk.Label(row_frame, text=f"Error creating {widget_type}", fg="red")
                    except Exception as e:
                         logging.error(f"General error creating widget '{widget_name}' ({widget_type}): {e}")
                         widget = tk.Label(row_frame, text=f"Error: {e}", fg="red")


                # --- Apply Theme ---
                if widget:
                    self.theme_manager.apply_theme_to_widget(widget, widget_type)

                # --- Packing (if not handled by special widget logic like Treeview) ---
                if widget and widget_type != "Treeview":
                    pack_options = col.get("pack_options", {})
                    # Sensible defaults based on widget type
                    if widget_type in ["Entry", "ttk.Entry", "Combobox", "ttk.Combobox", "Text", "Listbox", "Spinbox", "ttk.Spinbox"]:
                        default_pack_options = {"side": "left", "expand": True, "fill": "x", "padx": 5, "pady": 2}
                    elif widget_type in ["Notebook", "Frame", "LabelFrame"]:
                         default_pack_options = {"side": "left", "expand": True, "fill": "both", "padx": 5, "pady": 2}
                    elif widget_type == "Separator":
                         orient = widget.cget("orient")
                         fill = "x" if orient == "horizontal" else "y"
                         default_pack_options = {"side": "top", "expand": False, "fill": fill, "padx": 5, "pady": 5}
                    elif widget_type == "ColorPicker": # Sensible default for ColorPicker
                         default_pack_options = {"side": "left", "expand": False, "fill": "none", "padx": 5, "pady": 2}
                    else: # Buttons, Labels, Check/Radio, Scale, Picture etc.
                        default_pack_options = {"side": "left", "expand": False, "fill": "none", "padx": 5, "pady": 2}

                    default_pack_options.update(pack_options)
                    widget.pack(**default_pack_options)

                # --- Store Widget Reference ---
                if widget and widget_name:
                    if widget_name in self.widgets:
                         logging.warning(f"Duplicate widget name '{widget_name}' detected. Overwriting.")
                    self.widgets[widget_name] = widget


    def _resolve_widget_class(self, widget_type):
        # Added ColorPicker
        mapping = {
            # Standard tk
            "Label": tk.Label, 
            "Entry": tk.Entry, 
            "Button": tk.Button,
            "Checkbutton": tk.Checkbutton, 
            "Radiobutton": tk.Radiobutton,
            "Text": tk.Text, 
            "Frame": tk.Frame, 
            "LabelFrame": tk.LabelFrame,
            "Scale": tk.Scale, 
            "Spinbox": tk.Spinbox,
              "Listbox": tk.Listbox,
            # ttk (themed)
            "ttk.Button": ttk.Button, 
            "ttk.Checkbutton": ttk.Checkbutton,
            "ttk.Radiobutton": ttk.Radiobutton, 
            "ttk.Entry": ttk.Entry,
            "ttk.Scale": ttk.Scale, 
            "ttk.Spinbox": ttk.Spinbox,
            "Combobox": ttk.Combobox, 
            "Separator": ttk.Separator,
            "Notebook": ttk.Notebook, 
            "Treeview": ttk.Treeview,
            # Custom
            "Card": Card, 
            "InfoBox": InfoBox, 
            "Picture": Picture,
            "ColorPicker": ColorPicker # Added ColorPicker
        }
        resolved_class = mapping.get(widget_type)
        if resolved_class is None:
            if not widget_type.startswith("ttk."):
                resolved_class = mapping.get(f"ttk.{widget_type}")
            if resolved_class is None:
                logging.error(f"Unknown widget type: '{widget_type}'")
                return None
        return resolved_class

    def get_widget(self, name):
        """Get the raw widget object by its name."""
        widget = self.widgets.get(name)
        if widget is None:
            logging.error(f"Widget '{name}' not found.")
        return widget

    def get_widget_value(self, name):
        """Get the value from a widget by its name."""
        widget = self.get_widget(name)
        if widget is None: return None

        var = None
        # Try getting variable by widget name first
        if name in self.widget_vars:
            var = self.widget_vars.get(name)
            
        # Special handling for Radiobutton group variable
        elif isinstance(widget, (tk.Radiobutton, ttk.Radiobutton)):
             try:
                 var_name_tcl = str(widget.cget('variable'))
                 for group_name, tk_var in self.widget_vars.items():
                     if str(tk_var) == var_name_tcl:
                         var = tk_var
                         break
             except tk.TclError:
                 logging.error(f"Could not get variable for Radiobutton '{name}'.")

        # Get value from variable if found
        if var:
             try:
                 return var.get()
             except tk.TclError as e:
                 logging.error(f"Error getting value from variable for widget '{name}': {e}")
                 return None

        # Fallback or specific widget types without standard variables
        if isinstance(widget, (tk.Entry, ttk.Entry)):
            return widget.get()
        elif isinstance(widget, tk.Text):
            return widget.get("1.0", tk.END).strip()
        elif isinstance(widget, tk.Listbox):
            try:
                indices = widget.curselection()
                return [widget.get(i) for i in indices] if indices else []
            except tk.TclError as e:
                 logging.error(f"Error getting value from Listbox '{name}': {e}")
                 return None
        elif isinstance(widget, ttk.Combobox):
             return widget.get()
        elif isinstance(widget, ttk.Treeview):
             try:
                 return widget.selection()
             except tk.TclError as e:
                 logging.error(f"Error getting selection from Treeview '{name}': {e}")
                 return None
        elif isinstance(widget, ColorPicker): # Get value for ColorPicker
             return widget.get_color()
        # Add other widget types here if needed
        elif widget is not None:
             if not isinstance(widget, (tk.Radiobutton, ttk.Radiobutton)): # Already handled radio var search
                 logging.warning(f"Getting value for widget type '{type(widget).__name__}' named '{name}' is not explicitly supported via standard get_widget_value. Returning None.")

        return None

    def set_widget_option(self, name, option, value):
        """Set an option for a widget by its name."""
        widget = self.get_widget(name)
        if widget:
            try:
                # Special handling for Text widget content
                if isinstance(widget, tk.Text) and option == "text":
                    widget.delete("1.0", tk.END)
                    widget.insert("1.0", value)
                # Special handling for Entry widget content
                elif isinstance(widget, (tk.Entry, ttk.Entry)) and option == "text":
                     widget.delete(0, tk.END)
                     widget.insert(0, value)
                # Special handling for variable-based widgets
                elif option == "value" and name in self.widget_vars:
                     var = self.widget_vars[name]
                     var.set(value)
                # Special handling for Combobox values list
                elif isinstance(widget, ttk.Combobox) and option == "values":
                     widget['values'] = value
                # Special handling for ColorPicker color
                elif isinstance(widget, ColorPicker) and option == "color":
                     widget.set_color(value)
                # Special handling for Treeview (more complex, add dedicated methods)
                # elif isinstance(widget, ttk.Treeview) and option == 'data':
                #     self.clear_treeview(name)
                #     self.populate_treeview(name, value) # Requires dedicated methods
                else:
                    widget.config(**{option: value})

                # Optional: Re-apply theme if state changes affect it significantly
                # self.theme_manager.apply_theme_to_widget(widget, type(widget).__name__)
            except tk.TclError as e:
                logging.error(f"Error setting option '{option}' for widget '{name}': {e}")

    # --- Treeview Helper Methods (Example) ---
    # ... (clear_treeview, insert_treeview_item, get_treeview_item - unverändert) ...
    def clear_treeview(self, name):
        """Removes all items from a Treeview."""
        widget = self.get_widget(name)
        if isinstance(widget, ttk.Treeview):
            try:
                for item in widget.get_children():
                    widget.delete(item)
            except tk.TclError as e:
                logging.error(f"Error clearing Treeview '{name}': {e}")
        else:
            logging.error(f"Widget '{name}' is not a Treeview.")

    def insert_treeview_item(self, name, values, parent='', index=tk.END, item_id=None):
        """Inserts an item into the Treeview. Returns the item ID."""
        widget = self.get_widget(name)
        if isinstance(widget, ttk.Treeview):
            try:
                # Ensure values is a list or tuple
                if not isinstance(values, (list, tuple)):
                    values = [values]
                # Insert item and return its ID
                iid = widget.insert(parent, index, iid=item_id, values=values)
                return iid
            except tk.TclError as e:
                logging.error(f"Error inserting item into Treeview '{name}': {e}")
                return None
        else:
            logging.error(f"Widget '{name}' is not a Treeview.")
            return None

    def get_treeview_item(self, name, item_id):
        """Gets the data associated with a Treeview item ID."""
        widget = self.get_widget(name)
        if isinstance(widget, ttk.Treeview):
            try:
                return widget.item(item_id) # Returns dictionary with 'text', 'image', 'values', etc.
            except tk.TclError as e:
                logging.error(f"Error getting item '{item_id}' from Treeview '{name}': {e}")
                return None
        else:
            logging.error(f"Widget '{name}' is not a Treeview.")
            return None

    def run(self):
        self.root.mainloop()

