import math
import tkinter as tk

#tkinter configuration
window = tk.Tk()
canvas = tk.Canvas(window, bg = 'black', highlightthickness= 0)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.attributes("-fullscreen", True)
canvas.config(width = screen_width, height = screen_height)

canvas.pack()

class Pendulum:
    def __init__(self):
        self.canvas = canvas
        self.g = -9.81
        self.L = 100
        self.m = 5
        self.dt = 0.025

        self.theta = math.pi/2
        self.theta_ = 0
        self.theta__ = 0

        self.bx = screen_width/2
        self.bx_ = 0
        self.bx__ = 0

        self.by = screen_height/2 - 100

        self.x, self.y = self.getX(), self.getY()
        self.line = self.canvas.create_line(self.bx, self.by, self.x, self.y, fill = 'white', width = 2)
        self.point = self.canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill='white')

    #functions of motion
    def getTheta__(self):
        return -(1/self.L)*(self.g*math.sin(self.theta) - self.bx__*math.cos(self.theta))
    def getX(self):
        return self.bx - self.L*math.sin(self.theta)
    def getY(self):
        return self.by - self.L*math.cos(self.theta)

    #Base movement
    def move_left(self,event):
        self.bx__ = -50
    def move_right(self,event):
        self.bx__ = 50

    #main loop
    def update(self):
        self.theta__ = self.getTheta__()
        self.theta_ += self.theta__*self.dt
        self.theta += self.theta_*self.dt

        self.x = self.getX()
        self.y = self.getY()

        self.bx_ += self.bx__*self.dt
        self.bx += self.bx_*self.dt
    
        self.theta_ *= 0.999
        self.bx_ *= 0.9
        self.bx__ *= 0.99

        self.canvas.coords(self.line, [self.bx, self.by, self.x, self.y])
        self.canvas.coords(self.point, [self.x - 10, self.y - 10, self.x + 10, self.y + 10])
        self.canvas.after(2, lambda: self.update())

pendulum = Pendulum()
window.bind('<Left>', pendulum.move_left)
window.bind('<Right>', pendulum.move_right)
pendulum.update()
window.mainloop()