import tkinter as tk
from tkinter import ttk
import os

# Globals to be set from main.py
window = None
currency = {}
inventory = {}
update_inventory_display = None
currency_label = None
result_label = None
fish_types = {}
lives_label = None
lives = []

def open_shop():
    global window, currency, inventory, update_inventory_display, currency_label, result_label, fish_types, lives_label, lives

    shop_window = tk.Toplevel(window)
    shop_window.title("Fish Shop")
    shop_window.geometry("775x600")
    shop_window.configure(bg="#58a788")

    icon_image = tk.PhotoImage(file="assets\icon_image.png")
    shop_window.iconphoto(False, icon_image)

    # Set position to be near the main window
    x_offset = window.winfo_x() + 700
    y_offset = window.winfo_y()
    shop_window.geometry(f"+{x_offset}+{y_offset}")

    shop_label = ttk.Label(shop_window, text="Buy items or sell fish", font=("Helvetica", 14, "bold"), background="#2C3E50", foreground="white")
    shop_label.pack(pady=10)

    # Buy section
    buy_frame = tk.Frame(shop_window, bg="#34495E")
    buy_frame.pack(pady=10, padx=10, fill="x")

    # Configure grid columns for symmetry
    buy_frame.grid_columnconfigure(0, weight=1)
#    buy_frame.grid_columnconfigure(1, weight=1)
#    buy_frame.grid_columnconfigure(2, weight=1)
#    buy_frame.grid_columnconfigure(3, weight=1)
#    buy_frame.grid_columnconfigure(4, weight=1)

    def buy_item(item, quantity_str):
        price = 2 if item == "Live Bait" else 5
        try:
            quantity = int(quantity_str) if quantity_str.isdigit() else (currency["Gold"] // price)
            if quantity > 0 and currency["Gold"] >= quantity * price:
                currency["Gold"] -= quantity * price
                if item == "Life":
                    lives[0] += quantity
                    lives_label.config(text=f"Lives: {lives[0]}")
                    result_label.config(text=f"You bought {quantity} extra life(s)!", foreground="#4CAF50")
                else:
                    inventory[item] = inventory.get(item, 0) + quantity
                    update_inventory_display()
                    result_label.config(text=f"You bought {quantity} {item}(s)!", foreground="#4CAF50")
                currency_label.config(text=f"Gold: {currency['Gold']}")
            else:
                result_label.config(text="Not enough gold or invalid quantity!", foreground="#F44336")
        except ValueError:
            result_label.config(text="Invalid quantity!", foreground="#F44336")

    # Buy items buttons
    row_count = 0
    for item, price in [("Live Bait", 2), ("Life", 5)]:
        ttk.Label(buy_frame, text=f"Buy {item} ({price} gold each):", background="#34495E", foreground="white").grid(row=row_count, column=0, sticky='w', padx=5, pady=5)
        
        ttk.Button(buy_frame, text="Buy 1",     command=lambda i=item: buy_item(i, "1")).grid(row=row_count, column=1, padx=5, pady=5)
        ttk.Button(buy_frame, text="Buy 10",    command=lambda i=item: buy_item(i, "10")).grid(row=row_count, column=2, padx=5, pady=5)
        ttk.Button(buy_frame, text="Buy 100",   command=lambda i=item: buy_item(i, "100")).grid(row=row_count, column=3, padx=5, pady=5)
        ttk.Button(buy_frame, text="Buy Max",   command=lambda i=item: buy_item(i, "max")).grid(row=row_count, column=4, padx=5, pady=5)
        row_count += 1

    # Sell section
    sell_frame = tk.Frame(shop_window, bg="#34495E")
    sell_frame.pack(pady=10, padx=10, fill="x")

    # Configure grid columns for symmetry
    sell_frame.grid_columnconfigure(0, weight=1)
#    sell_frame.grid_columnconfigure(1, weight=1)
#    sell_frame.grid_columnconfigure(2, weight=1)
#    sell_frame.grid_columnconfigure(3, weight=1)
#    sell_frame.grid_columnconfigure(4, weight=1)

    def sell_fish(fish, quantity_str):
        if fish not in inventory:
            result_label.config(text=f"No {fish} in inventory!", foreground="#F44336")
            return

        try:
            quantity = int(quantity_str) if quantity_str.isdigit() else inventory[fish]
            if quantity > 0 and inventory[fish] >= quantity:
                points = fish_types[fish]['points']
                inventory[fish] -= quantity
                currency["Gold"] += quantity * points
                result_label.config(text=f"Sold {quantity} {fish} for {quantity * points} gold!", foreground="#4CAF50")
                update_inventory_display()
                currency_label.config(text=f"Gold: {currency['Gold']}")
            else:
                result_label.config(text=f"Not enough {fish} to sell!", foreground="#F44336")
        except ValueError:
            result_label.config(text="Invalid quantity!", foreground="#F44336")

    def sell_all_fish():
        total_earnings = 0
        for fish, data in fish_types.items():
            if fish in inventory and inventory[fish] > 0:
                total_earnings += inventory[fish] * data['points']
                inventory[fish] = 0

        if total_earnings > 0:
            currency["Gold"] += total_earnings
            result_label.config(text=f"Sold all fish for {total_earnings} gold!", foreground="#4CAF50")
            update_inventory_display()
            currency_label.config(text=f"Gold: {currency['Gold']}")
        else:
            result_label.config(text="No fish to sell!", foreground="#F44336")

    # Add labels and buttons for each fish type with proper column layout
    row_count = 0
    for fish, data in fish_types.items():
        ttk.Label(sell_frame, text=f"Sell {fish} ({data['points']} gold each):", background="#34495E", foreground="white").grid(row=row_count, column=0, sticky='w', padx=5, pady=5)

        # Buttons to sell different quantities of fish
        ttk.Button(sell_frame, text="Sell 1",   command=lambda f=fish: sell_fish(f, "1")).grid(row=row_count, column=1, padx=5, pady=5)
        ttk.Button(sell_frame, text="Sell 10",  command=lambda f=fish: sell_fish(f, "10")).grid(row=row_count, column=2, padx=5, pady=5)
        ttk.Button(sell_frame, text="Sell 100", command=lambda f=fish: sell_fish(f, "100")).grid(row=row_count, column=3, padx=5, pady=5)
        ttk.Button(sell_frame, text="Sell Max", command=lambda f=fish: sell_fish(f, "max")).grid(row=row_count, column=4, padx=5, pady=5)
        
        row_count += 1

    # Button to sell all fish at once
    ttk.Button(shop_window, text="Sell All Fish", command=sell_all_fish).pack(pady=10)


def set_globals(win, cur, inv, update_display, cur_label, res_label, fish_types_dict, lives_lbl, lives_list):
    global window, currency, inventory, update_inventory_display, currency_label, result_label, fish_types, lives_label, lives
    window = win
    currency = cur
    inventory = inv
    update_inventory_display = update_display
    currency_label = cur_label
    result_label = res_label
    fish_types = fish_types_dict
    lives_label = lives_lbl
    lives = lives_list
