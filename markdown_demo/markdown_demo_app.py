import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout
import simplegui.core_functions as core_commands  # Neues Modul mit den Befehlsfunktionen
import markdown_demo_app_functions as app_commands
import os # Hinzugefügt für os.path.exists
from simplegui.custom_widgets import HtmlPreviewArea  # Anpassung: Importieren der HtmlPreviewArea
import inspect


# --- Commands ---
# Hier importieren wir die Funktionen aus den Modulen
# und erstellen ein Dictionary, das die Funktionsnamen den Funktionen zuordnet.
# Dies ermöglicht eine einfache Zuordnung der Befehle im Layout.
commands = {
    name: func
    for module in [core_commands, app_commands]
    for name, func in inspect.getmembers(module, inspect.isfunction)
}

# --- Setup ---
root = tk.Tk()
app = SimpleGUI(root, title="Markdown Editor", size="1000x700")

# --- Konfiguration laden (VOR dem Layout-Aufbau) ---
config = app_commands.load_config()
saved_css_path = config.get("css_path")

if saved_css_path and os.path.exists(saved_css_path):
    print(f"Lade gespeicherte CSS-Konfiguration: {saved_css_path}")
    # Nur CSS-Inhalt laden, KEINE Vorschau-Aktualisierung hier!
    app_commands.apply_css_from_path(app, saved_css_path)
else:
    print("Keine gültige CSS-Konfiguration gefunden oder Datei existiert nicht.")

setup_layout(app, "markdown_demo_app_layout.yaml", commands)

# --- Event-Bindings nach dem Layout-Aufbau ---
# Textänderung-Event verbinden
editor = app.get_widget("editor_area")
if editor:
    def on_change(event=None):
        editor.edit_modified(0)
        app_commands.on_text_change(app)
    editor.bind("<<Modified>>", on_change)

    # Key-Binding für Bild einfügen (Strg+I)
    # Wir verwenden eine Lambda-Funktion, um das 'app'-Objekt an die Funktion zu übergeben
    editor.bind("<Control-i>", lambda event: app_commands.insert_image(app))
    # Optional für macOS: editor.bind("<Command-i>", lambda event: app_commands.insert_image(app))    

# Initiale Vorschau rendern (jetzt mit potenziell geladenem CSS)
app_commands.on_text_change(app)

app.run()
