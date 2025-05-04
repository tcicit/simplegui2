from simplegui.messages import Messages
from simplegui.filedialogs import FileDialogs
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk


def exit_app(app):
    """Exits the application gracefully."""
    print("Exiting application...")
    try:
        root = tk.Tk()
        root.quit()
    except Exception as e:
        print(f"Error while exiting the application: {e}")


def open_file(app):
    """Opens a file using a file dialog and displays a message if successful."""
    print("Opening file...")
    try:
        filename = FileDialogs.open_file()
        if filename:
            Messages.info("File opened", filename)
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while opening file: {e}")
        messagebox.showerror("Error", f"Could not open file:\n{e}")


def save_file_as(app):
    """Saves a file under a new name using a file dialog."""
    print("Saving file as...")
    try:
        filename = FileDialogs.save_file_as()
        if filename:
            Messages.info("File saved", filename)
        else:
            print("No file name provided.")
    except Exception as e:
        print(f"Error while saving file: {e}")
        messagebox.showerror("Error", f"Could not save file:\n{e}")


def open_directory(app):
    """Opens a directory dialog and prints the selected directory."""
    print("Attempting to open directory...")
    try:
        directory = filedialog.askdirectory(title="Select an image directory")
        if directory:
            print(f"Directory selected: {directory}")
        else:
            print("No directory selected.")
    except Exception as e:
        print(f"Error while opening directory: {e}")
        messagebox.showerror("Error", f"Could not open directory:\n{e}")


def show_about(app):
    """Displays an 'About' dialog with application information."""
    print("Showing 'About' information...")
    try:
        messagebox.showinfo("About", "This is a simple GUI application.\nVersion 1.0\n(c) 2025")
    except Exception as e:
        print(f"Error while showing 'About' dialog: {e}")


def save_file(app):
    """Saves the current file to a user-specified location."""
    print("Saving file...")
    try:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filepath:
            try:
                with open(filepath, 'w') as file:
                    file.write("File content")  # Replace with actual content to save
                messagebox.showinfo("File saved", f"File saved as:\n{filepath}")
            except Exception as e:
                print(f"Error while writing to file: {e}")
                messagebox.showerror("Error", f"Could not save file:\n{e}")
        else:
            print("No file name provided.")
    except Exception as e:
        print(f"Error while saving file: {e}")
        messagebox.showerror("Error", f"Could not save file:\n{e}")


def save_image_as(app):
    """Saves the currently displayed image under a new name."""
    print("Saving image as...")
    try:
        preview = app.widgets.get('image_preview')
        if hasattr(preview, '_pil_image') and preview._pil_image:
            filetypes = [("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("BMP", "*.bmp"), ("All files", "*.*")]
            filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)
            if filepath:
                try:
                    preview._pil_image.save(filepath)
                    messagebox.showinfo("Image saved", f"Image saved as:\n{filepath}")
                except Exception as e:
                    print(f"Error while saving image: {e}")
                    messagebox.showerror("Error", f"Could not save image:\n{e}")
            else:
                print("No file name provided.")
        else:
            print("No image loaded to save.")
            messagebox.showwarning("No Image", "No image loaded to save.")
    except Exception as e:
        print(f"Error while saving image: {e}")
        messagebox.showerror("Error", f"Could not save image:\n{e}")

def delete_file(app):
    """Deletes a selected file."""
    print("Deleting file...")
    try:
        filepath = filedialog.askopenfilename(title="Select a file to delete")
        if filepath:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n{filepath}")
            if confirm:
                os.remove(filepath)
                messagebox.showinfo("File Deleted", f"File deleted:\n{filepath}")
            else:
                print("File deletion canceled.")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while deleting file: {e}")
        messagebox.showerror("Error", f"Could not delete file:\n{e}")


import shutil

def copy_file(app):
    """Copies a selected file to a new location."""
    print("Copying file...")
    try:
        source = filedialog.askopenfilename(title="Select a file to copy")
        if source:
            destination = filedialog.asksaveasfilename(title="Select destination for the copied file")
            if destination:
                shutil.copy(source, destination)
                messagebox.showinfo("File Copied", f"File copied to:\n{destination}")
            else:
                print("No destination selected.")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while copying file: {e}")
        messagebox.showerror("Error", f"Could not copy file:\n{e}")

def move_file(app):
    """Moves a selected file to a new location."""
    print("Moving file...")
    try:
        source = filedialog.askopenfilename(title="Select a file to move")
        if source:
            destination = filedialog.asksaveasfilename(title="Select destination for the moved file")
            if destination:
                shutil.move(source, destination)
                messagebox.showinfo("File Moved", f"File moved to:\n{destination}")
            else:
                print("No destination selected.")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while moving file: {e}")
        messagebox.showerror("Error", f"Could not move file:\n{e}")

def rename_file(app):
    """Renames a selected file."""
    print("Renaming file...")
    try:
        source = filedialog.askopenfilename(title="Select a file to rename")
        if source:
            new_name = filedialog.asksaveasfilename(initialfile=os.path.basename(source), title="Enter new file name")
            if new_name:
                os.rename(source, new_name)
                messagebox.showinfo("File Renamed", f"File renamed to:\n{new_name}")
            else:
                print("No new name provided.")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while renaming file: {e}")
        messagebox.showerror("Error", f"Could not rename file:\n{e}")


def check_disk_space(app):
    """Checks the available disk space on the selected drive."""
    print("Checking disk space...")
    try:
        directory = filedialog.askdirectory(title="Select a directory to check disk space")
        if directory:
            stat = os.statvfs(directory)
            free_space = stat.f_bavail * stat.f_frsize
            total_space = stat.f_blocks * stat.f_frsize
            messagebox.showinfo("Disk Space", f"Total Space: {total_space / (1024**3):.2f} GB\n"
                                              f"Free Space: {free_space / (1024**3):.2f} GB")
        else:
            print("No directory selected.")
    except Exception as e:
        print(f"Error while checking disk space: {e}")
        messagebox.showerror("Error", f"Could not check disk space:\n{e}")


def list_files_in_directory(app):
    """Lists all files in a selected directory."""
    print("Listing files in directory...")
    try:
        directory = filedialog.askdirectory(title="Select a directory to list files")
        if directory:
            files = os.listdir(directory)
            if files:
                file_list = "\n".join(files)
                messagebox.showinfo("Files in Directory", f"Files in {directory}:\n\n{file_list}")
            else:
                messagebox.showinfo("Files in Directory", f"No files found in {directory}.")
        else:
            print("No directory selected.")
    except Exception as e:
        print(f"Error while listing files: {e}")
        messagebox.showerror("Error", f"Could not list files:\n{e}")


def validate_file_type(app, valid_extensions=(".png", ".jpg", ".jpeg")):
    """Validates if the selected file has a valid extension."""
    print("Validating file type...")
    try:
        filepath = filedialog.askopenfilename(title="Select a file to validate")
        if filepath:
            if filepath.lower().endswith(valid_extensions):
                messagebox.showinfo("File Validation", f"File is valid:\n{filepath}")
            else:
                messagebox.showwarning("File Validation", f"Invalid file type:\n{filepath}")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while validating file type: {e}")
        messagebox.showerror("Error", f"Could not validate file type:\n{e}")