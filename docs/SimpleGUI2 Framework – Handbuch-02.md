# SimpleGUI2 Framework – Handbuch

## 1. Idee und Intention

**SimpleGUI2** wurde entwickelt, um die Erstellung von grafischen Benutzeroberflächen (GUIs) in Python zu vereinfachen und zu beschleunigen. Ziel ist es, Layout und Logik strikt zu trennen: Das Layout wird deklarativ in YAML-Dateien beschrieben, die Logik bleibt in Python. So können Oberflächen schnell angepasst werden, ohne Python-Code zu ändern. Das Framework unterstützt Standard-Tkinter-Widgets, ttk-Widgets und eigene Erweiterungen.


---

## 2. Erklärung des Frameworks und der Architektur

### Grundprinzipien

- **Trennung von Layout und Logik:** Layout in YAML, Logik in Python.
- **Schnelles Prototyping:** GUI-Änderungen ohne Python-Code.
- **Wiederverwendbarkeit:** Layouts als Vorlagen nutzbar.
- **Deklaratives Layout:** Die GUI-Struktur wird in YAML-Dateien als Baum aus Zeilen (`rows`) und Spalten (`columns`) definiert.
- **Logik in Python:** Python-Funktionen werden über einen Mapping-Mechanismus (`command_mapping`) mit den in YAML referenzierten `command`-Strings verknüpft.
- **Theming:** Ein zentrales Theme-Objekt steuert Farben, Schriftarten etc. für einheitliches Aussehen.
- **Erweiterbarkeit:** Eigene Widgets und Themes sind einfach möglich.

### Architekturüberblick

- **core.py:** Enthält die zentrale Klasse [`SimpleGUI`](simplegui/core.py), die das Layout aufbaut und Methoden zur Widget-Interaktion bereitstellt.
- **layout_manager.py:** Lädt das YAML-Layout, mappt Commands und baut das Menü.
- **core_functions.py & core_demo_app_functions.py:** Enthalten die Logik für Standard- und App-spezifische Befehle.
- **theme_manager.py:** Zentrales Theming für alle Widgets.
- **custom_widgets.py:** Eigene Widgets wie Card, InfoBox, Picture, ColorPicker.
- **yaml_loader.py:** Lädt und parst YAML-Layouts.
- **validation.py:** Validiert Layout und Eingaben.
- **filedialogs.py:** Kapselt Datei- und Verzeichnisauswahldialoge.

---

## Voraussetzungen und Installation

### Voraussetzungen

- **Python 3.8 oder neuer**  
  Das Framework basiert auf Python 3 und nutzt Standardbibliotheken wie `tkinter` sowie optionale Pakete für erweiterte Widgets.
- **Tkinter**  
  Tkinter ist in den meisten Python-Distributionen bereits enthalten. Unter Linux kann es ggf. separat installiert werden (siehe unten).

### Installation

1. **Repository herunterladen oder klonen**

``` sh
    git clone <REPOSITORY-URL>
    cd simpleGUI2
```
  

2. **Abhängigkeiten installieren**

   Für die Grundfunktionen reicht in der Regel Python mit Tkinter.  
   Für optionale Features (z.B. Markdown/HTML-Vorschau) können weitere Pakete nötig sein:

``` sh
        pip install pyyaml
```

   Für Markdown/HTML-Vorschau ggf.:


``` sh
     pip install markdown
```

3. **Tkinter unter Linux installieren (falls nicht vorhanden)**

``` sh
    sudo apt-get install python3-tk
```

4. **Beispielanwendung starten**

``` sh
    python3 core_demo_app.py
```

### Hinweise

- Das Framework ist plattformübergreifend (Windows, Linux, macOS).
- Für eigene Projekte genügt es, das Verzeichnis simplegui in das eigene Projekt zu kopieren oder als Python-Paket einzubinden.
- Die YAML-Layouts und Beispielskripte dienen als Vorlage für eigene Anwendungen.


## 3. Liste der Widgets mit Attributen

### Standard Widgets (tk)

| Typ         | Attribute (Beispiele)         | Beschreibung                     |
|-------------|------------------------------|----------------------------------|
| Label       | text, bg, fg, font           | Textanzeige                      |
| Entry       | width, show, textvariable    | Einzeiliges Eingabefeld          |
| Button      | text, command, state         | Schaltfläche                     |
| Checkbutton | text, variable, value        | Kontrollkästchen                 |
| Radiobutton | text, value, variable        | Optionsfeld                      |
| Text        | width, height, wrap, state   | Mehrzeiliges Textfeld            |
| Frame       | bg, relief, bd               | Container für andere Widgets     |
| LabelFrame  | text, labelanchor, bg, fg    | Frame mit Titel                  |
| Scale       | from_, to, orient, value     | Schieberegler                    |
| Spinbox     | from_, to, increment, values | Zahlenfeld mit Pfeilen           |
| Listbox     | height, width, selectmode    | Liste auswählbarer Einträge      |
| Canvas      | width, height, bg            | Zeichenfläche                    |

### Themed Widgets (ttk)

| Typ         | Attribute (Beispiele)         | Beschreibung                     |
|-------------|------------------------------|----------------------------------|
| Combobox    | values, state, text          | Dropdown-Auswahlfeld             |
| Separator   | orient                       | Trennlinie                       |
| Notebook    | tabs                         | Tabbed-Container                 |
| Treeview    | columns, headings, show      | Tabellen-/Baumansicht            |

### Custom Widgets

| Typ         | Attribute (Beispiele)         | Beschreibung                     |
|-------------|------------------------------|----------------------------------|
| Card        | title, content               | Info-Karte mit Titel und Inhalt  |
| InfoBox     | message, info_type           | Info-/Warn-/Fehlermeldung        |
| Picture     | filepath, width, height      | Bildanzeige                      |
| ColorPicker | initial_color, button_text, show_hex, command | Farbauswahl mit Vorschau         |
| HtmlPreviewArea | -                        | HTML-Vorschau (Markdown-Editor)  |

---

## 4. Anwendungsbeispiele

### YAML-Layout mit Rows und Columns (Ausschnitt)

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
from simplegui.layout_manager import setup_layout

def handle_ok(app):
    username = app.get_widget_value("username_entry")
    print(f"Benutzername: {username}")

commands = { "handle_ok": handle_ok }
root = tk.Tk()
app = SimpleGUI(root, title="Demo", size="400x200")
setup_layout(app, "layout.yaml", commands)
app.run()

```

---

### YAML-Layout mit Grid (Ausschnitt)

``` YAML
grid:
  - row: 0
    column: 0
    type: Label
    options:
      text: "Vorname:"
  - row: 0
    column: 1
    type: Entry
    name: firstname_entry
    options:
      width: 20
  - row: 1
    column: 0
    type: Label
    options:
      text: "Nachname:"
  - row: 1
    column: 1
    type: Entry
    name: lastname_entry
    options:
      width: 20
  - row: 2
    column: 0
    type: Button
    options:
      text: "OK"
      command: "show_name"
    grid_options: # Korrigierte Einrückung für columnspan
      columnspan: 2
```


### Python-Code
``` python
import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout

def show_name(app):
    firstname = app.get_widget_value("firstname_entry")
    lastname = app.get_widget_value("lastname_entry")
    print(f"Name: {firstname} {lastname}")

commands = { "show_name": show_name }
root = tk.Tk()
app = SimpleGUI(root, title="Grid Demo", size="400x200")
setup_layout(app, "grid_layout.yaml", commands)
app.run()
```

---

## 5. Liste der Messages und Filedialoge

Das SimpleGUI2-Framework stellt mit der Klasse `Messages` und dem Modul `FileDialogs` komfortable Hilfsmittel für Benutzerinteraktionen bereit:

- **Messages**: Ermöglichen das Anzeigen von Informations-, Warn- und Fehlermeldungen sowie von Dialogen zur Benutzerabfrage (z.B. Ja/Nein, OK/Abbrechen).
- **FileDialogs**: Bieten einfache Methoden, um Dateien oder Verzeichnisse auszuwählen, zu speichern oder mehrere Dateien auszuwählen – alles mit nativen Systemdialogen.

Diese Funktionen erleichtern die Interaktion mit dem Benutzer und sind in jeder GUI-Anwendung unverzichtbar.

#### Beispiel: Verwendung von Messages und Filedialogen

```python
from simplegui.messages import Messages
from simplegui.filedialogs import FileDialogs

def open_and_show_file(app):
    filename = FileDialogs.open_file(filetypes=(("Textdateien", "*.txt"), ("Alle Dateien", "*.*")))
    if filename:
        Messages.info("Datei geöffnet", f"Sie haben die Datei ausgewählt:\n{filename}")
    else:
        Messages.warning("Abbruch", "Es wurde keine Datei ausgewählt.")

def ask_user(app):
    if Messages.yesno("Frage", "Möchten Sie fortfahren?"):
        Messages.info("Weiter", "Sie haben Ja gewählt.")
    else:
        Messages.error("Abbruch", "Sie haben Nein gewählt.")
```

**Hinweis:**  
Alle Methoden können direkt aufgerufen werden und benötigen kein eigenes Fenster-Handling – das übernimmt das Framework automatisch.

### Messages (simplegui/messages.py)


| Methode            | Beschreibung                                                    | Rückgabewert                |
|--------------------|-----------------------------------------------------------------|-----------------------------|
| info(title, msg)   | Zeigt eine Info-Messagebox an                                   | None                        |
| warning(title, msg)| Zeigt eine Warnung-Messagebox an                                | None                        |
| error(title, msg)  | Zeigt eine Fehler-Messagebox an                                 | None                        |
| question(title, msg)| Zeigt eine Frage-Dialogbox ("Ja"/"Nein" als String)            | "yes" oder "no"             |
| yesno(title, msg)  | Zeigt einen Ja/Nein-Dialog an                                   | True (Ja) / False (Nein)    |
| okcancel(title, msg)| Zeigt einen OK/Abbrechen-Dialog an                             | True (OK) / False (Abbruch) |
| retrycancel(title, msg)| Zeigt einen Wiederholen/Abbrechen-Dialog an                 | True (Wiederholen) / False (Abbruch) |
| yesnocancel(title, msg)| Zeigt einen Ja/Nein/Abbrechen-Dialog an                     | True (Ja) / False (Nein) / None (Abbruch) |

### Filedialogs (simplegui/filedialogs.py)

| Methode                        | Beschreibung                                      |
|---------------------------------|---------------------------------------------------|
| open_file(...)                  | Datei öffnen                                      |
| save_file(...)                  | Datei speichern                                   |
| open_directory(...)             | Verzeichnis auswählen                             |
| save_file_as(...)               | "Speichern unter..."                              |
| open_multiple_files(...)        | Mehrere Dateien auswählen                         |
| open_file_with_title(...)       | Datei öffnen mit Titel                            |
| save_file_with_title(...)       | Datei speichern mit Titel                         |
| open_directory_with_title(...)  | Verzeichnis auswählen mit Titel                   |
| ...                             | (Viele weitere Varianten mit initialdir, parent etc.) |

**Alle Filedialog-Methoden geben den gewählten Pfad (oder eine Liste von Pfaden) zurück.**

---

## 6. YAML-Layout-Referenz

### Grundstruktur

```yaml
rows:
  - columns:
      - type: Label
        options: { text: "Beispiel" }
      - type: Entry
        name: eingabe
        options: { width: 20 }
  - columns:
      - type: Button
        options: { text: "OK" }
        command: "handle_ok"
```

**Wichtige Felder:**
- `type`: Widget-Typ (siehe Widget-Liste)
- `name`: Eindeutiger Name für Python-Zugriff (optional, empfohlen)
- `options`: Widget-spezifische Optionen (z.B. `text`, `values`, `from_`, `to`)
- `pack_options` / `grid_options`: Steuerung der Platzierung (z.B. `side`, `fill`, `expand`, `sticky`, `columnspan`)
- `command`: Name der Python-Funktion (als String), die aufgerufen werden soll

### Grid-Layout

```yaml
grid:
  - row: 0
    column: 0
    type: Label
    options: { text: "Vorname:" }
    grid_options: { sticky: w }
  - row: 0
    column: 1
    type: Entry
    name: firstname_entry
    options: { width: 20 }
    grid_options: { sticky: ew }
  # ...
```

**Weitere Felder:**  
- `parent`: Name des Parent-Widgets (für verschachtelte Layouts)
- `columnspan`, `rowspan`: Widget über mehrere Spalten/Zeilen


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



---

### Grid-Gewichte (row_weight, column_weight)
Mit Grid-Gewichten (row_weight und column_weight) bestimmst du, wie sich Zeilen und Spalten beim Vergrößern des Fensters mit anpassen.
Ein höheres Gewicht bedeutet, dass die entsprechende Zeile oder Spalte mehr Platz erhält.

Verwendung im YAML-Layout:

```yaml
grid:
  - row: 0
    column: 0
    type: Label
    options: { text: "Vorname:" }
  - row: 0
    column: 1
    type: Entry
    name: firstname_entry
    options: { width: 20 }
  - row: 1
    column: 0
    type: Label
    options: { text: "Nachname:" }
  - row: 1
    column: 1
    type: Entry
    name: lastname_entry
    options: { width: 20 }
  - row: 2
    column: 0
    type: Button
    options: { text: "OK", command: "show_name" }
    grid_options: { columnspan: 2 }

# Grid-Gewichte für flexible Größenanpassung
row_weights:
  0: 1
  1: 1
  2: 0
column_weights:
  0: 0
  1: 1
```

### Erklärung:

- row_weights und column_weights sind Dictionaries, die für jede Zeile/Spalte das Gewicht angeben.
- Im Beispiel wächst die zweite Spalte (column 1) mit, wenn das Fenster breiter wird.
- Die Zeilen 0 und 1 wachsen vertikal, Zeile 2 (mit dem Button) bleibt fix.

**Hinweis:**

Die Unterstützung für row_weights und column_weights muss im Framework vorhanden sein (z.B. durch Aufruf von grid_rowconfigure und grid_columnconfigure im Code).


```python
import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout

def show_name(app):
    firstname = app.get_widget_value("firstname_entry")
    lastname = app.get_widget_value("lastname_entry")
    print(f"Name: {firstname} {lastname}")

commands = { "show_name": show_name }
root = tk.Tk()
app = SimpleGUI(root, title="Grid mit Gewichten", size="400x200")
setup_layout(app, "grid_with_weights.yaml", commands)
app.run()
```
**Tipp:**
Mit Grid-Gewichten erreichst du flexible, responsive Layouts – besonders nützlich für professionelle Oberflächen!

---

## 7. Menüsystem

### YAML-Beispiel

```yaml
menu:
  - label: "Datei"
    items:
      - label: "Öffnen"
        command: open_file
      - label: "Beenden"
        command: exit_app
  - label: "Hilfe"
    items:
      - label: "Über"
        command: show_about
```

**Hinweis:**  
Jeder Menüpunkt kann mit einer Python-Funktion (`command`) verknüpft werden.

---

## 8. Validierung und Fehlerbehandlung

Das Framework bietet Validierungsfunktionen für Eingaben und Layouts:

- **Eingabevalidierung:**  
  Über die Klasse `Validator` (`simplegui/validation.py`) können Felder auf "nicht leer", Regex-Muster etc. geprüft werden.

- **Layout-Validierung:**  
  Das Laden und Parsen der YAML-Dateien prüft automatisch auf Fehler und gibt hilfreiche Fehlermeldungen aus.

**Beispiel:**

```python
from simplegui.validation import Validator

if not Validator.is_not_empty(app.get_widget_value("username_entry")):
    Messages.warning("Eingabefehler", "Bitte geben Sie einen Benutzernamen ein.")
```

---

## 9. Theming und Anpassung

Das Aussehen der Anwendung kann zentral über den `ThemeManager` angepasst werden:

- Farben, Schriftarten und Styles werden in `simplegui/theme_manager.py` definiert.
- Eigene Themes können durch Ableiten und Überschreiben der Theme-Definition erstellt werden.

**Beispiel:**

```python
from simplegui.theme_manager import ThemeManager

ThemeManager.set_theme("dark")  # Beispiel für Theme-Wechsel
```

---

## 10. Eigene Widgets und Erweiterungen

Eigene Widgets können durch Ableiten von Tkinter- oder ttk-Widgets und Einbinden in `custom_widgets.py` hinzugefügt werden.  
Das Mapping erfolgt über die Methode `_resolve_widget_class` in `SimpleGUI`.

**Beispiel:**

```python
class MyWidget(ttk.Frame):
    # Eigene Logik
    pass
```

---

## 11. FAQ / Troubleshooting

**Häufige Probleme:**

- **Tkinter fehlt:**  
  → Installiere mit `sudo apt-get install python3-tk`
- **YAML-Fehler:**  
  → Prüfe Einrückungen und Syntax, nutze einen YAML-Validator.
- **Widgets erscheinen nicht:**  
  → Kontrolliere `name`- und `parent`-Angaben sowie die Layoutstruktur.
- **Command wird nicht ausgeführt:**  
  → Ist der Funktionsname im Python-Code korrekt und im Mapping enthalten?

---

## 12. API-Referenz (Kurzüberblick)

- **SimpleGUI**  
  - `build(layout)`: Baut das Layout auf
  - `get_widget(name)`: Liefert das Widget-Objekt
  - `get_widget_value(name)`: Liefert den Wert eines Eingabewidgets
  - `set_widget_option(name, option, value)`: Setzt eine Widget-Option

- **Messages**  
  - `info`, `warning`, `error`, `yesno`, `okcancel`, `retrycancel`, `yesnocancel`, `question`

- **FileDialogs**  
  - `open_file`, `save_file`, `open_directory`, `save_file_as`, ...

---

## 13. Lizenz und Mitwirken

- **Lizenz:**  
  Das Framework steht unter einer Open-Source-Lizenz (siehe Repository).
- **Mitwirken:**  
  Beiträge, Fehlerberichte und Feature-Wünsche sind willkommen!  
  Repository: `<REPOSITORY-URL>`

---

## 14. Changelog

- **v1.0 (2025-05):**  
  Erste stabile Version, YAML-Layout, Theming, Custom Widgets, Menüsystem, Validierung, Beispiele.

---

*Weitere Details und Beispiele findest du im Quellcode und in den YAML-Layouts im Projekt.*
