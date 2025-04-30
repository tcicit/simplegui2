# SimpleGUI2

**Deutsch | [English below](#english)**

## Übersicht

SimpleGUI2 ist ein flexibles Python-Framework zur schnellen Erstellung von grafischen Benutzeroberflächen (GUIs) mit Tkinter und YAML. Das Layout wird deklarativ in YAML-Dateien beschrieben, die Logik bleibt in Python. Das Framework unterstützt Standard-Tkinter-Widgets, ttk-Widgets und eigene Erweiterungen.

## Voraussetzungen

- **Python 3.8 oder neuer**
- **Tkinter** (bei den meisten Python-Installationen bereits enthalten)
- **PyYAML** (für das Parsen der YAML-Layouts)
- **Pillow** (optional, für Bild-Widgets)

## Installation

1. **Repository klonen**
    ```bash
    git clone https://github.com/dein-benutzername/simpleGUI2.git
    cd simpleGUI2
    ```

2. **Abhängigkeiten installieren**
    ```bash
    pip install pyyaml pillow
    ```

## Features

- **Deklaratives Layout:** GUI-Struktur in YAML, Logik in Python
- **Unterstützung für viele Widgets:** Label, Entry, Button, Checkbutton, Radiobutton, Combobox, Treeview, Canvas, u.v.m.
- **Tabbed-Interfaces:** Einfache Erstellung von Reitern (Notebook)
- **Custom Widgets:** Card, InfoBox, Picture, ColorPicker
- **Theming:** Zentrales Farbschema und Schriftarten
- **Einfache Erweiterbarkeit:** Eigene Widgets und Themes möglich

## Schnellstart

1. **YAML-Layout anlegen** (z.B. `layout.yaml`)
    ```yaml
    rows:
      - columns:
          - type: Label
            options: { text: "Benutzername:" }
          - type: Entry
            name: username_entry
            options: { width: 30 }
      - columns:
          - type: Button
            name: ok_button
            options: { text: "OK" }
            command: "handle_ok"
    ```

2. **Python-Code schreiben**
    ```python
    import tkinter as tk
    from simplegui.core import SimpleGUI
    from yaml_loader import load_yaml_layout

    def handle_ok():
        username = app.get_widget_value("username_entry")
        print(f"Benutzername: {username}")

    command_mapping = { "handle_ok": handle_ok }
    layout = load_yaml_layout("layout.yaml")
    # Mapping der Commands im Layout
    def map_layout_commands(layout_data, mapping):
        if isinstance(layout_data, dict):
            for key, value in layout_data.items():
                if key == "command" and isinstance(value, str) and value in mapping:
                    layout_data[key] = mapping[value]
                elif isinstance(value, (dict, list)):
                    map_layout_commands(value, mapping)
        elif isinstance(layout_data, list):
            for item in layout_data:
                map_layout_commands(item, mapping)
    map_layout_commands(layout, command_mapping)

    root = tk.Tk()
    app = SimpleGUI(root, title="Minimalbeispiel", size="300x120")
    app.build(layout)
    app.run()
    ```

3. **Starten**
    ```bash
    python demo_app_yaml.py
    ```

## Dokumentation

- Ausführliches Handbuch: [HANDBUCH.md](HANDBUCH.md)
- Beispiel-Layouts: `layout_enhanced.yaml`
- Beispiel-Menü: `menu.yaml`

---

# English

## Overview

SimpleGUI2 is a flexible Python framework for rapid GUI development using Tkinter and YAML. The layout is described declaratively in YAML files, while the logic remains in Python. The framework supports standard Tkinter widgets, ttk widgets, and custom extensions.

## Requirements

- **Python 3.8 or newer**
- **Tkinter** (usually included with Python)
- **PyYAML** (for parsing YAML layouts)
- **Pillow** (optional, for image widgets)

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/simpleGUI2.git
    cd simpleGUI2
    ```

2. **Install dependencies**
    ```bash
    pip install pyyaml pillow
    ```

## Features

- **Declarative layout:** GUI structure in YAML, logic in Python
- **Widget support:** Label, Entry, Button, Checkbutton, Radiobutton, Combobox, Treeview, Canvas, and more
- **Tabbed interfaces:** Easy creation of tabs (Notebook)
- **Custom widgets:** Card, InfoBox, Picture, ColorPicker
- **Theming:** Central color scheme and fonts
- **Easy extensibility:** Add your own widgets and themes

## Quick Start

1. **Create a YAML layout** (e.g. `layout.yaml`)
    ```yaml
    rows:
      - columns:
          - type: Label
            options: { text: "Username:" }
          - type: Entry
            name: username_entry
            options: { width: 30 }
      - columns:
          - type: Button
            name: ok_button
            options: { text: "OK" }
            command: "handle_ok"
    ```

2. **Write Python code**
    ```python
    import tkinter as tk
    from simplegui.core import SimpleGUI
    from yaml_loader import load_yaml_layout

    def handle_ok():
        username = app.get_widget_value("username_entry")
        print(f"Username: {username}")

    command_mapping = { "handle_ok": handle_ok }
    layout = load_yaml_layout("layout.yaml")
    # Map commands in layout
    def map_layout_commands(layout_data, mapping):
        if isinstance(layout_data, dict):
            for key, value in layout_data.items():
                if key == "command" and isinstance(value, str) and value in mapping:
                    layout_data[key] = mapping[value]
                elif isinstance(value, (dict, list)):
                    map_layout_commands(value, mapping)
        elif isinstance(layout_data, list):
            for item in layout_data:
                map_layout_commands(item, mapping)
    map_layout_commands(layout, command_mapping)

    root = tk.Tk()
    app = SimpleGUI(root, title="Minimal Example", size="300x120")
    app.build(layout)
    app.run()
    ```

3. **Run**
    ```bash
    python demo_app_yaml.py
    ```

## Documentation

- Full manual: [HANDBUCH.md](HANDBUCH.md) (German)
- Example layouts: `layout_enhanced.yaml`
- Example menu: `menu.yaml`

---

*Letzte Aktualisierung / Last update: 2025-04-30*