from simplegui.messages import Messages
from simplegui.filedialogs import FileDialogs
import tkinter as tk
from tkinter import filedialog, messagebox # Import messagebox
import os # Hinzugefügt für Verzeichnisoperationen
from PIL import Image, ImageTk # Für Bildverarbeitung (Thumbnails)


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


def undo(app):
    print("Rückgängig gemacht.")

def redo(app):
    print("Wiederholt.")

def show_about(app):
    print("Über diese Anwendung...")
    messagebox.showinfo("Über", "Dies ist eine einfache GUI-Anwendung.\nVersion 1.0\n(c) 2025")

def _update_preview_image(preview, pil_image):
    # Zielgröße bestimmen
    width = getattr(preview, "desired_width", None) or preview.winfo_width()
    height = getattr(preview, "desired_height", None) or preview.winfo_height()
    # Fallback: Versuche aus Optionen zu lesen
    if hasattr(preview, "options"):
        width = preview.options.get("width", width)
        height = preview.options.get("height", height)
    # Seitenverhältnis erhalten
    if width and height:
        img_w, img_h = pil_image.size
        ratio = min(width / img_w, height / img_h)
        new_size = (max(1, int(img_w * ratio)), max(1, int(img_h * ratio)))
        img = pil_image.copy().resize(new_size, Image.Resampling.LANCZOS)
    else:
        img = pil_image
    preview._photo_image = ImageTk.PhotoImage(img)
    preview.config(image=preview._photo_image)

def rotate_left(app):
    """Dreht das aktuell angezeigte Bild um 90 Grad nach links und skaliert es passend."""
    preview = app.widgets.get('image_preview')
    if hasattr(preview, '_pil_image') and preview._pil_image:
        img = preview._pil_image.rotate(90, expand=True)
        preview._pil_image = img
        _update_preview_image(preview, img)
    else:
        messagebox.showwarning("Kein Bild", "Kein Bild zum Drehen geladen.")

def rotate_right(app):
    """Dreht das aktuell angezeigte Bild um 90 Grad nach rechts und skaliert es passend."""
    preview = app.widgets.get('image_preview')
    if hasattr(preview, '_pil_image') and preview._pil_image:
        img = preview._pil_image.rotate(-90, expand=True)
        preview._pil_image = img
        _update_preview_image(preview, img)
    else:
        messagebox.showwarning("Kein Bild", "Kein Bild zum Drehen geladen.")

def crop_center(app):
    """Schneidet das Bild quadratisch in der Mitte zu."""
    preview = app.widgets.get('image_preview')
    if hasattr(preview, '_pil_image') and preview._pil_image:
        img = preview._pil_image
        w, h = img.size
        min_side = min(w, h)
        left = (w - min_side) // 2
        top = (h - min_side) // 2
        right = left + min_side
        bottom = top + min_side
        cropped = img.crop((left, top, right, bottom))
        preview._pil_image = cropped
        preview._photo_image = ImageTk.PhotoImage(cropped)
        preview.config(image=preview._photo_image)
    else:
        messagebox.showwarning("Kein Bild", "Kein Bild zum Zuschneiden geladen.")

def resize_half(app):
    """Verkleinert das Bild auf die Hälfte der aktuellen Größe."""
    preview = app.widgets.get('image_preview')
    if hasattr(preview, '_pil_image') and preview._pil_image:
        img = preview._pil_image
        w, h = img.size
        resized = img.resize((max(1, w // 2), max(1, h // 2)), Image.Resampling.LANCZOS)
        preview._pil_image = resized
        preview._photo_image = ImageTk.PhotoImage(resized)
        preview.config(image=preview._photo_image)
    else:
        messagebox.showwarning("Kein Bild", "Kein Bild zum Verkleinern geladen.")

def save_image_as(app):
    """Speichert das aktuell angezeigte Bild unter einem neuen Namen."""
    preview = app.widgets.get('image_preview')
    if hasattr(preview, '_pil_image') and preview._pil_image:
        filetypes = [("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("BMP", "*.bmp"), ("Alle Dateien", "*.*")]
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)
        if filepath:
            try:
                preview._pil_image.save(filepath)
                messagebox.showinfo("Bild gespeichert", f"Bild gespeichert als:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Fehler beim Speichern", str(e))
    else:
        messagebox.showwarning("Kein Bild", "Kein Bild zum Speichern geladen.")
