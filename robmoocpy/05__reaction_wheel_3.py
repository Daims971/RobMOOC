from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(ap,aw): 
    aw=-aw-ap;
    c=2*array([-sin(ap),cos(ap)])
    plot( [0,c[0]],[0,c[1]],'magenta', linewidth = 2)
    for i in arange(0,8):
        plot(c[0]+array([0,cos(aw+i*pi/4)]),c[1]+array([0,sin(aw+i*pi/4)]),'blue')
    pause(0.01)
    

def f(x,u): 
    x=x.flatten()
    return array([[x[1]],[a1*sin(x[0])-b1*u],[-a1*sin(x[0])+c1*u]])

# 3 Control avec y=alpha1*x1 + alpha2*x2 + alpha3*x3
def control(x): 
    x=x.flatten()
    v = -(c1*x[1]+b1*x[2]) - 3*(c1-b1)*a1*sin(x[0]) - 3*a1*(c1-b1)*x[1]*cos(x[0])
    ax = a1*(c1-b1)*(a1-x[1])*sin(x[0])
    aa = -b1*a1*(c1-b1)
    u = (v-ax)/aa
    return u


a1,b1,c1=10,1,2
dt = 0.02
x = array([[1],[0],[0]])
aw=0  # wheel angle
ax=init_figure(-3,3,-3,3)
for t in arange(0,10,dt) :
    u=control(x)
    x=x+f(x,u)*dt
    aw=aw+dt*x[2,0]
    clear(ax)
    draw(x[0,0],aw)

 


