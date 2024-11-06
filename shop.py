import tkinter as tk
from tkinter import ttk

def open_shop(window, currency, inventory, update_inventory_display, currency_label, result_label, fish_types):
    shop_window = tk.Toplevel(window)
    shop_window.title("Fish Shop")
    shop_window.geometry("600x600")
    shop_window.configure(bg="#2C3E50")

    icon_image = tk.PhotoImage(file="assets\icon_image.png")
    shop_window.iconphoto(False, icon_image)

    # Set position to be near the main window
    x_offset = window.winfo_x() + 750
    y_offset = window.winfo_y() + 0
    shop_window.geometry(f"+{x_offset}+{y_offset}")

    # Shop header
    shop_label = ttk.Label(shop_window, text="Buy items or sell fish", font=("Helvetica", 14, "bold"), background="#2C3E50", foreground="white")
    shop_label.pack(pady=10)

    # Container frame for buying items
    buy_frame = tk.Frame(shop_window, bg="#34495E")
    buy_frame.pack(pady=10, padx=10, fill="x")

    def buy_item(item, quantity_str, currency, inventory, update_inventory_display, currency_label, result_label):
        # Assuming 'price' is available in the scope, you may need to define it based on the item
        price = 0
        if item == "Live Bait":
            price = 2
        elif item == "Life":
            price = 5

        try:
            if quantity_str == "max":
                quantity = (currency["Gold"] // price) if price > 0 else 0  # Max quantity based on currency
            else:
                quantity = int(quantity_str)

            if quantity > 0:
                total_cost = quantity * price
                if currency["Gold"] >= total_cost:
                    currency["Gold"] -= total_cost
                    inventory[item] = inventory.get(item, 0) + quantity
                    currency_label.config(text=f"Gold: {currency['Gold']}")
                    result_label.config(text=f"Bought {quantity} {item}(s) for {total_cost} gold!", foreground="#4CAF50")
                    update_inventory_display()
                else:
                    result_label.config(text="Not enough gold!", foreground="#F44336")
            else:
                result_label.config(text="Invalid quantity!", foreground="#F44336")
        except ValueError:
            result_label.config(text="Invalid quantity entered.", foreground="#F44336")

    # Function to add buy item row
    def add_buy_row(item, price):
        item_label = ttk.Label(buy_frame, text=f"Enter {item} to buy:", background="#34495E", foreground="white")
        item_label.grid(row=row_count[0], column=0, padx=5, pady=5, sticky="e")

        entry = ttk.Entry(buy_frame, width=5)
        entry.grid(row=row_count[0], column=1, padx=5, pady=5)

        buy_button = ttk.Button(buy_frame, text=f"Buy ({price} gold each)", 
                                command=lambda: buy_item(item, entry.get(), currency, inventory, update_inventory_display, currency_label, result_label))
        buy_button.grid(row=row_count[0], column=2, padx=5, pady=5)

        buy_max_button = ttk.Button(buy_frame, text="Buy Max", 
                                    command=lambda: buy_item(item, "max", currency, inventory, update_inventory_display, currency_label, result_label))
        buy_max_button.grid(row=row_count[0], column=3, padx=5, pady=5)
        
        row_count[0] += 1

    # Add buy item rows
    row_count = [0]  # To keep track of row
    add_buy_row("Live Bait", 2)
    add_buy_row("Life", 5)

    # Fish selling section
    sell_frame = tk.Frame(shop_window, bg="#34495E")
    sell_frame.pack(pady=10, padx=10, fill="x")

    for fish, data in fish_types.items():
        fish_label = ttk.Label(sell_frame, text=f"Enter quantity of {fish} to sell:", background="#34495E", foreground="white")
        fish_label.grid(row=row_count[0], column=0, padx=5, pady=5, sticky="e")

        sell_entry = ttk.Entry(sell_frame, width=5)
        sell_entry.grid(row=row_count[0], column=1, padx=5, pady=5)

        sell_button = ttk.Button(sell_frame, text=f"Sell {fish} ({data['points']} gold each)",
                                 command=lambda f=fish, p=data['points'], e=sell_entry: sell_fish(f, p, e.get(), currency, inventory, currency_label, result_label, update_inventory_display))
        sell_button.grid(row=row_count[0], column=2, padx=5, pady=5)

        row_count[0] += 1

    # Sell all fish button
    sell_all_button = ttk.Button(
        shop_window, 
        text="Sell All Fish", 
        command=lambda: sell_all_fish(currency, inventory, currency_label, result_label, update_inventory_display, fish_types)
    )
    sell_all_button.pack(pady=10)

    # Additional padding and visual adjustments
    buy_frame.grid_columnconfigure(0, weight=1)
    sell_frame.grid_columnconfigure(0, weight=1)

def sell_fish(fish, price, quantity_str, currency, inventory, currency_label, result_label, update_inventory_display):
    try:
        quantity = int(quantity_str)
        if inventory.get(fish, 0) >= quantity > 0:
            inventory[fish] -= quantity
            currency["Gold"] += price * quantity  # Corrected to access "Gold"
            currency_label.config(text=f"Gold: {currency['Gold']}")
            result_label.config(text=f"Sold {quantity} {fish}(s) for {price * quantity} gold!", foreground="#4CAF50")
            update_inventory_display()
        else:
            result_label.config(text=f"Not enough {fish} to sell!", foreground="#F44336")
    except ValueError:
        result_label.config(text="Invalid quantity entered for selling.", foreground="#F44336")


def sell_all_fish(currency, inventory, currency_label, result_label, update_inventory_display, fish_types):
    total_currency = 0
    # Loop through the inventory and calculate the total currency from selling fish
    for fish, count in inventory.items():
        if fish in fish_types:
            # Assuming a fish can be sold for its points value * quantity
            total_currency += fish_types[fish]["points"] * count

            # Set the fish count to 0 after selling them
            inventory[fish] = 0

    # Add the total currency to the player's gold
    currency["Gold"] += total_currency  # Corrected to access "Gold"
    
    # Update the result label to show how much gold was earned
    result_label.config(text=f"Sold all fish for {total_currency} gold.", foreground="#4CAF50")
    
    # Update the inventory and currency displays
    update_inventory_display()
    currency_label.config(text=f"Gold: {currency['Gold']}")
