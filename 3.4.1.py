import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from random import randint as ri
import math

# TODO:
#       1. Тороидальное движение корабля
#       2. Дописать бинды для корабля
#       3. Столкновения корабля и астеройдов
#       4. Взрывы астеройдов
#       5. Окончание игры

class Polygon:

    def __init__(self):
        self.cfg = {
            'window_size_w': 800,
            'window_size_h': 600,
        }

        self.asteroids = []
        self.lifes = 3
        self.started = False

        self.init_cvs()


    def init_cvs(self):
        self.cfg['root'] = tk.Tk()
        self.cfg['c'] = tk.Canvas(self.cfg['root'], width=self.cfg['window_size_w'], height=self.cfg['window_size_h'])

        self.cfg['c'].pack()

        self.create_imgs()
        self.create_start()

        self.cfg['root'].mainloop()
    def create_imgs(self):
        self.imgs = {
            'bg': ImageTk.PhotoImage(file='img/nebula_blue.f2013.png'),
            'bg_mv': ImageTk.PhotoImage(file='img/debris2_blue.png'),
            'interface': ImageTk.PhotoImage(file='img/interface.png'),
            'asteroid': ImageTk.PhotoImage(file='img/asteroid_blue.png'),
        }

    def create_start(self):
        self.set_bg()
        self.set_bg_mv()
        self.lifes = 3
        self.set_interface()
        self.set_text()
        self.bind_mouse()

    def set_bg(self):
        self.cfg['c'].create_image(0, 0, image=self.imgs['bg'], anchor=tk.NW)
    def set_bg_mv(self):
        self.bg_mv = self.cfg['c'].create_image(0, 50, image=self.imgs['bg_mv'], anchor=tk.NW)
        self.bg_mv1 = self.cfg['c'].create_image(650, 50, image=self.imgs['bg_mv'], anchor=tk.NW)
        self.move_bg()
    def set_interface(self):
        self.interface = self.cfg['c'].create_image(400 - 200, 300 - 150, image=self.imgs['interface'], anchor=tk.NW)
    def set_text(self):
        self.cfg['c'].create_text(100, 30,
                                  text="Жизни: "+str(self.lifes),
                                  justify=CENTER, font="Verdana 14", fill='green', tag='lifes')
        self.cfg['c'].create_text(700, 30,
                                  text="Очки: 0",
                                  justify=CENTER, font="Verdana 14", fill='green', tag='score')

    def move_bg(self):
        self.cfg['c'].move(self.bg_mv, -1, 0)
        self.cfg['c'].move(self.bg_mv1, -1, 0)
        if self.cfg['c'].coords(self.bg_mv)[0] < -600:
            self.cfg['c'].coords(self.bg_mv, 640, 50)
        if self.cfg['c'].coords(self.bg_mv1)[0] < -600:
            self.cfg['c'].coords(self.bg_mv1, 640, 50)
        self.cfg['root'].after(10, self.move_bg)
    def bind_mouse(self):
        self.cfg['c'].bind('<Button-1>', self.start_game)
    def unbind_mouse(self):
        self.cfg['c'].unbind('<Button-1>')

    def start_game(self, e = False):
        if e.x >= 200 and e.x <= 600 and e.y >= 150 and e.y <= 450:
            self.started = True
            self.cfg['c'].delete(self.interface)
            self.unbind_mouse()
            self.ship = Ship(self.cfg)
            self.create_asteroids()
            self.move_asteroids()

    def create_asteroids(self):
        if self.started is False:
            return False
        x = ri(0, 800)
        y = ri(0, 800)
        ship_coords = self.ship.get_coords()
        if ship_coords[0]-100 < x < ship_coords[0]+190 and ship_coords[1]-100 < y < ship_coords[1]+190:
            x += 200
            y += 200
        self.asteroids.append(
            [self.cfg['c'].create_image(ri(0, 800), ri(0, 600), image=self.imgs['asteroid'], anchor=tk.NW, tag='asteroids'), ri(-3, 3), ri(-3, 3)])

        if len(self.asteroids) <= 6:
            self.cfg['root'].after(1000, self.create_asteroids)

    def move_asteroids(self):
        if self.started is False:
            return False
        for i in self.asteroids:
            x = self.cfg['c'].coords(i[0])[0]
            y = self.cfg['c'].coords(i[0])[1]
            ship_coords = self.ship.get_coords()
            shot_coords = self.cfg['c'].coords('shot')
            if len(shot_coords) > 0:
                if x < shot_coords[0] < x + 90 and y < shot_coords[1] < y + 90:
                    self.cfg['c'].delete(i[0])
                    self.cfg['c'].delete('shot')
                    self.asteroids.remove(i)
                    self.create_asteroids()
                    continue

            # if x < ship_coords[0] < x+90 and y < ship_coords[1] < y+90:
            #     print('столкновение')
            #     self.lifes -= 1
            #     self.restart()
            #     return False
            if ship_coords[0] < x < ship_coords[0]+80 and ship_coords[1] < y < ship_coords[1]+80:
                self.lifes -= 1
                self.restart()
                return False
            # or c.coords(i[0])[0]+45 < 0 or c.coords(i[0])[1]+45 > 600 or c.coords(i[0])[1]+45 < 0:
            if x + 45 > 800:
                self.cfg['c'].coords(i[0], 0 + 50, self.cfg['c'].coords(i[0])[1])
            if x + 45 < 0:
                self.cfg['c'].coords(i[0], 800 - 50, self.cfg['c'].coords(i[0])[1])
            if y + 45 > 600:
                self.cfg['c'].coords(i[0], self.cfg['c'].coords(i[0])[0], 0 + 50)
            if y + 45 < 0:
                self.cfg['c'].coords(i[0], self.cfg['c'].coords(i[0])[0], 600 - 50)
            self.cfg['c'].move(i[0], i[1], i[2])

        self.cfg['root'].after(70, self.move_asteroids)

    def restart(self):
        if self.lifes > 0:
            self.cfg['c'].delete('lifes')
            self.cfg['c'].create_text(100, 30,
                                      text="Жизни: "+str(self.lifes),
                                      justify=CENTER, font="Verdana 14", fill='green', tag='lifes')
            self.ship.moving = False
            self.delete_asteroids()
            self.delete_ship()

            self.ship = Ship(self.cfg)
            self.create_asteroids()
            self.move_asteroids()
        else:
            self.game_over()

    def delete_asteroids(self):
        self.cfg['c'].delete('asteroids')
        self.asteroids = []
    def delete_ship(self):
        self.cfg['c'].delete('ship')
        del(self.ship)
    def game_over(self):
        self.started = False
        self.unbind_keys()
        self.delete_asteroids()
        self.delete_ship()
        self.create_imgs()
        self.create_start()

    def unbind_keys(self):
        # bind clicks
        self.cfg['root'].unbind('<KeyPress-Up>')
        self.cfg['root'].unbind('<KeyRelease-Up>')
        self.cfg['root'].unbind('<KeyPress-Left>')
        self.cfg['root'].unbind('<KeyRelease-Left>')
        self.cfg['root'].unbind('<KeyPress-Right>')
        self.cfg['root'].unbind('<KeyRelease-Right>')
        self.cfg['root'].unbind('<KeyPress-space>')
        self.cfg['root'].unbind('<KeyRelease-space>')


class Ship:

    def __init__(self, cfg):
        self.cfg = cfg
        self.ship_img = Image.open('img/ship.png')
        self.fship_img = Image.open('img/fastship.png')
        # img = img.rotate(angle=160)
        self.ship_Pimg = ImageTk.PhotoImage(self.ship_img)

        self.moving = False
        self.turning = False
        self.angle = 0
        self.coords = [300,300]
        self.set_ship_img()
        self.bind_keys()

    def get_coords(self):
        return self.coords
    def set_ship_img(self):
        self.ship = self.cfg['c'].create_image(self.coords[0], self.coords[1], image=self.ship_Pimg, anchor=tk.NW, tag='ship')

    def bind_keys(self):
        # bind clicks
        self.cfg['root'].bind('<KeyPress-Up>', self.fast_ship)
        self.cfg['root'].bind('<KeyRelease-Up>', self.unfast_ship)
        self.cfg['root'].bind('<KeyPress-Left>', self.turn_ship)
        self.cfg['root'].bind('<KeyRelease-Left>', self.unturn_ship)
        self.cfg['root'].bind('<KeyPress-Right>', self.turn_ship)
        self.cfg['root'].bind('<KeyRelease-Right>', self.unturn_ship)
        self.cfg['root'].bind('<KeyPress-space>', self.shoot)
        self.cfg['root'].bind('<KeyRelease-space>', self.unshoot)

    def moving_ship(self):
        # while self.moving == True:
        #     self.move_strait()
        #     self.cfg['root'].update()
        if self.moving is False:
            return False
        elif self.moving is True:
            self.cfg['root'].after(1, self.move_strait)
        pass
    def move_strait(self):
        if self.moving is False:
            return False
        # print(self.cfg['c'].coords('asteroids'))
        if self.cfg['c'].coords('ship')[0] + 45 > 800:
            self.cfg['c'].coords('ship', 0 + 50, self.cfg['c'].coords('ship')[1])
        if self.cfg['c'].coords('ship')[0] + 45 < 0:
            self.cfg['c'].coords('ship', 800 - 50, self.cfg['c'].coords('ship')[1])
        if self.cfg['c'].coords('ship')[1] + 45 > 600:
            self.cfg['c'].coords('ship', self.cfg['c'].coords('ship')[0], 0 + 50)
        if self.cfg['c'].coords('ship')[1] + 45 < 0:
            self.cfg['c'].coords('ship', self.cfg['c'].coords('ship')[0], 600 - 50)

        # self.cfg['c'].move('ship', 5, 0)
        pos = self.cfg['c'].coords('ship')
        self.coords[0] = 5 * math.cos(math.radians(self.angle)) + pos[0]
        self.coords[1] = 5 * math.sin(math.radians(self.angle)) + pos[1]
        self.cfg['c'].coords('ship', self.coords[0], self.coords[1])

        if self.moving == True:
            self.cfg['root'].after(20, self.move_strait)
    def fast_ship(self, e):
        self.moving = True
        self.moving_ship()
        # self.move_strait()
        self.ship_Pimg = ImageTk.PhotoImage(self.fship_img)
        self.cfg['c'].itemconfig('ship', image=self.ship_Pimg)
        self.cfg['c'].update()
    def unfast_ship(self, e):
        self.ship_Pimg = ImageTk.PhotoImage(self.ship_img)
        self.cfg['c'].itemconfig('ship', image=self.ship_Pimg)
        self.moving = False
    def turn_ship(self, e):
        if e.keysym == 'Left':
            angle = -20
        else:
            angle = 20
        # angle %= 360
        self.angle += angle
        self.turning = True
        self.ship_img = self.ship_img.rotate(-angle)
        self.fship_img = self.fship_img.rotate(-angle)
        ship_img = self.ship_img
        if self.moving == True:
            ship_img = self.fship_img
        # ship_img = ship_img.rotate(angle)
        self.ship_Pimg = ImageTk.PhotoImage(ship_img)
        self.cfg['c'].itemconfig('ship', image=self.ship_Pimg)
        # self.cfg['c'].delete('ship')
        # self.cfg['c'].create_image(300, 300, image=self.ship_Pimg, anchor=tk.NW, tag='ship')x
        if self.cfg['c'].coords('ship')[0] + 45 > 800:
            self.cfg['c'].coords('ship', 0 + 50, self.cfg['c'].coords('ship')[1])
        if self.cfg['c'].coords('ship')[0] + 45 < 0:
            self.cfg['c'].coords('ship', 800 - 50, self.cfg['c'].coords('ship')[1])
        if self.cfg['c'].coords('ship')[1] + 45 > 600:
            self.cfg['c'].coords('ship', self.cfg['c'].coords('ship')[0], 0 + 50)
        if self.cfg['c'].coords('ship')[1] + 45 < 0:
            self.cfg['c'].coords('ship', self.cfg['c'].coords('ship')[0], 600 - 50)
        # print(self.cfg['c'].coords('ship'))

    def unturn_ship(self, e):
        pass
    def shoot(self, e):
        self.shot = Image.open('img/shot2.png')

        self.shot = ImageTk.PhotoImage(self.shot)
        self.cfg['c'].create_image((self.coords[0]+45), (self.coords[1]+45), image=self.shot, anchor=tk.NW, tag='shot')
        self.begin_shot_coords = [self.coords[0]+45, self.coords[1]+40]
        self.move_shot(self.begin_shot_coords)
    def move_shot(self, coords):
        x = 5 * math.cos(math.radians(self.angle)) + coords[0]
        y = 5 * math.sin(math.radians(self.angle)) + coords[1]
        if abs(x - self.begin_shot_coords[0]) > 200:
            self.cfg['c'].delete('shot')
            return False
        self.cfg['c'].coords('shot', x, y)
        self.cfg['c'].update()
        self.cfg['c'].after(10, self.move_shot, [x,y])
    def unshoot(self, e):
        pass

Polygon()