import tkinter as tk
from tkinter import ttk
import random

# Fish types and their probabilities of being caught and points
fish_types = {
    "Small Fish": {"catch_chance": 0.8, "points": 5},
    "Big Fish": {"catch_chance": 0.5, "points": 10},
    "Rare Fish": {"catch_chance": 0.2, "points": 20},
}

# Initialize score
score = 0

def cast_line():
    global score
    # Choose a random fish type
    fish = random.choice(list(fish_types.keys()))
    catch_chance = fish_types[fish]["catch_chance"]
    points = fish_types[fish]["points"]

    # Determine if fish is caught
    if random.random() < catch_chance:
        result_label.config(text=f"You caught a {fish}!", foreground="#4CAF50")  # Green for success
        score += points
        score_label.config(text=f"Score: {score}")
    else:
        result_label.config(text=f"The {fish} got away!", foreground="#F44336")  # Red for failure

def reset_game():
    global score
    score = 0
    score_label.config(text="Score: 0")
    result_label.config(text="Game reset. Try catching some fish!", foreground="white")

# Setting up the GUI
window = tk.Tk()
window.title("Fishing Game")
window.geometry("800x600")
window.configure(bg="#2C3E50")  # Dark background for modern look

# Load the new window icon image

icon_image = tk.PhotoImage(file="/FishingGameRevamped/icon_image.png") # May have to reconfigure path to image.
window.iconphoto(False, icon_image)

# Applying a style theme
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 12), padding=6, background="#3498DB", foreground="white")
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

# Score display
score_label = ttk.Label(window, text="Score: 0", font=("Helvetica", 14, "bold"))
score_label.pack(pady=10)

# Toolbar Frame
toolbar = ttk.Frame(window, padding=(10, 10, 10, 10))
toolbar.pack(pady=10)

# Toolbar Buttons
cast_button = ttk.Button(toolbar, text=" Cast Line", command=cast_line, style="TButton")
cast_button.grid(row=0, column=0, padx=5)

reset_button = ttk.Button(toolbar, text=" Reset Game", command=reset_game, style="TButton")
reset_button.grid(row=0, column=1, padx=5)

# Run the game loop
window.mainloop()
