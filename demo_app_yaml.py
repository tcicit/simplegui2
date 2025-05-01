# /home/tci/Dokumente/Entwicklung/Python/simpleGUI2/demo_app_yaml.py
import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.menu_manager import MenuManager
from simplegui.messages import Messages
from simplegui.filedialogs import FileDialogs
from simplegui.yaml_loader import load_yaml_layout
import random
# --- NEUE IMPORTE ---
import io
try:
    from PIL import Image
    PIL_AVAILABLE_FOR_SAVE = True
except ImportError:
    PIL_AVAILABLE_FOR_SAVE = False
    print("WARNUNG: Pillow (PIL) nicht gefunden. Speichern von Canvas ist nicht möglich.")
# --------------------

# --- Dummyfunktionen ---
# ... (open_file, save_file, etc. - unverändert) ...
def open_file():
    print("Öffne Datei...")
    filename = FileDialogs.open_file()
    if filename:
        Messages.info("Datei geöffnet", filename)

def save_file():
    Messages.info("Speichern", "Datei gespeichert.")

def copy_text():
    Messages.info("Bearbeiten", "Text kopiert.")

def save_file_as():
    print("Speichern unter...")
    filename = FileDialogs.save_file_as()
    if filename:
        Messages.info("Datei gespeichert", filename)

def open_directory():
    print("Öffne Verzeichnis...")
    directory = FileDialogs.open_directory()
    if directory:
        Messages.info("Verzeichnis geöffnet", directory)

def paste_text():
    Messages.info("Bearbeiten", "Text eingefügt.")

def about():
    # Version aktualisiert
    Messages.info("Über SimpleGUI", "SimpleGUI v1.5\nMit Canvas Speichern\n(c) 2025")

def register_user():
    username = app.get_widget_value("username_entry")
    password = app.get_widget_value("password_entry")
    terms = app.get_widget_value("terms_check")
    if username and password:
         if terms == 1:
             Messages.info("Registrieren", f"Benutzer '{username}' registriert!\nAGB akzeptiert.")
             app.set_widget_option("username_entry", "text", "")
             app.set_widget_option("password_entry", "text", "")
             app.set_widget_option("terms_check", "value", 0)
         else:
             Messages.warning("Registrieren", "Bitte akzeptieren Sie die AGB.")
    else:
        Messages.warning("Registrieren", "Benutzername und Passwort benötigt.")


def login_user():
    Messages.info("Login", "Login erfolgreich (Dummy).")

# --- Treeview Functions ---
# ... (populate_treeview, clear_treeview_cmd, show_tree_selection - unverändert) ...
def populate_treeview():
    """Füllt die Treeview-Tabelle mit Beispieldaten."""
    print("Fülle Treeview...")
    app.clear_treeview("data_table") # Clear existing data first
    data = [
        (101, "Apfel", random.randint(1, 100)),
        (102, "Banane", random.randint(1, 100)),
        (103, "Kirsche", random.randint(1, 100)),
        (201, "Orange", random.randint(1, 100)),
        (202, "Zitrone", random.randint(1, 100)),
    ]
    for item_values in data:
        # Insert item with tuple/list of values matching the columns order in YAML
        app.insert_treeview_item("data_table", values=item_values)
    Messages.info("Treeview", "Tabelle wurde gefüllt.")

def clear_treeview_cmd():
    """Leert die Treeview-Tabelle."""
    print("Leere Treeview...")
    app.clear_treeview("data_table")
    Messages.info("Treeview", "Tabelle wurde geleert.")

def show_tree_selection():
    """Zeigt die aktuell ausgewählten Elemente im Treeview an."""
    print("Zeige Treeview Auswahl...")
    selected_ids = app.get_widget_value("data_table") # Returns a tuple of item IDs
    if selected_ids:
        details = []
        for item_id in selected_ids:
            item_data = app.get_treeview_item("data_table", item_id)
            if item_data:
                # item_data is a dict like {'text': '', 'image': '', 'values': [101, 'Apfel', 50], 'open': 0, 'tags': ''}
                details.append(f"ID: {item_id}, Werte: {item_data.get('values', 'N/A')}")
            else:
                details.append(f"ID: {item_id} (Daten nicht gefunden)")
        Messages.info("Treeview Auswahl", "\n".join(details))
    else:
        Messages.info("Treeview Auswahl", "Kein Element ausgewählt.")



def show_all_values():
    """Zeigt Werte von verschiedenen Widgets an."""
    print("Zeige Werte...")
    values = []
    # Get values using the names defined in the YAML layout
    values.append(f"Username: {app.get_widget_value('username_entry')}")
    values.append(f"Password: ****")
    values.append(f"AGB Akzeptiert: {'Ja' if app.get_widget_value('terms_check') == 1 else 'Nein'}")
    values.append(f"Lieblingsfarbe: {app.get_widget_value('color_combo')}")
    values.append(f"Bewertung: {app.get_widget_value('rating_scale')}")
    values.append(f"Anzahl: {app.get_widget_value('count_spin')}")

    # --- Abfrage des Radiobutton-Gruppenwerts ---
    # Stelle sicher, dass 'radio_group' der Name ist, den du in YAML unter 'group:' verwendest
    radio_value = app.get_widget_value('radio_group')
    values.append(f"Option (Wert): {radio_value}") # Zeigt den 'value' des ausgewählten Buttons an

    # --- NEW: Get ColorPicker value ---
    values.append(f"Hintergrundfarbe: {app.get_widget_value('background_color_picker')}")

    Messages.info("Aktuelle Werte (Auswahl)", "\n".join(values))

def change_label():
    """Ändert den Text eines Labels dynamisch."""
    print("Ändere Label...")
    new_text = f"Geändert um {random.randint(1,100)}"
    app.set_widget_option("info_label", "text", new_text)

def exit_app():
    print("Beende die Anwendung...")
    root.quit()

# --- NEW Callback for ColorPicker (optional, if command used in YAML) ---
def background_color_changed(selected_color):
    """Callback function executed when the background color picker changes."""
    print(f"Callback: Hintergrundfarbe geändert zu: {selected_color}")
    # Example: Change root background color dynamically
    # try:
    #     root.config(bg=selected_color)
    # except tk.TclError:
    #     print(f"Warnung: Konnte Hintergrundfarbe nicht auf {selected_color} setzen.")
    Messages.info("Farbauswahl", f"Neue Hintergrundfarbe gewählt: {selected_color}")

# --- NEW Function for the test button ---
def set_color_red():
    """Sets the ColorPicker value to red programmatically."""
    print("Setze Farbe auf Rot...")
    app.set_widget_option("background_color_picker", "color", "#ff0000")

# --- Canvas Funktionen ---
def draw_on_canvas():
    """Zeichnet zufällige Formen auf das Canvas."""
    print("Zeichne auf Canvas...")
    canvas = app.get_widget("drawing_canvas") # Hole das Canvas-Widget über seinen Namen
    if canvas and isinstance(canvas, tk.Canvas):
        # Stelle sicher, dass das Canvas bereits eine Größe hat
        canvas.update_idletasks() # Wichtig, um sicherzustellen, dass winfo_width/height korrekt sind
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 1 or height <= 1: # Prüfen, ob Canvas sichtbar ist
             Messages.warning("Canvas", "Canvas ist noch nicht sichtbar oder zu klein zum Zeichnen.")
             return

        # Zufällige Position und Größe
        x1 = random.randint(10, width - 50 if width > 60 else width - 10)
        y1 = random.randint(10, height - 50 if height > 60 else height - 10)
        x2 = x1 + random.randint(20, 50)
        y2 = y1 + random.randint(20, 50)
        # Zufällige Farbe
        color = random.choice(["red", "green", "blue", "yellow", "orange", "purple", "black"])
        # Zufällige Form
        shape_type = random.choice(["oval", "rectangle", "line"])

        if shape_type == "oval":
            canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")
        elif shape_type == "rectangle":
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        elif shape_type == "line":
            canvas.create_line(x1, y1, x2, y2, fill=color, width=random.randint(1, 4))

        # Messages.info("Canvas", f"{shape_type.capitalize()} gezeichnet.") # Optional: Weniger Popups
    elif canvas:
        Messages.error("Canvas Fehler", f"Widget 'drawing_canvas' ist kein Canvas (Typ: {type(canvas)}).")
    else:
        Messages.error("Canvas Fehler", "Widget 'drawing_canvas' nicht gefunden.")

def clear_canvas():
    """Löscht alle Zeichnungen vom Canvas."""
    print("Leere Canvas...")
    canvas = app.get_widget("drawing_canvas")
    if canvas and isinstance(canvas, tk.Canvas):
        canvas.delete("all") # Löscht alle Elemente auf dem Canvas
        Messages.info("Canvas", "Zeichenbereich geleert.")
    elif canvas:
        Messages.error("Canvas Fehler", f"Widget 'drawing_canvas' ist kein Canvas (Typ: {type(canvas)}).")
    else:
        Messages.error("Canvas Fehler", "Widget 'drawing_canvas' nicht gefunden.")

# --- NEUE FUNKTION: Canvas speichern ---
def save_canvas_image():
    """Speichert den aktuellen Inhalt des Canvas als Bilddatei (PNG, JPG)."""
    print("Speichere Canvas...")

    if not PIL_AVAILABLE_FOR_SAVE:
        Messages.error("Fehler", "Pillow (PIL) Bibliothek nicht gefunden.\nSpeichern nicht möglich.")
        return

    canvas = app.get_widget("drawing_canvas")
    if not (canvas and isinstance(canvas, tk.Canvas)):
        Messages.error("Canvas Fehler", "Widget 'drawing_canvas' nicht gefunden oder kein Canvas.")
        return

    try:
        # Dateiauswahldialog anzeigen
        filepath = FileDialogs.save_file_as(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
        )

        if not filepath:
            print("Speichern abgebrochen.")
            return # Benutzer hat abgebrochen

        # Canvas als PostScript exportieren (im Speicher)
        # WICHTIG: Benötigt Ghostscript-Installation!
        ps_data = canvas.postscript(colormode='color')

        # PostScript-Daten mit Pillow öffnen
        img = Image.open(io.BytesIO(ps_data.encode('utf-8')))

        # Bild speichern (Format wird aus Dateiendung abgeleitet)
        img.save(filepath)
        Messages.info("Canvas gespeichert", f"Zeichnung gespeichert als:\n{filepath}")

    except tk.TclError as e:
        Messages.error("Speicherfehler (Tk)", f"Fehler beim Exportieren des Canvas:\n{e}\n\nMöglicherweise fehlt Ghostscript oder es ist nicht im Systempfad.")
        print(f"TclError during canvas save: {e}")
    except ImportError:
         # Sollte durch PIL_AVAILABLE_FOR_SAVE abgefangen werden, aber sicherheitshalber
         Messages.error("Fehler", "Pillow (PIL) Bibliothek nicht gefunden.\nSpeichern nicht möglich.")
    except Exception as e:
        Messages.error("Speicherfehler", f"Ein unerwarteter Fehler ist aufgetreten:\n{e}")
        print(f"Unexpected error during canvas save: {e}")


# --- Setup ---

# Mapping von Funktionsnamen (Strings in YAML) zu tatsächlichen Python-Funktionen
command_mapping = {
    "open_file": open_file,
    "save_file": save_file,
    "save_file_as": save_file_as,
    "open_directory": open_directory,
    "exit_app": exit_app,
    "copy_text": copy_text,
    "paste_text": paste_text,
    "about": about,
    "register_user": register_user,
    "login_user": login_user,
    "show_all_values": show_all_values,
    "change_label": change_label,
    "populate_treeview": populate_treeview,
    "clear_treeview_cmd": clear_treeview_cmd,
    "show_tree_selection": show_tree_selection,
    "background_color_changed": background_color_changed, # Map the optional callback
    "set_color_red": set_color_red, # Map the test button command
    # --- Canvas Commands ---
    "draw_on_canvas": draw_on_canvas,
    "clear_canvas": clear_canvas,
    "save_canvas_image": save_canvas_image, # <-- NEUES Mapping
}

# Layout und Menü laden
layout = load_yaml_layout("layout_enhanced.yaml")
# --- Korrektur: Command Mapping für Menü ---
# Das Mapping muss *nach* dem Laden erfolgen, nicht währenddessen.
# Die load_yaml_layout Funktion wurde angepasst, um das Mapping optional zu machen.
menu_structure_raw = load_yaml_layout("menu.yaml") # Erst laden
# Dann mappen (falls Menü Commands enthält, was hier der Fall ist)
def map_menu_commands(menu_data, mapping):
     if isinstance(menu_data, dict):
         for menu_name, items in menu_data.items():
             if isinstance(items, list):
                 for i, item in enumerate(items):
                     if isinstance(item, dict) and "command" in item:
                         command_name = item["command"]
                         if isinstance(command_name, str) and command_name in mapping:
                             items[i]["command"] = mapping[command_name]
                         elif not callable(command_name):
                             # Wenn nicht mapbar und nicht schon callable, auf None setzen
                             items[i]["command"] = None
     return menu_data

menu_structure = map_menu_commands(menu_structure_raw, command_mapping)
# -----------------------------------------

# --- App Erstellung und Start ---
root = tk.Tk()
# Fenstergröße leicht erhöht für den neuen Tab
app = SimpleGUI(root, title="SimpleGUI Enhanced Demo", size="750x850")

menu = MenuManager(root)
menu.build_menu(menu_structure) # Verwende die gemappte Struktur

# Mappe die Commands im Layout-Dict *nach* dem Laden und *vor* dem Build
def map_layout_commands(layout_data, mapping):
    if isinstance(layout_data, dict):
        for key, value in layout_data.items():
            if key == "command" and isinstance(value, str):
                if value in mapping:
                    layout_data[key] = mapping[value]
                else:
                    # Keep the string if not found, core.py will handle/warn
                    # logging.warning(f"Command '{value}' found in layout but not in command_mapping.")
                    pass # Let core.py handle it
            else:
                # Rekursiv für verschachtelte Strukturen (wie Tabs, Gruppen)
                map_layout_commands(value, mapping)
    elif isinstance(layout_data, list):
        for item in layout_data:
            map_layout_commands(item, mapping)

map_layout_commands(layout, command_mapping) # Wende Mapping auf das gesamte Layout an

app.build(layout)
app.run()
