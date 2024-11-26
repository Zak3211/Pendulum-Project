import tkinter as tk
import math

#constants
g = -9.81
m1 = 1
m2 = 1
L1 = 100
L2 = 100

#angles defining the system
th1 = 100
th2 = 50

#w1 = th1'. w2 = th2'
w1 = 5
w2 = 5

#o1 = w1'. o2 = w2'
o1 = 5
o2 = 5

dt = 0.001 

#define 2 differential equations to describe the system. x' = dx/dt

def fun3(th1, th2, w2):
    #o1 = w1'
    r = -g*(2*m1 + m2)*math.sin(th1)
    r -= m2*g*math.sin(th1 - 2*th2)
    r -= 2*m2*math.sin(th1 - th2)*((w2**2) * L2 + (w1**2)*L1*math.cos(th1 - th2))
    r /= L1*(2*m1 + m2 - m2*math.cos(2*th1 - 2*th2))
    return r

def fun4(th1, th2, w1, w2):
    #o2 = w2'
    r = 2*math.sin(th1 - th2)*((w1**2)*L1* (m1 + m2))
    r += g*(m1 + m2)*math.cos(th1)
    r += (w2**2)*L2*m2*math.cos(th1 - th2)
    r /= L2*(2*m1 + m2 - m2*math.cos(2*th1 - 2*th2))
    return r

def normalize(x):
    #normalizes a value between -2pi and 2pi
    if x < 0:
        return -x%(2*math.pi)
    else:
        return x%(2*math.pi)
    
def RK(th1, th2, w1, w2, o1, o2, n):
    #returns a single iteration of the Runge-Kutta Algorithm
    if n == 1:
        r = w1 + dt*o1
    elif n == 2:
        r =  w2 + dt*o2
    elif n == 3:
        k1 = fun3(th1, th2, w2)
        k2 = fun3(th1+dt*k1/2, th2+dt*k1/2 , w2+dt*k1/2)
        k3 = fun3(th1+dt*k2/2, th2+dt*k2/2, w2+dt*k2/2)
        k4 = fun3(th1+dt*k3, th2+dt*k3, w2+dt*k3)
        r =  o1 + dt/6*(k1+2*k2+2*k3+k4)
    elif n == 4:
        k1 = fun4(th1, th2, w1,  w2)
        k2 = fun4(th1+dt*k1/2, th2+dt*k1/2 ,w1+dt*k1/2 ,w2+dt*k1/2)
        k3 = fun4(th1+dt*k2/2, th2+dt*k2/2, w1+dt*k2/2, w2+dt*k2/2)
        k4 = fun4(th1+dt*k3, th2+dt*k3,w1+dt*k3, w2+dt*k3)
        r =  o2 + dt/6*(k1+2*k2+2*k3+k4)
    return normalize(r)


window = tk.Tk()
canvas = tk.Canvas(window, bg = 'black', highlightthickness= 0)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.attributes("-fullscreen", True)
canvas.config(width = screen_width, height = screen_height)

canvas.pack()

x1 = screen_width/2 + L1*math.sin(th1)
y1 = screen_height/2 -L1*math.cos(th1)
p1 = canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill='white')

x2 =  x1 + L2*math.sin(th2)
y2 = y1 + L2*math.cos(th2)
p2 = canvas.create_oval(x2 - 10, y2 - 10, x2 + 10, y2 + 10,fill = 'white')

canvas.create_oval(screen_width/2 - 5, screen_height/2 - 5, 
                   screen_width/2 + 5, screen_height/2 + 5,fill = 'red')

def update(th1, th2, w1, w2, o1, o2):
    th1 %= 2*math.pi
    th2 %= 2*math.pi

    th1 = th1 + dt*w1
    th2 = th2 + dt*w2

    new_w1 = RK(th1, th2, w1, w2, o1, o2, 1)
    new_w2 = RK(th1, th2, w1, w2, o1, o2, 2)
    new_o1 = RK(th1, th2, w1, w2, o1, o2, 3)
    new_o2 = RK(th1, th2, w1, w2, o1, o2, 4)

    w1, w2, o1, o2 = new_w1, new_w2, new_o1, new_o2

    x1 = screen_width/2 + L1*math.sin(th1)
    y1 = screen_height/2 -L1*math.cos(th1)

    x2 =  x1 + L2*math.sin(th2)
    y2 = y1 + L2*math.cos(th2)

    #print(f"{th1}, {th2}, {w1}, {o1}, {o2}")
    canvas.coords(p1, [x1 - 10, y1 - 10, x1 + 10, y1 + 10])
    canvas.coords(p2, [x2 - 10, y2 - 10, x2 + 10, y2 + 10])

    canvas.after(2, lambda: update(th1, th2, w1, w2, o1, o2))

update(th1, th2, w1, w2, o1, o2)
window.mainloop()

