from tkinter import messagebox

class Messages:
    """
    Utility class for showing various message and dialog boxes using tkinter.messagebox.
    All methods are static and can be called without instantiating the class.
    """

    @staticmethod
    def info(title, message):
        """Show an informational message box."""
        messagebox.showinfo(title, message)

    @staticmethod
    def warning(title, message):
        """Show a warning message box."""
        messagebox.showwarning(title, message)

    @staticmethod
    def error(title, message):
        """Show an error message box."""
        messagebox.showerror(title, message)
    
    @staticmethod
    def question(title, message):
        """Show a question dialog (returns 'yes' or 'no' as string)."""
        return messagebox.askquestion(title, message)
    
    @staticmethod
    def yesno(title, message):
        """Show a Yes/No dialog (returns True for Yes, False for No)."""
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def okcancel(title, message):
        """Show an OK/Cancel dialog (returns True for OK, False for Cancel)."""
        return messagebox.askokcancel(title, message)
    
    @staticmethod
    def retrycancel(title, message):
        """Show a Retry/Cancel dialog (returns True for Retry, False for Cancel)."""
        return messagebox.askretrycancel(title, message)
    
    @staticmethod
    def yesnocancel(title, message):
        """Show a Yes/No/Cancel dialog (returns True, False, or None)."""
        return messagebox.askyesnocancel(title, message)

    
