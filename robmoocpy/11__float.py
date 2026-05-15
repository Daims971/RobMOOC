from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_buoy(x):
    clear(ax) 
    x=x.flatten()
    plot([-10,10],[0,0],'black',linewidth=1)    
    d=x[0]
    P=array([[-ech,-1.8*ech],[ech,-1.8*ech],[ech,0],[-ech,0]])
    draw_polygon(ax,P,'blue')
    plot([   0,   L,  L,  L/2,   L/2,   L/2,  0,  0],
         [-L-d,-L-d, -d,   -d,   2-d,    -d, -d,-L-d],'black',linewidth=3)
    b=-x[2]     
    P=array([[0,-L-d+L],[L,-L-d+L],[L,-L/2-L*b/2-d],[0,-L/2-L*b/2-d]])
    draw_polygon(ax,P,'white')
    
    
def draw_buoy_2(x, y=0):
    # clear(ax) 
    x=x.flatten()
    plot([-10,10],[0,0],'black',linewidth=1)    
    d=x[0]
    P=array([[-ech,-1.8*ech],[ech,-1.8*ech],[ech,0],[-ech,0]])
    draw_polygon(ax,P,'blue')
    
    # Décalage de la forme de la bouée par y
    plot(array([   0,   L,  L,  L/2,   L/2,   L/2,  0,  0]) + y,
         [-L-d,-L-d, -d,   -d,   2-d,    -d, -d,-L-d],'black',linewidth=3)
    b=-x[2]     
    
    # Décalage du niveau d'eau à l'intérieur de la bouée par y
    P=array([[0,-L-d+L],[L,-L-d+L],[L,-L/2-L*b/2-d],[0,-L/2-L*b/2-d]])
    P[:,0] = P[:,0] + y
    draw_polygon(ax,P,'white')
    
def f(x,u):
    x=x.flatten()

    dv = g - ( g*max(0,L+min(x[0],0) + 0.5*cx*x[1]*np.abs(x[1]))) / ((1+beta*x[2])*L)

    xdot = array([[x[1]],[dv],[u]])

    return(xdot)

def control(x,w,dw,ddw):

    x=x.flatten()

    dv = g - ( g*max(0,L+min(x[0],0) + 0.5*cx*x[1]*np.abs(x[1]))) / ((1+beta*x[2])*L)

    s = w-x[0] + 2*(dw-x[1]) + ddw - dv
    u= sign(s)

    return u


def control_lin(x,w,dw,ddw,d3w):

    x=x.flatten()

    dv = g - ( g*max(0,L+min(x[0],0) + 0.5*cx*x[1]*np.abs(x[1]))) / ((1+beta*x[2])*L)

    d,v,b = x[0], x[1], x[2] 
    
    vabs_dot = sign(v)*dv

    A = -(cx/2)*(dv*abs(v)+v*vabs_dot)/((1+beta*b)*L)
    B = (g*L+0.5*cx*v*abs(v))*beta/(L*(1+beta*b)**2)

    vb = w-x[0] + 3*(dw-x[1]) + 3*(ddw - dv) + d3w 
    
    u = (vb - A)/B

    return u


ro0 = 1000
cx=1.05
beta=0.1
g=9.81

ech=5
x = array([[3],[0],[0]])
x2 = array([[5],[0],[0]])
L=1 #length of the cube
ax=init_figure(-ech,ech,-1.8*ech,0.2*ech)

dt=0.1
for t in arange(0,30,dt) :

    ## w=5m constant
    # w=5
    # dw=0
    # ddw=0
    # d3w=0

    ## w=3+sin(t/2) sinusoidal
    w = 3+sin(t/2)
    dw = (1/2)*cos(t/2)
    ddw = -(1/4)*sin(t/2)
    d3w = -(1/8)*cos(t/2)
    
    u=control(x,w,dw,ddw) # contrôle par sliding mode
    u2=control_lin(x2,w,dw,ddw,d3w) # contrôle par bouclage linéarisant

    x = x+dt*f(x,u)
    x2 = x2+dt*f(x2,u2)

    clear(ax) 

    draw_buoy_2(x) # contrôle par sliding mode
    draw_buoy_2(x2,2) # contrôle par bouclage linéarisant -> la dynamique de ce contrôle est plus lente

    plot([-ech,ech],[-w,-w],'red',linewidth=1)
    
pause(3)

