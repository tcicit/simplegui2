# SimpleGUI2 Framework – Handbuch

## Inhaltsverzeichnis

1. [Einführung](#einführung)
2. [Kernkonzept & Funktionsweise](#kernkonzept--funktionsweise)
3. [YAML-Layoutstruktur](#yaml-layoutstruktur)
4. [Widget-Referenz](#widget-referenz)
5. [Komplettes Beispiel](#komplettes-beispiel)
6. [Erweiterungen & Hinweise](#erweiterungen--hinweise)

---

## Einführung

**SimpleGUI2** ist ein Python-Framework auf Basis von Tkinter, das die Erstellung von grafischen Benutzeroberflächen (GUIs) durch deklarative Layouts in YAML-Dateien stark vereinfacht. Die Logik bleibt dabei in Python, das Layout wird in YAML beschrieben.

**Ziele:**
- **Trennung von Layout und Logik:** Layout in YAML, Logik in Python.
- **Schnelles Prototyping:** GUI-Änderungen ohne Python-Code.
- **Wiederverwendbarkeit:** Layouts als Vorlagen nutzbar.
- **Erweiterbarkeit:** Unterstützung für Standard-Tkinter, ttk und eigene Widgets.

---

## Kernkonzept & Funktionsweise

### Grundidee

- **Layout**: Die GUI-Struktur wird in einer YAML-Datei als Baum aus Zeilen (`rows`) und Spalten (`columns`) definiert.
- **Widgets**: Jedes Widget wird durch einen `type` (z.B. `Button`, `Entry`, `Notebook`), optionale `options` und einen eindeutigen `name` (für Python-Zugriff) beschrieben.
- **Logik**: Python-Funktionen werden über einen Mapping-Mechanismus (`command_mapping`) mit den in YAML referenzierten `command`-Strings verknüpft.
- **Theming**: Ein zentrales Theme-Objekt steuert Farben, Schriftarten etc. für einheitliches Aussehen.

### Ablauf

1. **Layout laden**: YAML-Datei wird eingelesen.
2. **Command-Mapping**: Strings wie `"register_user"` werden auf Python-Funktionen gemappt.
3. **GUI-Build**: Die `SimpleGUI`-Klasse baut rekursiv das Layout und erstellt alle Widgets.
4. **Interaktion**: Über Methoden wie `get_widget_value`, `set_widget_option` etc. kann die Logik mit den Widgets interagieren.

---

## YAML-Layoutstruktur

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

**Wichtige Felder:**
- `type`: Widget-Typ (siehe Widget-Referenz)
- `name`: Eindeutiger Name für Python-Zugriff (optional, aber empfohlen)
- `options`: Widget-spezifische Optionen (z.B. `text`, `values`, `from_`, `to`)
- `pack_options`: Steuerung der Platzierung (z.B. `side`, `fill`, `expand`)
- `command`: Name der Python-Funktion (als String), die aufgerufen werden soll

---

## Widget-Referenz

### Standard Widgets (tk)

| Typ           | Beschreibung                                 | Wichtige Optionen                |
|---------------|----------------------------------------------|----------------------------------|
| Label         | Textanzeige                                  | text, bg, fg, font               |
| Entry         | Einzeiliges Eingabefeld                      | width, show, textvariable        |
| Button        | Schaltfläche                                 | text, command, state             |
| Checkbutton   | Kontrollkästchen                             | text, variable, value, command   |
| Radiobutton   | Optionsfeld (Gruppe über `group`)            | text, value, variable, command   |
| Text          | Mehrzeiliges Textfeld                        | width, height, wrap, state       |
| Frame         | Container für andere Widgets                 | bg, relief, bd                   |
| LabelFrame    | Frame mit Titel                              | text, labelanchor, bg, fg        |
| Scale         | Schieberegler                                | from_, to, orient, value         |
| Spinbox       | Zahlenfeld mit Pfeilen                       | from_, to, increment, values     |
| Listbox       | Liste auswählbarer Einträge                  | height, width, selectmode        |
| Canvas        | Zeichenfläche                                | width, height, bg                |

### Themed Widgets (ttk)

| Typ         | Beschreibung                                   | Wichtige Optionen                |
|-------------|------------------------------------------------|----------------------------------|
| Combobox    | Dropdown-Auswahlfeld                           | values, state, text              |
| Separator   | Trennlinie (horizontal/vertikal)               | orient                           |
| Notebook    | Tabbed-Container                               | tabs (siehe YAML-Beispiel)       |
| Treeview    | Tabellen-/Baumansicht                          | columns, headings, show, height  |

### Custom Widgets

| Typ         | Beschreibung                                   | Wichtige Optionen                |
|-------------|------------------------------------------------|----------------------------------|
| Card        | Info-Karte mit Titel und Inhalt                | title, content                   |
| InfoBox     | Farbig hinterlegte Info-/Warn-/Fehlermeldung   | message, info_type               |
| Picture     | Bildanzeige (benötigt Pillow)                  | filepath, width, height          |
| ColorPicker | Farbauswahl mit Vorschau und Callback          | initial_color, button_text, show_hex, command |

---

Hier ist eine Liste aller in deiner YAML-Datei verwendeten `grid_options` mit Erklärung:

- **rowspan** 
  Gibt an, über wie viele Zeilen sich das Widget erstrecken soll. 
  *Beispiel:* `rowspan: 7` → Das Widget nimmt 7 Zeilen ein.

- **sticky** 
  Bestimmt, an welchen Seiten des Zellenbereichs das Widget „klebt“. 
  *Mögliche Werte:* 
  - `n` (oben), 
  - `s` (unten), 
  - `e` (rechts), 
  - `w` (links), 
  - Kombinationen wie `nsew` (füllt die Zelle komplett aus), `ew` (füllt horizontal), `new` (oben, rechts, links).

- **pady** 
  Fügt vertikalen Außenabstand (Padding) oberhalb und unterhalb des Widgets hinzu. 
  *Beispiel:* `pady: 5` → 5 Pixel Abstand oben und unten.

- **padx** 
  Fügt horizontalen Außenabstand (Padding) links und rechts des Widgets hinzu.  
  *Beispiel:* `padx: 10` → 10 Pixel Abstand links und rechts.

Diese Optionen steuern das Layout der Widgets im Tkinter-Grid-Manager.

# Grid Options

## Gewichte 
  Erklärung der Grid Gewichte :
    """
    The grid weights are used to determine how space is allocated to different rows and columns
    in a grid layout. Each weight represents the relative proportion of space that a row or column
    should occupy compared to others. A higher weight means that the corresponding row or column
    will take up more space when the grid is resized.

    For example:
    - A column with a weight of 2 will take up twice as much space as a column with a weight of 1.
    - If all weights are equal, the space will be distributed evenly.

    Grid weights are typically used in GUI frameworks to create flexible and responsive layouts.
    """

## row
  Erklärung der Grid Rows :
    """

  
## column
  Erklärung der Grid Columns :
    """


## Komplettes Beispiel

### YAML-Layout (minimal_layout.yaml)

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

### Python-Code

```python
import tkinter as tk
from simplegui.core import SimpleGUI
from yaml_loader import load_yaml_layout

def handle_ok():
    username = app.get_widget_value("username_entry")
    print(f"Benutzername: {username}")

# Mapping von Command-Strings zu Funktionen
command_mapping = {
    "handle_ok": handle_ok
}

# Layout laden und Commands mappen
layout = load_yaml_layout("minimal_layout.yaml")
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

# GUI aufbauen und starten
root = tk.Tk()
app = SimpleGUI(root, title="Minimalbeispiel", size="300x120")
app.build(layout)
app.run()
```

---

## Erweiterungen & Hinweise

- **Komplexere Layouts**: Siehe die mitgelieferte Datei `layout_enhanced.yaml` für verschachtelte Tabs, Treeview, Canvas, ColorPicker etc.
- **Theming**: Passe das Aussehen zentral im ThemeManager an.
- **Eigene Widgets**: Erweitere das Framework durch eigene Klassen in `custom_widgets.py`.
- **Fehlerbehandlung**: Das Framework gibt hilfreiche Log-Ausgaben bei YAML- oder Widget-Fehlern.
- **Command-Mapping**: Immer vor `app.build()` durchführen!

---

**Weitere Beispiele und Details findest du in den mitgelieferten YAML- und Python-Dateien sowie im Quellcode.**

---

*Letzte Aktualisierung: 2025-04-30*
