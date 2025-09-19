import tkinter as tk
import random

# Game settings
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
DELAY = 150  # Slower speed for better control

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0)
}

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 SNAKE ARCADE")
        self.root.configure(bg="black")

        # Scoreboard
        self.score = 0
        self.score_label = tk.Label(root, text=f"Score: {self.score}",
                                    font=("Courier", 16, "bold"),
                                    fg="lime", bg="black")
        self.score_label.pack()

        # Game canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg="black", highlightthickness=0)
        self.canvas.pack()

        # Buttons
        self.button_frame = tk.Frame(root, bg="black")
        self.button_frame.pack(pady=10)

        self.restart_btn = tk.Button(self.button_frame, text="🔁 Restart",
                                     font=("Courier", 12),
                                     command=self.restart_game,
                                     bg="gray20", fg="white", relief="raised")
        self.restart_btn.pack(side="left", padx=10)

        self.exit_btn = tk.Button(self.button_frame, text="❌ Exit",
                                  font=("Courier", 12),
                                  command=root.quit,
                                  bg="gray20", fg="white", relief="raised")
        self.exit_btn.pack(side="left", padx=10)

        # Key bindings
        self.root.bind("<Key>", self.change_direction)

        # Start the game
        self.start_game()

    def start_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.obstacles = self.generate_obstacles()  # ✅ Create obstacles first
        self.food = self.place_food()               # ✅ Now safe to place food
        self.running = True
        self.update()

    def restart_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.start_game()

    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE,
                                         fill="lime", tag="snake", outline="black")

    def draw_food(self):
        x, y = self.food
        self.canvas.create_oval(x, y, x + CELL_SIZE, y + CELL_SIZE,
                                fill="red", tag="food", outline="yellow")

    def draw_obstacles(self):
        self.canvas.delete("obstacle")
        for x, y in self.obstacles:
            self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE,
                                         fill="gray", tag="obstacle", outline="white")

    def move_snake(self):
        dx, dy = DIRECTIONS[self.direction]
        head_x, head_y = self.snake[0]

        # Wrap-around movement
        new_x = (head_x + dx * CELL_SIZE) % WIDTH
        new_y = (head_y + dy * CELL_SIZE) % HEIGHT
        new_head = (new_x, new_y)

        # Collision detection
        if new_head in self.snake or new_head in self.obstacles:
            self.running = False
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2,
                                    text="💀 GAME OVER 💀",
                                    fill="red", font=("Courier", 24, "bold"))
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.place_food()
        else:
            self.snake.pop()

    def place_food(self):
        while True:
            x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                return (x, y)

    def generate_obstacles(self):
        obstacle_count = 10
        obstacles = set()
        while len(obstacles) < obstacle_count:
            x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in self.snake:
                obstacles.add((x, y))
        return list(obstacles)

    def change_direction(self, event):
        new_dir = event.keysym
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_dir in DIRECTIONS and new_dir != opposites.get(self.direction):
            self.direction = new_dir

    def update(self):
        if self.running:
            self.move_snake()
            self.canvas.delete("food")
            self.draw_snake()
            self.draw_food()
            self.draw_obstacles()
            self.root.after(DELAY, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()