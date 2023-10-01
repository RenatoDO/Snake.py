from tkinter import *
import random
from PIL import ImageTk
from PIL import Image
from pygame import mixer

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 150 #Less is faster
SPACE_SIZE = 50 #25, 35
BODY_PARTS = 3
SNAKE_COLOR = "blue"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collisions(snake):
        game_over(snake)
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over(snake):
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER\n", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',35), text="\nYour Score is:{}".format(score), fill="red", tag="score")

def start():
    canvas.delete("gameover")
    canvas.delete("score")
    snake = Snake()
    food = Food()
    next_turn(snake, food)
    
def music():
    window.protocol('WM_DELETE_WINDOW', music_on_closing)
    mixer.init()
    mixer.music.load('Temple of Endless Sands.mp3')
    mixer.music.set_volume(0.1)
    mixer.music.play()

def music_on_closing():
    mixer.music.stop()    
    window.destroy()
    
def rules():
    Wrules = Tk()
    Wrules.title("Instructions")
    Wrules.iconbitmap('Snake.ico')
    Wrules.geometry("250x200")
 
    label = Label(Wrules, text='To play press GameStart', font=('consolas', 10)).pack(pady=10)
    label2 = Label(Wrules, text='W or Up arrow to move up', font=('consolas', 10)).pack()
    label3 = Label(Wrules, text='S or Down arrow to move down', font=('consolas', 10)).pack()
    label4 = Label(Wrules, text='A or Left arrow to move left', font=('consolas', 10)).pack()
    label5 = Label(Wrules, text='D or Right arrow to move right', font=('consolas', 10)).pack()
    label6 = Label(Wrules, text='Close game to restart', font=('consolas', 10)).pack(pady=10)


window = Tk()
window.title("Snake game")
window.iconbitmap('Snake.ico')

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry("1200x900")

music()

desertImage = Image.open('desert.jpg')
desertImage = desertImage.resize((1200,900), Image.ANTIALIAS)
resized = ImageTk.PhotoImage(desertImage)
background = Label(window, image = resized)
background.place(x=0, y=0)

score = 0
direction = 'down'


rules_button = Button(window, text="Rules", borderwidth=0)
rules_button.config(command=rules)
instructions = PhotoImage(file='instructions.png')
rules_button.config(image=instructions)
rules_button.pack(pady=10)

start_button = Button(window, text="Click to start the game", borderwidth=0)
start_button.config(command=start)
start_button.config(activebackground="black")
start_button.config(activeforeground="blue")
image = PhotoImage(file='start.png')
start_button.config(image=image)
start_button.pack(pady=10)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack(pady=10)

label = Label(window, text="Score:{}".format(score), font=('consolas', 30), bg='#cf9156')
label.pack(pady=10)

window.update()

window.bind('<a>', lambda event: change_direction('left'))
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))
window.bind('<Down>', lambda event: change_direction('down'))


window.mainloop()