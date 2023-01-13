import random
from tkinter import *

#Константы
width = 1200
height = 800
space = 25 #размер клетки
snake_length = 3
speed = 100
color = 'grey'
color_head = 'yellow'
color_body = 'white'
food_color = 'red'
#
class Snake:
    def __init__(self):
        self.snake_length = snake_length
        self.coord = [[0, 0]] * 3
        self.squares = []

        for x, y in self.coord:
            square = c.create_rectangle(x, y, x+space, y+space, fill=color_body)
            self.squares.append(square)

class Food:
    def __init__(self):
        # 1200/25 = 48
        x = random.randint(0, (width//space)-1)*space
        # 800/25 = 32
        y = random.randint(0, (height//space)-1)*space
        self.coord = [x, y]
        c.create_rectangle(x, y, x + space, y + space, fill=food_color)

def move(snake, food):
    for x, y in snake.coord:
        square = c.create_rectangle(x, y, x+space, y+space, fill=color_body, outline=color_body)
    x, y = snake.coord[0]

    if direction == 'down':
        y += space
    elif direction == 'up':
        y -= space
    elif direction == 'left':
        x -= space
    elif direction == 'right':
        x += space
    snake.coord.insert(0, (x, y))
    square = c.create_rectangle(x, y, x+space, y+space, fill=color_head, outline=color_head)
    snake.squares.insert(0, square)

    if x == food.coord[0] and y == food.coord[1]:
        global score
        global speed
        score += 1
        speed -= 2
        label.config(text=f'Счет: {score}')
        c.delete('food')
        food = Food()
    else:
        x, y = snake.coord[-1]
        square = c.create_rectangle(x, y, x+space, y+space, fill=color, outline=color)
        del snake.coord[-1]
        c.delete(snake.squares[-1])
        del snake.squares[-1]
    if collision(snake):
        game_over()
    else:
        root.after(speed, move, snake, food)

def change_direction(new_dir):
    global direction

    if new_dir == 'down':
        if direction != 'up':
            direction = new_dir
    if new_dir == 'up':
        if direction != 'down':
            direction = new_dir
    if new_dir == 'left':
        if direction != 'right':
            direction = new_dir
    if new_dir == 'right':
        if direction != 'left':
            direction = new_dir

def collision(snake):
    x, y = snake.coord[0]

    if x < 0 or x >= width:
        return True
    elif y < 0 or y >= height:
        return True
    for snake_length in snake.coord[1:]:
        if x == snake_length[0] and y == snake_length[1]:
            return True

def game_over():
    c.delete(ALL)
    c.create_text(width/2, height/2, font=('Arial', 50), text='Game over', fill='red')

#
root = Tk()
root.title('Змейка')
root.resizable(width=False, height=False)
root.bind('<Down>', lambda event: change_direction('down'))
root.bind('<Up>', lambda event: change_direction('up'))
root.bind('<Left>', lambda event: change_direction('left'))
root.bind('<Right>', lambda event: change_direction('right'))


score = 0
direction = 'down'

label = Label(root, text=f'Счет: {score}', font=('Arial',25))
label.pack()

c = Canvas(root, width=width, height=height, bg=color)
c.pack()

snake = Snake()
food = Food()
move(snake, food)

root.mainloop()
