import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
import time

# Game Constants
GRID_SIZE = 3
CELL_SIZE = 100

class JigsawPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Jigsaw Puzzle")
        self.start_screen()

    def start_screen(self):
        self.root.configure(bg="lightblue")
        title_label = tk.Label(self.root, text="Welcome to Jigsaw Puzzle", font=("Arial", 24, "bold"), bg="lightblue")
        title_label.pack(pady=20)

        start_button = tk.Button(self.root, text="Start Game", command=self.start_game, bg="orange")
        start_button.pack(pady=10)

    def start_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="pink")
        
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="pink")
        self.canvas.pack(padx=20, pady=20)

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image, bg="lightgreen")
        self.load_button.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_solution, bg="lightgreen")
        self.submit_button.pack(pady=10)
        self.submit_button.config(state=tk.DISABLED)

        self.tiles = []
        self.shuffled_tiles = []
        self.tile_positions = []
        self.selected_tile = None

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.start_time = None
        self.running = False

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.image = Image.open(file_path).resize((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
        self.split_image()
        self.shuffle_tiles()
        self.draw_tiles()

        self.start_time = time.time()
        self.running = True
        self.submit_button.config(state=tk.NORMAL)

    def split_image(self):
        self.tiles.clear()
        self.tile_positions.clear()
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                left, upper = col * CELL_SIZE, row * CELL_SIZE
                right, lower = left + CELL_SIZE, upper + CELL_SIZE
                tile = self.image.crop((left, upper, right, lower))
                self.tiles.append(ImageTk.PhotoImage(tile))
                self.tile_positions.append((col * CELL_SIZE, row * CELL_SIZE))

    def shuffle_tiles(self):
        self.shuffled_tiles = self.tiles[:]
        random.shuffle(self.shuffled_tiles)

    def draw_tiles(self):
        self.canvas.delete("all")
        self.tile_ids = []
        for index, (x, y) in enumerate(self.tile_positions):
            tile_id = self.canvas.create_image(x, y, anchor="nw", image=self.shuffled_tiles[index])
            self.tile_ids.append(tile_id)

    def on_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        if item in self.tile_ids:
            self.selected_tile = item

    def on_release(self, event):
        if self.selected_tile:
            closest_tile = self.canvas.find_closest(event.x, event.y)[0]
            if closest_tile in self.tile_ids and closest_tile != self.selected_tile:
                index1 = self.tile_ids.index(self.selected_tile)
                index2 = self.tile_ids.index(closest_tile)

                self.tile_ids[index1], self.tile_ids[index2] = self.tile_ids[index2], self.tile_ids[index1]
                self.shuffled_tiles[index1], self.shuffled_tiles[index2] = self.shuffled_tiles[index2], self.shuffled_tiles[index1]

                self.draw_tiles()
            self.selected_tile = None

    def check_solution(self):
        if not self.running:
            return
        
        if self.shuffled_tiles == self.tiles:
            self.running = False
            end_time = time.time()
            elapsed_time = int(end_time - self.start_time)
            score = max(1000 - elapsed_time * 10, 0)
            messagebox.showinfo("Congratulations!", f"You solved it! Time: {elapsed_time} seconds. Score: {score}")
        else:
            messagebox.showerror("Oops!", "The puzzle is not solved correctly. Try again!")

# Run Game
root = tk.Tk()
game = JigsawPuzzle(root)
root.mainloop()
