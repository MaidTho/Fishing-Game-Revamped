import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
import sys
import bcrypt
#   GLOBAL VARIABLES CONFIGURATION 
#   This is here to define the fish type variable and add new fish, catch chance & the points they are worth
fish_types = {
    "Small Fish":   {"catch_chance": 0.8, "points": 5},
    "Big Fish":     {"catch_chance": 0.5, "points": 10},
    "Rare Fish":    {"catch_chance": 0.01, "points": 200},
    }
#   This is the items available to purchase, their price and effect of each item.
items_for_sale = {
    "Live Bait":    {"price": 2, "effect": "required to catch fish"},
    "Life":         {"price": 5, "effect": "add an extra life."},
    }
#   This is the hazards the user encounters during the game, their effects and description of what they do.
hazards = {
    "Storm":        {"effect": "lose_life", "description": "A storm hits! You lose a life." },
    "Lost Bait":    {"effect": "lose_bait", "description": "Oh no some of the live bait worms ran away!" },
    "Thief":        {"effect": "lose_gold", "description": "A thief stole some of your gold!"},
    # "Broken Rod":   {"effect": "lose_item", "item": "Fishing Rod",  "description": "Your fishing rod broke!" }
    # Example of losing a specific item
    }
#   This is the treasure items the user can catch along with a description and value set of each item.
treasure_items = {
    "Golden Coin":      {"description": "A shiny golden coin.",                     "value": 50},
    "Old Boot":         {"description": "An old, worn-out boot. Not worth much.",   "value": 5},
    "Pearl Necklace":   {"description": "A beautiful pearl necklace.",              "value": 100},
    "Rusty Anchor":     {"description": "A heavy, rusty anchor.",                   "value": 20},
    "Ancient Relic":    {"description": "A mysterious relic from ancient times.",   "value": 200}
    }
#   This is where the global variables for the score, currency, inventory, lives and windows are. Do not move/touch unless adjusting values.
score       = 0                     # Starting score
currency    = {"Gold": 500}         # Starting cash
inventory   = {"Live Bait": 10}     # Starting bait
lives       = [3]                   # Starting life  
open_windows = []
def get_asset_path(filename):
    """Get the absolute path to an asset file."""
    if getattr(sys, 'frozen', False):  # Check if running as an executable
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.normpath(os.path.join(base_dir, 'assets', filename))
#   This is where we call the userdata to login / register.
USER_FILE = "users.txt"
def load_users():
    users = {}
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if not line or ',' not in line:
                    continue
                username, hashed_password = line.split(",", 1)
                users[username.strip()] = hashed_password.strip()
    except FileNotFoundError:
        pass
    return users
def save_users(users):
    with open(USER_FILE, "w") as file:
        for username, hashed_password in users.items():
            file.write(f"{username},{hashed_password}\n")
def hash_password(password):
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
def check_password(password, hashed):
    """Check a password against a hashed version."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
def login_registration_window():
    # Load users from file
    user_db = load_users()

    login_window = tk.Tk()
    login_window.title("Fishing Game - Login")
    login_window.geometry("500x500")
    login_window.configure(bg="#2da7d2")
    
    try:
        icon_path = get_asset_path('Fishing Game Logo.png')
        icon_image = tk.PhotoImage(file=icon_path)
    except tk.TclError:
        icon_image = None
    except Exception as e:
        print(f"Unexpected error: {e}")

    if icon_image:
        login_window.iconphoto(False, icon_image)

    ttk.Label(login_window, text="Login or Register", font=("Aptos", 16, "bold"), background="#2da7d2", foreground="white").pack(pady=20)

    username_label = ttk.Label(login_window, text="Username:", background="#2da7d2", foreground="white")
    username_label.pack(pady=5)
    username_entry = ttk.Entry(login_window)
    username_entry.pack(pady=5)

    password_label = ttk.Label(login_window, text="Password:", background="#2da7d2", foreground="white")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    def authenticate_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        # Check if the user exists
        if username in user_db:
            # Verify the plaintext password against the hashed password
            hashed_password = user_db[username]
            if check_password(password, hashed_password):
                messagebox.showinfo("Success", f"Welcome back, {username}!")
                login_window.destroy()
                launch_main_game(username)
            else:
                messagebox.showerror("Error", "Invalid password.")
        else:
            messagebox.showerror("Error", "Username not found.")


    def register_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        # Check if the username already exists
        if username in user_db:
            messagebox.showerror("Error", "Username already exists. Please choose a different one.")
        else:
            hashed_password = hash_password(password)
            user_db[username] = hashed_password
            save_users(user_db)
            messagebox.showinfo("Success", f"Account created for {username}!")

    login_button = ttk.Button(login_window, text="Login", command=authenticate_user)
    login_button.pack(pady=10)

    register_button = ttk.Button(login_window, text="Register", command=register_user)
    register_button.pack(pady=5)

    login_window.mainloop()
#   Main Game GUI
def launch_main_game(username):
    print(f"launching main game for user: {username}")
    window = tk.Tk()
    window.title(f"Fishing Game - {username}'s session")
    window.geometry("800x600")
    window.configure(bg="#2da7d2")
#   MAIN GAME 1.0.  IMAGE EXCEPTION This is where we call exception testing for the image icon error handling
    try:
        icon_path = get_asset_path('Fishing Game Logo.png')
        icon_image = tk.PhotoImage(file=icon_path)
    except tk.TclError:
        icon_image = None
    except Exception as e:
        print(f"Unexpected error: {e}")
#   MAIN GAME 1.1.  IMAGE ICON -    This is where we ensure the icon is called correctly
    if icon_image:
        window.iconphoto(False, icon_image)
#   MAIN GAME 2.0.  TRIGGERS -      This is where trigger treasure and hazards are called.
    def trigger_treasure():
        """Randomly catch a treasure with a 1% chance."""
        if random.random() < 0.01:  # 1% chance to catch a treasure
            treasure_type = random.choice(list(treasure_items.keys()))
            treasure_info = treasure_items[treasure_type]
            print("Treasure Found!:", treasure_info["description"])

            # Display the treasure found
            result_label.config(text=f"🎉 Treasure Found: {treasure_type}! {treasure_info['description']}", foreground="Gold")
            
            # Prompt the player to keep or sell the treasure
            prompt_keep_or_sell(treasure_type, treasure_info)
            return True
        return False
    def prompt_keep_or_sell(treasure_type, treasure_info):
        treasure_window = tk.Toplevel(window)
        treasure_window.title("Treasure Caught!")
        treasure_window.geometry("450x300") #   Width x Height
        treasure_window.configure(background="#800000")

        if icon_image:
            treasure_window.iconphoto(False, icon_image)
        
        style = ttk.Style(window)
        style.theme_use ("default")
        style.configure ("Keep.TButton", background="#3176CE", foreground="gold", font=("Aptos", 12, "bold"), relief="raised", padding=10)
        style.map       ("Keep.TButton", background=[("active", "#275CA1"), ("pressed", "#6e9edc")], foreground=[("disabled", "#D3D3D3")])

        style.configure ("Sell.TButton", background="#1F946F", foreground="gold", font=("Aptos", 12, "bold"), relief="raised", padding=10)
        style.map       ("Sell.TButton", background=[("active", "#28BE8F"), ("pressed", "#42D7A8")], foreground=[("disabled", "#D3D3D3")])

        # Set position to be near the main window
        x_offset = window.winfo_x() + 800
        y_offset = window.winfo_y() + 0
        treasure_window.geometry(f"+{x_offset}+{y_offset}")

        message = f"You caught a {treasure_type}! {treasure_info['description']}\nValue: {treasure_info['value']} Gold"
        message_label = ttk.Label(treasure_window, text=message, font=("Aptos", 12, "bold"), background="#800000", foreground="Gold", padding=(10, 10, 10, 10))
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
#   MAIN GAME 2.1.  CAST LINES -    This is where cast_lines function is called.
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
        if currency.get("Gold", 0) < 0:
            result_label.config(text="You're in debt! Quick sell some fish", foreground="#F44336")
            return
        # Check if player has 0 Gold
        if currency.get("Gold", 0) == 0:
            result_label.config(text="Uh Oh You have 0 gold, better hope a thief doesn't steal...", foreground="#F44336")
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
#   MAIN GAME 3.0.  SHOP -          This is where all the Shop components are
    def open_shop():
        #open_shop(window, icon_image)  
        shop_window = tk.Toplevel(window)
        shop_window.title("Shop")
        shop_window.geometry("700x500")
        shop_window.configure(bg="#58a788")        
        # Use your previous `open_shop` function.

        if icon_image:
            shop_window.iconphoto(False, icon_image)

        # Set position to be near the main window
        x_offset = window.winfo_x() + 800
        y_offset = window.winfo_y() + 100
        shop_window.geometry(f"+{x_offset}+{y_offset}")

        style = ttk.Style(shop_window)
        style.theme_use("default")
        style.configure ("Sell.TButton", background="Green", foreground="white", font=("Aptos", 12, "bold"), relief="raised", padding=10)
        style.map       ("Sell.TButton", background=[("active", "#5CDE4F"), ("pressed", "#44BC3B")], foreground=[("disabled", "#D3D3D3")])

        style.configure ("Buy.TButton", background="Blue", foreground="white", font=("Aptos", 12, "bold"), relief="raised", padding=10)
        style.map       ("Buy.TButton", background=[("active", "#5216e9"), ("pressed", "#B03030")], foreground=[("disabled", "#D3D3D3")])

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
        ttk.Button(shop_window, text="Close", command=shop_window.destroy).pack(pady=20)
#   MAIN GAME 4.0.  LEADERBOARD -   This is where all the Leaderboard components are
    #   File to store leaderboard data
    LEADERBOARD_FILE = "leaderboard.txt"
    #   Save a player's score to the leaderboard file
    def save_score(player_name, score):
        with open(LEADERBOARD_FILE, "a") as file:
            file.write(f"{player_name},{score}\n")
    # Leaderboard button
    def display_leaderboard():
        leaderboard_window = tk.Toplevel(window)
        open_windows.append(leaderboard_window)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("500x550")
        leaderboard_window.configure(bg="#34495E")

        if icon_image:
            leaderboard_window.iconphoto(False, icon_image)
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
        close_button.pack(pady=20, padx=20)
#   MAIN GAME 5.0.  EXIT -          This is where the game over, exit and reset score components are.
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
        messagebox.showinfo("Game Over", f"Game over {username}! Final score: {score} ... Exiting Game")
        reset_game_state()  # Reset all game variables
        window.destroy()
    def exit_game(): 
        confirm = tk.messagebox.askyesno("Exit Game", "Are you sure you want to exit the game?")
        if confirm:
            game_over()
            print("exited game!") 
#   MAIN GAME 6.0.  INVENTORY -     This is where the inventory display is updated.
    def update_inventory_display():
        """Update the inventory label on the main window."""
        inventory_text = "Inventory:\n" + "\n".join(f"{fish}: {count}" for fish, count in inventory.items())
        inventory_label.config(text=inventory_text)
#           GUI CONFIGURATION
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.TFrame", background="#000000")
    style.configure("Welcome.TLabel", background="#343434", foreground="white", font=("Aptos (Heading)", 18, "bold"), anchor="center", width=50) # Welcome Label
    style.configure("Custom1.TFrame", background="#000000")
    style.configure("Results.TLabel", background="#343434", foreground="white", font=("Aptos", 14, "bold"),  anchor="center", width=50) # Results Label
    style.configure("Custom2.TFrame", background="#620c97", anchor="center")
    style.configure("Custom3.TFrame", background="#620c97", anchor="center")
    style.configure("Shop.TFrame", background="#000000")
#   RESULTS   FRAME  CONFIG                        
    welcome_frame = ttk.Frame   (window, style="Custom.TFrame", padding=(10, 10, 10, 10))   # LEFT # TOP # RIGHT# BOTTOM
    welcome_frame.pack          (pady=25, padx=25, fill="x")
    welcome_label = ttk.Label   (welcome_frame, text=f"Welcome, {username}! You received 500 gold to be a fisherman", style="Welcome.TLabel")
    welcome_label.pack          (padx=10, pady=0, fill="x") 
#   WELCOME   FRAME  CONFIG 
    result_frame = ttk.Frame    (window, style="Custom1.TFrame", padding=(10, 10, 10, 10))
    result_frame.pack           (pady=25, padx=25, fill="x")
    result_label = ttk.Label    (result_frame, text="Be careful not to go -0 in Gold", style="Results.TLabel")
    result_label.pack           (padx=10, pady=0, fill="x") 
#   GAMEMENU  FRAME  CONFIG 
    gamemenu = ttk.Frame(window, style="Custom2.TFrame", padding=(5, 10, 5, 10))
    gamemenu.pack(pady=25, padx=25, fill="x")

    for i in range(4):  # Adjust the range based on the number of columns you have# Make sure the columns expand equally
        gamemenu.grid_columnconfigure(i, weight=1, uniform="equal")
    gamemenu.grid_rowconfigure(1, weight=1) #   Make sure the row expands equally (for row 1 where labels are placed)
#   SCORE DISPLAY CONFIG        (GAMEMENU FRAME)
    style.configure("Gamemenu.TLabel", background="#620c97", foreground="white", font=("Aptos (Heading)", 10, "bold"), anchor="center", width=50) # Labels
    score_label = ttk.Label(gamemenu, text="Score: 0", style="Gamemenu.TLabel")
    score_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
#   CURRENCY DISPLAY CONFIG     (GAMEMENU FRAME)
    currency_label = ttk.Label(gamemenu, text=f"Gold: {currency['Gold']}", style="Gamemenu.TLabel")
    currency_label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
#   LIVES DISPLAY CONFIG        (GAMEMENU FRAME)
    lives_label = ttk.Label(gamemenu, text="Lives: 3", style="Gamemenu.TLabel")
    lives_label.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
#   INVENTORY DISPLAY CONFIG    (GAMEMENU FRAME)
    inventory_label = ttk.Label(gamemenu, text="Inventory:", style="Gamemenu.TLabel")
    inventory_label.grid(row=1, column=3, columnspan=3, padx=10, pady=10, sticky="nsew")
    update_inventory_display()
#   CAST LINE ENTRY DESC        (GAMEMENU FRAME)
    cast_label = ttk.Label(gamemenu, text="Enter Cast Amount", style="Gamemenu.TLabel")
    cast_label.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
#   CAST LINE ENTRY CONFIG      (GAMEMENU FRAME)
    cast_entry = ttk.Entry(gamemenu, width=10, font=("Arial", 10))
    cast_entry.grid(row=2, column=1,  padx=5, pady=5)
    cast_entry.insert(0, "1")  # Default value of 1 for casting
#   GAMEMENU2 FRAME CONFIG
    gamemenu2 = ttk.Frame(window, style="Custom3.TFrame", padding=(10, 10, 10, 10))
    gamemenu2.pack(pady=2, padx=25, fill="x")
# Make sure the columns expand equally
    for i in range(4):  # Adjust the range based on the number of columns you have
        gamemenu2.grid_columnconfigure(i, weight=1, uniform="equal")
# Make sure the row expands equally (for row 1 where labels are placed)
    gamemenu2.grid_rowconfigure(1, weight=1)
#           " Custom TButton Config "               #
    style.configure ("Custom.TButton",font=("Helvetica", 10, "bold"), padding=10, background="#3498db", foreground="black")
    style.map       ("Custom.TButton", background=[("active", "#2980b9")])  # Active state color
#   Cast Button
    cast_button = ttk.Button        (gamemenu2, text="Cast Line",   command=cast_lines              ,style="Custom.TButton")
    cast_button.grid                (row=3, column=0, padx=5, pady=5)
#   Shop Button
    shop_button = ttk.Button        (gamemenu2, text="Shop",        command=open_shop               ,style="Custom.TButton")
    shop_button.grid                (row=3, column=1, padx=5, pady=5)
#   Leaderboard Button 
    leaderboard_button = ttk.Button (gamemenu2, text="Leaderboard", command=display_leaderboard     ,style="Custom.TButton")
    leaderboard_button.grid         (row=3, column=2, padx=5, pady=5)
#   Exit Button
    exit_button = ttk.Button        (gamemenu2, text="Exit Game",   command=exit_game               ,style="Custom.TButton")
    exit_button.grid                (row=3, column=3,  padx=5, pady=5)
#   This is where we end the window.mainloop.
    window.mainloop()
#   Launch the login window
login_registration_window()