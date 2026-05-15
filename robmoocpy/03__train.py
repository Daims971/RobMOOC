from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    xr,yr,θr,vr=x.flatten()
    u1,u2=u.flatten()
    return (array([[vr*cos(θr)],[vr*sin(θr)],[u1],[u2]]))



ax=init_figure(-30,30,-30,30)


omega=0.1
Lx=15
Ly=7


def control(x,w,dw,ddw):
    xr,yr,θr,vr=x.flatten()

    # X = array([[xr],[yr]])

    A = array([[ -vr*sin(θr),  cos(θr)],
               [  vr*cos(θr),  sin(θr)]])

    u = np.linalg.inv(A).dot((w-array([[xr],[yr]]))+2*(dw-array([[vr*cos(θr)],[vr*sin(θr)]]))+ddw)

    return u

dt = 0.1
x = array([[0],[1],[pi/3],[1]])
u = array([[1],[1]])

# draw_ellipse0(ax, array([[0],[0]]), array([[Lx**2, 0],[0, Ly**2]]), 1, 'red')
# pause(0.5)

# draw_ellipse0(ax, [0,0], array([[Lx**2, 0],[0, Ly**2]]), 1, 'red')
# pause(0.5)

for t in arange(0,20,dt) :
    clear(ax)
    draw_tank(x)  	

    w = array([[Lx*sin(omega*t)],[Ly*cos(omega*t)]]) # ellipse à suivre (column vectors)
    dw = array([[Lx*omega*cos(omega*t)],[-Ly*omega*sin(omega*t)]]) # dérivée de w
    ddw = array([[Lx*omega**2*sin(omega*t)],[-Ly*omega**2*cos(omega*t)]]) # dérivée de dw

    plot(w[0,0], w[1,0], 'ro', markersize=10)
    # draw_ellipse0(ax, array([[0],[0]]), array([[Lx**2, 0],[0, Ly**2]]), 1, 'red')
    # draw_ellipse0(ax, array([[0],[0]]), array([[Lx**2, 0],[0, Ly**2]]), 1, 'red')
    draw_ellipse0(ax, [0,0], array([[Lx**2, 0],[0, Ly**2]]), 1, 'cyan')


    # pause(0.01)

    u = control(x,w,dw,ddw)

    x = x+dt*f(x,u)
pause(1)