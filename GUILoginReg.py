import tkinter as tk
from tkinter import messagebox
from auth import Auth
import subprocess
import sys
import os

class FishingGameApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Fishing Game Login/Register")
        self.master.geometry("400x300")
        self.auth = Auth()

        # Welcome Label
        self.welcome_label = tk.Label(self.master, text="Welcome to the Fishing Game!\nPlease log in or register below:", font=("Arial", 12))
        self.welcome_label.pack(pady=(10, 20))

        # Create a frame for the input fields
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        # Username Label and Entry
        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        # Password Label and Entry
        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        # Login Button
        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, pady=5)

        # Register Button
        self.register_button = tk.Button(self.frame, text="Register", command=self.register)
        self.register_button.grid(row=2, column=1, pady=5)

        # Test Label
        self.ty_label = tk.Label(self.master, text="Thank you so much for playing my game!!!", font=("Arial", 12))
        self.ty_label.pack(pady=(10, 20))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth.login(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.launch_game()
        else:
            messagebox.showerror("Error", "Login failed. Please try again.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth.register(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.launch_game()
        else:
            messagebox.showerror("Error", "Registration failed. Please try again.")

    def launch_game(self):
        username = self.username_entry.get()  # Get the username
        self.master.quit()  # Close the login window
        # Get the path to the main.py file
        script_path = os.path.join(os.path.dirname(__file__), 'main.py')
        # Launch the game script and pass the username as an argument
        subprocess.Popen([sys.executable, script_path, username])

if __name__ == "__main__":
    root = tk.Tk()
    app = FishingGameApp(root)
    root.mainloop()