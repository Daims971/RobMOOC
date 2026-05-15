from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x    = x.flatten()
    return array([[5*cos(x[2])],[5*sin(x[2])],[u]])


def control(x):
    x = x.flatten()
    alpha = arctan2(x[1], x[0])
    theta = x[2]
    phi = pi - alpha + theta
    if cos(phi) <= 1/sqrt(2):
        u = 1
    else:
        u=-sin(phi)
    return u

theta = linspace(0, 2*pi, 100)
x    = array([[15],[20],[1]])
x    = array([[15],[20],[10]])
x    = array([[-15],[-20],[10]])
x    = array([[50],[20],[pi/4]])
# x    = array([[500],[20],[pi/4]])
dt   = 0.1
# ax=init_figure(-300,300,-300,300)
ax=init_figure(-30,30,-30,30)
for t in arange(0,20,dt):
    clear(ax)
    # draw_disk(ax,array([[0],[0]]).flatten(),10,"cyan")
    # draw_disk(ax,[0, 0],10,"cyan")
    ax.fill(10*cos(theta), 10*sin(theta), color='cyan', alpha=0.7)
    u = control(x)
    draw_tank(x,'red')
    x = x+dt*f(x,u)            

