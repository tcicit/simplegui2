import tkinter as tk  # Importieren von tkinter für die Menüerstellung
import inspect
from simplegui.yaml_loader import load_yaml_layout
import logging # Importiere logging

def setup_layout(app, layout_file, command_mapping):
    """
    Lädt das Layout, mappt die Commands und baut das Layout.

    Args:
        app (SimpleGUI): Die Instanz der SimpleGUI-Klasse.
        layout_file (str): Der Pfad zur YAML-Layout-Datei.
        command_mapping (dict): Mapping von Funktionsnamen zu Python-Funktionen.
    """
    # Layout laden
    layout = load_yaml_layout(layout_file)

    # Menüdaten separat speichern, bevor das Layout-Dict modifiziert wird
    menu_data = layout.pop("menu", None)

    # Commands im Layout mappen
    map_layout_commands(layout, command_mapping, app)

    # Baue das Grid-Layout zuerst
    app.build(layout)

    # Lade das Menü danach, falls vorhanden
    if menu_data:
        setup_menu(app, menu_data, command_mapping)

def map_layout_commands(layout, command_mapping, app): # Füge 'app' als Parameter hinzu
    # Rekursive Funktion, um durch verschachtelte Layouts zu gehen
    def _recursive_map(data):
        if isinstance(data, dict):
            # Prüfen, ob dieses Dictionary ein Widget mit 'command' darstellt
            if "command" in data and isinstance(data["command"], str):
                command_name = data["command"]
                mapped_func = command_mapping.get(command_name) # Hole die Funktion
                
                if mapped_func:
                    # Ersetze String durch ein Lambda, das die Funktion mit app aufruft
                    data["command"] = lambda app=app, cmd=mapped_func: cmd(app)
                else:
                    logging.warning(f"Befehl '{command_name}' im Layout gefunden, aber nicht im commands_module.")
                    data["command"] = None # Oder eine Dummy-Funktion

            # Rekursiv für alle Werte im Dictionary aufrufen
            for key, value in data.items():
                # Speziell für 'options' oder andere bekannte Strukturen, die Commands enthalten könnten
                if isinstance(value, (dict, list)): # Rekursiv für alle dicts und lists
                    _recursive_map(value)

        elif isinstance(data, list):
            # Rekursiv für alle Elemente in der Liste aufrufen
            for item in data:
                _recursive_map(item)
    _recursive_map(layout) # Starte die rekursive Suche/Ersetzung
    
def setup_menu(app, menu_data, command_mapping):
    """
    Erstellt ein Menü basierend auf der Menüstruktur in der YAML-Datei.

    Args:
        app (SimpleGUI): Die Instanz der SimpleGUI-Klasse.
        menu_data (list): Die Menüstruktur aus der YAML-Datei.
        command_mapping (dict): Ein Mapping von Funktionsnamen zu Python-Funktionen.
    """
    menu_bar = tk.Menu(app.root)
    for menu in menu_data:
        menu_label = menu.get("label", "Unbenannt")
        menu_items = menu.get("items", [])
        menu_dropdown = tk.Menu(menu_bar, tearoff=0)
        for item in menu_items:
            item_label = item.get("label", "Unbenannt")
            command_name = item.get("command")
            item_command = command_mapping.get(command_name) # Hole die Funktion

            if item_command:
                # WICHTIG: Erstelle Lambda, das die Funktion mit der app-Instanz aufruft
                menu_dropdown.add_command(
                    label=item_label,
                    command=lambda app=app, cmd=item_command: cmd(app)
                )
            else:
                menu_dropdown.add_command(label=item_label, state="disabled") # Deaktiviere, wenn kein Befehl gefunden
        menu_bar.add_cascade(label=menu_label, menu=menu_dropdown)
    app.root.config(menu=menu_bar)