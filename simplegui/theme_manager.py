# /home/tci/Dokumente/Entwicklung/Python/simpleGUI2/simplegui/theme_manager.py
import tkinter as tk
from tkinter import ttk
import logging
# Import custom widgets to check instance types if needed later


class ThemeManager:
    # Expanded theme dictionary with more specific keys
    theme = {
        "font_family": "Arial",
        "font_size": 10,
        "root_bg": "#f0f0f0", # Specific background for the root window
        "frame_bg": "#f0f0f0", # Background for standard frames
        "label_fg": "#000000",
        "label_bg": "#f0f0f0", # Labels often need explicit bg matching frame
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "entry_border": "#cccccc",
        "button_bg": "#007BFF",
        "button_fg": "#ffffff",
        "button_active_bg": "#0056b3",
        "button_active_fg": "#ffffff",
        "button_relief": "raised",
        "checkbutton_bg": "#f0f0f0", # Match frame bg usually
        "radiobutton_bg": "#f0f0f0", # Match frame bg usually
        "text_bg": "#ffffff",
        "text_fg": "#000000",
        "listbox_bg": "#ffffff",
        "listbox_fg": "#000000",
        "scale_bg": "#f0f0f0",
        "scale_troughcolor": "#d3d3d3",
        "canvas_bg": "#ffffff", # <-- NEU: Hintergrund für Canvas
        "card_bg": "#ffffff", # Custom widget theming
        "card_border": "#dddddd",
        "infobox_info_bg": "#d9edf7",
        "infobox_warning_bg": "#fcf8e3",
        "infobox_error_bg" : "#ED6666",
        "picture_bg": "#f0f0f0",
        "separator_bg": "#cccccc",
        "notebook_bg": "#f0f0f0",
        "notebook_tab_bg": "#d9d9d9",
        "notebook_tab_active_bg": "#f0f0f0",
        "notebook_tab_fg": "#000000",
        "treeview_bg": "#ffffff",
        "treeview_fg": "#000000",
        "treeview_field_bg": "#ffffff",
        "treeview_heading_bg": "#e1e1e1",
        "treeview_heading_fg": "#000000",
        "treeview_heading_relief": "raised",
        "ttk_theme": "clam",
        # --- NEW Theme settings for ColorPicker ---
        "colorpicker_bg": "#f0f0f0", # Background for the ColorPicker frame itself
        "colorpicker_display_border": "#a0a0a0", # Border for the color preview box
        # Optional: Specific button colors, otherwise uses default button theme
        # "colorpicker_button_bg": "#e0e0e0",
        # "colorpicker_button_fg": "#000000",
    }

    # ... (init, set_theme, get_font, _configure_ttk_styles - unverändert) ...
    def __init__(self):
        self.style = ttk.Style()
        # Apply ttk theme immediately if specified
        if "ttk_theme" in self.theme:
            try:
                available_themes = self.style.theme_names()
                if self.theme["ttk_theme"] in available_themes:
                    self.style.theme_use(self.theme["ttk_theme"])
                    logging.info(f"Using ttk theme: {self.theme['ttk_theme']}")
                else:
                    logging.warning(f"ttk theme '{self.theme['ttk_theme']}' not available. Available: {available_themes}. Using default.")
            except Exception as e:
                 logging.error(f"Failed to set ttk theme: {e}")
        # Configure custom ttk styles AFTER setting the theme
        self._configure_ttk_styles()


    @classmethod
    def set_theme(cls, new_theme_settings):
        """Update the theme dictionary with new settings."""
        cls.theme.update(new_theme_settings)
        # Re-configure ttk styles if theme changes during runtime
        # Note: This requires an instance or making _configure_ttk_styles a class method
        # For simplicity, we assume theme is set at init for now.
        # self._configure_ttk_styles() # Would need adjustment

    def get_font(self, style=None):
        """Helper to get the combined font tuple, potentially with style."""
        size = self.theme.get("font_size", 10)
        family = self.theme.get("font_family", "Arial")
        if style:
            return (family, size, style)
        return (family, size)

    def _configure_ttk_styles(self):
        """Configure ttk styles based on the theme dictionary."""
        font = self.get_font()
        heading_font = self.get_font("bold")

        try:
            # Separator
            self.style.configure("TSeparator",
                                 background=self.theme.get("separator_bg", "#cccccc"))

            # Notebook
            self.style.configure("TNotebook",
                                 background=self.theme.get("notebook_bg", "#f0f0f0"),
                                 tabmargins=[2, 5, 2, 0]) # left, top, right, bottom
            self.style.configure("TNotebook.Tab",
                                 background=self.theme.get("notebook_tab_bg", "#d9d9d9"),
                                 foreground=self.theme.get("notebook_tab_fg", "#000000"),
                                 padding=[10, 2], # horizontal, vertical
                                 font=font)
            # Style for the *selected* tab
            self.style.map("TNotebook.Tab",
                           background=[("selected", self.theme.get("notebook_tab_active_bg", "#f0f0f0"))],
                           expand=[("selected", [1, 1, 1, 0])]) # Add slight padding expansion when selected

            # Treeview
            self.style.configure("Treeview",
                                 background=self.theme.get("treeview_bg", "#ffffff"),
                                 foreground=self.theme.get("treeview_fg", "#000000"),
                                 fieldbackground=self.theme.get("treeview_field_bg", "#ffffff"),
                                 rowheight=int(self.theme.get("font_size", 10) * 2.5), # Adjust row height based on font
                                 font=font)
            # Remove border around Treeview itself if using inside a themed frame
            self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Remove default border

            # Treeview Heading
            self.style.configure("Treeview.Heading",
                                 background=self.theme.get("treeview_heading_bg", "#e1e1e1"),
                                 foreground=self.theme.get("treeview_heading_fg", "#000000"),
                                 font=heading_font,
                                 relief=self.theme.get("treeview_heading_relief", "raised"))

            # Apply base font to other common ttk widgets if not overridden by theme
            common_ttk = ["TButton", "TCheckbutton", "TRadiobutton", "TCombobox", "TEntry", "TScale", "TSpinbox"]
            for widget_style in common_ttk:
                 try:
                     self.style.configure(widget_style, font=font)
                 except tk.TclError:
                     pass # Ignore if style doesn't exist in the current ttk theme

        except tk.TclError as e:
            logging.error(f"Error configuring ttk styles: {e}")



    def apply_theme_to_root(self, root):
        """Applies basic theme settings to the root window."""
        try:
            root.configure(bg=self.theme.get("root_bg", "#f0f0f0"))
        except tk.TclError as e:
            logging.warning(f"Could not apply root background: {e}")

    def apply_theme_to_widget(self, widget, widget_type_str):
        """Applies theme settings to a specific widget based on its type."""
        # Import custom widgets locally to avoid circular dependency at module level
        from simplegui.custom_widgets import Card, InfoBox, Picture, ColorPicker # Added ColorPicker

        font = self.get_font()
        common_options = {}
        specific_options = {}

        # --- Standard Tk Widgets ---
        if isinstance(widget, tk.Frame):
             # Ensure it's not one of the custom Frame subclasses before applying default Frame bg
             if not isinstance(widget, (Card, InfoBox, ColorPicker)): # Added ColorPicker check
                specific_options["bg"] = self.theme.get("frame_bg", "#f0f0f0")
        elif isinstance(widget, tk.Label):
            # Exclude Picture widget here, handled separately
            if not isinstance(widget, Picture):
                specific_options["font"] = font
                specific_options["fg"] = self.theme.get("label_fg", "#000000")
                specific_options["bg"] = self.theme.get("label_bg", "#f0f0f0")
        elif isinstance(widget, tk.Entry):
            specific_options["font"] = font
            specific_options["bg"] = self.theme.get("entry_bg", "#ffffff")
            specific_options["fg"] = self.theme.get("entry_fg", "#000000")
            specific_options["relief"] = "sunken"
            specific_options["bd"] = 1
        elif isinstance(widget, tk.Button):
            specific_options["font"] = font
            specific_options["bg"] = self.theme.get("button_bg", "#007BFF")
            specific_options["fg"] = self.theme.get("button_fg", "#ffffff")
            specific_options["activebackground"] = self.theme.get("button_active_bg", "#0056b3")
            specific_options["activeforeground"] = self.theme.get("button_active_fg", "#ffffff")
            specific_options["relief"] = self.theme.get("button_relief", "raised")
            specific_options["bd"] = 1
        elif isinstance(widget, tk.Checkbutton):
            specific_options["font"] = font
            specific_options["bg"] = self.theme.get("checkbutton_bg", "#f0f0f0")
            specific_options["activebackground"] = self.theme.get("checkbutton_bg", "#f0f0f0")
        elif isinstance(widget, tk.Radiobutton):
            specific_options["font"] = font
            specific_options["bg"] = self.theme.get("radiobutton_bg", "#f0f0f0")
            specific_options["activebackground"] = self.theme.get("radiobutton_bg", "#f0f0f0")
        elif isinstance(widget, tk.Text):
            specific_options["font"] = font
            specific_options["bg"] = self.theme.get("text_bg", "#ffffff")
            specific_options["fg"] = self.theme.get("text_fg", "#000000")
            specific_options["relief"] = "sunken"
            specific_options["bd"] = 1
        elif isinstance(widget, tk.Listbox):
            specific_options["font"] = font
            specific_options["bg"] = self.theme.get("listbox_bg", "#ffffff")
            specific_options["fg"] = self.theme.get("listbox_fg", "#000000")
            specific_options["relief"] = "sunken"
            specific_options["bd"] = 1
        elif isinstance(widget, tk.Scale):
             specific_options["font"] = font
             specific_options["bg"] = self.theme.get("scale_bg", "#f0f0f0")
             specific_options["troughcolor"] = self.theme.get("scale_troughcolor", "#d3d3d3")
             specific_options["sliderrelief"] = "raised"
             specific_options["highlightthickness"] = 0
        elif isinstance(widget, tk.Spinbox):
             specific_options["font"] = font
             specific_options["bg"] = self.theme.get("entry_bg", "#ffffff")
             specific_options["fg"] = self.theme.get("entry_fg", "#000000")
             specific_options["buttonbackground"] = self.theme.get("frame_bg", "#f0f0f0")
             specific_options["relief"] = "sunken"
             specific_options["bd"] = 1
        elif isinstance(widget, tk.LabelFrame):
             specific_options["fg"] = self.theme.get("label_fg", "#000000")
             specific_options["bg"] = self.theme.get("frame_bg", "#f0f0f0")
             specific_options["font"] = self.get_font("bold") # Make label bold
        # --- NEU: Theming für Canvas ---
        elif isinstance(widget, tk.Canvas):
             specific_options["bg"] = self.theme.get("canvas_bg", "#ffffff")
             specific_options["highlightthickness"] = 0 # Oft gewünscht, um Standardrahmen zu entfernen


        # --- TTK Widgets ---
        elif isinstance(widget, (ttk.Combobox, ttk.Button, ttk.Checkbutton, ttk.Radiobutton,
                                 ttk.Entry, ttk.Scale, ttk.Spinbox, ttk.Separator,
                                 ttk.Notebook, ttk.Treeview)):
             pass # Styling handled by ttk.Style


        # --- Custom Widgets ---
        elif isinstance(widget, Card):
            specific_options["bg"] = self.theme.get("card_bg", "#ffffff")
        elif isinstance(widget, InfoBox):
            pass # Reads theme internally
        elif isinstance(widget, Picture):
            specific_options["bg"] = self.theme.get("picture_bg", self.theme.get("frame_bg", "#f0f0f0"))
        elif isinstance(widget, ColorPicker): # Apply theme to ColorPicker Frame
            specific_options["bg"] = self.theme.get("colorpicker_bg", self.theme.get("frame_bg", "#f0f0f0"))
            # Optionally apply theme to internal parts if needed (e.g., border color)
            try:
                border_color = self.theme.get("colorpicker_display_border", "#a0a0a0")
                if hasattr(widget, 'color_display'): # Check if internal widget exists
                    widget.color_display.config(highlightbackground=border_color, highlightcolor=border_color) # Use highlight for border
            except tk.TclError as e:
                 logging.warning(f"Could not apply theme option to internal ColorPicker part: {e}")


        # Apply collected options
        all_options = {**common_options, **specific_options}
        if all_options:
            try:
                widget.config(**all_options)
            except tk.TclError as e:
                logging.warning(f"Could not apply theme option to {widget_type_str} ({type(widget)}): {e}. Options: {all_options}")
