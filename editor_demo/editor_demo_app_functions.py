import tkinter as tk
from simplegui.messages import Messages
from simplegui.filedialogs import FileDialogs
from simplegui.yaml_loader import load_yaml_layout

def save_text_to_file(app):
    """Speichert den Inhalt des Textbereichs in einer Datei."""
    text_widget = app.get_widget("text_editor_area")
    if text_widget:
        try:
            file_path = FileDialogs.save_file_as(
                defaultextension=".txt",
                filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = text_widget.get("1.0", tk.END).strip()
                    file.write(content)
                Messages.info("Erfolg", f"Text erfolgreich gespeichert:\n{file_path}")
            else:
                print("Speichern abgebrochen.")
        except Exception as e:
            Messages.error("Fehler", f"Fehler beim Speichern der Datei:\n{e}")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def load_text_from_file(app):
    """Lädt den Inhalt einer Datei in den Textbereich."""
    text_widget = app.get_widget("text_editor_area")
    if text_widget:
        try:
            file_path = FileDialogs.open_file(filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")])
            if file_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    text_widget.delete("1.0", tk.END)
                    text_widget.insert("1.0", content)
                Messages.info("Erfolg", f"Text erfolgreich geladen:\n{file_path}")
            else:
                print("Laden abgebrochen.")
        except Exception as e:
            Messages.error("Fehler", f"Fehler beim Laden der Datei:\n{e}")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def clear_text_area(app):
    """Leert den Textbereich."""
    text_widget = app.get_widget("text_editor_area")
    if text_widget:
        text_widget.delete("1.0", tk.END)
        Messages.info("Erfolg", "Textbereich geleert.")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def find_and_replace(app, find_text, replace_text):
    """Sucht nach einem Text und ersetzt ihn durch einen anderen."""
    text_widget = app.get_widget("text_editor_area")
    if text_widget:
        content = text_widget.get("1.0", tk.END)
        new_content = content.replace(find_text, replace_text)
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", new_content)
        Messages.info("Erfolg", f"'{find_text}' wurde durch '{replace_text}' ersetzt.")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def undo_last_action(app):
    """Macht die letzte Aktion rückgängig."""
    text_widget = app.get_widget("text_editor_area")
    if text_widget:
        if hasattr(app, "undo_buffer") and len(app.undo_buffer) > 1:
            # Aktuellen Zustand entfernen und vorherigen Zustand wiederherstellen
            app.undo_buffer.pop()
            last_state = app.undo_buffer[-1]
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", last_state)
            Messages.info("Erfolg", "Letzte Aktion wurde rückgängig gemacht.")
        else:
            Messages.info("Info", "Keine weiteren Aktionen zum Rückgängigmachen.")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def select_all_text(app):
    """Markiert den gesamten Text im Editor."""
    text_widget = app.get_widget("text_editor_area")
    if text_widget:
        text_widget.tag_add("sel", "1.0", tk.END)
        text_widget.focus_set()
        Messages.info("Erfolg", "Gesamter Text wurde markiert.")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def count_lines(app):
    """Zählt die Anzahl der Zeilen im Textbereich."""
    text_widget = app.get_widget("text_editor_area")
    if text_widget:
        line_count = int(text_widget.index(tk.END).split('.')[0]) - 1
        Messages.info("Zeilenanzahl", f"Der Textbereich enthält {line_count} Zeilen.")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def save_as(app):
    """Speichert den Text unter einem neuen Namen."""
    text_widget = app.get_widget("text_editor_area")
    if text_widget:
        try:
            file_path = FileDialogs.save_file_as(
                defaultextension=".txt",
                filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = text_widget.get("1.0", tk.END).strip()
                    file.write(content)
                Messages.info("Erfolg", f"Text erfolgreich unter '{file_path}' gespeichert.")
            else:
                print("Speichern abgebrochen.")
        except Exception as e:
            Messages.error("Fehler", f"Fehler beim Speichern der Datei:\n{e}")
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")

def initialize_undo_buffer(app):
    """Initialisiert den Undo-Buffer."""
    app.undo_buffer = []  # Liste für den Undo-Buffer
    text_widget = app.get_widget("text_editor_area")
    if text_widget:
        # Textänderungen überwachen
        def on_text_change(event=None):
            content = text_widget.get("1.0", tk.END).strip()
            if not app.undo_buffer or app.undo_buffer[-1] != content:
                app.undo_buffer.append(content)
            text_widget.edit_modified(False)  # Status zurücksetzen

        # Textänderungen überwachen (bei jeder Eingabe)
        text_widget.bind("<<Modified>>", on_text_change)
        text_widget.edit_modified(False)  # Status zurücksetzen

        # Initialen Zustand speichern
        app.undo_buffer.append(text_widget.get("1.0", tk.END).strip())
    else:
        Messages.error("Fehler", "Textbereich nicht gefunden.")