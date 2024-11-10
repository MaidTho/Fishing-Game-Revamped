import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from auth import Auth
import subprocess
import sys
import os

class FishingGameApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Fishing Game Login/Register")
        self.master.geometry("500x450")
        self.auth = Auth()       
        self.master.configure(bg="#2C3E50") # Set up a background color and frame
        
        self.icon_image = PhotoImage(file="assets/icon_image.png")
        self.master.iconphoto(False, self.icon_image)  # Use iconphoto() for PNG support
        
        self.frame = ttk.Frame(self.master, padding=20)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Welcome Label
        self.welcome_label = tk.Label(
            self.frame, 
            text="Welcome to the Fishing Game!\nPlease log in or register:", 
            font=("Helvetica", 16, "bold"),
            fg="#000000", 
            #bg="#2C3E50"  
            # Font color black, background color matches window
        )
        self.welcome_label.pack(pady=(10, 20))

        # Username Label
        self.username_label = tk.Label(
            self.frame, 
            text="Username", 
            font=("Arial", 12), 
            fg="#000000",
        #   bg="#FFFFFF"
        )
        self.username_label.pack(anchor=tk.CENTER, pady=(10, 5))
        
        # Username Entry
        self.username_entry = ttk.Entry(
            self.frame, 
            text="Username", 
            font=("Arial", 12), 
            width=30
        )
        self.username_entry.pack(pady=5)

        # Password Label
        self.password_label = tk.Label(
            self.frame, 
            text="Password", 
            font=("Arial", 12), 
            fg="#000000", 
        #    bg="#FFFFFF"
        )
        self.password_label.pack(anchor=tk.CENTER, pady=(20, 5))
        
        # Password Entry
        self.password_entry = ttk.Entry(
            self.frame, 
            show="*", 
            text="Password", 
            font=("Arial", 12), 
            width=30)
        self.password_entry.pack(pady=5)

        # Buttons Frame
        self.button_frame = tk.Frame(
            self.frame, 
            #bg="#2C3E50"
            )
        self.button_frame.pack(pady=30)

        # Login Button
        self.login_button = tk.Button(
            self.button_frame, 
            text="Login", 
            command=self.login, 
            font=("Arial", 12, "bold"),
            bg="#27AE60", 
            fg="white",
            activebackground="#2ECC71", 
            activeforeground="white",
            relief=tk.FLAT, width=12, height=1
        )
        self.login_button.grid(row=0, column=0, padx=10)

        # Register Button
        self.register_button = tk.Button(
            self.button_frame, 
            text="Register",
            command=self.register,
            font=("Arial", 12, "bold"),
            bg="#3498DB", fg="white",
            activebackground="#5DADE2", 
            activeforeground="white",
            relief=tk.FLAT, width=12, height=1
        )
        self.register_button.grid(row=0, column=1, padx=10)

        # Thank You Label
        self.ty_label = tk.Label(
            self.frame, 
            text="Thank you for playing!", 
            font=("Arial", 12), 

          #  bg="#2C3E50"
            fg="#000000",           
        )
        self.ty_label.pack(pady=(20, 10))

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
