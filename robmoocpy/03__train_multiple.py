from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    xr,yr,θr,vr=x.flatten()
    u1,u2=u.flatten()
    return (array([[vr*cos(θr)],[vr*sin(θr)],[u1],[u2]]))



ax=init_figure(-30,30,-30,30)


omega=0.1
Lx=15
Ly=7
l = 10 # distance entre robots


def control(x,w,dw,ddw):
    xr,yr,θr,vr=x.flatten()

    # X = array([[xr],[yr]])

    A = array([[ -vr*sin(θr),  cos(θr)],
               [  vr*cos(θr),  sin(θr)]])

    u = np.linalg.inv(A).dot((w-array([[xr],[yr]]))+2*(dw-array([[vr*cos(θr)],[vr*sin(θr)]]))+ddw)

    return u


def target_w(t):
    w = array([[Lx*sin(omega*t)],[Ly*cos(omega*t)]]) # ellipse à suivre (column vectors)
    dw = array([[Lx*omega*cos(omega*t)],[-Ly*omega*sin(omega*t)]]) # dérivée de w
    ddw = array([[Lx*omega**2*sin(omega*t)],[-Ly*omega**2*cos(omega*t)]]) # dérivée de dw
    return w, dw, ddw

dt = 0.1
x = array([[0],[1],[pi/3],[1]])
u = array([[1],[1]])
ub = array([[1],[1]])

xb = array([[-5],[8],[pi/4],[1]]) # position initiale du 2ème robot
xc = array([[-10],[6],[pi/2],[1]]) # position initiale du 3ème robot

for t in arange(0,30,dt) :

    w, dw, ddw = target_w(t)
    wb = array([[x[0,0]],[x[1,0]]]) - l*array([[cos(x[2,0])],[sin(x[2,0])]]) # position à suivre du 2ème robot
    wc = array([[xb[0,0]],[xb[1,0]]]) - l*array([[cos(xb[2,0])],[sin(xb[2,0])]]) # position à suivre du 3ème robot

    u = control(x,w,dw,ddw)
    x = x+dt*f(x,u)

    ub = control(xb,wb,dw,ddw)
    xb = xb+dt*f(xb,ub)

    uc = control(xc,wc,dw,ddw)
    xc = xc+dt*f(xc,uc)

    clear(ax)
    draw_ellipse0(ax, [0,0], array([[Lx**2, 0],[0, Ly**2]]), 1, 'red')

    draw_tank(x,'blue')  	
    draw_tank(xb, 'green')
    draw_tank(xc, 'cyan')

    plot(w[0,0], w[1,0], 'ro', markersize=10)
    plot(wb[0,0], wb[1,0], 'bo', markersize=10)
    plot(wc[0,0], wc[1,0], 'go', markersize=10)
    # pause(0.01)


    

pause(1)