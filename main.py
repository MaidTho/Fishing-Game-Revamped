import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import os
import sys

#   Initialize the main window
window = tk.Tk()
window.title("Fishing Game")
window.geometry("650x800")  #   Width x Height
window.configure(bg="#4f4eb1")

#   Load the new window icon image
icon_image = tk.PhotoImage(file="assets\icon_image.png")
window.iconphoto(False, icon_image)


# Use os.path.join to handle paths correctly across systems
icon_path = os.path.join('assets', 'icon_image.png')

# Load the image using the corrected path
icon_image = tk.PhotoImage(file=icon_path)

if getattr(sys, 'frozen', False):  # If running as an executable
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(BASE_DIR, 'assets', 'icon_image.png')

# Load the icon image
icon_image = tk.PhotoImage(file=icon_path)



# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#              LEADERBOARD SECTION                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

#   Fetch the username passed from the login script
username = sys.argv[1] if len(sys.argv) > 1 else "Player"

#   Display a welcome message with the username
welcome_label = ttk.Label( 
    window, 
    text=f"Welcome, {username}! Let's start fishing!", 
    font=("Helvetica", 14, "bold"))
welcome_label.pack(pady=(30, 30))

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
    leaderboard_window.geometry("500x600") #   Width x Height
    leaderboard_window.configure(bg="#34495E")

    # Load the new window icon image
    icon_image = tk.PhotoImage(file="assets/icon_image.png")
    leaderboard_window.iconphoto(False, icon_image)

    # Set position to be near the main window
    x_offset = window.winfo_x() + 700
    y_offset = window.winfo_y() + 0
    leaderboard_window.geometry(f"+{x_offset}+{y_offset}")

    # Leaderboard title label
    title_label = ttk.Label(
        leaderboard_window, 
        text="🏆 Leaderboard 🏆", 
        font=("Helvetica", 18, "bold"), 
        background="#34495E", 
        foreground="gold"
    )
    title_label.pack(pady=20)

    # Style for the Treeview widget
    style = ttk.Style()
    style.configure("Treeview", background="#2C3E50", foreground="white", rowheight=30, fieldbackground="#2C3E50")
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#1ABC9C", foreground="black")
    style.map("Treeview", background=[("selected", "#3498DB")])

    # Treeview widget for displaying scores
    leaderboard_tree = ttk.Treeview(
        leaderboard_window, 
        columns=("Rank", "Player", "Score"), 
        show="headings", 
        height=10
    )
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
    close_button = ttk.Button(
        leaderboard_window, 
        text="Close", 
        command=leaderboard_window.destroy,
        style="Custom.TButton"
    )
    close_button.pack(pady=20)

#   Example use: Call save_score at the end of the game
def end_game():
    save_score(username, score)  # Save current game score
    display_leaderboard()        # Show leaderboard

#   Save score on exit
def on_exit():
    save_score(username, score)  # Save the current score with the username
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_exit)

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                VARIABLES SECTION                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

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
open_windows = []

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                GAME LOGIC SECTION                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - #

def game_over():
    save_score(username, score)
    messagebox.showinfo("Game Over", f"Game over {username}! Final score: {score} ... Returing to Login.")
    reset_game_state()  # Reset all game variables
    window.destroy()
    os.system("python GUILoginReg.py")

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
    treasure_window.configure(bg="#34495E")
    
    # Set position to be near the main window
    x_offset = window.winfo_x() + 600
    y_offset = window.winfo_y()
    treasure_window.geometry(f"+{x_offset}+{y_offset}")

    # Load the new window icon image
    icon_image = tk.PhotoImage(file="assets/icon_image.png")
    treasure_window.iconphoto(False, icon_image)

    message = f"You caught a {treasure_type}! {treasure_info['description']}\nValue: {treasure_info['value']} Gold"
    message_label = ttk.Label(treasure_window, text=message, background="#34495E", foreground="white")
    message_label.pack(pady=10)    
    
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

    keep_button = ttk.Button(treasure_window, text="Keep", command=keep_treasure)
    keep_button.pack(side=tk.LEFT, padx=20, pady=20)

    sell_button = ttk.Button(treasure_window, text="Sell", command=sell_treasure)
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

def reset_game_state():
    global score, currency, inventory, lives, open_windows

    # Reset game variables to their initial state
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

def exit_game():
    confirm = tk.messagebox.askyesno("Exit Game", "Are you sure you want to exit to the login screen")
    if confirm:
        save_score(username, score)
        reset_game_state()  
        window.destroy()

        os.system("python GUILoginReg.py")

window.protocol("WM_DELETE_WINDOW", exit_game)
# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                   SHOP SECTION                    #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

from shop import open_shop, set_globals

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                INVENTORY SECTION                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

def open_inventory():
    """Open the inventory window with fixed size and scrollbar."""
    inventory_window = tk.Toplevel(window)
    inventory_window.title("Inventory")
    inventory_window.geometry("600x300")
    inventory_window.configure(bg="#34495E")
    
    # Load the new window icon image
    icon_image = tk.PhotoImage(file="assets/icon_image.png")
    inventory_window.iconphoto(False, icon_image)

    # Set position to be near the main window
    x_offset = window.winfo_x() + 50
    y_offset = window.winfo_y() + 50
    inventory_window.geometry(f"+{x_offset}+{y_offset}")

    inventory_label = ttk.Label(
        inventory_window, 
        text="Your Inventory", 
        font=("Helvetica", 12, "bold"), 
        background="#34495E", 
        foreground="white"
    )
    inventory_label.pack(pady=10)

    # Frame to hold the inventory text widget and scrollbar
    inventory_frame = ttk.Frame(inventory_window)
    inventory_frame.pack(pady=5)

    # Scrollbar for inventory
    scrollbar = tk.Scrollbar(inventory_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Inventory display with fixed height and width
    inventory_display = tk.Text(
        inventory_frame, 
        height=10, 
        width=40, 
        wrap='word', 
        font=("Helvetica", 10), 
        yscrollcommand=scrollbar.set
    )
    inventory_display.pack()
    scrollbar.config(command=inventory_display.yview)

    # Insert the inventory items
    inventory_display.insert(tk.END, "\n".join(f"{fish}: {count}" for fish, count in inventory.items()))
    inventory_display.config(state='disabled')

def update_inventory_display():
    """Update the inventory label on the main window."""
    inventory_text = "Inventory:\n" + "\n".join(f"{fish}: {count}" for fish, count in inventory.items())
    inventory_label.config(text=inventory_text)

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                    GUI SECTION                    #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

#   Applying a style theme
style = ttk.Style()
style.theme_use("alt")
# VVV Results, Inventory and Stats Frame Stying VVV
style.configure("Custom.TFrame", background="#2C3E50")  # Update for styling
#   VVV Shop button Styling VVV
style.configure(
    "TButton", 
    font=("Helvetica", 10), 
    padding=20, 
    background="#2C3E50", 
    foreground="white") 

#   VVV Main GUI Button Styling VVV
style.configure( 
    "Custom.TButton",
    font=("Helvetica", 10, "bold"), 
    padding=10, 
    background="#3498db", 
    foreground="black")
style.map("Custom.TButton", background=[("active", "#2980b9")])  # Active state color

#   Custom Label Stying
style.configure("TLabel", font=("Helvetica", 10), padding=20, background="#2C3E50", foreground="white")

#   Instructions Label
instructions_label = ttk.Label(
    window, 
    text="🎣 Cast your line to catch some fish!", 
   # font=("Helvetica", 14, "bold"),
    anchor='center',
    style="TLabel"
    )
instructions_label.pack(pady=10, padx=10, fill="x")

result_frame = ttk.Frame(
    window, 
    style="Custom.TFrame",
    padding=(10, 10, 10, 10)
)
result_frame.pack(pady=10, padx=10, fill="x")

# Set minimum size for the frame (so it doesn't collapse)
result_frame.grid_rowconfigure(0, minsize=50)   # Minimum height for row 0
result_frame.grid_columnconfigure(0, minsize=600)  # Minimum width for column 0

#   Toolbar Frame
toolbar = ttk.Frame(
    window, 
    style="Custom.TFrame", 
    padding=(10, 10, 10, 10)
    )
toolbar.pack(pady=10, padx=10, fill="x")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#                           LABEL MAPPING                               #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# Result message with a fixed width
result_label = ttk.Label(
    result_frame, 
    text="", 
    font=("Helvetica", 12), 
    background="#2C3E50", 
    foreground="white", 
    anchor="center",
    width=50
)
result_label.pack( padx=5, pady=5,fill="x") 

#   Score Display
score_label = ttk.Label(
    toolbar, 
    text="Score: 0", 
    font=("Helvetica", 14, "bold")
    )
score_label.grid(row=1, column=0,  padx=5, pady=5)

#   Currency Display
currency_label = ttk.Label(
    toolbar, 
    text=f"Gold: {currency['Gold']}", 
    font=("Helvetica", 14, "bold")
    )
currency_label.grid(row=1, column=1,  padx=5, pady=5)

#   Lives Display
lives_label = ttk.Label(
    toolbar, 
    text="Lives: 3",
    font=("Helvetica", 14, "bold")
    )
lives_label.grid(row=1, column=2,  padx=5, pady=5)

#   Inventory Display
inventory_label = ttk.Label(
    toolbar,
    text="Inventory:", 
    font=("Helvetica", 10, "bold")
    )
inventory_label.grid(row=1, column=3, columnspan=3, padx=5, pady=5)
update_inventory_display()

#   Cast line input Description
cast_label = ttk.Label(
    toolbar, 
    text="Number of casts:",
    )
cast_label.grid(row=2, column=0,  padx=5, pady=5)

#   Cast line input
font_size = 15  
cast_entry = ttk.Entry(
    toolbar, 
    width=8, 
    font=("Arial", font_size)
    )
cast_entry.grid(row=2, column=1,  padx=5, pady=5)
cast_entry.insert(0, "1")  # Default value of 1 for casting

set_globals(window, currency, inventory, update_inventory_display, currency_label, result_label, fish_types, lives_label, lives)

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#               MENU BUTTON SECTION                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

#   Cast Button
cast_button = ttk.Button(toolbar, text=" Cast Line", command=cast_lines, style="Custom.TButton")
cast_button.grid(row=3, column=0, padx=5, pady=5)

#   Shop Button
shop_button = ttk.Button(toolbar, text=" Shop", command=open_shop, style="Custom.TButton")
shop_button.grid(row=3, column=1, padx=5, pady=5)

#   Leaderboard Button 
leaderboard_button = ttk.Button(toolbar, text="Leaderboard", command=display_leaderboard, style="Custom.TButton")
leaderboard_button.grid(row=3, column=2, padx=5, pady=5)

#   Exit Button
exit_button = ttk.Button(toolbar, text="Exit Game", command=exit_game, style="Custom.TButton")
exit_button.grid(row=3, column=3,  padx=5, pady=5)

#  - - - RUN GAME LOOP - - - #
window.mainloop()
