import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import os
import sys

def get_asset_path(filename):
    """Get the absolute path to an asset file."""
    if getattr(sys, 'frozen', False):  # Check if running as an executable
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.normpath(os.path.join(base_dir, 'assets', filename))

#   Initialize the main window

#   Fetch the username passed from the login script
username = sys.argv[1] if len(sys.argv) > 1 else "Player"

open_windows = []

#window.title        ("Fishing Game - {username}'s session")
def update_title(username):
    window.title(f"Fishing Game - {username}'s session")

# Function to set the window position with optional offsets
def set_window_position(window, width=800, height=650, x_offset=None, y_offset=None):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Center the window if no offsets are provided
    if x_offset is None:
        x_offset = (screen_width - width) // 2
    if y_offset is None:
        y_offset = (screen_height - height) // 2

    # Set window size and position
    window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

# Initialize the main window
window = tk.Tk()

# Customize the window position by changing x_offset and y_offset here
custom_x_offset = 100   # Change this value to your desired X position
custom_y_offset = 200   # Change this value to your desired Y position

# Set window size and position
set_window_position(window, 650, 650, custom_x_offset, custom_y_offset)

# window.geometry     ("800x650")  #   Width x Height
window.configure    (bg="#2da7d2") 

# username = "Player1"  # Replace this with your actual username retrieval logic
update_title(username)

# Load an icon image with error handling
try:
    icon_path = get_asset_path('icon_image.png')
    icon_image = tk.PhotoImage(file=icon_path)
except tk.TclError:
    icon_image = None
except Exception as e:
    print(f"Unexpected error: {e}")

# Ensure the icon image is not garbage collected
if icon_image:
    window.iconphoto(False, icon_image)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                                           VARIABLES CONFIGURATION                                                               #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

#   Fish types and their probabilities of being caught and points
fish_types = {
    "Small Fish":   {"catch_chance": 0.8, "points": 5},
    "Big Fish":     {"catch_chance": 0.5, "points": 10},
    "Rare Fish":    {"catch_chance": 0.2, "points": 20},
}

#   Item shop settings
items_for_sale = {
    "Live Bait":    {"price": 2, "effect": "required to catch fish"},
    "Life":         {"price": 5, "effect": "add an extra life."},
}

#   Define hazards and their effects in a dictionary
hazards = {
    "Storm":        {"effect": "lose_life", "description": "A storm hits! You lose a life." },
    "Lost Bait":    {"effect": "lose_bait", "description": "Oh no some of the live bait worms ran away!" },
    "Thief":        {"effect": "lose_gold", "description": "A thief stole some of your gold!"},
    # "Broken Rod":   {"effect": "lose_item", "item": "Fishing Rod",  "description": "Your fishing rod broke!" }
    # Example of losing a specific item
}

# Define treasure items and their values
treasure_items = {
    "Golden Coin":      {"description": "A shiny golden coin.",                     "value": 50},
    "Old Boot":         {"description": "An old, worn-out boot. Not worth much.",   "value": 5},
    "Pearl Necklace":   {"description": "A beautiful pearl necklace.",              "value": 100},
    "Rusty Anchor":     {"description": "A heavy, rusty anchor.",                   "value": 20},
    "Ancient Relic":    {"description": "A mysterious relic from ancient times.",   "value": 200}
}

#   Initialize score, currency, inventory, items, and lives
score       = 0                     # Starting score
currency    = {"Gold": 500}         # Starting cash
inventory   = {"Live Bait": 10}     # Starting bait
lives       = [3]                   # Starting life

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                                            GAME LOGIC                                                                           #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# - Cast Line           - DONE

def trigger_treasure():
    """Randomly catch a treasure with a 10% chance."""
    if random.random() < 0.1:  # 10% chance to catch a treasure
        treasure_type = random.choice(list(treasure_items.keys()))
        treasure_info = treasure_items[treasure_type]
        print("Treasure Found!:", treasure_info["description"])

        # Display the treasure found
        result_label.config(text=f"🎉 Treasure Found: {treasure_type}! {treasure_info['description']}", foreground="#FFD700")
        
        # Prompt the player to keep or sell the treasure
        prompt_keep_or_sell(treasure_type, treasure_info)
        return True
    return False

def prompt_keep_or_sell(treasure_type, treasure_info):
    treasure_window = tk.Toplevel(window)
    treasure_window.title("Treasure Caught!")
    treasure_window.geometry("400x200") #   Width x Height
    treasure_window.configure(background="#34495E")

    if icon_image:
        treasure_window.iconphoto(False, icon_image)
    
    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure("Keep.TButton", background="#ba1eb8", foreground="gold", font=("Aptos", 12, "bold"), relief="raised", padding=10)
    style.map("Keep.TButton", background=[("active", "#E94545"), ("pressed", "#B03030")], foreground=[("disabled", "#D3D3D3")])

    style.configure("Sell.TButton", background="#1f946f", foreground="gold", font=("Aptos", 12, "bold"), relief="raised", padding=10)
    style.map("Sell.TButton", background=[("active", "#E94545"), ("pressed", "#B03030")], foreground=[("disabled", "#D3D3D3")])

    # Set position to be near the main window
    x_offset = window.winfo_x() + 800
    y_offset = window.winfo_y() + 0
    treasure_window.geometry(f"+{x_offset}+{y_offset}")

    # Load the new window icon image
    #icon_image = tk.PhotoImage(file="assets/icon_image.png")
    #treasure_window.iconphoto(False, icon_image)

    message = f"You caught a {treasure_type}! {treasure_info['description']}\nValue: {treasure_info['value']} Gold"
    message_label = ttk.Label(treasure_window, text=message, font=("Aptos", 12, "bold"), background="#34495E", foreground="white", padding=(10, 10, 10, 10))
    message_label.pack(pady=10, padx=10)    
    
    # Button to keep the treasure
    def keep_treasure():
        inventory[treasure_type] = inventory.get(treasure_type, 0) + 1
        result_label.config(text=f"You kept the {treasure_type}!", foreground="#4CAF50")
        treasure_window.destroy()
        update_inventory_display()

    # Button to sell the treasure
    def sell_treasure():
        currency["Gold"] += treasure_info["value"]
        result_label.config(text=f"You sold the {treasure_type} for {treasure_info['value']} Gold!", foreground="#FFD700")
        currency_label.config(text=f"Gold: {currency['Gold']}")
        treasure_window.destroy()

    keep_button = ttk.Button(treasure_window, text="Keep", style="Keep.TButton", command=keep_treasure)
    keep_button.pack(side=tk.LEFT, padx=20, pady=20)

    sell_button = ttk.Button(treasure_window, text="Sell", style="Sell.TButton", command=sell_treasure)
    sell_button.pack(side=tk.RIGHT, padx=20, pady=20)

def trigger_hazard(hazard_type=None):
    # If no hazard_type is passed, choose a random hazard
    if not hazard_type:
        hazard_type = random.choice(list(hazards.keys()))

    hazard_info = hazards[hazard_type]
    print("Hazard triggered:", hazard_info["description"])

    # Apply the hazard effect based on its type
    if hazard_info["effect"] == "lose_life":
        if lives[0] > 0:  # Check if the player has lives left
            lives[0] -= 1
            result_label.config(text=hazard_info["description"], foreground="#F44336")

    elif hazard_info["effect"] == "lose_bait":
        if inventory.get("Live Bait", 0) > 0:
            inventory["Live Bait"] -= 1
            result_label.config(text=hazard_info["description"], foreground="#F44336")
    
    elif hazard_info["effect"] == "lose_gold":
        if currency.get("Gold", 0) > 0:
            currency["Gold"] -= 10  # Example penalty amount
            result_label.config(text=hazard_info["description"], foreground="#F44336")
    
    elif hazard_info["effect"] == "lose_item":
        if inventory.get(hazard_info["item"], 0) > 0:
            inventory[hazard_info["item"]] -= 1
            result_label.config(text=hazard_info["description"], foreground="#F44336")

    # Update the UI immediately
    window.update()

    # Add a delay before clearing the message
    def clear_message():
        result_label.config(text="")
    
    # Schedule the message to clear after 2 seconds
    window.after(20000, clear_message)

    # Update the inventory and labels
    update_inventory_display()
    lives_label.config(text=f"Lives: {lives[0]}")
    currency_label.config(text=f"Gold: {currency.get('Gold', 0)}")
    
    return 1 if hazard_info else 0

def cast_lines():
    global score, inventory, lives
    successes = 0
    fails = 0

    # Read the number of casts from the entry field
    num_casts = int(cast_entry.get()) if cast_entry.get().isdigit() else 1

    # Check if the player has enough bait
    if inventory.get("Live Bait", 0) < 1:
        result_label.config(text="No bait left! Buy more from the shop.", foreground="#F44336")
        return

    # Check if player is - Gold
    if currency.get("Gold", 0) < 1:
        result_label.config(text="You're in debt! Quick sell some fish", foreground="#F44336")
        return

    for _ in range(num_casts):
        # Trigger hazard before each cast with a 20% chance
        if random.random() < 0.2:
            hazard_triggered = trigger_hazard()
            if hazard_triggered:
                if lives[0] <= 0:
                    result_label.config(text="You have no lives left!", foreground="#F44336")
                    game_over()
                    return
                continue  # Skip this cast if a hazard was triggered

        # Check for treasure
        if trigger_treasure():
            continue  # Skip catching fish if treasure is found

        # Deduct one bait for each cast
        if inventory["Live Bait"] > 0:
            inventory["Live Bait"] -= 1

            # Randomly choose a fish type to attempt catching
            fish = random.choice(list(fish_types.keys()))
            catch_chance = fish_types[fish]["catch_chance"]
            points = fish_types[fish]["points"]

            # Determine if the fish is caught
            if random.random() < catch_chance:
                successes += 1
                score += points
                inventory[fish] = inventory.get(fish, 0) + 1
                score_label.config(text=f"Score: {score}")
                result_label.config(text=f"You caught a {fish}!", foreground="#4CAF50")  # Success message
                print("You caught a ", {fish},"!")
            else:
                # Casting failed, show the message for no fish biting
                fails += 1
                score -= 2  # Penalty for missing fish
                result_label.config(text="No fish biting, reel it in.", foreground="#F44336")  # Fail message
                print("No fish biting, reel it in.")
        else:
            result_label.config(text="Out of bait!", foreground="#F44336")
            print("Out of bait!")
            break  # Stop casting if no bait is left

        # Check if lives have run out
        if lives[0] <= 0:
            result_label.config(text="You have no lives left!", foreground="#F44336")
            game_over()
            return


        window.update_idletasks()  # Ensure the UI is updated immediately

    # Update the inventory and labels after all casts are completed
    update_inventory_display()
    score_label.config(text=f"Score: {score}")
    currency_label.config(text=f"Gold: {currency.get('Gold', 0)}")
    lives_label.config(text=f"Lives: {lives[0]}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                                            SHOP LOGIC                                                                           #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

def open_shop():
    #window = tk.TopLevel()
    #window.title("Fish Shop")
    #window.geometry("800x500")
    #window.configure(bg="#58a788")

    shop_window = tk.Toplevel(window)
    open_windows.append(shop_window)
    shop_window.title("Fish Shop")
    shop_window.geometry("800x500") #   Width x Height
    shop_window.configure(bg="#58a788")

    #if icon_image:
    #    leaderboard_window.iconphoto(False, icon_image)

    if icon_image:
        shop_window.iconphoto(False, icon_image)

    # Set position to be near the main window
    x_offset = shop_window.winfo_x() + 600
    y_offset = shop_window.winfo_y() + 250
    shop_window.geometry(f"+{x_offset}+{y_offset}")

    style = ttk.Style(shop_window)
    style.theme_use("clam")
    style.configure("Sell.TButton", background="#49b655", foreground="gold", font=("Aptos", 12, "bold"), relief="raised", padding=10)
    style.map("Sell.TButton", background=[("active", "#38dd65"), ("pressed", "#B03030")], foreground=[("disabled", "#D3D3D3")])

    style.configure("Buy.TButton", background="#5946b9", foreground="white", font=("Aptos", 12, "bold"), relief="raised", padding=10)
    style.map("Buy.TButton", background=[("active", "#5216e9"), ("pressed", "#B03030")], foreground=[("disabled", "#D3D3D3")])

    shop_label = ttk.Label(shop_window, text="Buy items or sell fish", font=("Aptos", 14, "bold"), background="#2C3E50", foreground="white", anchor="center")
    shop_label.pack(pady=10, padx=10, fill="x")

    # Buy section
    buy_frame = tk.Frame(shop_window, bg="#34495E")
    buy_frame.pack(pady=10, padx=10, fill="x")

    # Configure grid columns for symmetry
    buy_frame.grid_columnconfigure(0, weight=1)

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
        ttk.Label(buy_frame, text=f"Buy {item} ({price} gold each):", background="#34495E", foreground="white").grid(row=row_count, column=0, sticky='w', padx=10, pady=10)
        
        ttk.Button(buy_frame, text="Buy 1",     command=lambda i=item: buy_item(i, "1"), style="Buy.TButton").grid(row=row_count, column=1, padx=10, pady=10)
        ttk.Button(buy_frame, text="Buy 10",    command=lambda i=item: buy_item(i, "10"), style="Buy.TButton").grid(row=row_count, column=2, padx=10, pady=10)
        ttk.Button(buy_frame, text="Buy 100",   command=lambda i=item: buy_item(i, "100"), style="Buy.TButton").grid(row=row_count, column=3, padx=10, pady=10)
        ttk.Button(buy_frame, text="Buy Max",   command=lambda i=item: buy_item(i, "max"), style="Buy.TButton").grid(row=row_count, column=4, padx=10, pady=10)
        row_count += 1

    # Sell section
    sell_frame = tk.Frame(shop_window, bg="#34495E")
    sell_frame.pack(pady=10, padx=10, fill="x")

    # Configure grid columns for symmetry
    sell_frame.grid_columnconfigure(0, weight=1)

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

        ttk.Label(sell_frame, text=f"Sell {fish} ({data['points']} gold each):", background="#34495E", foreground="white").grid(row=row_count, column=0, sticky='w', padx=10, pady=10)

        # Buttons to sell different quantities of fish
        ttk.Button(sell_frame, text="Sell 1",   command=lambda f=fish: sell_fish(f, "1"), style="Sell.TButton").grid(row=row_count, column=1, padx=10, pady=10)
        ttk.Button(sell_frame, text="Sell 10",  command=lambda f=fish: sell_fish(f, "10"), style="Sell.TButton").grid(row=row_count, column=2, padx=10, pady=10)
        ttk.Button(sell_frame, text="Sell 100", command=lambda f=fish: sell_fish(f, "100"), style="Sell.TButton").grid(row=row_count, column=3, padx=10, pady=10)
        ttk.Button(sell_frame, text="Sell Max", command=lambda f=fish: sell_fish(f, "max"), style="Sell.TButton").grid(row=row_count, column=4, padx=10, pady=10)    
        row_count += 1

    # Button to sell all fish at once
    ttk.Button(shop_window, text="Sell All Fish", command=sell_all_fish, style="Sell.TButton").pack(padx=10, pady=10)

    # close_button = ttk.Button(window, text="Close", command=window.destroy, style="Custom.TButton")
    # close_button.pack(pady=20)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                                        LEADERBOARD LOGIC                                                                        #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

#   File to store leaderboard data
LEADERBOARD_FILE = "leaderboard.txt"
#   Save a player's score to the leaderboard file
def save_score(player_name, score):
    with open(LEADERBOARD_FILE, "a") as file:
        file.write(f"{player_name},{score}\n")

#   Load and display the leaderboard
def display_leaderboard():

    leaderboard_window = tk.Toplevel(window)
    open_windows.append(leaderboard_window)
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("500x500") #   Width x Height
    leaderboard_window.configure(bg="#34495E")

    if icon_image:
        leaderboard_window.iconphoto(False, icon_image)

    # Load the new window icon image
    #icon_image = tk.PhotoImage(file="assets/icon_image.png")
    #leaderboard_window.iconphoto(False, icon_image)

    # Set position to be near the main window
    x_offset = window.winfo_x() + 100
    y_offset = window.winfo_y() + 0
    leaderboard_window.geometry(f"+{x_offset}+{y_offset}")

    # Leaderboard title label
    title_label = ttk.Label(leaderboard_window, text="🏆 Leaderboard 🏆", font=("Helvetica", 18, "bold"), background="#34495E", foreground="gold")
    title_label.pack(pady=20)

    # Style for the Treeview widget
    style = ttk.Style()
    style.configure("Treeview", background="#2C3E50", foreground="white", rowheight=30, fieldbackground="#2C3E50")
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#1ABC9C", foreground="black")
    style.map("Treeview", background=[("selected", "#3498DB")])

    # Treeview widget for displaying scores
    leaderboard_tree = ttk.Treeview(leaderboard_window, columns=("Rank", "Player", "Score"), show="headings", height=10)
    leaderboard_tree.pack(padx=20, pady=10)

    # Define column headings
    leaderboard_tree.heading("Rank", text="Rank")
    leaderboard_tree.heading("Player", text="Player")
    leaderboard_tree.heading("Score", text="Score")

    # Set column widths
    leaderboard_tree.column("Rank", width=50, anchor="center")
    leaderboard_tree.column("Player", width=200, anchor="center")
    leaderboard_tree.column("Score", width=100, anchor="center")

    # Read scores from the file and sort them
    scores = []
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            for line in file:
                name, score = line.strip().split(",")
                scores.append((name, int(score)))
        scores.sort(key=lambda x: x[1], reverse=True)

    # Insert scores into the Treeview
    for rank, (name, score) in enumerate(scores[:10], 1):  # Show top 10 scores
        leaderboard_tree.insert("", "end", values=(rank, name, score))

    # Button to close the leaderboard window
    close_button = ttk.Button(leaderboard_window, text="Close", command=leaderboard_window.destroy, style="Custom.TButton")
    close_button.pack(pady=20)

# - Exit Game           - DONE!
def reset_game_state():
    global score, currency, inventory, lives, open_windows  
    
    score = 0
    currency = {"Gold": 500}
    inventory = {"Live Bait": 10}
    lives = [3]
    
    # Close all open game-related windows
    for win in open_windows:
        if win.winfo_exists():
            win.destroy()
    open_windows.clear()
    
    # Clear the result label
    result_label.config(text="")
    score_label.config(text=f"Score: {score}")
    lives_label.config(text=f"Lives: {lives[0]}")
    currency_label.config(text=f"Gold: {currency['Gold']}")


def game_over():
    save_score(username, score)
    messagebox.showinfo("Game Over", f"Game over {username}! Final score: {score} ... Returing to Login.")
    reset_game_state()  # Reset all game variables
    window.destroy()
    os.system("python GUILoginReg.py")

def exit_game(): 
    confirm = tk.messagebox.askyesno("Exit Game", "Are you sure you want to exit to the login screen")
    if confirm:
        save_score(username, score)
        game_over()
        #reset_game_state() 
        print("exited game!") 
        window.destroy()

# - INVENTORY SECTION   - DONE!

def update_inventory_display():
    """Update the inventory label on the main window."""
    inventory_text = "Inventory:\n" + "\n".join(f"{fish}: {count}" for fish, count in inventory.items())
    inventory_label.config(text=inventory_text)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                                        GUI CONFIGURATION                                                                        #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.TFrame", background="black")
style.configure("Welcome.TLabel", background="#5a44bb", foreground="white", font=("Aptos (Heading)", 18), anchor="center", width=50) # Welcome Label
style.configure("Custom1.TFrame", background="black")
style.configure("Results.TLabel", background="#5a44bb", foreground="white", font=("Aptos", 16),  anchor="center", width=50) # Results Label
style.configure("Custom2.TFrame", background="#620c97", anchor="center")
style.configure("Custom3.TFrame", background="#620c97", anchor="center")
style.configure("Shop.TFrame", background="black")

# -- -- -- RESULTS FRAME CONFIG -- -- -- #
welcome_frame = ttk.Frame   (window, style="Custom.TFrame", padding=(   5, # LEFT
                                                                        10, # TOP
                                                                        5, # RIGHT
                                                                        10  # BOTTOM
                                                                    )
                            )
welcome_frame.pack          (pady=25, padx=25, fill="x")

welcome_label = ttk.Label   (welcome_frame, text=f"Welcome, {username}! Let's start fishing!", style="Welcome.TLabel")
welcome_label.pack          (padx=10, pady=10, fill="x") 

# -- -- -- WELCOME FRAME CONFIG -- -- -- #
result_frame = ttk.Frame    (window, style="Custom1.TFrame", padding=(5, 10, 5, 10))
result_frame.pack           (pady=25, padx=25, fill="x")

result_label = ttk.Label    (result_frame, text="Results Go here", style="Results.TLabel")
result_label.pack           (padx=10, pady=10, fill="x") 

# -- -- -- GAME MENU FRAME CONFIG -- -- -- #
gamemenu = ttk.Frame(window, style="Custom2.TFrame", padding=(5, 10, 5, 10))
gamemenu.pack(pady=25, padx=25, fill="x")

# Make sure the columns expand equally
for i in range(4):  # Adjust the range based on the number of columns you have
    gamemenu.grid_columnconfigure(i, weight=1, uniform="equal")

# Make sure the row expands equally (for row 1 where labels are placed)
gamemenu.grid_rowconfigure(1, weight=1)

#   Score Display
style.configure("Gamemenu.TLabel", background="#620c97", foreground="white", font=("Aptos (Heading)", 10, "bold"), anchor="center", width=50) # Labels
score_label = ttk.Label(gamemenu, text="Score: 0", style="Gamemenu.TLabel")
score_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

#   Currency Display
currency_label = ttk.Label(gamemenu, text=f"Gold: {currency['Gold']}", style="Gamemenu.TLabel")
currency_label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

#   Lives Display
lives_label = ttk.Label(gamemenu, text="Lives: 3", style="Gamemenu.TLabel")
lives_label.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

#   Inventory Display
inventory_label = ttk.Label(gamemenu, text="Inventory:", style="Gamemenu.TLabel")
inventory_label.grid(row=1, column=3, columnspan=3, padx=10, pady=10, sticky="nsew")
update_inventory_display()

#   Cast line input Description
cast_label = ttk.Label(gamemenu, text="Enter Cast Amount", style="Gamemenu.TLabel")
cast_label.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

#   Cast line input
cast_entry = ttk.Entry(gamemenu, width=10, font=("Arial", 10))
cast_entry.grid(row=2, column=1,  padx=5, pady=5)
cast_entry.insert(0, "1")  # Default value of 1 for casting

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                                                           BUTTON CONFIGURATION                                                                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# -- -- -- GAME MENU BUTTONS FRAME CONFIG -- -- -- #

gamemenu2 = ttk.Frame(window, style="Custom3.TFrame", padding=(10, 10, 10, 10))
gamemenu2.pack(pady=10, padx=10, fill="x")

# Make sure the columns expand equally
for i in range(4):  # Adjust the range based on the number of columns you have
    gamemenu2.grid_columnconfigure(i, weight=1, uniform="equal")

# Make sure the row expands equally (for row 1 where labels are placed)
gamemenu2.grid_rowconfigure(1, weight=1)

#           " Custom TButton Config "               #
style.configure ("Custom.TButton",font=("Helvetica", 10, "bold"), padding=10, background="#3498db", foreground="black")
style.map       ("Custom.TButton", background=[("active", "#2980b9")])  # Active state color

#   Cast Button
cast_button = ttk.Button(gamemenu2, text=" Cast Line", command=cast_lines, style="Custom.TButton")
cast_button.grid(row=3, column=0, padx=5, pady=5)

#   Shop Button
shop_button = ttk.Button(gamemenu2, text=" Shop", command=open_shop, style="Custom.TButton")
shop_button.grid(row=3, column=1, padx=5, pady=5)

#   Leaderboard Button 
leaderboard_button = ttk.Button(gamemenu2, text="Leaderboard", command=display_leaderboard, style="Custom.TButton")
leaderboard_button.grid(row=3, column=2, padx=5, pady=5)

#   Exit Button
exit_button = ttk.Button(gamemenu2, text="Exit Game", command=exit_game, style="Custom.TButton")
exit_button.grid(row=3, column=3,  padx=5, pady=5)

# - - - - - END GAME LOOP - - - - - #
window.mainloop()