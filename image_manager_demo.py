import os
import tkinter as tk
from tkinter import messagebox
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("WARNUNG: Pillow (PIL) ist nicht installiert. Bildanzeige und -bearbeitung nicht möglich.")
    # Optional: exit() oder GUI mit Fehlermeldung anzeigen

from simplegui.core import SimpleGUI
from simplegui.yaml_loader import load_yaml_layout
from simplegui.filedialogs import FileDialogs
from simplegui.custom_widgets import Picture # Import Picture für Monkey-Patching oder Vererbung

# --- Picture Widget Erweiterung (Monkey Patching - wie zuvor) ---
# Besser: Diese Methoden direkt in custom_widgets.Picture einbauen!
def picture_set_image(self, pil_image):
    if not PIL_AVAILABLE: return
    try:
        # Zeigt ein PIL-Image im Picture-Widget an
        pil_image = pil_image.copy()
        # Skaliere das Bild für die Vorschau, behalte Seitenverhältnis bei
        pil_image.thumbnail((self.winfo_width() if self.winfo_width() > 1 else 400,
                             self.winfo_height() if self.winfo_height() > 1 else 400))
        self._imgtk = ImageTk.PhotoImage(pil_image)
        self.config(image=self._imgtk, width=self._imgtk.width(), height=self._imgtk.height()) # Größe anpassen
    except Exception as e:
        print(f"Fehler beim Setzen des Bildes im Picture Widget: {e}")
        self.clear() # Bei Fehler leeren

def picture_clear(self):
    self.config(image="")
    self._imgtk = None
    self.config(width=1, height=1) # Zurücksetzen, falls nötig

Picture.set_image = picture_set_image
Picture.clear = picture_clear
# --- Ende Picture Widget Erweiterung ---


class ImageManagerApp:
    def __init__(self, root):
        self.root = root
        if not PIL_AVAILABLE:
             root.title("Fehler")
             tk.Label(root, text="Fehler: Pillow (PIL) Bibliothek nicht gefunden.\nBitte installieren Sie Pillow (`pip install Pillow`).", fg="red", padx=20, pady=20).pack()
             return

        # --- Zustand ---
        self.current_dir = None
        self.image_files = []
        self.current_image = None
        self.current_image_path = None

        # --- Widgets (werden nach build() gefüllt) ---
        self.listbox = None
        self.image_label = None
        self.image_preview = None

        # --- SimpleGUI Instanz ---
        self.app = SimpleGUI(root, title="Bilderverwaltung", size="1100x500")

        # --- Layout laden ---
        self.layout = load_yaml_layout("image_manager_layout.yaml")
        if not self.layout:
            messagebox.showerror("Fehler", "Layout-Datei 'image_manager_layout.yaml' konnte nicht geladen werden.")
            root.destroy()
            return

        # --- Command Mapping (jetzt mit self.methoden) ---
        command_mapping = {
            "select_directory": self.select_directory,
            # "on_image_select" wird direkt via bind() verbunden, nicht über YAML command
            "rotate_left": self.rotate_left,
            "rotate_right": self.rotate_right,
            "crop_center": self.crop_center,
            "resize_half": self.resize_half,
            "save_image_as": self.save_image_as,
        }
        self._map_layout_commands(self.layout, command_mapping)

        # --- GUI bauen ---
        self.app.build(self.layout)

        # --- Widget-Referenzen holen ---
        self._get_widget_references()

        # --- Event Binding ---
        self._bind_events()

    def _get_widget_references(self):
        """Holt Referenzen auf wichtige Widgets nach dem Build."""
        self.listbox = self.app.get_widget("image_listbox")
        self.image_label = self.app.get_widget("image_label")
        self.image_preview = self.app.get_widget("image_preview")

        # Überprüfen, ob Widgets gefunden wurden
        if not self.listbox:
            messagebox.showerror("Layout Fehler", "Widget 'image_listbox' nicht im Layout gefunden!")
        if not self.image_label:
             messagebox.showerror("Layout Fehler", "Widget 'image_label' nicht im Layout gefunden!")
        if not self.image_preview:
             messagebox.showerror("Layout Fehler", "Widget 'image_preview' nicht im Layout gefunden!")
        # Ggf. Programm beenden, wenn kritische Widgets fehlen
        if not all([self.listbox, self.image_label, self.image_preview]):
             self.root.destroy()


    def _bind_events(self):
        """Bindet notwendige Tkinter-Events."""
        if self.listbox:
            self.listbox.bind("<<ListboxSelect>>", self.on_image_select)
        else:
            print("FEHLER: Konnte Event nicht binden, da 'image_listbox' nicht gefunden wurde.")

    # --- Hilfsfunktion zum Mappen (intern) ---
    def _map_layout_commands(self, layout_data, mapping):
        if isinstance(layout_data, dict):
            for key, value in layout_data.items():
                if key == "command" and isinstance(value, str) and value in mapping:
                    layout_data[key] = mapping[value]
                elif isinstance(value, (dict, list)):
                    self._map_layout_commands(value, mapping)
        elif isinstance(layout_data, list):
            for item in layout_data:
                self._map_layout_commands(item, mapping)

    # --- Methoden (vorher globale Funktionen) ---
    def is_image_file(self, filename):
        return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')) # Mehr Formate

    def update_image_listbox(self):
        if not self.listbox: return
        self.listbox.delete(0, tk.END)
        for fname in self.image_files:
            self.listbox.insert(tk.END, fname)

    def select_directory(self):
        dirname = FileDialogs.open_directory()
        if dirname:
            self.current_dir = dirname
            try:
                # TODO: Feedback für Benutzer bei großen Verzeichnissen
                files = os.listdir(dirname)
                # Verwende self.image_files direkt
                self.image_files = sorted([f for f in files if self.is_image_file(f)], key=str.lower) # Sortiert
                self.update_image_listbox()
                if self.image_label:
                    self.image_label.config(text="Kein Bild ausgewählt.")
                if self.image_preview:
                    self.image_preview.clear()
                self.current_image = None
                self.current_image_path = None
            except OSError as e:
                 messagebox.showerror("Fehler", f"Fehler beim Lesen des Verzeichnisses:\n{e}")
            except Exception as e:
                 messagebox.showerror("Fehler", f"Ein unerwarteter Fehler ist aufgetreten:\n{e}")


    def on_image_select(self, event=None):
        # Verwende event.widget statt self.app.get_widget()
        listbox_widget = event.widget
        selection = listbox_widget.curselection()
        if not selection:
            return

        idx = selection[0]
        if 0 <= idx < len(self.image_files): # Sicherheitscheck
            fname = self.image_files[idx]
            if not self.current_dir: return # Sicherstellen, dass ein Verzeichnis gewählt wurde
            path = os.path.join(self.current_dir, fname)
            try:
                img = Image.open(path)
                # Wichtig: .copy(), damit Originaldatei nicht gesperrt bleibt (manchmal nötig)
                self.current_image = img.copy()
                self.current_image_path = path
                img.close() # Originaldatei schließen

                if self.image_label:
                    self.image_label.config(text=f"Bild: {fname}")
                if self.image_preview:
                    self.image_preview.set_image(self.current_image) # Kopie anzeigen

            except FileNotFoundError:
                 messagebox.showerror("Fehler", f"Datei nicht gefunden:\n{path}")
                 self.image_files.pop(idx) # Entferne nicht gefundene Datei aus Liste
                 self.update_image_listbox()
            except (Image.UnidentifiedImageError, OSError) as e: # Spezifischere Fehler
                messagebox.showerror("Fehler", f"Bild konnte nicht geladen oder identifiziert werden:\n{fname}\n\n{e}")
                # Optional: Datei aus Liste entfernen oder markieren
            except Exception as e:
                messagebox.showerror("Fehler", f"Bild konnte nicht geladen werden:\n{e}")
        else:
            print(f"Ungültiger Index {idx} in on_image_select.")


    def rotate_left(self):
        if self.current_image and self.image_preview:
            self.current_image = self.current_image.rotate(90, expand=True)
            self.image_preview.set_image(self.current_image)

    def rotate_right(self):
        if self.current_image and self.image_preview:
            self.current_image = self.current_image.rotate(-90, expand=True)
            self.image_preview.set_image(self.current_image)

    def crop_center(self):
        if self.current_image and self.image_preview:
            try:
                w, h = self.current_image.size
                # Crop auf ein Viertel der Fläche in der Mitte
                margin_w = w // 4
                margin_h = h // 4
                left = margin_w
                top = margin_h
                right = w - margin_w
                bottom = h - margin_h
                # Sicherstellen, dass die Box gültig ist
                if left < right and top < bottom:
                    self.current_image = self.current_image.crop((left, top, right, bottom))
                    self.image_preview.set_image(self.current_image)
                else:
                    messagebox.showwarning("Crop", "Bild ist zu klein zum Zuschneiden.")
            except Exception as e:
                 messagebox.showerror("Fehler", f"Fehler beim Zuschneiden:\n{e}")


    def resize_half(self):
        if self.current_image and self.image_preview:
            w, h = self.current_image.size
            if w > 1 and h > 1: # Nur verkleinern, wenn sinnvoll
                self.current_image = self.current_image.resize((w // 2, h // 2), Image.Resampling.LANCZOS) # Bessere Qualität
                self.image_preview.set_image(self.current_image)
            else:
                 messagebox.showwarning("Resize", "Bild ist bereits sehr klein.")

    def save_image_as(self):
        if self.current_image:
            # Bessere Dateitypen
            filetypes = [
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg;*.jpeg"),
                ("Bitmap Image", "*.bmp"),
                ("WebP Image", "*.webp"),
                ("All Files", "*.*")
            ]
            # Vorschlag für Dateinamen basierend auf Original + Suffix
            original_name = os.path.basename(self.current_image_path) if self.current_image_path else "image"
            name_part, ext_part = os.path.splitext(original_name)
            initial_file = f"{name_part}_edited.png" # Standardmäßig PNG vorschlagen

            filepath = FileDialogs.save_file_as(
                defaultextension=".png",
                filetypes=filetypes,
                initialfile=initial_file,
                initialdir=self.current_dir # Im aktuellen Verzeichnis starten
            )
            if filepath:
                try:
                    # Speichern mit Optimierung/Qualität je nach Typ
                    file_ext = os.path.splitext(filepath)[1].lower()
                    save_options = {}
                    if file_ext == ".png":
                        save_options['optimize'] = True
                    elif file_ext in [".jpg", ".jpeg"]:
                        save_options['quality'] = 90 # Gute Qualität für JPG
                        save_options['optimize'] = True

                    self.current_image.save(filepath, **save_options)
                    messagebox.showinfo("Gespeichert", f"Bild gespeichert als:\n{filepath}")
                except ValueError:
                     messagebox.showerror("Fehler", f"Unbekanntes oder nicht unterstütztes Dateiformat zum Speichern:\n{file_ext}")
                except Exception as e:
                    messagebox.showerror("Fehler", f"Bild konnte nicht gespeichert werden:\n{e}")

    def run(self):
        """Startet die Tkinter Hauptschleife."""
        if PIL_AVAILABLE and self.layout: # Nur starten, wenn alles ok ist
            self.root.mainloop()

# --- App starten ---
if __name__ == "__main__":
    root = tk.Tk()
    app_instance = ImageManagerApp(root)
    app_instance.run()
