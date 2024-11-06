import tkinter as tk
from tkinter import ttk
import random

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                VARIABLES SECTION                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

# Fish types and their probabilities of being caught and points
fish_types = {
    "Small Fish":   {"catch_chance": 0.8, "points": 5},
    "Big Fish":     {"catch_chance": 0.5, "points": 10},
    "Rare Fish":    {"catch_chance": 0.2, "points": 20},
}

# Item shop settings
items_for_sale = {
    "Live Bait":    {"price": 2, "effect": "required to catch fish"},
    "Life":         {"price": 5, "effect": "add an extra life."},
}

# Initialize score, currency, inventory, items, and lives
score = 0                       # Starting score
currency = 0                    # Starting cash
inventory = {"Live Bait": 10}   # Starting bait
lives = 3                       # Starting life

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                GAME LOGIC SECTION                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

def storm_hazard():
    global lives
    storm_chance = 0.05  # 5% chance for a storm to occur
    if random.random() < storm_chance:
        lives -= 1
        result_label.config(
            text="A sudden storm hit! You lost 1 life.",
            foreground="#F44336"
        )
        lives_label.config(text=f"Lives: {lives}")
        if lives <= 0:
            result_label.config(text="Game Over! You've lost all your lives.", foreground="#F44336")
            reset_game()
            return True  # End the game if lives are 0
    return False

# Define the Tangled Line Hazard
def tangled_line_hazard():
    global inventory
    tangle_chance = 0.1  # 10% chance for line to get tangled
    if random.random() < tangle_chance:
        bait_lost = min(2, inventory.get("Live Bait", 0))  # Lose up to 2 bait
        inventory["Live Bait"] -= bait_lost
        result_label.config(
            text=f"The line got tangled! Lost {bait_lost} bait.",
            foreground="#F44336"
        )
        update_inventory_display()

def cast_lines(num_casts):
    global score, inventory, lives
    successes = 0
    fails = 0

# User runs out of bait
    if inventory.get("Live Bait", 0) < 1:
        result_label.config(text="No bait left! Buy more from the shop.", foreground="#F44336")
        return

    if storm_hazard():  # Calls the storm hazard; ends casting if lives are depleted
        return

    for _ in range(num_casts):
        if inventory["Live Bait"] > 0:
            inventory["Live Bait"] -= 1
            fish            = random.choice(list(fish_types.keys()))
            catch_chance    = fish_types[fish]["catch_chance"]
            points          = fish_types[fish]["points"]

            if random.random() < catch_chance:
                successes += 1
                score += points
                inventory[fish] = inventory.get(fish, 0) + 1
            else:
                fails += 1
                score -= 2  # Penalty for missing fish
            
            # Tangled Line Hazard check after each cast
            tangled_line_hazard()
            
        else:
            break  # Stop casting if no bait is left

    # Update displays
    score_label.config(text=f"Score: {score}")
    lives_label.config(text=f"Lives: {lives}")  # Update lives display

    if lives <= 0:
        result_label.config(text="Game Over! You've lost all your lives.", foreground="#F44336")
        reset_game()
    else:
        result_label.config(
            text=f"Casts complete! Caught {successes} fish, missed {fails}.",
            foreground="#4CAF50" if successes > 0 else "#F44336"
        )
    update_inventory_display()

def reset_game():
    global score, currency, inventory, lives
    score = 0
    currency = 0
    inventory = {"Live Bait": 10}  # Reset to 10 bait
    lives = 3  # Reset lives
    score_label.config(text="Score: 0")
    currency_label.config(text="$: 0")
    lives_label.config(text="Lives: 3")
    result_label.config(text="Game reset. Try catching some fish!", foreground="white")
    update_inventory_display()

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                   SHOP SECTION                    #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

def open_shop():
    shop_window = tk.Toplevel(window)
    shop_window.title("Fish Shop")
    shop_window.geometry("400x900")
    shop_window.configure(bg="#34495E")

    shop_label = ttk.Label(shop_window, text="Buy items or sell fish", font=("Helvetica", 12, "bold"))
    shop_label.pack(pady=10)

    # Input for buying bait
    buy_bait_label = ttk.Label(shop_window, text="Enter quantity of Live Bait to buy:")
    buy_bait_label.pack(pady=5)
    buy_bait_entry = ttk.Entry(shop_window)
    buy_bait_entry.pack()

    buy_bait_button = ttk.Button(
        shop_window,
        text="Buy Live Bait for $2 each ",
        command=lambda: buy_item("Live Bait", buy_bait_entry.get())
    )
    buy_bait_button.pack(pady=5)
    
    buy_max_bait_button = ttk.Button(
        shop_window,
        text="Buy Max Live Bait",
        command=lambda: buy_item("Live Bait", "max")
    )
    buy_max_bait_button.pack(pady=5)

    # Input for buying lives
    buy_life_label = ttk.Label(shop_window, text="Enter lives to buy:")
    buy_life_label.pack(pady=5)
    buy_life_entry = ttk.Entry(shop_window)
    buy_life_entry.pack()

    buy_life_button = ttk.Button(
        shop_window,
        text="Buy Lives for $5 each ",
        command=lambda: buy_item("Life", buy_life_entry.get())
    )
    buy_life_button.pack(pady=5)
    
    buy_max_life_button = ttk.Button(
        shop_window,
        text="Buy Max Lives",
        command=lambda: buy_item("Life", "max")
    )
    buy_max_life_button.pack(pady=5)

    # Fish selling section
    for fish, data in fish_types.items():
        sell_label = ttk.Label(shop_window, text=f"Enter quantity of {fish} to sell:")
        sell_label.pack(pady=5)
        sell_entry = ttk.Entry(shop_window)
        sell_entry.pack()

        sell_button = ttk.Button(
            shop_window,
            text=f"Sell {fish} (${data['points']} each)",
            command=lambda f=fish, p=data['points'], e=sell_entry: sell_fish(f, p, e.get())
        )
        sell_button.pack(pady=5)

    sell_all_button = ttk.Button(shop_window, text="Sell All Fish", command=sell_all_fish)
    sell_all_button.pack(pady=10)

def sell_fish(fish, price, quantity_str):
    global currency
    try:
        quantity = int(quantity_str)
        if inventory.get(fish, 0) >= quantity > 0:
            inventory[fish] -= quantity
            currency += price * quantity
            currency_label.config(text=f"$: {currency}")
            result_label.config(text=f"Sold {quantity} {fish}(s) for ${price * quantity}!", foreground="#4CAF50")
            update_inventory_display()
        else:
            result_label.config(text=f"Not enough {fish} to sell!", foreground="#F44336")
    except ValueError:
        result_label.config(text="Invalid quantity entered for selling.", foreground="#F44336")

def sell_all_fish():
    global currency
    total_currency = 0
    for fish, count in list(inventory.items()):
        if fish != "Live Bait":
            total_currency += fish_types[fish]["points"] * count
            inventory[fish] = 0
    currency += total_currency
    currency_label.config(text=f"$: {currency}")
    result_label.config(text=f"Sold all fish for ${total_currency}!", foreground="#4CAF50")
    update_inventory_display()

def buy_item(item, quantity_str):
    global currency
    try:
        if quantity_str == "max":
            # Calculate the maximum number of items that can be bought
            max_quantity = currency // items_for_sale[item]["price"]
            quantity = max_quantity if max_quantity > 0 else 0
        else:
            quantity = int(quantity_str)
        
        price = items_for_sale[item]["price"] * quantity
        if currency >= price and quantity > 0:
            currency -= price
            inventory[item] = inventory.get(item, 0) + quantity
            currency_label.config(text=f"$: {currency}")
            result_label.config(text=f"Bought {quantity} {item}(s) for ${price}!", foreground="#4CAF50")
            update_inventory_display()
        else:
            result_label.config(text=f"Not enough $$$ to buy {quantity} {item}(s).", foreground="#F44336")
    except ValueError:
        result_label.config(text="Invalid quantity entered for buying.", foreground="#F44336")

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                INVENTORY SECTION                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

def open_inventory():
    inventory_window = tk.Toplevel(window)
    inventory_window.title("Inventory")
    inventory_window.geometry("400x250")
    inventory_window.configure(bg="#34495E")

    inventory_label = ttk.Label(inventory_window, text="Your Inventory", font=("Helvetica", 12, "bold"))
    inventory_label.pack(pady=10)

    inventory_display = tk.Text(inventory_window, height=10, width=30, state='normal', wrap='word', font=("Helvetica", 10))
    inventory_display.pack(pady=5)
    inventory_display.insert(tk.END, "\n".join(f"{fish}: {count}" for fish, count in inventory.items()))
    inventory_display.config(state='disabled')

def update_inventory_display():
    inventory_text = "Inventory:\n" + "\n".join(f"{fish}: {count}" for fish, count in inventory.items())
    inventory_label.config(text=inventory_text)

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                    GUI SECTION                    #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

# Setting up the GUI
window = tk.Tk()
window.title("Fishing Game")
window.geometry("800x600")
window.configure(bg="#2C3E50")

# Load the new window icon image
icon_image = tk.PhotoImage(file="assets\icon_image.png")
window.iconphoto(False, icon_image)

# Applying a style theme
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 12), padding=12, background="#3498DB", foreground="black")
style.configure("TLabel", background="#2C3E50", foreground="white", font=("Helvetica", 12))

# Instructions Label
instructions_label = ttk.Label(window, text="🎣 Cast your line to catch some fish!")
instructions_label.pack(pady=10)

# Frame to hold the result message
result_frame = ttk.Frame(window, padding=(10, 10, 10, 10))
result_frame.pack(pady=10)

# Result message
result_label = ttk.Label(result_frame, text="", font=("Helvetica", 14, "italic"))
result_label.pack()

# Score, Currency, and Lives display
score_label = ttk.Label(window, text="Score: 0", font=("Helvetica", 14, "bold"))
score_label.pack(pady=10)

currency_label = ttk.Label(window, text="Currency: 0", font=("Helvetica", 14, "bold"))
currency_label.pack(pady=10)

lives_label = ttk.Label(window, text="Lives: 3", font=("Helvetica", 14, "bold"))
lives_label.pack(pady=10)

# Inventory display
inventory_label = ttk.Label(window, text="Inventory:", font=("Helvetica", 12))
inventory_label.pack(pady=10)
update_inventory_display()

# Toolbar Frame
toolbar = ttk.Frame(window, padding=(10, 10, 10, 10))
toolbar.pack(pady=10)

# Cast line input
cast_label = ttk.Label(toolbar, text="Number of casts:")
cast_label.grid(row=0, column=0, padx=5)

cast_entry = ttk.Entry(toolbar, width=5)
cast_entry.grid(row=0, column=1, padx=5)

cast_entry.insert(0, "1")  # Default value of 1 for casting

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#               MENU BUTTON SECTION                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

cast_button = ttk.Button(toolbar, text=" Cast Line", command=lambda: cast_lines(int(cast_entry.get()) if cast_entry.get().isdigit() else 1))
cast_button.grid(row=0, column=2, padx=5)

shop_button = ttk.Button(toolbar, text=" Shop", command=open_shop)
shop_button.grid(row=0, column=3, padx=5)

inventory_button = ttk.Button(toolbar, text=" Inventory", command=open_inventory)
inventory_button.grid(row=0, column=4, padx=5)

reset_button = ttk.Button(toolbar, text=" Reset Game", command=reset_game)
reset_button.grid(row=0, column=5, padx=5)

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#               RUN GAME LOOP                       #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 
window.mainloop()
