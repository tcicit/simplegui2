from tkinter import filedialog

class FileDialogs:
    @staticmethod
    def open_file(filetypes=(("All files", "*.*"),)):
        """Open a file dialog and return the selected file path."""
        return filedialog.askopenfilename(filetypes=filetypes)

    @staticmethod
    def save_file(defaultextension=".txt", filetypes=(("Text files", "*.txt"),)):
        """Open a save file dialog and return the selected file path."""
        return filedialog.asksaveasfilename(defaultextension=defaultextension, filetypes=filetypes)
    
    @staticmethod
    def open_directory():
        """Open a directory dialog and return the selected directory path."""
        return filedialog.askdirectory()
    
    @staticmethod
    def save_file_as(defaultextension=".txt", filetypes=(("Text files", "*.txt"),)):
        """Open a 'save as' dialog and return the selected file path."""
        return filedialog.asksaveasfilename(defaultextension=defaultextension, filetypes=filetypes)
    
    @staticmethod
    def open_multiple_files(filetypes=(("All files", "*.*"),)):
        """Open a dialog to select multiple files and return the selected file paths."""
        return filedialog.askopenfilenames(filetypes=filetypes)
    
    @staticmethod
    def open_file_with_title(title, filetypes=(("All files", "*.*"),)):
        """Open a file dialog with a custom title."""
        return filedialog.askopenfilename(title=title, filetypes=filetypes)
    
    @staticmethod
    def save_file_with_title(title, defaultextension=".txt", filetypes=(("Text files", "*.txt"),)):
        """Open a save file dialog with a custom title."""
        return filedialog.asksaveasfilename(title=title, defaultextension=defaultextension, filetypes=filetypes)
    
    @staticmethod
    def open_directory_with_title(title):
        """Open a directory dialog with a custom title."""
        return filedialog.askdirectory(title=title)
    
    @staticmethod
    def open_multiple_files_with_title(title, filetypes=(("All files", "*.*"),)):
        """Open a dialog to select multiple files with a custom title."""
        return filedialog.askopenfilenames(title=title, filetypes=filetypes)

    @staticmethod
    def open_file_with_initialdir(initialdir, filetypes=(("All files", "*.*"),)):
        """Open a file dialog with a custom initial directory."""
        return filedialog.askopenfilename(initialdir=initialdir, filetypes=filetypes)

    @staticmethod
    def save_file_with_initialdir(initialdir, defaultextension=".txt", filetypes=(("Text files", "*.txt"),)):
        """Open a save file dialog with a custom initial directory."""
        return filedialog.asksaveasfilename(initialdir=initialdir, defaultextension=defaultextension, filetypes=filetypes)

    @staticmethod
    def open_directory_with_initialdir(initialdir):
        """Open a directory dialog with a custom initial directory."""
        return filedialog.askdirectory(initialdir=initialdir)

    @staticmethod
    def open_multiple_files_with_initialdir(initialdir, filetypes=(("All files", "*.*"),)):
        """Open a dialog to select multiple files with a custom initial directory."""
        return filedialog.askopenfilenames(initialdir=initialdir, filetypes=filetypes)

    @staticmethod
    def open_file_with_initialdir_and_title(initialdir, title, filetypes=(("All files", "*.*"),)):
        """Open a file dialog with a custom initial directory and title."""
        return filedialog.askopenfilename(initialdir=initialdir, title=title, filetypes=filetypes)

    @staticmethod
    def save_file_with_initialdir_and_title(initialdir, title, defaultextension=".txt", filetypes=(("Text files", "*.txt"),)):
        """Open a save file dialog with a custom initial directory and title."""
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, defaultextension=defaultextension, filetypes=filetypes)

    @staticmethod
    def open_directory_with_initialdir_and_title(initialdir, title):
        """Open a directory dialog with a custom initial directory and title."""
        return filedialog.askdirectory(initialdir=initialdir, title=title)

    @staticmethod
    def open_multiple_files_with_initialdir_and_title(initialdir, title, filetypes=(("All files", "*.*"),)):
        """Open a dialog to select multiple files with a custom initial directory and title."""
        return filedialog.askopenfilenames(initialdir=initialdir, title=title, filetypes=filetypes)

    @staticmethod
    def open_file_with_initialdir_and_title_and_parent(initialdir, title, parent, filetypes=(("All files", "*.*"),)):
        """Open a file dialog with a custom initial directory, title, and parent window."""
        return filedialog.askopenfilename(initialdir=initialdir, title=title, parent=parent, filetypes=filetypes)

    @staticmethod
    def save_file_with_initialdir_and_title_and_parent(initialdir, title, parent, defaultextension=".txt", filetypes=(("Text files", "*.txt"),)):
        """Open a save file dialog with a custom initial directory, title, and parent window."""
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, parent=parent, defaultextension=defaultextension, filetypes=filetypes)

    @staticmethod
    def open_directory_with_initialdir_and_title_and_parent(initialdir, title, parent):
        """Open a directory dialog with a custom initial directory, title, and parent window."""
        return filedialog.askdirectory(initialdir=initialdir, title=title, parent=parent)

    @staticmethod
    def open_multiple_files_with_initialdir_and_title_and_parent(initialdir, title, parent, filetypes=(("All files", "*.*"),)):
        """Open a dialog to select multiple files with a custom initial directory, title, and parent window."""
        return filedialog.askopenfilenames(initialdir=initialdir, title=title, parent=parent, filetypes=filetypes)

    @staticmethod
    def open_file_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options, filetypes=(("All files", "*.*"),)):
        """Open a file dialog with a custom initial directory, title, parent window, and options."""
        return filedialog.askopenfilename(initialdir=initialdir, title=title, parent=parent, options=options, filetypes=filetypes)

    @staticmethod
    def save_file_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options, defaultextension=".txt", filetypes=(("Text files", "*.txt"),)):
        """Open a save file dialog with a custom initial directory, title, parent window, and options."""
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, parent=parent, options=options, defaultextension=defaultextension, filetypes=filetypes)

    @staticmethod
    def open_directory_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options):
        """Open a directory dialog with a custom initial directory, title, parent window, and options."""
        return filedialog.askdirectory(initialdir=initialdir, title=title, parent=parent, options=options)

    @staticmethod
    def open_multiple_files_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options, filetypes=(("All files", "*.*"),)):
        """Open a dialog to select multiple files with a custom initial directory, title, parent window, and options."""
        return filedialog.askopenfilenames(initialdir=initialdir, title=title, parent=parent, options=options, filetypes=filetypes)

    @staticmethod
    def open_file_with_initialdir_and_title_and_parent_and_options_and_filters(initialdir, title, parent, options, filters, filetypes=(("All files", "*.*"),)):
        """Open a file dialog with a custom initial directory, title, parent window, options, and filters."""
        return filedialog.askopenfilename(initialdir=initialdir, title=title, parent=parent, options=options, filters=filters, filetypes=filetypes)

    @staticmethod
    def save_file_with_initialdir_and_title_and_parent_and_options_and_filters(initialdir, title, parent, options, filters, defaultextension=".txt", filetypes=(("Text files", "*.txt"),)):
        """Open a save file dialog with a custom initial directory, title, parent window, options, and filters."""
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, parent=parent, options=options, filters=filters, defaultextension=defaultextension, filetypes=filetypes)

    @staticmethod
    def open_directory_with_initialdir_and_title_and_parent_and_options_and_filters(initialdir, title, parent, options, filters):
        """Open a directory dialog with a custom initial directory, title, parent window, options, and filters."""
        return filedialog.askdirectory(initialdir=initialdir, title=title, parent=parent, options=options, filters=filters)

    @staticmethod
    def open_multiple_files_with_initialdir_and_title_and_parent_and_options_and_filters(initialdir, title, parent, options, filters, filetypes=(("All files", "*.*"),)):
        """Open a dialog to select multiple files with a custom initial directory, title, parent window, options, and filters."""
        return filedialog.askopenfilenames(initialdir=initialdir, title=title, parent=parent, options=options, filters=filters, filetypes=filetypes)

    @staticmethod
    def save_file_as_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options, defaultextension=".txt", filetypes=(("Text files", "*.txt"),)):
        """Open a 'save as' dialog with a custom initial directory, title, parent window, and options."""
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, parent=parent, options=options, defaultextension=defaultextension, filetypes=filetypes)
