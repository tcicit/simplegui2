from simplegui.messages import Messages
from simplegui.filedialogs import FileDialogs
import tkinter as tk
from tkinter import filedialog, messagebox # Import messagebox
import os # Hinzugefügt für Verzeichnisoperationen
from PIL import Image, ImageTk # Für Bildverarbeitung (Thumbnails)
import math # Für Grid-Berechnungen (optional, aber nützlich)


def exit_app(app):
    print("Beende Anwendung...")
    root = tk.Tk()
    root.quit()

def open_file(app):
    print("Öffne Datei...")
    filename = FileDialogs.open_file()
    if filename:
        Messages.info("Datei geöffnet", filename)

def save_file(app):
    Messages.info("Speichern", "Datei gespeichert.")
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

def save_file_as(app):
    print("Speichern unter...")
    filename = FileDialogs.save_file_as()
    if filename:
        Messages.info("Datei gespeichert", filename)

def open_directory(app): # Nimmt jetzt die app-Instanz entgegen
    """Öffnet einen Dialog zur Auswahl eines Verzeichnisses und lädt Bilddateien."""
    print("Versuche Verzeichnis zu öffnen...")
    directory = filedialog.askdirectory(title="Wähle ein Bildverzeichnis")

    if directory:
        print(f"Verzeichnis ausgewählt: {directory}")
        # Rufe die neue Funktion auf, um die Thumbnails zu laden
        populate_thumbnail_grid(app, directory)
    else:
        print("Kein Verzeichnis ausgewählt.")

def populate_thumbnail_grid(app, directory):
    """Leert den thumbnail_container und füllt ihn mit klickbaren Bild-Thumbnails."""
    """Füllt den thumbnail_container mit Bild-Thumbnails aus dem Verzeichnis."""
    container = app.widgets.get('thumbnail_container')
    if not container:
        print("Fehler: thumbnail_container nicht im Layout gefunden.")
        return

    # Alte Widgets im Container löschen
    for widget in list(container.winfo_children()): # Wichtig: Kopie der Liste iterieren
        widget.destroy()

    # Thumbnail-Einstellungen
    THUMBNAIL_SIZE = (80, 80) # Größe der Thumbnails
    NUM_COLUMNS = 3          # Anzahl der Spalten im Grid
    PADDING = 5              # Abstand zwischen Thumbnails

    image_files = []
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp') # Erweiterte Liste
    try:
        for filename in os.listdir(directory):
            if filename.lower().endswith(valid_extensions):
                image_files.append(os.path.join(directory, filename))
        image_files.sort(key=str.lower) # Sortieren nach Namen
    except OSError as e:
        messagebox.showerror("Fehler beim Lesen des Verzeichnisses", f"Konnte Verzeichnis nicht lesen:\n{e}")
        return

    # Thumbnails erstellen und im Grid platzieren
    row_num = 0
    col_num = 0
    app.thumbnail_references = [] # WICHTIG: Referenzen speichern!

    for image_path in image_files:
        try:
            img = Image.open(image_path)
            img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS) # Thumbnail erstellen
            tk_thumb = ImageTk.PhotoImage(img)
            # WICHTIG: Referenz auf tk_thumb speichern, sonst wird sie vom Garbage Collector entfernt!
            # Wir speichern sie direkt am Button-Widget selbst.

            # Button (oder Label) für das Thumbnail erstellen
            thumb_button = tk.Button(container, image=tk_thumb,
                                     command=lambda p=image_path: show_preview(app, p))
            # Speichere die Referenz AM WIDGET, um GC zu verhindern
            thumb_button.image = tk_thumb

            # thumb_label.bind("<Button-1>", lambda e, p=image_path: show_preview(app, p))

            thumb_button.grid(row=row_num, column=col_num, padx=PADDING, pady=PADDING)

            # Nächste Grid-Position berechnen
            col_num += 1
            if col_num >= NUM_COLUMNS:
                col_num = 0
                row_num += 1

        except Exception as e:
            print(f"Fehler beim Laden/Verarbeiten von {os.path.basename(image_path)}: {e}")
            # Optional: Platzhalter anzeigen oder Eintrag überspringen

def show_preview(app, image_path):
    """Zeigt das ausgewählte Bild im 'image_preview' Widget an."""
    preview_widget = app.widgets.get('image_preview')
    label_widget = app.widgets.get('image_label')

    if preview_widget and hasattr(preview_widget, 'load_image'):
        print(f"Lade Vorschau für: {image_path}")
        # Rufe die neue load_image Methode des Picture Widgets auf
        preview_widget.load_image(image_path)
    elif preview_widget:
        print(f"Fehler: Widget 'image_preview' hat keine Methode 'load_image'.")
    else:
        print(f"Fehler: Widget 'image_preview' nicht gefunden.")

    if label_widget:
        label_widget.config(text=os.path.basename(image_path))


def undo():
    print("Rückgängig gemacht.")

def redo():
    print("Wiederholt.")

def show_about():
    print("Über diese Anwendung...")
