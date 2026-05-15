from roblib import *


def f(x,u):
    θ,v=x[2,0],x[3,0]
    return array([[v*cos(θ)],[v*sin(θ)],[u[0,0]],[u[1,0]]])

def xi(X,i):  return X[:,i%m].flatten().reshape(4,1)


def relative_pos(X,i,j):
    m = X.shape[1]  # On récupère le nombre de colonnes (nombre de robots)
    
    # On applique les modulos ici pour éviter le dépassement
    xi = X[:, i%m].flatten().reshape(4,1)
    xj = X[:, j%m].flatten().reshape(4,1)

    pi = xi[0:2]
    pj = xj[0:2]

    theta_i = xi[2,0]
    theta_j = xj[2,0]

    Ri = array([[cos(theta_i),sin(theta_i)],[-sin(theta_i),cos(theta_i)]])

    dtheta = theta_j - theta_i
    dp = Ri@(pj-pi)

    # return xj-xi
    return dp, dtheta


def control(X,i):
    x1,x2,theta,v = xi(X,i).flatten()

    kt=2
    kv=1
    kr=15

    dp, dtheta = relative_pos(X,i,i+1)
    w = dp - 2*array([[cos(dtheta)],[sin(dtheta)]]) # on soustrait la position de l'encre de chaque robot

    for j in range(m):
        if j != i and j != (i+1)%m:
            dp, dtheta = relative_pos(X,i,j)
            w = w - kr*dp/(norm(dp)**3) # force de répulsion entre chaque robot

    u1 = kt*sawtooth(arctan2(w[1,0],w[0,0]))
    u2 = kv*(norm(w)-v)

    return array([[u1],[u2]])


m=6
np.random.seed(0)
dt = 0.05
ax=init_figure(-15,15,-15,15)
X=5*randn(4,m)
for t in arange(0,20,dt):
    clear(ax)
    X_=X.copy()
    for i in range(m):
        x=xi(X_,i)
        draw_tank(x[[0,1,2]],'red',0.25)
        # u=array([[1],[0]])
        u = control(X_,i)
        X[:,i]=(x+dt*f(x,u)).flatten()
    pause(0.01)
