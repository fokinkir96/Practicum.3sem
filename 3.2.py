from tkinter import *

class Ball:

    def __init__(self, c, x1, y1, x2, y2, radius, mass, color='white'):

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.radius = radius
        self.c = c

        self.speed = 4
        self.resistance = 0.015 * self.speed * radius
        self.mass = mass
        self.acceleration = (self.resistance / mass) * 50
        self.ball = c.create_oval(self.x1 - self.radius, self.y1 - self.radius, self.x2 +
                                  self.radius, self.y2 + self.radius, fill=color, outline='white', width=2)

    def move_ball(self):
        if c.coords(self.ball)[3] < height//2:
            c.move(self.ball, 0, self.speed)
            c.after(1000//60, self.move_ball)
        elif height//2 <= c.coords(self.ball)[3] + self.resistance < height:
            c.move(self.ball, 0, self.resistance)
            c.after(1000//60, self.move_ball)
        else:
            c.move(self.ball, 0, height + 1 - c.coords(self.ball)[3])
            c.after(1000 // 60, self.iter_1)

    def iter_1(self):
        if c.coords(self.ball)[3] - self.acceleration >= height - self.mass * 0.2:
            c.move(self.ball, 0, -self.acceleration)
            c.after(1000 // 60, self.iter_1)
        else:
            c.after(1000 // 60, self.iter_2)

    def iter_2(self):
        if c.coords(self.ball)[3] + self.acceleration < height:
            c.move(self.ball, 0, self.acceleration)
            c.after(1000 // 60, self.iter_2)
        else:
            c.move(self.ball, 0, height + 1 - c.coords(self.ball)[3])
            c.after(1000 // 60, self.iter_3)

    def iter_3(self):
        if c.coords(self.ball)[3] - self.acceleration >= height - self.mass * 0.1:
            c.move(self.ball, 0, -self.acceleration)
            c.after(1000 // 60, self.iter_3)
        else:
            c.after(1000 // 60, self.iter_stop)

    def iter_stop(self):
        if c.coords(self.ball)[3] + self.acceleration < height:
            c.move(self.ball, 0, self.acceleration)
            c.after(1000 // 60, self.iter_stop)

        else:
            c.move(self.ball, 0, height - 2 - c.coords(self.ball)[3])
root = Tk()
root.title("Силы Сопротивления")
root.maxsize(600, 600)
width = 600
height = 600
c = Canvas(root, width=width, height=height, bg="black")
c.pack()
c.create_rectangle(0, height//2, width, height, fill='grey')

#Шары

r1 = 40
mass1 = 60
ball1 = Ball(c, 100, 20, 100,
             20, r1, mass1, color="#a0a0a0")
ball1.move_ball()

r2 = 25
mass2 = 50
ball2 = Ball(c, 200, 20, 200,
             20, r2, mass2, color="#a0a0a0")
ball2.move_ball()

r3 = 20
mass3 = 40
ball3 = Ball(c, 300, 20, 300,
             20, r3, mass3, color="#a0a0a0")
ball3.move_ball()

r4 = 36
mass4 = 75
ball4 = Ball(c, 400, 20, 400,
             20, r4, mass4, color="#a0a0a0")
ball4.move_ball()

r5 = 15
mass5 = 10
ball5 = Ball(c, 510, 20, 510,
             20, r5, mass5, color="#a0a0a0")
ball5.move_ball()


r6 = 25
mass6 = 30
ball6 = Ball(c, 570, 20, 570,
             20, r6, mass6, color='#a0a0a0')
ball6.move_ball()


root.mainloop()