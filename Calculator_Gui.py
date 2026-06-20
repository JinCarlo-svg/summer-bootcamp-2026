import tkinter as tk

def button_click(number):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(number))

def clear_screen():
    entry.delete(0, tk.END)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

root = tk.Tk()
root.title("Calculator")
root.geometry("350x450")
root.configure(bg="#222831")

entry = tk.Entry(root, font=("Helvetica", 24), bg="#393E46", fg="#EEEEEE", borderwidth=0, justify="right")
entry.grid(row=0, column=0, columnspan=4, ipady=20, padx=10, pady=10, sticky="nsew")

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),
]
for i in range(5):
    root.rowconfigure(i, weight=1)
for i in range(4):
    root.columnconfigure(i, weight=1)


for (text, row, col) in buttons:
    if text == '=':
        btn = tk.Button(root, text=text, font=("Helvetica", 18), bg="#080189", fg="#EEEEEE", borderwidth=0, command=calculate)
    elif text == 'C':
        btn = tk.Button(root, text=text, font=("Helvetica", 18), bg="#E82300", fg="#EEEEEE", borderwidth=0, command=clear_screen)
    else:
        btn = tk.Button(root, text=text, font=("Helvetica", 18), bg="#393E46", fg="#EEEEEE", borderwidth=0, command=lambda t=text: button_click(t))
        
    btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
root.mainloop()
