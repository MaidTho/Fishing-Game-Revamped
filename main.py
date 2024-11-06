import tkinter as tk
from tkinter import ttk
import random
import os
import sys

# Initialize the main window
window = tk.Tk()
window.title("Fishing Game")
window.geometry("800x600")
window.configure(bg="#2C3E50")

# Load the new window icon image
icon_image = tk.PhotoImage(file="assets\icon_image.png")
window.iconphoto(False, icon_image)

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#              LEADERBOARD SECTION                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

# Fetch the username passed from the login script
username = sys.argv[1] if len(sys.argv) > 1 else "Player"

# Display a welcome message with the username
welcome_label = ttk.Label(window, text=f"Welcome, {username}! Let's start fishing!", font=("Helvetica", 14, "bold"))
welcome_label.pack(pady=10)

# File to store leaderboard data
LEADERBOARD_FILE = "leaderboard.txt"

# Save a player's score to the leaderboard file
def save_score(player_name, score):
    with open(LEADERBOARD_FILE, "a") as file:
        file.write(f"{player_name},{score}\n")

# Load and display the leaderboard
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

# Example use: Call save_score at the end of the game
def end_game():
    save_score(username, score)  # Save current game score
    display_leaderboard()        # Show leaderboard

# Save score on exit
def on_exit():
    save_score(username, score)  # Save the current score with the username
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_exit)


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
score       = 0                     # Starting score
currency    = {"Gold": 500}         # Starting cash
inventory   = {"Live Bait": 10}     # Starting bait
lives       = 3                     # Starting life

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                GAME LOGIC SECTION                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

def cast_lines(num_casts):
    global score, inventory, lives
    successes = 0
    fails = 0

    if inventory.get("Live Bait", 0) < 1:       # User runs out of bait
        result_label.config(text="No bait left! Buy more from the shop.", foreground="#F44336")
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

from shop import open_shop

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#                INVENTORY SECTION                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

def open_inventory():
    inventory_window = tk.Toplevel(window)
    inventory_window.title("Inventory")
    inventory_window.geometry("400x250")
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

# Applying a style theme
style = ttk.Style()
style.theme_use("default")
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

#   Score Display
score_label = ttk.Label(    
                            window, 
                            text="Score: 0", 
                            font=("Helvetica", 14, "bold"))
score_label.pack(pady=10)

#   Currency Display 
currency_label = ttk.Label( 
                            window, 
                            text=f"Gold: {currency['Gold']}",   
                            font=("Helvetica", 14, "bold"),     
                            background="#2C3E50", foreground="white")
currency_label.pack(pady=10)

#   Lives display
lives_label = ttk.Label(    
                            window, 
                            text="Lives: 3", 
                            font=("Helvetica", 14, "bold"))
lives_label.pack(pady=10)

# Inventory display (Front Page)
inventory_label = ttk.Label(    
                                window, 
                                text="Inventory:", 
                                font=("Helvetica", 12))
inventory_label.pack(pady=10)
update_inventory_display()

# Toolbar Frame
toolbar = ttk.Frame(window, padding=(10, 10, 10, 10))
toolbar.pack(pady=10)

# - - - - - - - - - - - - - - - - - - - - - - - - - # 
#               MENU BUTTON SECTION                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - # 

# Cast line input
cast_label = ttk.Label(toolbar, text="Number of casts:")
cast_label.grid(row=0, column=0, padx=5)

font_size = 15  
cast_entry = ttk.Entry(toolbar, width=8, font=("Arial", font_size))
cast_entry.grid(row=0, column=1, padx=5)

cast_entry.insert(0, "1")  # Default value of 1 for casting

#   Cast Button
cast_button = ttk.Button(toolbar, text=" Cast Line", command=lambda: cast_lines(int(cast_entry.get()) if cast_entry.get().isdigit() else 1))
cast_button.grid(row=0, column=2, padx=5)

#   Leaderboard Button 
leaderboard_button = ttk.Button(toolbar, text="Leaderboard", command=display_leaderboard)
leaderboard_button.grid(row=0, column=3, padx=5)

#   Shop Button
shop_button = ttk.Button(toolbar, text=" Shop", command=lambda: open_shop(window, currency, inventory, update_inventory_display, currency_label, result_label, fish_types))
shop_button.grid(row=1, column=1, padx=5)

#   Inventory Button
inventory_button = ttk.Button(toolbar, text=" Inventory", command=open_inventory)
inventory_button.grid(row=1, column=2, padx=5)

#   Reset Button
reset_button = ttk.Button(toolbar, text=" Reset Game", command=reset_game)
reset_button.grid(row=1, column=3, padx=5)

#  - - - - - - - - - - - - - - - - - - - - - - - - -             RUN GAME LOOP  - - - - - - - - - - - - - - - - - - - - - - - - - #
window.mainloop()