from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
from numpy import *


def f(x,u):
    x,u=x.flatten(),u.flatten()
    xdot = array([[x[3]*cos(x[2])],[x[3]*sin(x[2])],[u[0]],[u[1]]])
    return(xdot)

def control(x,w,dw,ddw):
    x = x.flatten()
    y = array([[x[0]],[x[1]]])
    dy = array([[x[3]*cos(x[2])], [x[3]*sin(x[2])]])
    
    A = array([[-x[3]*sin(x[2]), cos(x[2])], [x[3]*cos(x[2]), sin(x[2])]])
    v = (w-y) + 2*(dw-dy) + ddw
    u = np.linalg.inv(A).dot(v)
    return u    
    

ax=init_figure(-50,50,-50,50)
m   = 20
X   = 10*randn(4,m)
a,dt = 0.1,0.1

for t in arange(0,20,dt):
    clear(ax)
    for i in range(m):        
        c = array([[cos(a*t+2*i*pi/m)],[sin(a*t+2*i*pi/m)]])
        dc = array([[-a*sin(a*t+2*i*pi/m)],[a*cos(a*t+2*i*pi/m)]]) 
        ddc = array([[-a**2*cos(a*t+2*i*pi/m)],[-a**2*sin(a*t+2*i*pi/m)]]) 

        El = array([[20+15*sin(a*t),0],[0,20]])
        dEl = array([[15*a*cos(a*t),0],[0,0]])
        ddEl = array([[-15*a**2*sin(a*t),0],[0,0]])

        R= array([[cos(a*t),-sin(a*t)],[sin(a*t),cos(a*t)]])
        dR = array([[-a*sin(a*t),-a*cos(a*t)],[a*cos(a*t),-a*sin(a*t)]])
        # ddR = array([[a**2*cos(a*t),a**2*sin(a*t)],[-a**2*sin(a*t),a**2*cos(a*t)]])
        ddR = -(a**2)*R

        w = R.dot(El).dot(c)
        dw = dR.dot(El).dot(c) + R.dot(dEl).dot(c) + R.dot(El).dot(dc)
        ddw = ddR.dot(El).dot(c) + R.dot(ddEl).dot(c) + R.dot(El).dot(ddc)  + 2*dR.dot(dEl).dot(c) + 2*dR.dot(El).dot(dc) + 2*R.dot(dEl).dot(dc) 
        
        x=X[:,i].reshape(4,1)
        u       = control(x,w,dw,ddw)
        x=X[:,i].reshape(4,1)
        draw_tank(x,'b',0.1)
        x=x+f(x,u)*dt        
        X[:,i]  = x.flatten()
        plot([w[0][0]],[w[1][0]],'r+')


