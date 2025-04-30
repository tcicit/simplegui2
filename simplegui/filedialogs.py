
from tkinter import filedialog

class FileDialogs:
    @staticmethod
    def open_file(filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilename(filetypes=filetypes)

    @staticmethod
    def save_file(defaultextension=".txt", filetypes=(("Textdateien", "*.txt"),)):
        return filedialog.asksaveasfilename(defaultextension=defaultextension, filetypes=filetypes)
    
    @staticmethod
    def open_directory():
        return filedialog.askdirectory()
    
    @staticmethod
    def save_file_as(defaultextension=".txt", filetypes=(("Textdateien", "*.txt"),)):
        return filedialog.asksaveasfilename(defaultextension=defaultextension, filetypes=filetypes)
    
    @staticmethod
    def open_multiple_files(filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilenames(filetypes=filetypes)
    
    @staticmethod
    def open_file_with_title(title, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilename(title=title, filetypes=filetypes)
    
    @staticmethod
    def save_file_with_title(title, defaultextension=".txt", filetypes=(("Textdateien", "*.txt"),)):
        return filedialog.asksaveasfilename(title=title, defaultextension=defaultextension, filetypes=filetypes)
    
    @staticmethod
    def open_directory_with_title(title):
        return filedialog.askdirectory(title=title)
    
    @staticmethod
    def open_multiple_files_with_title(title, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilenames(title=title, filetypes=filetypes)
    @staticmethod
    def open_file_with_initialdir(initialdir, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilename(initialdir=initialdir, filetypes=filetypes)
    @staticmethod
    def save_file_with_initialdir(initialdir, defaultextension=".txt", filetypes=(("Textdateien", "*.txt"),)):
        return filedialog.asksaveasfilename(initialdir=initialdir, defaultextension=defaultextension, filetypes=filetypes)
    @staticmethod
    def open_directory_with_initialdir(initialdir):
        return filedialog.askdirectory(initialdir=initialdir)
    @staticmethod
    def open_multiple_files_with_initialdir(initialdir, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilenames(initialdir=initialdir, filetypes=filetypes)
    @staticmethod
    def open_file_with_initialdir_and_title(initialdir, title, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilename(initialdir=initialdir, title=title, filetypes=filetypes)
    @staticmethod
    def save_file_with_initialdir_and_title(initialdir, title, defaultextension=".txt", filetypes=(("Textdateien", "*.txt"),)):
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, defaultextension=defaultextension, filetypes=filetypes)
    @staticmethod
    def open_directory_with_initialdir_and_title(initialdir, title):
        return filedialog.askdirectory(initialdir=initialdir, title=title)
    @staticmethod
    def open_multiple_files_with_initialdir_and_title(initialdir, title, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilenames(initialdir=initialdir, title=title, filetypes=filetypes)
    @staticmethod
    def open_file_with_initialdir_and_title_and_parent(initialdir, title, parent, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilename(initialdir=initialdir, title=title, parent=parent, filetypes=filetypes)
    @staticmethod
    def save_file_with_initialdir_and_title_and_parent(initialdir, title, parent, defaultextension=".txt", filetypes=(("Textdateien", "*.txt"),)):
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, parent=parent, defaultextension=defaultextension, filetypes=filetypes)
    @staticmethod
    def open_directory_with_initialdir_and_title_and_parent(initialdir, title, parent):
        return filedialog.askdirectory(initialdir=initialdir, title=title, parent=parent)
    @staticmethod
    def open_multiple_files_with_initialdir_and_title_and_parent(initialdir, title, parent, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilenames(initialdir=initialdir, title=title, parent=parent, filetypes=filetypes)
    @staticmethod
    def open_file_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilename(initialdir=initialdir, title=title, parent=parent, options=options, filetypes=filetypes)
    @staticmethod
    def save_file_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options, defaultextension=".txt", filetypes=(("Textdateien", "*.txt"),)):
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, parent=parent, options=options, defaultextension=defaultextension, filetypes=filetypes)
    @staticmethod
    def open_directory_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options):
        return filedialog.askdirectory(initialdir=initialdir, title=title, parent=parent, options=options)
    @staticmethod
    def open_multiple_files_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilenames(initialdir=initialdir, title=title, parent=parent, options=options, filetypes=filetypes)
    @staticmethod
    def open_file_with_initialdir_and_title_and_parent_and_options_and_filters(initialdir, title, parent, options, filters, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilename(initialdir=initialdir, title=title, parent=parent, options=options, filters=filters, filetypes=filetypes)
    @staticmethod
    def save_file_with_initialdir_and_title_and_parent_and_options_and_filters(initialdir, title, parent, options, filters, defaultextension=".txt", filetypes=(("Textdateien", "*.txt"),)):
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, parent=parent, options=options, filters=filters, defaultextension=defaultextension, filetypes=filetypes)
    @staticmethod
    def open_directory_with_initialdir_and_title_and_parent_and_options_and_filters(initialdir, title, parent, options, filters):
        return filedialog.askdirectory(initialdir=initialdir, title=title, parent=parent, options=options, filters=filters)
    @staticmethod
    def open_multiple_files_with_initialdir_and_title_and_parent_and_options_and_filters(initialdir, title, parent, options, filters, filetypes=(("Alle Dateien", "*.*"),)):
        return filedialog.askopenfilenames(initialdir=initialdir, title=title, parent=parent, options=options, filters=filters, filetypes=filetypes)
    @staticmethod
    def save_file_as_with_initialdir_and_title_and_parent_and_options(initialdir, title, parent, options, defaultextension=".txt", filetypes=(("Textdateien", "*.txt"),)):
        return filedialog.asksaveasfilename(initialdir=initialdir, title=title, parent=parent, options=options, defaultextension=defaultextension, filetypes=filetypes)
