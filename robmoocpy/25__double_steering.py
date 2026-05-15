from roblib import *
import sympy as sp

def draw_robot(x):
   p1,p2,ψ,s1,s2,s3=list(x[0:6,0])
   M0=array([[ -1  ,1],[0,0]])
   M0=add1(M0)
   W=array([[-0.5,0.5],[0,0],[1,1]])
   R1=tran2H(p1,p2)@rot2H(ψ)
   M1=R1@M0
   δ1=arctan2(s1,s3)
   δ2=arctan2(s2,s3)
   W1=R1@tran2H(1,0)@rot2H(δ1)@W
   W2=R1@tran2H(-1,0)@rot2H(δ2)@W
   plot2D(M1,'blue',1)
   plot2D(W1,'green',1)
   plot2D(W2,'black',1)

def Aψ(ψ):
    return array([[-0.5*sin(ψ),-0.5*sin(ψ), cos(ψ)], [0.5*cos(ψ),0.5*cos(ψ),sin(ψ)],[1,-1,0]])

def f(x,u):
    u1,u2,u3,u4=list(u[0:4,0])
    ψ,s1,s2,s3=list(x[2:7,0])
    v1=sqrt(s1**2+s3**2)
    v2=sqrt(s2**2+s3**2)
    ds = array([[(s1/v1)*u1+s3*u2], [(s2/v2)*u3+s3*u4],[(s3/v1)*u1-s1*u2]])
    s=array([[s1],[s2],[s3]])
    return(vstack((Aψ(ψ)@s,ds)))

def control(x,w,dw,ddw):
    p1,p2,ψ,s1,s2,s3 = x.flatten()
    p = array([[p1],[p2],[ψ]])
    s = array([[s1],[s2],[s3]])

    dpsi = s1-s2
    dAψ = array([[-0.5*cos(ψ),-0.5*cos(ψ), -sin(ψ)], [-0.5*sin(ψ),-0.5*sin(ψ),cos(ψ)],[0,0,0]])

    sd = inv(Aψ(ψ))@(w-p+dw)
    v = dw + ddw - dpsi*dAψ@sd
    dsd = inv(Aψ(ψ))@v - s

    uv = vstack((sd - s + dsd, [[0]]))

    B = np.array([[s1/sqrt(s1**2+s3**2), s3, 0, 0],
                  [0, 0, s2/sqrt(s2**2+s3**2), s3],
                  [s3/sqrt(s1**2+s3**2), -s1, 0, 0],
                  [-s3/sqrt(s1**2+s3**2), s1, s3/sqrt(s2**2+s3**2), -s2]])

    u = inv(B)@uv
    return u

a=array([4,1])
t=sp.symbols('t')

x,y=3*sp.cos(t),3*sp.sin(2*t)

xd=sp.lambdify(t,x)
yd=sp.lambdify(t,y)
dxd = sp.lambdify(t,sp.diff(x,t))
dyd = sp.lambdify(t,sp.diff(y,t))
ddxd = sp.lambdify(t,sp.diff(x,t,2))
ddyd = sp.lambdify(t,sp.diff(y,t,2))

# psi = arctan2(a[1]-y,a[0]-x)
psi = sp.atan2(a[1]-y,a[0]-x)

psid = sp.lambdify(t,psi)
dpsid = sp.lambdify(t,sp.diff(psi,t))
ddpsid = sp.lambdify(t,sp.diff(psi,t,2))

# pd = array([[xd(t)],[yd(t)],[psid(t)]])
# dpd = array([[dxd(t)],[dyd(t)],[dpsid(t)]])
# ddpd = array([[ddxd(t)],[ddyd(t)],[ddpsid(t)]])

ax = init_figure(-5,5,-5,5)
x=array([[3],[-4],[0],[1],[1],[1]]) #x,y,ψ,s1,s2,s3
dt=0.01
for t in arange(0,10,dt):
    clear(ax)
    draw_robot(x)
    draw_disk(ax,a,0.1,"blue")
    # plot(a[0],a[1],"o",color='blue')
    T = arange(0,2*pi,0.01)
    plot(3*cos(T), 3*sin(2*T),color='magenta')
    plot(3*sp.cos(t),3*sp.sin(2*t),color='red',marker='o')
    pause(0.001)

    pd = array([[xd(t)],[yd(t)],[psid(t)]])
    dpd = array([[dxd(t)],[dyd(t)],[dpsid(t)]])
    ddpd = array([[ddxd(t)],[ddyd(t)],[ddpsid(t)]])

    u = control(x,pd,dpd,ddpd)
    x = x + dt*f(x,u)
pause(1)

