
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return (array([[x[3]*cos(x[2])],     [x[3]*sin(x[2])],  [u[0]],[u[1]]]))
    
    
    
def control(x,w,dw,ddw):
    # u=array([[0],[0]]) #TO DO
    x = x.flatten()
    y = array([[x[0]],[x[1]]])
    dy = array([[x[3]*cos(x[2])], [x[3]*sin(x[2])]])
    
    A = array([[-x[3]*sin(x[2]), cos(x[2])], [x[3]*cos(x[2]), sin(x[2])]])
    v = (w-y) + 2*(dw-dy) + ddw
    u = np.linalg.inv(A).dot(v)

    return u    


def slinding_control(x,w,dw,K):
    x = x.flatten()
    y = array([[x[0]],[x[1]]])
    dy = array([[x[3]*cos(x[2])], [x[3]*sin(x[2])]])
    
    A = array([[-x[3]*sin(x[2]), cos(x[2])], [x[3]*cos(x[2]), sin(x[2])]])
    s = (w-y) + (dw-dy)
    v=K*np.sign(s)
    u = np.linalg.inv(A).dot(v)

    return u


def target(t):
    w = array([[10*cos(t)],[10*sin(3*t)]])
    dw = array([[-10*sin(t)],[30*cos(3*t)]])
    ddw = array([[-10*cos(t)],[-90*sin(3*t)]])
    return w,dw,ddw


ax=init_figure(-30,30,-30,30)
dt = 0.02
xa = array([[10],[0],[1],[1]])
xb = array([[10],[0],[1],[1]])

ua = array([[1],[1]])
ub = array([[1],[1]])

L=10
s = arange(0,2*pi,0.01)
for t in arange(0,10,dt) :
    clear(ax)
    plot(L*cos(s), L*sin(3*s),color='magenta')
    draw_tank(xa,'green')  # robot with classic lienarization control 
    draw_tank(xb,'blue') # robot with sliding control
    w,dw,ddw = target(t)
    ua=control(xa,w,dw,ddw) # classic linearization control 
    ub=slinding_control(xb,w,dw,80) # sliding control

    plot(w[0,0], w[1,0], 'ro')  # Plot the target point with time
    xa = xa + dt*f(xa,ua)
    xb = xb + dt*f(xb,ub)


