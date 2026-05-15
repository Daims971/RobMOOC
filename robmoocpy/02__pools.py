from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

import matplotlib

def draw_pools(x):
    def draw_polygon(ax,P,col):
        patches = []
        patches.append(Polygon(P,closed=True, edgecolor='black', facecolor='skyblue'))
        p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4, color=col)
        ax.add_collection(p)
    x=x.flatten()
    plot([0,0],[10,1],'black',linewidth=2)    
    plot([-7,23],[0,0],'black',linewidth=5)    
    plot([16,16],[1,10],'black',linewidth=2)    
    plot([4,4,6,6],[10,1,1,10],'black',linewidth=2)    
    plot([10,10,12,12],[10,1,1,10],'black',linewidth=2)    
    P=array([[0,x[0]],[0,1],[-6,0],[22,0],[16,1],[16,x[2]],[12,x[2]],[12,1]
            ,[10,1],[10,x[1]],[6,x[1]],[6,1],[4,1],[4,x[0]]])
    draw_polygon(ax,P,'blue')
    P=array([[1,10],[1,x[0]],[1+0.1*u[0,0],x[0]],[1+0.1*u[0,0],10]])
    draw_polygon(ax,P,'blue')
    P=array([[13,10],[13,x[2]],[13+0.1*u[1,0],x[2]],[13+0.1*u[1,0],10]])
    draw_polygon(ax,P,'blue')


# def f(x,u):
#     return(array([[0.1],[0.3],[1.5]]))

def alpha(h):
    a = 0.4
    g = 9.81
    return a*sign(h)*sqrt(2*g*abs(h))

# xdot = f(x,u) = [h1_dot, h2_dot, h3_dot]
def f(x,u):
    xdot = array([[-alpha(x[0,0]) - alpha(x[0,0]-x[1,0]) + u[0,0]],
                  [alpha(x[0,0]-x[1,0]) - alpha(x[1,0]-x[2,0])],
                  [-alpha(x[2,0]) + alpha(x[1,0] - x[2,0]) + u[1,0]]])
    return xdot

# Régulateur
def b(x):
    return array([[-alpha(x[0,0]) - alpha(x[0,0]-x[1,0])],
                  [-alpha(x[2,0]) + alpha(x[1,0] - x[2,0])]])


dt = 0.05
x = array([[4],[5],[2]])
u = array([[1],[2]])

y = array([[x[0,0]],[x[2,0]]]) # sortie du système (hauteur des 2 bacs extérieurs)
z = array([[0],[0]])

ax=init_figure(-10,25,-2,12)

for t in arange(0,5,dt) :
    clear(ax)
    draw_pools(x)
    x = x + dt*f(x,u)  
    y = array([[x[0,0]],[x[2,0]]]) # sortie du système (hauteur des 2 bacs extérieurs)
    
    w = array([[5],[8]]) # consigne de hauteur à atteindre
    wdot = array([[0],[0]]) # consigne en hauteur

    zdot = w - y
    z = z + zdot*dt
    v = z + 2*(w-y) + wdot
    u = v - b(x)


pause(3)
