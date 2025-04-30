
from tkinter import messagebox

class Messages:
    @staticmethod
    def info(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def warning(title, message):
        messagebox.showwarning(title, message)

    @staticmethod
    def error(title, message):
        messagebox.showerror(title, message)
    
    @staticmethod
    def question(title, message):
        return messagebox.askquestion(title, message)
    
    @staticmethod
    def yesno(title, message):
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def okcancel(title, message):
        return messagebox.askokcancel(title, message)
    
    @staticmethod
    def retrycancel(title, message):
        return messagebox.askretrycancel(title, message)
    
    @staticmethod
    def yesnocancel(title, message):
        return messagebox.askyesnocancel(title, message)
    @staticmethod
    def askstring(title, message):
        return messagebox.askstring(title, message)
    @staticmethod
    def askinteger(title, message):
        return messagebox.askinteger(title, message)
    @staticmethod
    def askfloat(title, message):
        return messagebox.askfloat(title, message)
    @staticmethod
    def askcolor(title, message):
        return messagebox.askcolor(title, message)
    @staticmethod
    def askdirectory(title, message):
        return messagebox.askdirectory(title, message)
    @staticmethod
    def askopenfilename(title, message):
        return messagebox.askopenfilename(title, message)
    @staticmethod
    def asksaveasfilename(title, message):
        return messagebox.asksaveasfilename(title, message)
    @staticmethod
    def askopenfilenames(title, message):
        return messagebox.askopenfilenames(title, message)
    @staticmethod
    def askopenfile(title, message):
        return messagebox.askopenfile(title, message)
    @staticmethod
    def askopenfiles(title, message):
        return messagebox.askopenfiles(title, message)
    @staticmethod
    def askopenfiletypes(title, message):
        return messagebox.askopenfiletypes(title, message)
    @staticmethod
    def askopenfilestypes(title, message):
        return messagebox.askopenfilestypes(title, message)
    @staticmethod
    def askopenfiletypes(title, message):
        return messagebox.askopenfiletypes(title, message)
    @staticmethod
    def askopenfilestypes(title, message):
        return messagebox.askopenfilestypes(title, message)
    @staticmethod
    def askopenfiletypes(title, message):
        return messagebox.askopenfiletypes(title, message)
    @staticmethod
    def askopenfilestypes(title, message):
        return messagebox.askopenfilestypes(title, message)
