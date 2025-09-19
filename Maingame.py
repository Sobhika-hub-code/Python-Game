import subprocess
import tkinter as tk
from PIL import Image, ImageTk
import itertools

def run_game(game_path):
    try:
        subprocess.run(["python", game_path])
    except Exception as e:
        print(f"Error running {game_path}: {e}")

# Animate title with glowing effect
def animate_title():
    colors = itertools.cycle(["#472FC9", "#EA3680", "#774342", "#EA3FF7", "#24AD87"])
    def update_color():
        title_label.config(fg=next(colors))
        root.after(500, update_color)
    update_color()

# Animate box titles
def animate_label(label):
    colors = itertools.cycle(["black", "blue", "purple"])
    def update_color():
        label.config(fg=next(colors))
        root.after(500, update_color)
    update_color()

# Hover effect for buttons
def on_enter(event, button, original_bg):
    button.config(bg="lightblue")

def on_leave(event, button, original_bg):
    button.config(bg=original_bg)

# Create the main window
root = tk.Tk()
root.geometry("600x400")
root.resizable(True, True)

# Add Background Image
background_img = Image.open("back2.png")
background_photo = ImageTk.PhotoImage(background_img)

# Create a canvas
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)

# Update background
def update_background(event):
    width = event.width
    height = event.height
    resized_bg = background_img.resize((width, height))
    background_photo_resized = ImageTk.PhotoImage(resized_bg)
    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo_resized)
    canvas.image = background_photo_resized

canvas.bind("<Configure>", update_background)

# Load images for buttons (Increased size to 130x130)
jigsaw_img = ImageTk.PhotoImage(Image.open("jigsaw.png").resize((130, 130)))
bricks_img = ImageTk.PhotoImage(Image.open("brickss.png").resize((130, 130)))
flappy_img = ImageTk.PhotoImage(Image.open("flappy.png").resize((130, 130)))
word_img = ImageTk.PhotoImage(Image.open("wordsearch.png").resize((130, 130)))

# Create buttons
btn1 = tk.Button(root, image=jigsaw_img, command=lambda: run_game("puzzle.py"), borderwidth=5)
btn2 = tk.Button(root, image=bricks_img, command=lambda: run_game("bricks.py"), borderwidth=5)
btn3 = tk.Button(root, image=flappy_img, command=lambda: run_game("bird.py"), borderwidth=5)
btn4 = tk.Button(root, image=word_img, command=lambda: run_game("word1.py"), borderwidth=5)

# Store original button background color
original_bg = btn1.cget("bg")

# Bind hover effects
for btn in [btn1, btn2, btn3, btn4]:
    btn.bind("<Enter>", lambda event, button=btn: on_enter(event, button, original_bg))
    btn.bind("<Leave>", lambda event, button=btn: on_leave(event, button, original_bg))

# Place buttons
btn1.place(relx=0.2, rely=0.5, anchor="center")
btn2.place(relx=0.4, rely=0.5, anchor="center")
btn3.place(relx=0.6, rely=0.5, anchor="center")
btn4.place(relx=0.8, rely=0.5, anchor="center")

# Add titles for buttons
label1 = tk.Label(root, text="Jigsaw Puzzle", font=("Arial", 12, "bold"))
label2 = tk.Label(root, text="Brick Breaker", font=("Arial", 12, "bold"))
label3 = tk.Label(root, text="Flappy Bird", font=("Arial", 12, "bold"))
label4 = tk.Label(root, text="Word Search", font=("Arial", 12, "bold"))

# Place labels below buttons
label1.place(relx=0.2, rely=0.65, anchor="center")
label2.place(relx=0.4, rely=0.65, anchor="center")
label3.place(relx=0.6, rely=0.65, anchor="center")
label4.place(relx=0.8, rely=0.65, anchor="center")

# Animate titles
for lbl in [label1, label2, label3, label4]:
    animate_label(lbl)

# Add title label without background and with glowing animation
title_label = tk.Label(root, text="Playtime with Python", font=("Arial", 36, "bold"), bg=root['bg'])
title_label.place(relx=0.5, rely=0.1, anchor="center")

# Start animation
animate_title()

# Run the main loop
root.mainloop()
