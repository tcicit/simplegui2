import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout
import simplegui.core_functions as core_commands  # Neues Modul mit den Befehlsfunktionen
import core_demo_app_functions as app_commands  # Neues Modul mit den Befehlsfunktionen
import inspect

# --- Commands ---
commands = {
    name: func
    for module in [core_commands, app_commands]
    for name, func in inspect.getmembers(module, inspect.isfunction)
}

# --- Setup ---
root = tk.Tk()
app = SimpleGUI(root, title="Demo App", size="900x700")


# Layout und Menü laden und automatisch Commands mappen
setup_layout(app, "core_demo_app_layout.yaml", commands)

# Anwendung starten
app.run()
