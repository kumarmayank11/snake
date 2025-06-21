import tkinter as tk
import random

# Game config
WIDTH = 600
HEIGHT = 400
SPEED = 60  # lower = faster
PIXEL_STEP = 10
FOOD_SIZE = 10
SNAKE_SIZE = 10
BG_COLOR = "#1e1e1e"
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF4040"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Realistic Snake Game")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, bg=BG_COLOR, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.score = 0
        self.direction = "Right"
        self.running = True

        self.snake = [[100, 100]]
        self.snake_rects = []
        self.food = None

        self.score_label = tk.Label(root, text="Score: 0", font=("Consolas", 16), bg=BG_COLOR, fg="white")
        self.score_label.pack()

        self.spawn_food()
        self.root.bind("<KeyPress>", self.change_direction)
        self.update()

    def spawn_food(self):
        while True:
            x = random.randint(0, (WIDTH - FOOD_SIZE) // PIXEL_STEP) * PIXEL_STEP
            y = random.randint(0, (HEIGHT - FOOD_SIZE) // PIXEL_STEP) * PIXEL_STEP
            if [x, y] not in self.snake:
                break
        self.food = [x, y]

    def change_direction(self, event):
        key = event.keysym
        opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if key in ["Left", "Right", "Up", "Down"]:
            if key != opposites.get(self.direction):
                self.direction = key

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            head_y -= PIXEL_STEP
        elif self.direction == "Down":
            head_y += PIXEL_STEP
        elif self.direction == "Left":
            head_x -= PIXEL_STEP
        elif self.direction == "Right":
            head_x += PIXEL_STEP

        new_head = [head_x, head_y]

        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.spawn_food()
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        # Wall collision
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT
        ):
            return True
        # Self collision
        if head in self.snake[1:]:
            return True
        return False

    def draw_snake(self):
        for segment in self.snake_rects:
            self.canvas.delete(segment)
        self.snake_rects = []

        for index, (x, y) in enumerate(self.snake):
            fill = SNAKE_COLOR
            rect = self.canvas.create_rectangle(
                x, y, x + SNAKE_SIZE, y + SNAKE_SIZE,
                fill=fill, outline=""
            )
            self.snake_rects.append(rect)

            if index == 0:
                # Draw eyes for the head
                eye_size = 2
                offset = 2
                if self.direction in ("Left", "Right"):
                    eyey = y + offset
                    eyex1 = x + (2 if self.direction == "Right" else 6)
                    eyex2 = x + (6 if self.direction == "Right" else 2)
                    self.canvas.create_oval(eyex1, eyey, eyex1 + eye_size, eyey + eye_size, fill="black")
                    self.canvas.create_oval(eyex2, eyey + 5, eyex2 + eye_size, eyey + 5 + eye_size, fill="black")
                else:
                    eyex = x + offset
                    eyey1 = y + (2 if self.direction == "Down" else 6)
                    eyey2 = y + (6 if self.direction == "Down" else 2)
                    self.canvas.create_oval(eyex, eyey1, eyex + eye_size, eyey1 + eye_size, fill="black")
                    self.canvas.create_oval(eyex + 5, eyey2, eyex + 5 + eye_size, eyey2 + eye_size, fill="black")

    def draw_food(self):
        x, y = self.food
        self.canvas.delete("food")
        self.canvas.create_oval(x, y, x + FOOD_SIZE, y + FOOD_SIZE, fill=FOOD_COLOR, tag="food")

    def game_over(self):
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2,
            text="GAME OVER", fill="red", font=("Arial", 30, "bold")
        )
        self.running = False

    def update(self):
        if self.running:
            self.move_snake()
            if self.check_collision():
                self.game_over()
            else:
                self.canvas.delete("all")
                self.draw_food()
                self.draw_snake()
                self.root.after(SPEED, self.update)

# Run game
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
