import tkinter as tk
from tkinter import filedialog, messagebox
import markdown
from markdown.extensions.tables import TableExtension
from simplegui.custom_widgets import HtmlPreviewArea
import os # Hinzugefügt für os.path.basename
# Versuche, YAML zu importieren, und setze ein Flag
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("WARNUNG: PyYAML nicht gefunden. Konfiguration kann nicht im YAML-Format gespeichert/geladen werden.")


current_file = None
current_css_content = None # Globale Variable für den CSS-Inhalt
CONFIG_FILE = "markdown_editor_config.yaml" # Name der Konfigurationsdatei (geändert zu YAML)

def on_text_change(app):
    """Aktualisiert die HTML-Vorschau, wenn sich der Text ändert, und wendet geladenes CSS an."""
    global current_css_content
    text = app.get_widget_value("editor_area")
    body_html = markdown.markdown(text, extensions=[TableExtension(use_align_attribute=True)]) # Markdown in HTML-Body umwandeln

    # Baue den HTML-Header
    html_head = "<!DOCTYPE html>\n"
    html_head += "<html>\n<head>\n"
    html_head += '  <meta charset="UTF-8">\n' # Wichtig für korrekte Zeichenanzeige

    # Füge das CSS hinzu, falls vorhanden
    if current_css_content:
        html_head += f"  <style>\n{current_css_content}\n  </style>\n"

    html_head += "</head>\n"

    preview = app.get_widget("HtmlPreviewArea")
    if preview:
        # Kombiniere Header und Body zum vollständigen HTML
        full_html = html_head + f"<body>\n{body_html}\n</body>\n</html>"
        preview.set_html(full_html)

def new_file(app):
    global current_file
    app.set_widget_option("editor_area", "text", "")
    current_file = None
    on_text_change(app)

def open_file(app):
    global current_file
    filename = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            app.set_widget_option("editor_area", "text", content)
            current_file = filename
            on_text_change(app)
        except Exception as e:
            messagebox.showerror("Fehler", f"Datei konnte nicht geöffnet werden:\n{e}")

def save_file(app):
    global current_file
    if not current_file:
        save_file_as(app)
        return
    text = app.get_widget_value("editor_area")
    try:
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        messagebox.showerror("Fehler", f"Datei konnte nicht gespeichert werden:\n{e}")

def save_file_as(app):
    global current_file
    filename = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        current_file = filename
        save_file(app)

def clear_text(app):
    app.set_widget_option("editor_area", "text", "")
    on_text_change(app)
    current_file = None
    # Hier wird der aktuelle Dateiname zurückgesetzt
    # und die Vorschau aktualisiert

def show_about(app):
    messagebox.showinfo("Über Markdown Editor", "Markdown Editor\nVersion 1.0\nEin einfacher Markdown-Editor mit Vorschau.")
def show_help(app):
    
    messagebox.showinfo("Hilfe", "Markdown Editor Hilfe\n\n"
                                  "1. Erstellen Sie eine neue Datei: Datei > Neu\n"
                                  "2. Öffnen Sie eine bestehende Datei: Datei > Öffnen\n"
                                  "3. Speichern Sie die aktuelle Datei: Datei > Speichern\n"
                                  "4. Speichern unter: Datei > Speichern unter\n"
                                  "5. Vorschau anzeigen: Vorschau > Vorschau anzeigen\n"
                                  "6. Über den Editor: Hilfe > Über")
def save_html(app):
    global current_file
    if not current_file:
        messagebox.showerror("Fehler", "Bitte speichern Sie zuerst die Markdown-Datei.")
        return

    # Korrektur: Generiere das HTML neu aus dem Editor-Inhalt
    markdown_text = app.get_widget_value("editor_area")
    body_html = markdown.markdown(markdown_text)

    # Baue den HTML-Header (genau wie in on_text_change)
    html_head = "<!DOCTYPE html>\n"
    html_head += "<html>\n<head>\n"
    html_head += '  <meta charset="UTF-8">\n'
    if current_css_content: # Füge CSS hinzu, falls vorhanden
        html_head += f"  <style>\n{current_css_content}\n  </style>\n"
    html_head += "</head>\n"

    full_html = html_head + f"<body>\n{body_html}\n</body>\n</html>"
    html_filename = current_file.replace(".md", ".html")
    try:
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(full_html) # Speichere das vollständige HTML
        messagebox.showinfo("Erfolg", f"HTML-Datei gespeichert als: {html_filename}")
    except Exception as e:
        messagebox.showerror("Fehler", f"HTML-Datei konnte nicht gespeichert werden:\n{e}")

def show_markdown_help(app):
    messagebox.showinfo("Markdown Hilfe", "Markdown Syntax Hilfe\n\n"
                                          "1. Überschriften: # Überschrift 1, ## Überschrift 2, ### Überschrift 3\n"
                                          "2. Fett: **fett**\n"
                                          "3. Kursiv: *kursiv*\n"
                                          "4. Listen: - Punkt 1, - Punkt 2\n"
                                          "5. Links: [Linktext](URL)\n"
                                          "6. Bilder: ![Alt-Text](Bild-URL)\n"
                                          "7. Zitate: > Zitat")
    
def insert_image(app):
    """Öffnet einen Dateidialog zur Auswahl eines Bildes und fügt den Markdown-Link ein."""
    editor = app.get_widget("editor_area")
    if not editor:
        messagebox.showerror("Fehler", "Editor-Widget nicht gefunden.")
        return

    filepath = filedialog.askopenfilename(
        title="Bild auswählen",
        filetypes=[
            ("Bilddateien", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("Alle Dateien", "*.*")
        ]
    )

    if filepath: # Nur fortfahren, wenn eine Datei ausgewählt wurde
        # Verwende den Dateinamen als Standard-Alt-Text
        alt_text = os.path.basename(filepath)
        # Konvertiere den Pfad in eine file:// URI
        # Wichtig: Sicherstellen, dass der Pfad absolut ist
        
        #file_uri = f"file://{os.path.abspath(filepath)}"
        # Erstelle den Markdown-Link
        markdown_link = f"![{alt_text}]({filepath})"
        #markdown_link = f"![{alt_text}]({file_uri})"

        # Füge den Link an der aktuellen Cursorposition ein
        editor.insert(tk.INSERT, markdown_link)
        editor.focus_set() # Setze den Fokus zurück auf den Editor

def load_config():
    """Lädt die Konfiguration aus der YAML-Datei."""
    if not YAML_AVAILABLE:
        return {} # YAML nicht verfügbar

    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    
                # Verwende yaml.safe_load statt json.load
                config_data = yaml.safe_load(f)
                # Stelle sicher, dass es ein Dictionary ist (falls die Datei leer ist oder nur einen Skalar enthält)
                return config_data if isinstance(config_data, dict) else {}
    except (yaml.YAMLError, IOError) as e:
        print(f"Fehler beim Laden der Konfigurationsdatei ({CONFIG_FILE}): {e}")
    return {} # Leeres Dictionary bei Fehlern oder wenn Datei nicht existiert

def save_config(data):
    """Speichert die Konfiguration in der YAML-Datei."""
    if not YAML_AVAILABLE:
        print(f"WARNUNG: PyYAML nicht verfügbar. Konfiguration kann nicht in {CONFIG_FILE} gespeichert werden.")
        return
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            # Verwende yaml.dump statt json.dump
            yaml.dump(data, f, default_flow_style=False, indent=2, allow_unicode=True)
    except (yaml.YAMLError, IOError) as e:
        print(f"Fehler beim Speichern der Konfigurationsdatei ({CONFIG_FILE}): {e}")


def load_css_file(app):
    """Öffnet einen Dateidialog zum Laden einer CSS-Datei und aktualisiert die Vorschau."""
    global current_css_content
    filepath = filedialog.askopenfilename(
        title="CSS-Datei für Vorschau auswählen",
        filetypes=[("CSS-Dateien", "*.css"), ("Alle Dateien", "*.*")]
    )
    if filepath:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                current_css_content = f.read()
            messagebox.showinfo("CSS Geladen", f"CSS-Datei '{os.path.basename(filepath)}' geladen.\nDie Vorschau wird aktualisiert.")
            # Vorschau neu rendern, um das neue CSS anzuwenden
            on_text_change(app)
        except Exception as e:
            current_css_content = None # Bei Fehler zurücksetzen
            messagebox.showerror("Fehler beim CSS-Laden", f"Konnte CSS-Datei nicht laden:\n{e}")
            # Ggf. Vorschau ohne CSS neu rendern
            on_text_change(app)
