from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x = x.flatten()
    θ = x[2]
    return array([[cos(θ)],[sin(θ)],[u]])

def control(x):
    x = x.flatten()
    u=2*arctan(tan((thetabar-x[2])/2))/pi
    return u
    

def control_left(x):
    x = x.flatten()
    u=(2*arctan(tan((thetabar-x[2] + pi)/2)) + pi)/(2*pi)
    return u


def control_right(x):
    x = x.flatten()
    u=(2*arctan(tan((thetabar-x[2] + pi)/2)) - pi)/(2*pi)
    return u
    
x   = array([[0],[0],[0.1]])
xl = array([[-1],[0],[0.1]]) # robot who only turn left
xr = array([[1],[0],[0.1]]) # robot who only turn right

dt  = 0.1
ax=init_figure(-10,10,-10,10)

for t in arange(0,10,dt):
    clear(ax)
    thetabar =  1

    u = control(x)
    ul = control_left(xl)
    ur = control_right(xr) #+ 0.5*randn() # add some noise to the right robot

    x = x + dt*f(x,u)    
    xl = xl + dt*f(xl,ul)
    xr = xr + dt*f(xr,ur)

    draw_tank(x,'red',0.3) 
    draw_tank(xl,'blue',0.3)
    draw_tank(xr,'green',0.3)
    
