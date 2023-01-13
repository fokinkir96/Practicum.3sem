from tkinter import *
from random import randint as r


class Dot():

    def __init__(self, root, c, window_size, dot_size, speed):

        self.window_size = window_size
        self.size = dot_size
        self.maxsize = 10
        self.x = r(window_size / 10, window_size / 10 * 9)
        self.y = r(window_size / 10, window_size / 10 * 9)
        self.speed = speed[0]
        self.changeSpeed = speed[1]
        self.changeWidth = speed[2]
        self.c = c
        self.root = root

        self.dot = c.create_oval(self.x, self.y, self.x - self.size, self.y - self.size, fill='white', width=self.size)
        self.move()

    def speedUp(self, event):
        self.changeSpeed += 1
        self.changeWidth += 0.1
        print(self.speed)
    def speedDown(self, event):
        self.changeSpeed -= 1
        self.changeWidth -= 0.1
        print(self.speed)

    def move(self):
        # print(c.coords(self.dot))
        x_coords = self.c.coords(self.dot)[0]
        y_coords = self.c.coords(self.dot)[1]

        if x_coords > self.window_size or y_coords > self.window_size or x_coords < 0 or y_coords < 0:
            self.c.delete(self.dot)
            del(self)
            return

        if self.size <= self.maxsize:
            self.size += self.changeWidth
            self.c.coords(self.dot, x_coords, y_coords, x_coords + self.size, y_coords + self.size)

        x = (x_coords - self.window_size / 2) / 50
        y = (y_coords - self.window_size / 2) / 50


        self.c.move(self.dot, x, y)
        if self.speed > 1:
            self.speed -= self.changeSpeed

        self.root.after(self.speed, self.move)


class Window:

    def __init__(self):

        self.window_size = 600
        self.root = Tk()
        self.c = Canvas(self.root, width=self.window_size, height=self.window_size, bg="black")
        self.c.pack()
        self.speed = 50
        self.changeSpeed = 1
        self.changeWidth = 0.1
        self.dots = []

        self.dot_maxwidth = 10

        self.root.bind('<Up>', self.speedUp)
        self.root.bind('<Down>', self.speedDown)

        self.create_dots()

        self.root.mainloop()

    def create_dots(self):
        self.dots.append(Dot(self.root, self.c, self.window_size, 0.5, [self.speed, self.changeSpeed, self.changeWidth]))
        for i in self.dots:
            if len(self.c.coords(i.dot)) == 0:
                self.dots.remove(i)

        create_speed = 15

        self.root.after(create_speed, self.create_dots)

    def speedUp(self, event):
        self.speed = 20 if self.speed-5 < 20 else self.speed-5

        self.changeSpeed += 1
        self.changeWidth += 0.1
        print(self.speed)
    def speedDown(self, event):
        self.speed = 60 if self.speed+5 > 60 else self.speed+5
        self.changeSpeed = 1
        self.changeWidth = 0.2 if self.changeWidth-0.1 < 0.2 else self.changeWidth
        print(self.speed)

Window()