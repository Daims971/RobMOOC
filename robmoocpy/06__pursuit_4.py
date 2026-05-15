from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return (array([[u[0]*cos(x[2])], [u[0]*sin(x[2])],[u[1]]]))

def control(xa,xb,v,w, dw):
    # u=array([[0],[0]]) #TO DO
    xb = xb.flatten()
    xa = xa.flatten()
    R1 = array([[cos(xa[2]), sin(xa[2]), 0],[-sin(xa[2]), cos(xa[2]), 0],[0, 0, 1]])
    x = R1.dot(xb - xa)
    # x.flatten()
    A = array([[-1, x[1]],[0, -x[0]]])
    bx = array([[v[1]*cos(x[2])], [v[1]*sin(x[2])]])
    v_y = w-x + dw

    u = np.linalg.inv(A).dot(v_y - bx)

    return u    

ax=init_figure(-30,30,-30,30)
dt = 0.1

xa = array([[-10], [-10],[0]])
xb = array([[-5],[-5],[0]])

w = array([[10],[0]])
dw = array([[0],[0]])

for t in arange(0,15,dt) :
    clear(ax)
    v = array([[3],[sin(0.2*t)]])
    u=control(xa,xb,v,w,dw)
    draw_tank(xa,'blue')  	
    draw_tank(xb,'red')  	
    xa = xa + dt*f(xa,u)
    xb = xb + dt*f(xb,v)
#show()


    
