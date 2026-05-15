
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x,u=x.flatten(),u.flatten()
    xdot = array([[x[3]*cos(x[2])],[x[3]*sin(x[2])],
                  [u[0]],[u[1]],[x[3]]])
    return(xdot)


# def control(x,w,dw,ddw):
#     xr,yr,θr,vr,sr=x.flatten()

#     # X = array([[xr],[yr]])

#     A = array([[ -vr*sin(θr),  cos(θr)],
#                [  vr*cos(θr),  sin(θr)]])

#     u = np.linalg.inv(A).dot((w-array([[xr],[yr]]))+2*(dw-array([[vr*cos(θr)],[vr*sin(θr)]]))+ddw)

#     return u

    

def control(x,w,dw):
    xr,yr,θr,vr,sr=x.flatten()

    # X = array([[xr],[yr]])

    A = array([[ -vr*sin(θr),  cos(θr)],
               [  vr*cos(θr),  sin(θr)]])

    u = np.linalg.inv(A).dot((w-array([[xr],[yr]]))+(dw-array([[vr*cos(θr)],[vr*sin(θr)]])))

    return u

ax=init_figure(-30,30,-30,30)
xa  = array([[10],[0],[1],[1],[0]])
m= 6
X=array([4*arange(0,m),zeros(m),ones(m),3*ones(m),zeros(m)])
Lx,Ly = 20,5
e   = np.linspace(0.,2*pi,30)
p   = array([[Lx*cos(e)],[Ly*sin(e)]])
S   = zeros((5,1))
dt  = 0.05
omega=0.1
ds= 0.1
d=5

print("X=",X)

for t in arange(0,100,dt):
    clear(ax)
    
    wa = array([[Lx*sin(omega*t)],[Ly*cos(omega*t)]]) # ellipse à suivre (column vectors)
    dwa = array([[Lx*omega*cos(omega*t)],[-Ly*omega*sin(omega*t)]]) # dérivée de w
    # ddwa = array([[Lx*omega**2*sin(omega*t)],[-Ly*omega**2*cos(omega*t)]]) # dérivée de dw

    ua  = control(xa,wa,dwa)    
    plot(wa[0][0],wa[1][0],'ro')
    plot(p[0][0],p[1][0])
    draw_tank(xa,'blue')
    xa  = xa + dt*f(xa,ua)
    for i in range(m):

        if xa[4][0] > ds:
            S = np.hstack((S,xa))
            xa[4][0] = 0

        j = int(S.shape[1] - (d*i)/ds -1)
        if j>=0:

            xai = S[:,j].reshape(5,1)

            wi = array([[xai[0][0]],[xai[1][0]]])
            dwi = array([[xa[3][0]*cos(xa[2][0])],[xa[3][0]*sin(xai[2][0])]])

            x=X[:,i].reshape(5,1)
            ui = control(x,wi,dwi)

            draw_tank(x,'black')
            x=x+f(x,ui)*dt        
            X[:,i]  = x.flatten()            
pause(1)


