import tkinter as tk
from tkinter import ttk

def open_inventory(window):
    inventory_window = tk.Toplevel(window)
    inventory_window.title("Inventory")
    inventory_window.geometry("400x250")
    inventory_window.configure(bg="#34495E")

    # Set position to be near the main window
    x_offset = window.winfo_x() + 50
    y_offset = window.winfo_y() + 50
    inventory_window.geometry(f"+{x_offset}+{y_offset}")

    inventory_label = ttk.Label(inventory_window, text="Your Inventory", font=("Helvetica", 12, "bold"))
    inventory_label.pack(pady=10)

    inventory_display = tk.Text(inventory_window, height=10, width=30, state='normal', wrap='word', font=("Helvetica", 10))
    inventory_display.pack(pady=5)
    inventory_display.insert(tk.END, "\n".join(f"{fish}: {count}" for fish, count in inventory.items()))
    inventory_display.config(state='disabled')
