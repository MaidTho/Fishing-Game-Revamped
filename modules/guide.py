# - - - - - IMPORTS - - - - - #
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys

def get_asset_path(filename):
    if getattr(sys, 'frozen', False):  # Check if running as an executable
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Use os.path.join to handle different path separators
    return os.path.normpath(os.path.join(base_dir, 'assets', filename))

# - - - - - GLOBAL VARIABLES - - - - - #

# - - - - - WINDOW INITIALIZATION  - - - - - #
window = tk.Tk()
window.title("Simple Button Game")
window.geometry("300x200")  # Width x Height

# Load an icon image with error handling
try:
    icon_path = get_asset_path('icon_image.png')
    print(f"Looking for icon at: {icon_path}")  # Debugging statement
    icon_image = tk.PhotoImage(file=icon_path)
except tk.TclError as e:
    print(f"Error loading icon image: {e}")
    icon_image = None  # Fallback if the image is not found
except Exception as e:
    print(f"Unexpected error: {e}")

if icon_image:
    window.iconphoto(False, icon_image)

# - - - - - GAME LOGIC SECTION - - - - - #

score = 0

def increase_score():
    """Increase the score and update the label."""
    global score
    score += 1
    score_label.config(text=f"Score: {score}")

# - - - - - CAST LINES - - - - - #

# - - - - - SHOP SECTION - - - - - #

# - - - - - LEADERBOARD SECTION - - - - - #

# - - - - - EXIT GAME - - - - - #
def exit_game():
    answer = messagebox.askyesno("Exit Game", "Are you sure you want to exit?")
    if answer:
        print("Thank you for playing! Exiting the game...")
        sys.exit()

# - - - - - GUI - - - - - #
style = ttk.Style()
style.theme_use("classic")
style.configure("Custom.TButton",font=("Helvetica", 10, "bold"), padding=10, background="#3498db", foreground="black")      #   Play Button Style
style.configure("Custom2.TButton",font=("Arial", 20, "bold"), padding=10, background="red", foreground="black")             #   Exit Button Style

# - - - - - FRAMES - - - - - #
score_frame = ttk.Frame(window, padding=(10, 10, 10, 10))
score_frame.pack(pady=10, padx=10, fill="x")

# - - - - - LABEL - - - - - #
score_label = ttk.Label(window, text="Score: 0", font=("Helvetica", 14, "bold"))
score_label.pack(pady=10, padx=10, fill="x")

# - - - - - BUTTONS - - - - - #
score_button = ttk.Button(window, text="Increase Score", style="Custom.TButton", command=increase_score)
score_button.pack(pady=10, padx=10)

exit_button = ttk.Button(window, text="Exit Game", style="Custom2.TButton", command=exit_game)
exit_button.pack(pady=10, padx=10)



#  - - - RUN GAME LOOP - - - #    
window.mainloop()