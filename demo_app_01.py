import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout
import simplegui.commands as commands  # Neues Modul mit den Befehlsfunktionen


# --- Setup ---
root = tk.Tk()
app = SimpleGUI(root, title="Demo App", size="800x600")

# Layout und Menü laden und automatisch Commands mappen
setup_layout(app, "image_manager_layout.yaml", commands)

# Anwendung starten
app.run()
