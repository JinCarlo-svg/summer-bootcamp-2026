import tkinter as tk
from tkinter import messagebox
import string
import secrets

def generate_password():
    try:
        length = int(length_entry.get())
        
        if length < 4:
            messagebox.showwarning("warning","the length of the password must be at least 4 characters!")
            return
        all_characters = string.ascii_letters + string.digits + string.punctuation
        
        password = "".join(secrets.choice(all_characters) for _ in range(length))
        
        result_entry.delete(0, tk.END)
        result_entry.insert(0, password)
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for the password length!")

def copy_to_clipboard():
    password = result_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Success", "Password copied to clipboard successfully! 📋")
    else:
        messagebox.showwarning("Warning", "The field is empty, please generate a password first!")

root = tk.Tk()
root.title("Password Generator")
root.geometry("400x350")
root.configure(bg="#1e1e2e") # Dark elegant design

title_label = tk.Label(root, text="Password Generator", font=("Helvetica", 18, "bold"), bg="#1e1e2e", fg="#cdd6f4")
title_label.pack(pady=15)

length_label = tk.Label(root, text="Password Length:", font=("Helvetica", 11), bg="#1e1e2e", fg="#a6adc8")
length_label.pack(pady=5)

length_entry = tk.Entry(root, font=("Helvetica", 12), width=10, justify="center", bg="#313244", fg="#cdd6f4", borderwidth=0)
length_entry.insert(0, "12")
length_entry.pack(pady=5)

gen_button = tk.Button(root, text="Generate Secure Password 🚀", font=("Helvetica", 12, "bold"), bg="#a6e3a1", fg="#11111b", borderwidth=0, padx=10, pady=5, command=generate_password)
gen_button.pack(pady=15)
result_entry = tk.Entry(root, font=("Helvetica", 14), width=25, justify="center", bg="#313244", fg="#f38ba8", borderwidth=0)
result_entry.pack(pady=10)

copy_button = tk.Button(root, text="Copy to Clipboard 📋", font=("Helvetica", 10), bg="#89b4fa", fg="#11111b", borderwidth=0, command=copy_to_clipboard)
copy_button.pack(pady=10)
root.mainloop()
