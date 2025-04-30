# /home/tci/Dokumente/Entwicklung/Python/simpleGUI2/simplegui/custom_widgets.py
import tkinter as tk
from tkinter import colorchooser # Import color chooser
from simplegui.theme_manager import ThemeManager
import logging
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    # Logging warning already happens in the Picture class if needed

# --- Existing Card and InfoBox classes ---
class Card(tk.Frame):
    # ... (keep existing Card code) ...
    def __init__(self, parent, title="", content="", **kwargs):
        # Get theme settings
        theme = ThemeManager.theme # Access class variable directly
        bg_color = theme.get("card_bg", "#ffffff")
        border_color = theme.get("card_border", "#dddddd") # Example border color
        title_font = (theme.get("font_family", "Arial"), theme.get("font_size", 10) + 2, "bold") # Slightly larger bold font
        content_font = (theme.get("font_family", "Arial"), theme.get("font_size", 10))
        label_fg = theme.get("label_fg", "#000000")

        # Apply theme settings to the Frame itself
        # Use highlightbackground/highlightcolor for border effect if relief isn't enough
        super().__init__(parent,
                         bg=bg_color,
                         padx=10, pady=10,
                         relief="solid", # Use solid relief for border color
                         bd=1, # Border width
                         highlightbackground=border_color, # Color when not focused
                         highlightcolor=border_color, # Color when focused
                         **kwargs) # Pass other kwargs

        # Configure internal widgets with theme settings
        if title:
            tk.Label(self, text=title, font=title_font, fg=label_fg, bg=bg_color).pack(anchor="w", pady=(0, 5))
        if content:
            tk.Label(self, text=content, font=content_font, fg=label_fg, bg=bg_color).pack(anchor="w")


class InfoBox(tk.Frame):
    # ... (keep existing InfoBox code) ...
    def __init__(self, parent, message="", info_type="info", **kwargs):
        # Get theme settings for info boxes
        theme = ThemeManager.theme
        colors = {
            "info": theme.get("infobox_info_bg", "#d9edf7"),
            "warning": theme.get("infobox_warning_bg", "#fcf8e3"),
            "error": theme.get("infobox_error_bg", "#F69090")
        }
        bg_color = colors.get(info_type, colors["info"]) # Default to info color
        text_font = (theme.get("font_family", "Arial"), theme.get("font_size", 10))
        text_fg = theme.get("label_fg", "#000000") # Use standard label fg color

        # Apply theme settings to the Frame
        super().__init__(parent, bg=bg_color, padx=10, pady=10, relief="solid", bd=1, **kwargs)

        # Configure internal label with theme settings
        tk.Label(self, text=message, bg=bg_color, fg=text_fg, font=text_font).pack(anchor="center")


class Picture(tk.Label):
    # ... (keep existing Picture code) ...
    def __init__(self, parent, filepath=None, width=None, height=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._photo_image = None # Crucial: Keep reference

        if not PIL_AVAILABLE:
            self.config(text="Error: Pillow not installed", fg="red")
            return
        if not filepath:
            self.config(text="Error: Image filepath missing", fg="red")
            return

        try:
            img = Image.open(filepath)
            original_width, original_height = img.size

            # Calculate new size while maintaining aspect ratio if only one dimension is given
            if width and not height:
                ratio = width / original_width
                height = int(original_height * ratio)
            elif height and not width:
                ratio = height / original_height
                width = int(original_width * ratio)

            # Resize if width or height is specified
            if width and height:
                img = img.resize((width, height), Image.Resampling.LANCZOS)

            self._photo_image = ImageTk.PhotoImage(img)
            self.config(image=self._photo_image)

        except FileNotFoundError:
            logging.error(f"Image file not found: {filepath}")
            self.config(text=f"Error: File not found\n{filepath}", fg="red", justify="left")
        except Exception as e:
            logging.error(f"Error loading image {filepath}: {e}")
            self.config(text=f"Error loading image:\n{e}", fg="red", justify="left")


# --- NEW ColorPicker Widget ---
class ColorPicker(tk.Frame):
    """A custom widget with a button to open the color chooser and display the selected color."""
    def __init__(self, parent, initial_color="#ffffff", button_text="Choose Color", show_hex=True, command=None, **kwargs):
        """
        Args:
            parent: The master widget.
            initial_color (str): The initial color hex string (e.g., "#RRGGBB").
            button_text (str): Text displayed on the button.
            show_hex (bool): If True, displays the selected hex color code next to the preview.
            command (callable, optional): A function to call after a color is selected.
                                          It receives the selected hex color string as an argument.
            **kwargs: Additional options passed to the main tk.Frame.
        """
        theme = ThemeManager.theme
        frame_bg = theme.get("colorpicker_bg", theme.get("frame_bg", "#f0f0f0"))
        super().__init__(parent, bg=frame_bg, **kwargs) # Apply background to the container frame

        self._current_color = initial_color
        self._show_hex = show_hex
        self._external_command = command

        # --- Internal Widgets ---
        # Button to trigger the color chooser
        self.button = tk.Button(self, text=button_text, command=self._open_color_chooser)
        # Apply button theme (optional, could inherit standard button theme)
        # You might want specific theme keys like 'colorpicker_button_bg' etc.
        self.button.config(
            bg=theme.get("button_bg", "#007BFF"),
            fg=theme.get("button_fg", "#ffffff"),
            activebackground=theme.get("button_active_bg", "#0056b3"),
            activeforeground=theme.get("button_active_fg", "#ffffff"),
            relief=theme.get("button_relief", "raised"),
            bd=1,
            font=(theme.get("font_family", "Arial"), theme.get("font_size", 10))
        )
        self.button.pack(side="left", padx=(0, 5))

        # Frame to display the selected color
        self.color_display = tk.Frame(self, width=30, height=20, relief="sunken", bd=1)
        self.color_display.pack(side="left", padx=(0, 5))

        # Label to show the hex code (optional)
        self.hex_label = None
        if self._show_hex:
            self.hex_label = tk.Label(self, text=self._current_color, bg=frame_bg,
                                      fg=theme.get("label_fg", "#000000"),
                                      font=(theme.get("font_family", "Arial"), theme.get("font_size", 10)))
            self.hex_label.pack(side="left")

        # Set initial color
        self.set_color(self._current_color) # Use the method to ensure display is updated

    def _open_color_chooser(self):
        """Opens the color chooser dialog and updates the widget."""
        # askcolor returns ((r, g, b), '#rrggbb') or (None, None)
        result = colorchooser.askcolor(initialcolor=self._current_color, title="Choose Color")
        if result and result[1]: # Check if a color was chosen and hex is available
            new_color_hex = result[1]
            self.set_color(new_color_hex)
            # Execute external command if provided
            if callable(self._external_command):
                try:
                    self._external_command(self._current_color)
                except Exception as e:
                    logging.error(f"Error executing ColorPicker command: {e}")


    def get_color(self):
        """Returns the currently selected color hex string."""
        return self._current_color

    def set_color(self, color_hex):
        """Sets the color of the picker programmatically."""
        # Basic validation (can be improved)
        if isinstance(color_hex, str) and color_hex.startswith("#") and len(color_hex) in [4, 7]:
            try:
                # Update internal state
                self._current_color = color_hex
                # Update color display background
                self.color_display.config(bg=self._current_color)
                # Update hex label text if it exists
                if self.hex_label:
                    self.hex_label.config(text=self._current_color)
            except tk.TclError as e:
                logging.warning(f"Invalid color string for ColorPicker: {color_hex} - {e}")
        else:
             logging.warning(f"Attempted to set invalid color format in ColorPicker: {color_hex}")

