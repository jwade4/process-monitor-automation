import tkinter as tk
from tkinter import messagebox

def notify_user(filepath):
    if filepath is None:
        return
    
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Process Monitor", f"Report saved successfully to:\n{filepath}")

    root.destroy()

    return None