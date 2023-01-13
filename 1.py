from tkinter import *
from math import cos, sin, radians

size = 600
root = Tk()
c = Canvas(root, width=size, height=size, bg="white")
c.pack()

radius = 200
coords = (size/2-radius, size/2+radius)
oval = c.create_oval(coords[0], coords[0], coords[1], coords[1], fill='green')

dot = c.create_oval(size/2, coords[0]-30, size/2-3, coords[0]-27, fill='black')
speed = 10
direction = 1  # 1 / -1

def move(angle):
    x = direction * 4 * cos(radians(angle))
    y = 4 * sin(radians(angle))
    angle += 1
    c.move(dot, x, y)
    root.after(speed, move, angle)

move(0)

root.mainloop()
