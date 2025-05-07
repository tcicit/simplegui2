from simplegui.messages import Messages
from simplegui.filedialogs import FileDialogs
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

def exit_app(app):
    """Exit the application."""
    app.root.quit()  # Use the root reference from the app instance

def open_file(app):
    """Open a file using a file dialog and display a message if successful."""
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
    """Save a file under a new name using a file dialog."""
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
    """Open a directory dialog and return the selected directory."""
    print("Selecting directory...")
    try:
        directory = filedialog.askdirectory(title="Select directory")
        if directory:
            print(f"Selected directory: {directory}")
            return directory
        else:
            print("No directory selected.")
            return None
    except Exception as e:
        print(f"Error while opening directory: {e}")
        messagebox.showerror("Error", f"Could not open directory:\n{e}")
        return None

def show_about(app):
    """Display an 'About' dialog with application information."""
    print("Showing 'About' information...")
    try:
        messagebox.showinfo("About", "This is a simple GUI application.\nVersion 1.0\n(c) 2025")
    except Exception as e:
        print(f"Error while showing 'About' dialog: {e}")

def save_file(app):
    """Save the current file to a user-specified location."""
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
    """Save the currently displayed image under a new name."""
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
    """Delete a selected file."""
    print("Deleting file...")
    try:
        filepath = filedialog.askopenfilename(title="Select a file to delete")
        if filepath:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n{filepath}")
            if confirm:
                try:
                    os.remove(filepath)
                    messagebox.showinfo("File Deleted", f"File deleted:\n{filepath}")
                except Exception as e:
                    print(f"Error while deleting file: {e}")
                    messagebox.showerror("Error", f"Could not delete file:\n{e}")
            else:
                print("File deletion canceled.")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while deleting file: {e}")
        messagebox.showerror("Error", f"Could not delete file:\n{e}")

def copy_file(app):
    """Copy a selected file to a new location."""
    print("Copying file...")
    try:
        source = filedialog.askopenfilename(title="Select a file to copy")
        if source:
            destination = filedialog.asksaveasfilename(title="Select destination for the copied file")
            if destination:
                try:
                    shutil.copy(source, destination)
                    messagebox.showinfo("File Copied", f"File copied to:\n{destination}")
                except Exception as e:
                    print(f"Error while copying file: {e}")
                    messagebox.showerror("Error", f"Could not copy file:\n{e}")
            else:
                print("No destination selected.")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while copying file: {e}")
        messagebox.showerror("Error", f"Could not copy file:\n{e}")

def move_file(app):
    """Move a selected file to a new location."""
    print("Moving file...")
    try:
        source = filedialog.askopenfilename(title="Select a file to move")
        if source:
            destination = filedialog.asksaveasfilename(title="Select destination for the moved file")
            if destination:
                try:
                    shutil.move(source, destination)
                    messagebox.showinfo("File Moved", f"File moved to:\n{destination}")
                except Exception as e:
                    print(f"Error while moving file: {e}")
                    messagebox.showerror("Error", f"Could not move file:\n{e}")
            else:
                print("No destination selected.")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while moving file: {e}")
        messagebox.showerror("Error", f"Could not move file:\n{e}")

def rename_file(app):
    """Rename a selected file."""
    print("Renaming file...")
    try:
        source = filedialog.askopenfilename(title="Select a file to rename")
        if source:
            new_name = filedialog.asksaveasfilename(initialfile=os.path.basename(source), title="Enter new file name")
            if new_name:
                try:
                    os.rename(source, new_name)
                    messagebox.showinfo("File Renamed", f"File renamed to:\n{new_name}")
                except Exception as e:
                    print(f"Error while renaming file: {e}")
                    messagebox.showerror("Error", f"Could not rename file:\n{e}")
            else:
                print("No new name provided.")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while renaming file: {e}")
        messagebox.showerror("Error", f"Could not rename file:\n{e}")

def check_disk_space(app):
    """Check the available disk space on the selected drive."""
    print("Checking disk space...")
    try:
        directory = filedialog.askdirectory(title="Select a directory to check disk space")
        if directory:
            try:
                stat = os.statvfs(directory)
                free_space = stat.f_bavail * stat.f_frsize
                total_space = stat.f_blocks * stat.f_frsize
                messagebox.showinfo("Disk Space", f"Total Space: {total_space / (1024**3):.2f} GB\n"
                                                  f"Free Space: {free_space / (1024**3):.2f} GB")
            except Exception as e:
                print(f"Error while checking disk space: {e}")
                messagebox.showerror("Error", f"Could not check disk space:\n{e}")
        else:
            print("No directory selected.")
    except Exception as e:
        print(f"Error while checking disk space: {e}")
        messagebox.showerror("Error", f"Could not check disk space:\n{e}")

def list_files_in_directory(app):
    """List all files in a selected directory."""
    print("Listing files in directory...")
    try:
        directory = filedialog.askdirectory(title="Select a directory to list files")
        if directory:
            try:
                files = os.listdir(directory)
                if files:
                    file_list = "\n".join(files)
                    messagebox.showinfo("Files in Directory", f"Files in {directory}:\n\n{file_list}")
                else:
                    messagebox.showinfo("Files in Directory", f"No files found in {directory}.")
            except Exception as e:
                print(f"Error while listing files: {e}")
                messagebox.showerror("Error", f"Could not list files:\n{e}")
        else:
            print("No directory selected.")
    except Exception as e:
        print(f"Error while listing files: {e}")
        messagebox.showerror("Error", f"Could not list files:\n{e}")

def validate_file_type(app, valid_extensions=(".png", ".jpg", ".jpeg")):
    """Validate if the selected file has a valid extension."""
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

def show_file_properties(app):
    """Display properties of a selected file."""
    print("Showing file properties...") 
    try:
        filepath = filedialog.askopenfilename(title="Select a file to show properties")
        if filepath:
            try:
                properties = os.stat(filepath)
                properties_info = f"File: {filepath}\n" \
                                  f"Size: {properties.st_size} bytes\n" \
                                  f"Last Modified: {properties.st_mtime}\n" \
                                  f"Last Accessed: {properties.st_atime}\n" \
                                  f"Creation Time: {properties.st_ctime}"
                messagebox.showinfo("File Properties", properties_info)
            except Exception as e:
                print(f"Error while getting file properties: {e}")
                messagebox.showerror("Error", f"Could not show file properties:\n{e}")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error while showing file properties: {e}")
        messagebox.showerror("Error", f"Could not show file properties:\n{e}")

def crate_directory(app):
    """
    Create a new directory at the specified location.
    The user selects a parent directory and enters a new directory name.
    """
    print("Creating directory...")
    try:
        # Ask user to select the parent directory
        parent_dir = filedialog.askdirectory(title="Select a location to create a new directory")
        if not parent_dir:
            print("No location selected.")
            return

        # Ask user for the new directory name (using a simple dialog)
        from tkinter.simpledialog import askstring
        new_dir_name = askstring("New Directory", "Enter new directory name:")
        if not new_dir_name or not new_dir_name.strip():
            print("No directory name provided.")
            messagebox.showwarning("No Name", "No directory name provided.")
            return

        # Compose the full path and create the directory
        new_dir_path = os.path.join(parent_dir, new_dir_name.strip())
        if os.path.exists(new_dir_path):
            print("Directory already exists.")
            messagebox.showwarning("Directory Exists", f"Directory already exists:\n{new_dir_path}")
            return

        os.makedirs(new_dir_path, exist_ok=False)
        messagebox.showinfo("Directory Created", f"Directory created:\n{new_dir_path}")
    except Exception as e:
        print(f"Error while creating directory: {e}")
        messagebox.showerror("Error", f"Could not create directory:\n{e}")

def delete_directory(app):
    """
    Delete a selected directory after user confirmation.
    The user selects a directory and must confirm deletion.
    """
    print("Deleting directory...")
    try:
        # Ask user to select the directory to delete
        directory = filedialog.askdirectory(title="Select a directory to delete")
        if not directory:
            print("No directory selected.")
            return

        # Prevent accidental deletion of root or home directories
        if directory in ("/", os.path.expanduser("~")):
            print("Refusing to delete system root or home directory.")
            messagebox.showwarning("Refused", "Refusing to delete system root or home directory.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n{directory}")
        if not confirm:
            print("Directory deletion canceled.")
            return

        # Delete the directory
        shutil.rmtree(directory)
        messagebox.showinfo("Directory Deleted", f"Directory deleted:\n{directory}")
    except Exception as e:
        print(f"Error while deleting directory: {e}")
        messagebox.showerror("Error", f"Could not delete directory:\n{e}")