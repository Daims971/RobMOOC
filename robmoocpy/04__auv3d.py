from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(x,Pd):
    ax_lim = 40
    # clean3D(ax,-ax_lim/2,ax_lim/2,-ax_lim,ax_lim,-ax_lim,ax_lim)
    # clean3D(ax,-20,20,-20,20,-20,20)
    clean3D(ax,0,60,0,20,-20,40)
    draw_axis3D(ax,0,0,0,eye(3,3),10)
    draw_robot3D(ax,x[0:3],eulermat(*x[4:7,0]),'blue')
    # draw_robot3D(ax,Pd,eulermat(0,0,0),'red')
    ax.scatter(Pd[0,0],Pd[1,0],Pd[2,0],color='red',s=50)
    ax.scatter(1,2,3,color='magenta')
           

def f(x,u):
    x,u=x.flatten(),u.flatten()
    v,φ,θ,ψ=x[3],x[4],x[5],x[6];
    cφ,sφ,cθ,sθ,cψ,sψ= cos(φ),sin(φ),cos(θ),sin(θ),cos(ψ),sin(ψ)
    return array([ [v*cθ*cψ],[v*cθ*sψ],[-v*sθ],[u[0]] ,
                    [-0.1*sφ*cθ + tan(θ)*v*(sφ*u[1]+cφ*u[2])] ,
                     [cφ*v*u[1] - sφ*v*u[2]] ,
                     [(sφ/cθ)*v*u[1] + (cφ/cθ)*v*u[2]]])
              

# Consigne

f1=0.01
f2=6*f1
f3=3*f1
R=20

def consigne(t):
    Pd = array([[R*sin(f1*t) + R*sin(f2*t)],[R*cos(f1*t) + R*cos(f2*t)],[R*sin(f3*t)]])
    dPd = array([[R*f1*cos(f1*t) + R*f2*cos(f2*t)],[ -R*f1*sin(f1*t) - R*f2*sin(f2*t)],[R*f3*cos(f3*t)]])
    ddPd = array([[-R*(f1**2)*sin(f1*t) - R*(f2**2)*sin(f2*t)],[ -R*(f1**2)*cos(f1*t) - R*(f2**2)*cos(f2*t)],[ -R*(f3**2)*sin(f3*t)]])
    return Pd,dPd,ddPd

def control(x,Pd,dPd,ddPd):
    x,xr=x.flatten(),Pd.flatten()
    v,φ,θ,ψ=x[3],x[4],x[5],x[6];
    cφ,sφ,cθ,sθ,cψ,sψ= cos(φ),sin(φ),cos(θ),sin(θ),cos(ψ),sin(ψ)
    A1 = array([[cθ*cψ, -v*sθ*cψ, -v*cθ*sψ],[cθ*sψ, -v*sθ*sψ, v*cθ*cψ],[-sθ, -v*cθ, 0]])
    A2 = array([[1,0,0],[0,v*cφ, -v*sφ],[0,v*sφ/cθ, v*cφ/cθ]])
    A = A1.dot(A2)
    u = np.linalg.inv(A).dot(0.04*(Pd - array([[x[0]],[x[1]],[x[2]]])) + 0.4*(dPd - array([[v*cθ*cψ],[v*cθ*sψ],[-v*sθ]])) + ddPd )
    # print("A1=",A1)
    # print("A2=",A2)
    # print("A=",A)
    # print("u=",u)
    # print("x=",x)
    # print("x[0:3]=",x[0:3])
    # print("array([[x[0]],[x[1]],[x[2]]])=",array([[x[0]],[x[1]],[x[2]]]))
    return u

x = array([[0,0,10,15,0,1,0]]).T
u = array([[0,0,0.1]]).T
dt = 0.05

ax=figure3D()
for t in arange(0,30,dt):
    Pd,dPd,ddPd=consigne(t)
    u=control(x,Pd,dPd,ddPd)
    xdot=f(x,u)
    x = x + dt * xdot
    draw(x,Pd) # x in blue, Pd in red
    pause(0.001)
pause(1)    