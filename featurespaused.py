def reset_game():
    global score, currency, inventory, lives, open_windows

    # Close any additional windows that are open
    for window in open_windows:
        if window.winfo_exists():
            window.destroy()
    open_windows.clear()

    # Reset game variables
    score = 0                    # Reset score
    currency = {"Gold": 500}     # Reset gold to 500
    inventory = {"Live Bait": 10}  # Reset inventory with 10 bait
    lives = [3]                  # Reset lives to 3

    # Update UI elements
    score_label.config(text="Score: 0")
    currency_label.config(text=f"Gold: {currency['Gold']}")
    lives_label.config(text=f"Lives: {lives[0]}")
    result_label.config(text="Game reset. Try catching some fish!", foreground="white")

    # Update the inventory display
    update_inventory_display()

    # Clear input fields if any
    cast_entry.delete(0, tk.END)

    # Reset any state-specific flags if needed
    window.update()


#   Reset Button
#   reset_button = ttk.Button(toolbar, text=" Reset Game", command=reset_game, style="Custom.TButton")
#   reset_button.grid(row=3, column=3,  padx=5, pady=5)

# -- -- -- BUTTON COLORISATION -- -- -- #

#def change_color_on_hover(event):
#    cast_button2.configure(bg="blue", fg="white")
#    cast_button3.configure(bg="green", fg="white")

#def reset_color(event):
#    cast_button2.configure(bg="SystemButtonFace", fg="black")
#    cast_button3.configure(bg="green", fg="white")

#def change_color_on_click():
#    cast_button2.configure(bg="green", fg="white")
#    cast_button3.configure(bg="green", fg="white")

#cast_button2 = tk.Button(window, text="cast2")
#cast_button2.pack(side="top", fill="none", expand=True, padx=10, pady=10, anchor="center")
#cast_button2.bind("<Enter>", change_color_on_hover)  # Change color on hover
#cast_button2.bind("<Leave>", reset_color)  # Reset color when mouse leaves
#cast_button2.configure(command=change_color_on_click)  # Change color on click

#cast_button3 = tk.Button(window, text="cast3")
#cast_button3.pack(side="top", fill="none", expand=True, padx=10, pady=10, anchor="center")
#cast_button3.bind("<Enter>", change_color_on_hover)  # Change color on hover
#cast_button3.bind("<Leave>", reset_color)  # Reset color when mouse leaves
#cast_button3.configure(command=change_color_on_click, comman=open_shop)  # Change color on click