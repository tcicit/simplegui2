# /home/tci/Dokumente/Entwicklung/Python/simpleGUI2/demo_app_yaml.py
import tkinter as tk
#from simplegui.core import SimpleGUI
#from simplegui.menu_manager import MenuManager
from simplegui.messages import Messages
from simplegui.filedialogs import FileDialogs
from simplegui.yaml_loader import load_yaml_layout
import random
import io
try:
    from PIL import Image
    PIL_AVAILABLE_FOR_SAVE = True
except ImportError:
    PIL_AVAILABLE_FOR_SAVE = False
    print("WARNUNG: Pillow (PIL) nicht gefunden. Speichern von Canvas ist nicht möglich.")
# --------------------


def register_user(app):
    try:
        username = app.get_widget_value("username_entry")
        password = app.get_widget_value("password_entry")
        terms = app.get_widget_value("terms_check")
    except Exception as e:
        Messages.error("Fehler", f"Fehler beim Auslesen der Eingabefelder:\n{e}")
        return

    if username is None or password is None or terms is None:
        Messages.error("Fehler", "Mindestens ein Eingabefeld konnte nicht gefunden werden.")
        return

    if username and password:
        if terms == 1:
            Messages.info("Registrieren", f"Benutzer '{username}' registriert!\nAGB akzeptiert.")
            try:
                app.set_widget_option("username_entry", "text", "")
                app.set_widget_option("password_entry", "text", "")
                app.set_widget_option("terms_check", "value", 0)
            except Exception as e:
                Messages.warning("Warnung", f"Fehler beim Zurücksetzen der Felder:\n{e}")
        else:
            Messages.warning("Registrieren", "Bitte akzeptieren Sie die AGB.")
    else:
        Messages.warning("Registrieren", "Benutzername und Passwort benötigt.")


def login_user(app):
    try:
        Messages.info("Login", "Login erfolgreich (Dummy).")
    except Exception as e:
        Messages.error("Fehler", f"Fehler beim Login:\n{e}")

# --- Treeview Functions ---
# ... (populate_treeview, clear_treeview_cmd, show_tree_selection - unverändert) ...
def populate_treeview(app):
    """Füllt die Treeview-Tabelle mit Beispieldaten."""
    print("Fülle Treeview...")
    try:
        app.clear_treeview("data_table")
    except Exception as e:
        Messages.error("Fehler", f"Fehler beim Leeren der Tabelle:\n{e}")
        return

    data = [
        (101, "Apfel", random.randint(1, 100)),
        (102, "Banane", random.randint(1, 100)),
        (103, "Kirsche", random.randint(1, 100)),
        (201, "Orange", random.randint(1, 100)),
        (202, "Zitrone", random.randint(1, 100)),
    ]
    try:
        for item_values in data:
            app.insert_treeview_item("data_table", values=item_values)
        Messages.info("Treeview", "Tabelle wurde gefüllt.")
    except Exception as e:
        Messages.error("Fehler", f"Fehler beim Füllen der Tabelle:\n{e}")

def clear_treeview_cmd(app):
    """Leert die Treeview-Tabelle."""
    print("Leere Treeview...")
    try:
        app.clear_treeview("data_table")
        Messages.info("Treeview", "Tabelle wurde geleert.")
    except Exception as e:
        Messages.error("Fehler", f"Fehler beim Leeren der Tabelle:\n{e}")

def show_tree_selection(app):
    """Zeigt die aktuell ausgewählten Elemente im Treeview an."""
    print("Zeige Treeview Auswahl...")
    try:
        selected_ids = app.get_widget_value("data_table")
    except Exception as e:
        Messages.error("Fehler", f"Fehler beim Auslesen der Auswahl:\n{e}")
        return

    if not selected_ids:
        Messages.info("Treeview Auswahl", "Kein Element ausgewählt.")
        return

    details = []
    for item_id in selected_ids:
        try:
            item_data = app.get_treeview_item("data_table", item_id)
            if item_data:
                details.append(f"ID: {item_id}, Werte: {item_data.get('values', 'N/A')}")
            else:
                details.append(f"ID: {item_id} (Daten nicht gefunden)")
        except Exception as e:
            details.append(f"ID: {item_id} (Fehler: {e})")
    Messages.info("Treeview Auswahl", "\n".join(details))

def show_all_values(app):
    """Zeigt Werte von verschiedenen Widgets an."""
    print("Zeige Werte...")
    values = []
    try:
        username = app.get_widget_value('username_entry')
        terms = app.get_widget_value('terms_check')
        color = app.get_widget_value('color_combo')
        rating = app.get_widget_value('rating_scale')
        count = app.get_widget_value('count_spin')
        radio_value = app.get_widget_value('radio_group')
        bg_color = app.get_widget_value('background_color_picker')
    except Exception as e:
        Messages.error("Fehler", f"Fehler beim Auslesen der Werte:\n{e}")
        return

    values.append(f"Username: {username if username is not None else '(nicht gefunden)'}")
    values.append(f"Password: ****")
    values.append(f"AGB Akzeptiert: {'Ja' if terms == 1 else 'Nein'}")
    values.append(f"Lieblingsfarbe: {color if color is not None else '(nicht gefunden)'}")
    values.append(f"Bewertung: {rating if rating is not None else '(nicht gefunden)'}")
    values.append(f"Anzahl: {count if count is not None else '(nicht gefunden)'}")
    values.append(f"Option (Wert): {radio_value if radio_value is not None else '(nicht gefunden)'}")
    values.append(f"Hintergrundfarbe: {bg_color if bg_color is not None else '(nicht gefunden)'}")

    Messages.info("Aktuelle Werte (Auswahl)", "\n".join(values))

def change_label(app):
    """Ändert den Text eines Labels dynamisch."""
    print("Ändere Label...")
    new_text = f"Geändert um {random.randint(1,100)}"
    try:
        app.set_widget_option("info_label", "text", new_text)
    except Exception as e:
        Messages.error("Fehler", f"Label konnte nicht geändert werden:\n{e}")


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
def set_color_red(app):
    """Sets the ColorPicker value to red programmatically."""
    print("Setze Farbe auf Rot...")
    app.set_widget_option("background_color_picker", "color", "#ff0000")

# --- Canvas Funktionen ---
def draw_on_canvas(app):
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

def clear_canvas(app):
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

def save_canvas_image(app):
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

def save_text_to_file(app):
    """Speichert den Inhalt des Textbereichs in einer Datei."""
    text_widget = app.get_widget("text_view_area")
    if text_widget:
        try:
            file_path = FileDialogs.save_file_as(
                defaultextension=".txt",
                filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = text_widget.get("1.0", tk.END).strip()
                    file.write(content)
                Messages.info("Erfolg", f"Text erfolgreich gespeichert:\n{file_path}")
            else:
                print("Speichern abgebrochen.")
        except Exception as e:
            Messages.error("Fehler", f"Fehler beim Speichern der Datei:\n{e}")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def load_text_from_file(app):
    """Lädt den Inhalt einer Datei in den Textbereich."""
    text_widget = app.get_widget("text_view_area")
    if text_widget:
        try:
            file_path = FileDialogs.open_file(filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")])
            if file_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    text_widget.delete("1.0", tk.END)
                    text_widget.insert("1.0", content)
                Messages.info("Erfolg", f"Text erfolgreich geladen:\n{file_path}")
            else:
                print("Laden abgebrochen.")
        except Exception as e:
            Messages.error("Fehler", f"Fehler beim Laden der Datei:\n{e}")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def clear_text_area(app):
    """Leert den Textbereich."""
    text_widget = app.get_widget("text_view_area")
    if text_widget:
        text_widget.delete("1.0", tk.END)
        Messages.info("Erfolg", "Textbereich geleert.")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")


