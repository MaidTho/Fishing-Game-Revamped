import tkinter as tk

root = tk.Tk()
root.geometry("300x200")
root.title("Button test")

def change_color_on_hover(event):
    button.configure(bg="blue", fg="white")

def reset_color(event):
    button.configure(bg="SystemButtonFace", fg="black")

def change_color_on_click():
    button.configure(bg="green", fg="white")

button = tk.Button(root, text="hover or click me")
button.pack()

# Bind the events to the button
button.bind("<Enter>", change_color_on_hover)  # Change color on hover
button.bind("<Leave>", reset_color)  # Reset color when mouse leaves
button.configure(command=change_color_on_click)  # Change color on click

root.mainloop()
