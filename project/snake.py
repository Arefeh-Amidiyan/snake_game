import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.resizable(False, False)

        # Constants
        self.GAME_WIDTH = 600
        self.GAME_HEIGHT = 400
        self.SPEED = 150  # Slower initial speed for better playability
        self.SPACE_SIZE = 20
        self.BODY_SIZE = 3
        self.SNAKE_COLOR = "#32CD32"  # Lime green for better visibility
        self.FOOD_COLOR = "#FF4444"   # Coral red for food
        self.BACKGROUND_COLOR = "#1a1a1a"  # Dark gray background

        # Game variables
        self.direction = 'right'
        self.score = 0
        self.game_started = False
        self.game_over_state = False
        
        # Create score label
        self.label = tk.Label(
            self.master, 
            text=f"Score: {self.score}", 
            font=('Arial', 16),
            bg='black',
            fg='white'
        )
        self.label.pack(pady=10)

        # Create canvas
        self.canvas = tk.Canvas(
            self.master, 
            width=self.GAME_WIDTH,
            height=self.GAME_HEIGHT,
            bg=self.BACKGROUND_COLOR
        )
        self.canvas.pack(padx=10, pady=10)

        # Show welcome message
        self.show_welcome_message()

        # Initialize game objects
        self.snake = []
        self.food = None

        # Bind keys
        self.master.bind('<Left>', lambda e: self.change_direction('left'))
        self.master.bind('<Right>', lambda e: self.change_direction('right'))
        self.master.bind('<Up>', lambda e: self.change_direction('up'))
        self.master.bind('<Down>', lambda e: self.change_direction('down'))
        self.master.bind('<space>', lambda e: self.start_game())
        self.master.bind('<Return>', lambda e: self.start_game())

    def show_welcome_message(self):
        self.canvas.create_text(
            self.GAME_WIDTH/2,
            self.GAME_HEIGHT/2 - 30,
            font=('Arial', 30),
            text="Welcome to Snake Game!",
            fill="white"
        )
        self.canvas.create_text(
            self.GAME_WIDTH/2,
            self.GAME_HEIGHT/2 + 30,
            font=('Arial', 20),
            text="Press SPACE or ENTER to start\nUse arrow keys to move",
            fill="white",
            justify=tk.CENTER
        )

    def start_game(self):
        if not self.game_started or self.game_over_state:
            self.game_started = True
            self.game_over_state = False
            self.score = 0
            self.direction = 'right'
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("all")
            self.snake.clear()
            self.create_snake()
            self.create_food()
            self.next_turn()

    def create_snake(self):
        starting_x = self.GAME_WIDTH // 4
        starting_y = self.GAME_HEIGHT // 2

        for i in range(self.BODY_SIZE):
            x = starting_x - i * self.SPACE_SIZE
            square = self.canvas.create_rectangle(
                x, starting_y,
                x + self.SPACE_SIZE, starting_y + self.SPACE_SIZE,
                fill=self.SNAKE_COLOR,
                outline="#228B22",  # Darker green outline
                tags="snake"
            )
            self.snake.append(square)

    def create_food(self):
        while True:
            x = random.randint(0, (self.GAME_WIDTH - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
            y = random.randint(0, (self.GAME_HEIGHT - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
            
            # Check if the position overlaps with the snake
            overlap = False
            for segment in self.snake:
                seg_coords = self.canvas.coords(segment)
                if x == seg_coords[0] and y == seg_coords[1]:
                    overlap = True
                    break
            
            if not overlap:
                break

        self.food = self.canvas.create_oval(
            x, y,
            x + self.SPACE_SIZE, y + self.SPACE_SIZE,
            fill=self.FOOD_COLOR,
            outline="#CC3333",  # Darker red outline
            tags="food"
        )

    def next_turn(self):
        if not self.game_started:
            return

        head = self.snake[0]
        head_coords = self.canvas.coords(head)

        if self.direction == 'left':
            new_x = head_coords[0] - self.SPACE_SIZE
            new_y = head_coords[1]
        elif self.direction == 'right':
            new_x = head_coords[0] + self.SPACE_SIZE
            new_y = head_coords[1]
        elif self.direction == 'up':
            new_x = head_coords[0]
            new_y = head_coords[1] - self.SPACE_SIZE
        elif self.direction == 'down':
            new_x = head_coords[0]
            new_y = head_coords[1] + self.SPACE_SIZE

        new_head = self.canvas.create_rectangle(
            new_x, new_y,
            new_x + self.SPACE_SIZE, new_y + self.SPACE_SIZE,
            fill=self.SNAKE_COLOR,
            outline="#228B22"
        )
        self.snake.insert(0, new_head)

        if self.check_food_collision():
            self.score += 10
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.create_food()
            # Increase speed every 50 points
            if self.score % 50 == 0:
                self.SPEED = max(50, self.SPEED - 10)
        else:
            self.canvas.delete(self.snake[-1])
            self.snake.pop()

        if self.check_game_over():
            self.game_over()
            return

        self.master.after(self.SPEED, self.next_turn)

    def check_food_collision(self):
        head_coords = self.canvas.coords(self.snake[0])
        food_coords = self.canvas.coords(self.food)
        return head_coords == food_coords

    def check_game_over(self):
        head_coords = self.canvas.coords(self.snake[0])
        
        # Check wall collision
        if (head_coords[0] < 0 or 
            head_coords[0] >= self.GAME_WIDTH or
            head_coords[1] < 0 or 
            head_coords[1] >= self.GAME_HEIGHT):
            return True

        # Check self collision
        for segment in self.snake[1:]:
            if head_coords == self.canvas.coords(segment):
                return True
        
        return False

    def game_over(self):
        self.game_over_state = True
        self.game_started = False
        self.canvas.create_rectangle(
            self.GAME_WIDTH/4,
            self.GAME_HEIGHT/3,
            self.GAME_WIDTH*3/4,
            self.GAME_HEIGHT*2/3,
            fill="black",
            outline="white"
        )
        self.canvas.create_text(
            self.GAME_WIDTH/2,
            self.GAME_HEIGHT/2 - 30,
            font=('Arial', 30),
            text=f"Game Over!",
            fill="white"
        )
        self.canvas.create_text(
            self.GAME_WIDTH/2,
            self.GAME_HEIGHT/2 + 10,
            font=('Arial', 20),
            text=f"Final Score: {self.score}\nPress SPACE or ENTER to play again",
            fill="white",
            justify=tk.CENTER
        )

    def change_direction(self, new_direction):
        if not self.game_started:
            return
            
        if (new_direction == 'left' and self.direction != 'right' or
            new_direction == 'right' and self.direction != 'left' or
            new_direction == 'up' and self.direction != 'down' or
            new_direction == 'down' and self.direction != 'up'):
            self.direction = new_direction

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()