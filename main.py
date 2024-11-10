import tkinter as tk
from tkinter import ttk
import random
import os
import sys

#   Initialize the main window
window = tk.Tk()
window.title("Fishing Game")
window.geometry("700x800")
window.configure(bg="#4f4eb1")

#   Load the new window icon image
icon_image = tk.PhotoImage(file="assets\icon_image.png")
window.iconphoto(False, icon_image)

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
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("400x300")
    leaderboard_window.configure(bg="#34495E")

    # Load the new window icon image
    icon_image = tk.PhotoImage(file="assets\icon_image.png")
    leaderboard_window.iconphoto(False, icon_image)

    # Set position to be near the main window
    x_offset = window.winfo_x() + 50
    y_offset = window.winfo_y() + 50
    leaderboard_window.geometry(f"+{x_offset}+{y_offset}")
    
    # Label for leaderboard
    title_label = ttk.Label(leaderboard_window, text="Leaderboard", font=("Helvetica", 16, "bold"), background="#34495E", foreground="white")
    title_label.pack(pady=10)

    # Read scores and sort them
    scores = []
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            for line in file:
                name, score = line.strip().split(",")
                scores.append((name, int(score)))
        scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score descending
    
    # Display top scores
    leaderboard_text = tk.Text(leaderboard_window, height=10, width=30, state="normal", font=("Helvetica", 12))
    leaderboard_text.pack(pady=10)
    leaderboard_text.insert(tk.END, "Top Scores:\n\n")
    
    for rank, (name, score) in enumerate(scores[:10], 1):  # Show top 10
        leaderboard_text.insert(tk.END, f"{rank}. {name} - {score} points\n")
    leaderboard_text.config(state="disabled")

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

#   Initialize score, currency, inventory, items, and lives
score       = 0                     # Starting score
currency    = {"Gold": 500}         # Starting cash
inventory   = {"Live Bait": 10}     # Starting bait
lives       = [3]                   # Starting life

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                GAME LOGIC SECTION                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

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

    for _ in range(num_casts):
        # Trigger hazard before each cast with a 20% chance
        if random.random() < 0.2:
            hazard_triggered = trigger_hazard()
            if hazard_triggered:
                continue  # Skip this cast if a hazard was triggered

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

        window.update_idletasks()  # Ensure the UI is updated immediately

    # Update the inventory and labels after all casts are completed
    update_inventory_display()
    currency_label.config(text=f"Gold: {currency.get('Gold', 0)}")
    lives_label.config(text=f"Lives: {lives[0]}")

def reset_game():
    global score, currency, inventory, lives
    score       = 0                     # Reset Score to 0.
    score_label.config(text="Score: 0")

    currency    = {"Gold: 500"}         # Reset Gold to 500.
    currency_label.config(text=f"Gold: {currency['Gold']}")    
    
    inventory   = {"Live Bait": 10}     # Reset to 10 bait.
    
    lives       = 3                     # Reset lives to 3.
    lives_label.config(text="Lives: 3")
    
    result_label.config(text="Game reset. Try catching some fish!", foreground="white")
    update_inventory_display()

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                   SHOP SECTION                    #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

from shop import open_shop, set_globals

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                INVENTORY SECTION                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

def open_inventory():
    inventory_window = tk.Toplevel(window)
    inventory_window.title("Inventory")
    inventory_window.geometry("600x250")
    inventory_window.configure(bg="#34495E")
    
    # Load the new window icon image
    icon_image = tk.PhotoImage(file="assets\icon_image.png")
    inventory_window.iconphoto(False, icon_image)

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

def update_inventory_display():
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
    font=("Helvetica", 14, "bold")
    )
instructions_label.pack(pady=10)

#   Frame to hold the result message with a minimum size
result_frame = ttk.Frame(
    window, 
    style="Custom.TFrame",
    padding=(10, 10, 10, 10)
    )
result_frame.pack(pady=10)
result_frame.grid_rowconfigure(0, minsize=50)  # Minimum height for row 0 #   Set minimum size for the frame (so it doesn't collapse)
result_frame.grid_columnconfigure(0, minsize=400)  # Minimum width for column 0

#   Result message
result_label = ttk.Label(
    result_frame, 
    text="His mind would turn onto the waters.", 
    font=("Helvetica", 14, "italic")
    )
result_label.grid(row=0, column=0)

#   Apply the style to your frame
stats_frame = ttk.Frame(
    window, 
    style="Custom.TFrame", 
    padding=(10, 10)
    )
stats_frame.pack(pady=10)

#   Score Display
score_label = ttk.Label(
    stats_frame, 
    text="Score: 0", 
    font=("Helvetica", 14, "bold")
    )
score_label.grid(row=0, column=0, padx=10, pady=5)

#   Currency Display
currency_label = ttk.Label(
    stats_frame, 
    text=f"Gold: {currency['Gold']}", 
    font=("Helvetica", 14, "bold")
    )
currency_label.grid(row=0, column=1, padx=10, pady=5)

#   Lives Display
lives_label = ttk.Label(
    stats_frame, 
    text="Lives: 3",
    font=("Helvetica", 14, "bold")
    )
lives_label.grid(row=0, column=2, padx=10, pady=5)

#   Inventory Display
inventory_label = ttk.Label(
    stats_frame,
    text="Inventory:", 
    font=("Helvetica", 14, "bold")
    )
inventory_label.grid(row=1, column=0, columnspan=3, pady=10)
update_inventory_display()

#   Toolbar Frame
toolbar = ttk.Frame(
    window, 
    style="Custom.TFrame", 
    padding=(10, 10, 10, 10)
    )
toolbar.pack(pady=10)

#   Cast line input Description
cast_label = ttk.Label(
    toolbar, 
    text="Number of casts:",
    )
cast_label.grid(row=0, column=0, padx=5)

#   Cast line input
font_size = 15  
cast_entry = ttk.Entry(
    toolbar, 
    width=8, 
    font=("Arial", font_size)
    )
cast_entry.grid(row=0, column=1, padx=5)

cast_entry.insert(0, "1")  # Default value of 1 for casting

set_globals(window, currency, inventory, update_inventory_display, currency_label, result_label, fish_types, lives_label, lives)

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#               MENU BUTTON SECTION                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

#   Cast Button
cast_button = ttk.Button(toolbar, text=" Cast Line", command=cast_lines, style="Custom.TButton")
cast_button.grid(row=0, column=2, padx=5)

#   Shop Button
shop_button = ttk.Button(toolbar, text=" Shop", command=open_shop, style="Custom.TButton")
shop_button.grid(row=1, column=1, padx=5)

#   Leaderboard Button 
leaderboard_button = ttk.Button(toolbar, text="Leaderboard", command=display_leaderboard, style="Custom.TButton")
leaderboard_button.grid(row=1, column=2, padx=5)

#   Reset Button
reset_button = ttk.Button(toolbar, text=" Reset Game", command=reset_game, style="Custom.TButton")
reset_button.grid(row=1, column=3, padx=5)

#  - - - RUN GAME LOOP - - - #
window.mainloop()
