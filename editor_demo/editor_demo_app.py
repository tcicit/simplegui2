import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout
import simplegui.core_functions as core_commands
import editor_demo_app_functions as app_commands
import inspect

# --- Commands ---
commands = {
    name: func
    for module in [core_commands, app_commands]
    for name, func in inspect.getmembers(module, inspect.isfunction)
}

# --- Setup ---
root = tk.Tk()
app = SimpleGUI(root, title="Text Editor", size="800x600")

# Layout und Menü laden
setup_layout(app, "editor_demo_app_layout.yaml", commands)

print("Lade Buffer")
# --- Widgets ---
# Nach dem Laden des Layouts den Undo-Buffer initialisieren
app_commands.initialize_undo_buffer(app)  # Undo-Buffer initialisieren

# Tastenkombination für Undo (Ctrl+Z) binden
root.bind("<Control-z>", lambda event: app_commands.undo_last_action(app))

# Anwendung starten
app.run()