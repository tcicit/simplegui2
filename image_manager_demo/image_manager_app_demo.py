import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout
import simplegui.core_functions as core_commands  # Neues Modul mit den Befehlsfunktionen
import image_manager_app_functions as app_commands  # Neues Modul mit den Befehlsfunktionen
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
# Hier erstellen wir die Hauptanwendung und laden das Layout.
# Wir verwenden die Funktion setup_layout, um das Layout zu laden und die Befehle zuzuordnen.
# Diese Funktion kümmert sich um die Rekursion und das Mapping der Befehle.
# Wir verwenden die YAML-Datei "image_manager_app_layout.yaml" für das Layout.
# Diese Datei sollte im gleichen Verzeichnis wie dieses Skript liegen.
# Wenn Sie die Datei an einem anderen Ort gespeichert haben, passen Sie den Pfad entsprechend an.
root = tk.Tk()
app = SimpleGUI(root, title="Image ManagerDemo App", size="1200x600")

setup_layout(app, "image_manager_app_layout.yaml", commands)

# Anwendung starten
# Hier starten wir die Anwendung. Die Methode run() startet die Hauptschleife der Anwendung.
# Diese Methode blockiert den Code, bis die Anwendung geschlossen wird.
# Während die Anwendung läuft, können Benutzer mit der GUI interagieren.
# Die Anwendung bleibt aktiv, bis der Benutzer das Fenster schließt.
# Dies ist der Hauptpunkt, an dem die Anwendung tatsächlich gestartet wird.
# Die Anwendung wird in einer Endlosschleife ausgeführt, die auf Benutzerinteraktionen wartet.
app.run()
