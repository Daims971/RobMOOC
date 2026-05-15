from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return array([[x[3]*cos(x[2])],[x[3]*sin(x[2])],[u[0]],[u[1]]])
        
def control (x,w,dw):
    x=x.flatten()
    A = array([[-x[3]*sin(x[2]), cos(x[2])],
                  [x[3]*cos(x[2]), sin(x[2])]])
    y = array([[x[0]],[x[1]]])
    dy = array([[x[3]*cos(x[2])],[x[3]*sin(x[2])]])
    return inv(A) @ ((w - y) + 2*(dw - dy))

    

def bint(i,n,t):
    bi = factorial(n)/(factorial(i)*factorial(n-i)) * t**i * (1-t)**(n-i)
    return bi

def dbint(i,n,t):
    if i==0: 
        dbi = -n*((1-t)**(n-1))
    elif i==n:
        dbi = n*t**(n-1)
    else:
        dbi = factorial(n)/(factorial(i)*factorial(n-i)) * (-(n-i)* (1-t)**(n-i-1)*t**i + i*((1-t)**(n-i))*t**(i-1))
    return dbi
    

def setpoint(t,n,p): 
    # w = array([[5+cos(t)],[5+sin(t)]])
    w = array([[0],[0]])
    for i in range(n+1):
        # w = array([[w[0]+bint(i,n,t)*p[i][0]],[w[1]+bint(i,n,t)*p[i][1]]])
        w = w + bint(i,n,t)*p[:,i:i+1]

    return w

def dsetpoint(t,n,p): 
    # dw = array([[-sin(t)],[cos(t)]])
    dw = array([[0],[0]])
    for i in range(n+1):
        # dw = array([[dw[0]+dbint(i,n,t)*p[i][0]],[dw[1]+dbint(i,n,t)*p[i][1]]])
        dw = dw + dbint(i,n,t)*p[:,i:i+1]
    return dw

    
ax=init_figure(-1,11,-1,11)

P = array([[1,1,1,1,2, 3,4,5,4,8,10,8],
           [1,4,7,9,10,8,6,4,0,0,0,8]])
n = len(P[0])-1
plot(P[0], P[1], 'or')
dt = 0.1
k=0


A1=array([[2,0],[4,2],[2,7]])
A2=array([[7,2],[8,3],[3,10]])
draw_polygon(ax,A1,'green')
draw_polygon(ax,A2,'green')

tmax = 50
T = arange(0,tmax,dt)
# wT = setpoint(T,n,P)
wT = array([setpoint(t/tmax, n, P).flatten() for t in T]).T   # forme (2, len(T))

plot(wT[0],wT[1], 'y-')

x = array([[0,0,0,1]]).T

# s0  = 0.0
# w0  = setpoint(s0, n, P)
# dw0 = dsetpoint(s0, n, P)

# theta0 = arctan2(dw0[1,0], dw0[0,0])
# v0     = norm(dw0) / tmax      # <-- cohérent avec dw = dsetpoint/tmax
# print("theta0 = ", theta0)
# print("v0 = ", v0)
# x = array([[w0[0,0], w0[1,0], theta0, v0]]).T

for t in arange(0,tmax,dt):
    w = setpoint(t/tmax,n,P)
    dw = (1/tmax)*dsetpoint(t/tmax,n,P)
    u = control(x,w,dw)
    plot(w[0,0],w[1,0], 'm.')
    # plot(wT[0],wT[1], 'r.')
    x = x+f(x,u)*dt
    if (t/dt) % 5 == 0:
        draw_tank(x,'darkblue',0.2)
    pause(0.05)
pause(1*2)

# plt.show()