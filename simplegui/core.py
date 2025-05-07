# /home/tci/Dokumente/Entwicklung/Python/simpleGUI2/simplegui/core.py
import tkinter as tk
from tkinter import ttk
from simplegui.theme_manager import ThemeManager
from simplegui.custom_widgets import Card, InfoBox, Picture, ColorPicker, HtmlPreviewArea # Added ColorPicker
import logging

logging.basicConfig(level=logging.INFO)

class SimpleGUI:
    def __init__(self, root, title="SimpleGUI App", size="600x400"):
        """
        Initializes the SimpleGUI application.

        Args:
            root: The root Tkinter window (tk.Tk).
            title (str): The title of the window.
            size (str): The initial size of the window (e.g., "600x400").
        """
        self.root = root
        self.root.title(title)
        self.root.geometry(size)
        # Instantiate ThemeManager AFTER root is created
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_theme_to_root(root) # Apply theme to root window
        self.widgets = {} # Stores widget objects, keyed by name
        self.widget_vars = {} # Stores associated tk.Variable objects, keyed by name/group_name

    def build(self, layout):
        self._current_layout = layout  # Store the current layout for later reference
        """
        Builds the GUI layout based on the provided dictionary structure.

        Args:
            layout (dict): A dictionary describing the GUI layout (usually loaded from YAML).
                           Expected structure: {"rows": [...]} or {"grid": [...]}
        """
        container = tk.Frame(self.root)  # Main container frame
        container.pack(fill="both", expand=True, padx=10, pady=10)
        self.theme_manager.apply_theme_to_widget(container, "Frame")  # Theme the main container

        # Check for grid or rows layout
        if "grid" in layout:
            print("Grid layout detected. Building grid...")
            self._build_grid(container, layout["grid"])
        elif "rows" in layout:
            print("Rows layout detected. Building rows...")
            self._build_recursive(container, layout["rows"])


    def _build_recursive(self, parent_container, rows_layout):
        """
        Recursively builds widgets row by row and column by column within a given parent container.

        Args:
            parent_container: The Tkinter container widget (e.g., Frame) to build into.
            rows_layout (list): A list of dictionaries, where each dictionary represents a row.
        """
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
                widget_name = col.get("name") # Name for the widget or the group
                options = col.get("options", {}).copy() # Work with a copy

                # --- Special Handling for Radiobutton Groups ---
                if "group" in col:
                    group_name = col.get("group")
                    if not group_name:
                        logging.error(f"Radiobutton group defined without a 'group' name in row {row_idx}, col {col_idx}. Skipping.")
                        continue

                    # Create the shared variable for the group if it doesn't exist
                    if group_name not in self.widget_vars:
                        # Find the initially selected value (optional)
                        initial_value = None
                        for radio_item in col.get("columns", []):
                            radio_options = radio_item.get("options", {})
                            if radio_options.get("selected", False): # YAML could have 'selected: true'
                                initial_value = radio_options.get("value")
                                break
                        # Use StringVar to handle various value types (int, str, etc.)
                        self.widget_vars[group_name] = tk.StringVar(value=initial_value)

                    group_variable = self.widget_vars[group_name]

                    # Create a container frame for the radio buttons in the group
                    group_frame = tk.Frame(row_frame)
                    self.theme_manager.apply_theme_to_widget(group_frame, "Frame")
                    # Packing options for the group frame (can be customized via YAML)
                    group_pack_options = col.get("pack_options", {"side": "left", "fill": "none", "expand": False, "padx": 0, "pady": 0})
                    group_frame.pack(**group_pack_options)

                    # Create the individual radio buttons within the group
                    for radio_idx, radio_item in enumerate(col.get("columns", [])):
                        radio_type_str = radio_item.get("type")
                        if radio_type_str not in ["Radiobutton", "ttk.Radiobutton"]:
                            logging.warning(f"Item inside group '{group_name}' is not a Radiobutton (type: {radio_type_str}). Skipping.")
                            continue

                        radio_class = self._resolve_widget_class(radio_type_str)
                        if not radio_class: continue

                        radio_options = radio_item.get("options", {}).copy()
                        radio_name = radio_item.get("name") # Optional name for the individual button
                        radio_value = radio_options.get("value") # Value associated with this button

                        if radio_value is None:
                             logging.error(f"Radiobutton '{radio_name}' in group '{group_name}' is missing 'value' in options. Skipping.")
                             continue

                        # Add the shared variable and the specific value to the options
                        radio_options['variable'] = group_variable
                        radio_options['value'] = radio_value

                        # Remove 'selected' as it's only used for initializing the variable
                        radio_options.pop('selected', None)

                        try:
                            radio_widget = radio_class(group_frame, **radio_options)
                            self.theme_manager.apply_theme_to_widget(radio_widget, radio_type_str)

                            # Packing options for the individual radio button
                            radio_pack_options = radio_item.get("pack_options", {"side": "left", "fill": "none", "expand": False, "padx": 2, "pady": 2})
                            radio_widget.pack(**radio_pack_options)

                            # Store reference to the individual button if it has a name
                            if radio_name:
                                if radio_name in self.widgets:
                                    logging.warning(f"Duplicate widget name '{radio_name}' detected (Radiobutton in group '{group_name}'). Overwriting.")
                                self.widgets[radio_name] = radio_widget

                        except tk.TclError as e:
                            logging.error(f"Error creating Radiobutton '{radio_name}' in group '{group_name}' with options {radio_options}: {e}")
                        except Exception as e:
                            logging.error(f"General error creating Radiobutton '{radio_name}' in group '{group_name}': {e}")

                    continue # IMPORTANT: Skip the rest of the loop for this 'col', move to the next item

                # --- End of Special Handling for Radiobutton Groups ---


                # --- Standard Widget Processing ---
                if not widget_type:
                    # Skip if no type and not a group definition
                    if "group" not in col: # Only warn if it wasn't a group
                         logging.warning(f"Widget type missing and not a group in row {row_idx}, column {col_idx}. Skipping.")
                    continue

                widget_class = self._resolve_widget_class(widget_type)
                if not widget_class: # Check if resolving failed
                    logging.error(f"Could not resolve widget class for type '{widget_type}'. Skipping.")
                    continue

                # --- Command Handling ---
                command_func = None
                command_name = col.get("command") # Get command name string from YAML
                # Check if command is a string (needs mapping) or already a callable function
                # Check if command is a string (needs mapping) or already a callable function
                if isinstance(command_name, str) and widget_type in ["Button", "Checkbutton", "Radiobutton", "ttk.Button", "ttk.Checkbutton", "ttk.Radiobutton"]:
                    # Assume mapping happened before build()
                    # Logging-Level angepasst, da map_layout_commands dies nun tun sollte
                    logging.debug(f"Command '{command_name}' for {widget_type} '{widget_name}' seems to be a string. Assuming it was mapped.")
                    command_func = command_name # Pass the string/mapped function
                elif callable(command_name): # If it was already mapped
                     command_func = command_name

                # Add command to options if applicable (ColorPicker handles its command internally)
                if command_func and 'command' not in options and widget_type not in ["ColorPicker"]:
                    options['command'] = command_func


                # --- Variable Handling (for non-Radiobutton group widgets) ---
                var = None
                var_key = widget_name # Use the widget's name as the key for its variable

                # Handle variables for standard tk and ttk widgets that use them
                # NOTE: Radiobutton group variable is handled in the 'group' block above
                if widget_type in ["Checkbutton", "ttk.Checkbutton"]:
                    var = tk.IntVar()
                    if 'variable' not in options: options['variable'] = var
                    # Set initial value if defined in YAML (e.g., value: 1 for checked)
                    initial_val = options.pop('value', None)
                    if initial_val is not None: var.set(initial_val)

                elif widget_type in ["Combobox", "ttk.Combobox", "Entry", "ttk.Entry", "Spinbox", "ttk.Spinbox"]:
                    var = tk.StringVar()
                    if 'textvariable' not in options: options['textvariable'] = var
                    # Set initial text if defined in YAML (e.g., text: "default value")
                    initial_text = options.pop('text', None)
                    if initial_text is not None: var.set(initial_text)

                elif widget_type in ["Scale", "ttk.Scale"]:
                    var = tk.DoubleVar() # Use DoubleVar for potentially fractional values
                    if 'variable' not in options: options['variable'] = var
                     # Set initial value if defined in YAML (e.g., value: 50)
                    initial_val = options.pop('value', None)
                    if initial_val is not None: var.set(initial_val)

                # Store the variable under the widget's name if one was created
                if var and var_key:
                     if var_key in self.widget_vars:
                         logging.warning(f"Duplicate variable key '{var_key}' detected (for {widget_type}). Overwriting.")
                     self.widget_vars[var_key] = var


                # --- Special Widget Handling (Notebook, Treeview, Picture, ColorPicker) ---
                widget = None
                if widget_type == "Notebook":
                    tabs_data = options.pop("tabs", [])
                    notebook = widget_class(row_frame, **options)
                    for tab_info in tabs_data:
                        tab_title = tab_info.get("title", "Tab")
                        tab_layout = tab_info.get("layout", {})
                        tab_frame = tk.Frame(notebook) # Create a frame for each tab's content
                        self.theme_manager.apply_theme_to_widget(tab_frame, "Frame")
                        notebook.add(tab_frame, text=tab_title)
                        # Recursively build the content of the tab
                        self._build_recursive(tab_frame, tab_layout.get("rows", []))
                    widget = notebook

                elif widget_type == "Treeview":
                    # Create a container for Treeview + Scrollbars
                    tree_container = tk.Frame(row_frame)
                    self.theme_manager.apply_theme_to_widget(tree_container, "Frame")
                    v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
                    h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal")

                    tree_options = options.copy() # Work with options copy
                    # Link scrollbars to treeview
                    tree_options['yscrollcommand'] = v_scrollbar.set
                    tree_options['xscrollcommand'] = h_scrollbar.set

                    # Extract Treeview specific configurations from options
                    columns = tree_options.pop("columns", []) # List of column identifiers
                    headings = tree_options.pop("headings", []) # List of display names for headings
                    widths = tree_options.pop("widths", {}) # Dict of column_id: width
                    anchors = tree_options.pop("anchors", {}) # Dict of column_id: anchor (w, e, center)
                    show = tree_options.pop("show", "tree headings") # Control visibility ('tree', 'headings')

                    # Create the Treeview widget
                    tree = widget_class(tree_container, **tree_options)

                    # Configure scrollbar commands
                    v_scrollbar.config(command=tree.yview)
                    h_scrollbar.config(command=tree.xview)

                    # Configure Treeview columns and headings
                    tree['columns'] = columns
                    tree['show'] = show

                    # Configure the special '#0' column (tree column) if shown
                    if 'tree' in show:
                        tree.column("#0", width=widths.get("#0", 150), anchor=anchors.get("#0", 'w'))
                        tree.heading("#0", text=headings[0] if headings else "Tree") # Use first heading for #0 if provided
                    else:
                         tree.column("#0", width=0, stretch=tk.NO) # Hide tree column if not in 'show'

                    # Configure the data columns
                    col_start_index = 1 if 'tree' in show else 0 # Headings list index offset
                    for i, col_id in enumerate(columns):
                        col_idx_in_headings = i + col_start_index
                        heading_text = headings[col_idx_in_headings] if col_idx_in_headings < len(headings) else col_id.capitalize()
                        width = widths.get(col_id, 100) # Default width 100
                        anchor = anchors.get(col_id, 'w') # Default anchor 'w' (west)
                        tree.column(col_id, width=width, anchor=anchor)
                        tree.heading(col_id, text=heading_text)

                    # Pack scrollbars and treeview within their container
                    v_scrollbar.pack(side="right", fill="y")
                    h_scrollbar.pack(side="bottom", fill="x")
                    tree.pack(side="left", fill="both", expand=True)

                    widget = tree # The Treeview widget itself is stored

                    # Pack the container frame (tree_container)
                    pack_options = col.get("pack_options", {})
                    default_pack_options = {"side": "left", "expand": True, "fill": "both", "padx": 5, "pady": 2}
                    default_pack_options.update(pack_options)
                    tree_container.pack(**default_pack_options)


                elif widget_type == "Picture":
                    filepath = options.pop("filepath", None)
                    width = options.pop("width", None)
                    height = options.pop("height", None)
                    widget = widget_class(row_frame, filepath=filepath, width=width, height=height, **options)

                elif widget_type == "ColorPicker": # Handle ColorPicker creation
                    initial_color = options.pop("initial_color", "#ffffff")
                    button_text = options.pop("button_text", "Choose Color")
                    show_hex = options.pop("show_hex", True)
                    # Handle command specifically for ColorPicker (passed to its constructor)
                    cp_command_func = None
                    cp_command_name = options.pop("command", None) # Get command name/func from options
                    if isinstance(cp_command_name, str):
                         logging.warning(f"Command '{cp_command_name}' for ColorPicker '{widget_name}' seems to be a string. Ensure it was mapped.")
                         cp_command_func = cp_command_name # Pass string or mapped func
                    elif callable(cp_command_name):
                         cp_command_func = cp_command_name

                    widget = widget_class(row_frame,
                                          initial_color=initial_color,
                                          button_text=button_text,
                                          show_hex=show_hex,
                                          command=cp_command_func, # Pass the mapped command
                                          **options) # Pass remaining standard Frame options


                # --- Create Standard Widget (if not handled by special cases above) ---
                if widget is None: # If not a Notebook, Treeview, Picture, or ColorPicker
                    try:
                        # Pass the mapped command_func if it exists and applicable
                        # Radiobutton command is not typically set individually, but via group interaction
                        if command_func and 'command' in widget_class.__init__.__code__.co_varnames and widget_type not in ["Radiobutton", "ttk.Radiobutton"]:
                             options['command'] = command_func
                        widget = widget_class(row_frame, **options)
                    except tk.TclError as e:
                         logging.error(f"Error creating widget '{widget_name}' ({widget_type}) with options {options}: {e}")
                         widget = tk.Label(row_frame, text=f"Error creating {widget_type}", fg="red") # Display error in GUI
                    except Exception as e:
                         logging.error(f"General error creating widget '{widget_name}' ({widget_type}): {e}")
                         widget = tk.Label(row_frame, text=f"Error: {e}", fg="red")


                # --- Apply Theme ---
                if widget:
                    self.theme_manager.apply_theme_to_widget(widget, widget_type)

                # --- Packing (if not handled by special widget logic like Treeview or RadioGroup) ---
                # RadioGroup frame is packed within the 'group' block, Treeview container is packed above
                if widget and widget_type not in ["Treeview"]:
                    pack_options = col.get("pack_options", {})
                    # Provide sensible default packing based on widget type
                    if widget_type in ["Entry", "ttk.Entry", "Combobox", "ttk.Combobox", "Text", "Listbox", "Spinbox", "ttk.Spinbox"]:
                        default_pack_options = {"side": "left", "expand": True, "fill": "x", "padx": 5, "pady": 2}
                    elif widget_type in ["Notebook", "Frame", "LabelFrame"]:
                         default_pack_options = {"side": "left", "expand": True, "fill": "both", "padx": 5, "pady": 2}
                    elif widget_type == "Separator":
                         # Separator needs fill based on orientation
                         orient = widget.cget("orient")
                         fill = "x" if orient == "horizontal" else "y"
                         default_pack_options = {"side": "top", "expand": False, "fill": fill, "padx": 5, "pady": 5}
                    elif widget_type == "ColorPicker": # Sensible default for ColorPicker (doesn't usually expand)
                         default_pack_options = {"side": "left", "expand": False, "fill": "none", "padx": 5, "pady": 2}
                    # --- NEU: Standard-Packing für Canvas ---
                    elif widget_type == "Canvas":
                         default_pack_options = {"side": "left", "expand": True, "fill": "both", "padx": 5, "pady": 2}
                    else: # Buttons, Labels, Check/Radio (individual), Scale, Picture etc.
                        default_pack_options = {"side": "left", "expand": False, "fill": "none", "padx": 5, "pady": 2}

                    # Update defaults with any specific pack_options from YAML
                    default_pack_options.update(pack_options)
                    widget.pack(**default_pack_options)

                # --- Store Widget Reference by Name ---
                # Store the actual widget (or special container like Notebook/Treeview)
                # Do not store the Radiobutton group frame itself under the group name, only the variable.
                if widget and widget_name:
                    if widget_name in self.widgets:
                         logging.warning(f"Duplicate widget name '{widget_name}' detected. Overwriting.")
                    self.widgets[widget_name] = widget


    def _build_grid(self, parent_container, grid_layout):
        """
        Builds widgets in a grid layout.

        Args:
            parent_container: The Tkinter container widget (e.g., Frame) to build into.
            grid_layout (list): A list of dictionaries, where each dictionary represents a widget with row/column info.
        """
        # --- NEU: Spalten- und Zeilengewichte aus dem Layout setzen ---
        layout = getattr(self, "_current_layout", None)
        if layout is None:
            # Versuche, das Layout aus dem Aufruf zu bekommen (siehe build())
            import inspect
            frame = inspect.currentframe()
            outer_frames = inspect.getouterframes(frame)
            for f in outer_frames:
                if "layout" in f.frame.f_locals:
                    layout = f.frame.f_locals["layout"]
                    break

        # Spaltengewichte setzen
        if layout and "column_weights" in layout:
            for col, weight in layout["column_weights"].items():
                parent_container.grid_columnconfigure(int(col), weight=weight)
        # Zeilengewichte setzen
        if layout and "row_weights" in layout:
            for row, weight in layout["row_weights"].items():
                parent_container.grid_rowconfigure(int(row), weight=weight)

        # 1. Mapping von Namen zu Frame-Widgets (nur für Frames im Grid)
        frame_widgets = {}
        for widget_data in grid_layout:
            if widget_data.get("type") == "Frame" and "name" in widget_data:
                # Sicherstellen, dass options immer ein Dictionary ist, bevor .copy() aufgerufen wird
                options = (widget_data.get("options") or {}).copy()
                grid_options = widget_data.get("grid_options", {"padx": 5, "pady": 5})
                widget = tk.Frame(parent_container, **options)
                widget.grid(row=widget_data.get("row", 0), column=widget_data.get("column", 0), **grid_options)
                self.theme_manager.apply_theme_to_widget(widget, "Frame")
                frame_widgets[widget_data["name"]] = widget
                if widget_data["name"] not in self.widgets:
                    self.widgets[widget_data["name"]] = widget

        # 2. Alle anderen Widgets platzieren (Buttons etc.)
        for widget_data in grid_layout:
            if widget_data.get("type") == "Frame":
                continue  # Schon oben erstellt

            parent_name = widget_data.get("parent")
            if parent_name and parent_name in frame_widgets:
                container = frame_widgets[parent_name]
            else:
                container = parent_container

            row = widget_data.get("row", 0)
            column = widget_data.get("column", 0)
            widget_type = widget_data.get("type")
            widget_name = widget_data.get("name")
            # Sicherstellen, dass options immer ein Dictionary ist, bevor .copy() aufgerufen wird
            options = (widget_data.get("options") or {}).copy()
            grid_options = widget_data.get("grid_options", {"padx": 5, "pady": 5})

            widget_class = self._resolve_widget_class(widget_type)
            if not widget_class:
                logging.error(f"Unknown widget type '{widget_type}' in grid layout.")
                continue

            try:
                widget = widget_class(container, **options)
                widget.grid(row=row, column=column, **grid_options)
                self.theme_manager.apply_theme_to_widget(widget, widget_type)
                if widget_name:
                    self.widgets[widget_name] = widget
            except Exception as e:
                logging.error(f"Error creating widget '{widget_name}' in grid layout: {e}")


    def _resolve_widget_class(self, widget_type):
        """Maps a widget type string (from YAML) to its corresponding Tkinter class."""
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
            "Canvas": tk.Canvas, # <-- NEU: Canvas hinzugefügt
            # ttk (themed)
            "ttk.Button": ttk.Button,
            "ttk.Checkbutton": ttk.Checkbutton,
            "ttk.Radiobutton": ttk.Radiobutton,
            "ttk.Entry": ttk.Entry,
            "ttk.Scale": ttk.Scale,
            "ttk.Spinbox": ttk.Spinbox,
            "Combobox": ttk.Combobox, # Explicit ttk version
            "Separator": ttk.Separator, # Explicit ttk version
            "Notebook": ttk.Notebook, # Explicit ttk version
            "Treeview": ttk.Treeview, # Explicit ttk version
            # Custom Wirdgets
            "Card": Card,
            "InfoBox": InfoBox,
            "Picture": Picture,
            "ColorPicker": ColorPicker, # Added ColorPicker,
            "HtmlPreviewArea": HtmlPreviewArea # Added HtmlPreviewArea
        }

        resolved_class = mapping.get(widget_type)
        if resolved_class is None:
            # Try adding 'ttk.' prefix if not found (common convention)
            if not widget_type.startswith("ttk."):
                resolved_class = mapping.get(f"ttk.{widget_type}")
            if resolved_class is None:
                logging.error(f"Unknown widget type: '{widget_type}'")
                return None
        return resolved_class

    @classmethod
    def get_widget_class_mapping(cls):
        """Return the widget type to class mapping used by _resolve_widget_class."""
        # Copy the mapping from _resolve_widget_class
        return {
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
            "Canvas": tk.Canvas,
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
            "Card": Card,
            "InfoBox": InfoBox,
            "Picture": Picture,
            "ColorPicker": ColorPicker,
            "HtmlPreviewArea": HtmlPreviewArea,
        }

    def get_widget(self, name):
        """
        Retrieves a widget object by its assigned name.

        Args:
            name (str): The name of the widget (from YAML 'name' field).

        Returns:
            The widget object, or None if not found.
        """
        widget = self.widgets.get(name)
        if widget is None:
            # Check if the name might refer to a variable group (like Radiobuttons)
            # which doesn't have a single widget associated with the group name.
            if name in self.widget_vars:
                 # It's okay if it's just a variable name (e.g., radio group)
                 # Return None because there's no single *widget* for the group name.
                 return None
            # Only log error if name is not found in widgets *and* not in variables
            logging.error(f"Widget '{name}' not found.")
        return widget

    def get_widget_value(self, name):
        """
        Gets the current value from a widget or its associated variable by name.
        Handles different widget types appropriately.

        Args:
            name (str): The name of the widget or variable group (from YAML 'name' or 'group').

        Returns:
            The current value of the widget/variable, or None if not applicable/found.
        """
        # --- PRIORITY 1: Check if the name directly corresponds to a stored variable ---
        # This is the primary way to get values for Radiobutton groups, Checkbuttons, Entries, etc.
        if name in self.widget_vars:
            var = self.widget_vars.get(name)
            if var:
                try:
                    return var.get()
                except tk.TclError as e:
                    logging.error(f"Error getting value from variable '{name}': {e}")
                    return None
            else:
                 # Should not happen if name is in dict keys, but safety check
                 logging.warning(f"Variable '{name}' found in dict keys but object is None.")
                 return None

        # --- PRIORITY 2: If no direct variable found, try finding the widget by name ---
        widget = self.get_widget(name)
        if widget is None:
            # Error message already logged by get_widget if truly not found
            # Or it was a variable-only name (handled above)
            return None

        # --- PRIORITY 3: Get value based on widget type (for widgets without direct var or as fallback) ---
        var = None # Reset var for this section

        # Fallback: Try to find the variable associated with an *individual* Radiobutton
        # This is NOT the recommended way (use group name), but included for potential edge cases.
        if isinstance(widget, (tk.Radiobutton, ttk.Radiobutton)):
             try:
                 # Get the Tcl name of the variable linked to this specific button
                 var_name_tcl = str(widget.cget('variable'))
                 # Find the corresponding tk.Variable object in our storage
                 found_var = None
                 for group_name, tk_var in self.widget_vars.items():
                     if str(tk_var) == var_name_tcl:
                         found_var = tk_var
                         logging.warning(f"Getting value via individual Radiobutton name '{name}'. Recommended: Use group name ('{group_name}').")
                         break
                 var = found_var # Assign if found
             except tk.TclError:
                 logging.error(f"Could not get variable Tcl name for Radiobutton '{name}'.")

        # If a variable was found (e.g., via the Radiobutton fallback)
        if var:
             try:
                 return var.get()
             except tk.TclError as e:
                 logging.error(f"Error getting value from fallback variable for widget '{name}': {e}")
                 return None

        # --- Specific Widget Type Value Retrieval (if no variable method worked) ---
        if isinstance(widget, (tk.Entry, ttk.Entry)):
            return widget.get()
        elif isinstance(widget, tk.Text):
            return widget.get("1.0", tk.END).strip() # Get text from start to end, remove trailing newline/whitespace
        elif isinstance(widget, tk.Listbox):
            try:
                indices = widget.curselection() # Returns tuple of selected line indices
                return [widget.get(i) for i in indices] if indices else [] # Return list of selected items
            except tk.TclError as e:
                 logging.error(f"Error getting value from Listbox '{name}': {e}")
                 return None
        elif isinstance(widget, ttk.Combobox):
             return widget.get() # Returns the currently selected/entered text
        elif isinstance(widget, ttk.Treeview):
             try:
                 return widget.selection() # Returns tuple of selected item IDs (e.g., ('I001', 'I002'))
             except tk.TclError as e:
                 logging.error(f"Error getting selection from Treeview '{name}': {e}")
                 return None
        elif isinstance(widget, ColorPicker): # Get value for custom ColorPicker
             return widget.get_color() # Use the widget's specific method
        # --- NEU: Canvas hat keinen direkten 'Wert' ---
        elif isinstance(widget, tk.Canvas):
             logging.warning(f"Getting value for Canvas widget '{name}' is not supported via get_widget_value. Access the widget directly.")
             return None

        # Add other specific widget value retrievals here if needed

        # --- Final Fallback ---
        # Log a warning if value retrieval isn't explicitly handled for this type
        # (Avoid warning for Radiobuttons here, as group retrieval is the primary method)
        if widget is not None and not isinstance(widget, (tk.Radiobutton, ttk.Radiobutton, tk.Canvas)):
             logging.warning(f"Getting value for widget type '{type(widget).__name__}' named '{name}' is not explicitly supported via standard get_widget_value. Returning None.")

        # If no method applied, return None
        # logging.warning(f"Could not determine how to get value for widget '{name}' of type {type(widget).__name__}. Returning None.") # Reduced verbosity
        return None


    def set_widget_option(self, name, option, value):
        """
        Sets an option for a widget or its associated variable by name.

        Args:
            name (str): The name of the widget or variable group.
            option (str): The name of the option to set (e.g., "text", "value", "state").
            value: The new value for the option.
        """
        # --- PRIORITY 1: Check if setting 'value' on a known variable ---
        # This allows setting the value of Radiobutton groups, Checkbuttons, Scales etc. by name
        if name in self.widget_vars and option == "value":
            var = self.widget_vars.get(name)
            if isinstance(var, tk.Variable): # Ensure it's a Tkinter variable
                try:
                    var.set(value)
                    logging.info(f"Set value for variable/group '{name}' to '{value}'.")
                    return # Value set successfully via variable
                except tk.TclError as e:
                    logging.error(f"Error setting value for variable/group '{name}': {e}")
                    return # Error occurred
            # If 'name' is in widget_vars but not a tk.Variable, fall through to widget logic

        # --- PRIORITY 2: Find the widget and set option directly ---
        widget = self.get_widget(name)
        if widget:
            try:
                # --- Special Handling for Specific Options/Widgets ---
                if isinstance(widget, tk.Text) and option == "text":
                    widget.delete("1.0", tk.END) # Clear existing content
                    widget.insert("1.0", value) # Insert new content
                elif isinstance(widget, (tk.Entry, ttk.Entry)) and option == "text":
                     widget.delete(0, tk.END) # Clear existing content
                     widget.insert(0, value) # Insert new content
                # Setting 'value' via variable is preferred (handled above), but keep this
                # as a fallback if someone tries to set 'value' on a widget that also has a var.
                elif option == "value" and name in self.widget_vars:
                     var = self.widget_vars[name]
                     var.set(value)
                elif isinstance(widget, ttk.Combobox) and option == "values":
                     widget['values'] = value # Set the list of dropdown items
                elif isinstance(widget, ColorPicker) and option == "color":
                     widget.set_color(value) # Use the custom widget's method
                # Example for Treeview (requires dedicated methods for complex data)
                # elif isinstance(widget, ttk.Treeview) and option == 'data':
                #     self.clear_treeview(name)
                #     self.populate_treeview(name, value) # Assumes helper methods exist

                # --- Generic Option Setting ---
                else:
                    widget.config(**{option: value}) # Use config for standard options

                # Optional: Re-apply theme if state changes affect appearance significantly
                # self.theme_manager.apply_theme_to_widget(widget, type(widget).__name__) # Might be overkill

            except tk.TclError as e:
                logging.error(f"Error setting option '{option}' for widget '{name}': {e}")
        elif name not in self.widget_vars: # Only log error if neither widget nor variable was found
             logging.error(f"Cannot set option: Widget or variable '{name}' not found.")


    # --- Treeview Helper Methods (Examples) ---
    def clear_treeview(self, name):
        """Removes all items from a Treeview widget."""
        widget = self.get_widget(name)
        if isinstance(widget, ttk.Treeview):
            try:
                # Get all top-level item IDs and delete them recursively
                for item in widget.get_children():
                    widget.delete(item)
            except tk.TclError as e:
                logging.error(f"Error clearing Treeview '{name}': {e}")
        else:
            logging.error(f"Widget '{name}' is not a Treeview or not found.")

    def insert_treeview_item(self, name, values, parent='', index=tk.END, item_id=None, text=''):
        """
        Inserts an item into the Treeview.

        Args:
            name (str): The name of the Treeview widget.
            values (list or tuple): A list/tuple of values corresponding to the Treeview columns.
            parent (str): The item ID of the parent item (default is root '').
            index (int or str): Position to insert at (e.g., tk.END, 0).
            item_id (str, optional): A specific ID to assign to the new item.
            text (str): Text for the primary (#0) column if 'tree' is shown.

        Returns:
            The item ID (iid) of the newly inserted item, or None on error.
        """
        widget = self.get_widget(name)
        if isinstance(widget, ttk.Treeview):
            try:
                # Ensure values is a list or tuple if provided
                if values is not None and not isinstance(values, (list, tuple)):
                    values = [values] # Make it a list if single value passed

                # Insert item and return its ID
                iid = widget.insert(parent, index, iid=item_id, text=text, values=values)
                return iid
            except tk.TclError as e:
                logging.error(f"Error inserting item into Treeview '{name}': {e}")
                return None
        else:
            logging.error(f"Widget '{name}' is not a Treeview or not found.")
            return None

    def get_treeview_item(self, name, item_id):
        """
        Gets the data associated with a specific Treeview item ID.

        Args:
            name (str): The name of the Treeview widget.
            item_id (str): The ID of the item to retrieve.

        Returns:
            A dictionary containing item data (e.g., 'text', 'values', 'tags'), or None on error.
        """
        widget = self.get_widget(name)
        if isinstance(widget, ttk.Treeview):
            try:
                if widget.exists(item_id):
                    return widget.item(item_id) # Returns dict like {'text': '...', 'values': [...], ...}
                else:
                    logging.warning(f"Item '{item_id}' does not exist in Treeview '{name}'.")
                    return None
            except tk.TclError as e:
                logging.error(f"Error getting item '{item_id}' from Treeview '{name}': {e}")
                return None
        else:
            logging.error(f"Widget '{name}' is not a Treeview or not found.")
            return None

    def run(self):
        """Starts the Tkinter main event loop."""
        self.root.mainloop()
