from roblib import *


def f(x,u):
    θ,v=x[2,0],x[3,0]
    return array([[v*cos(θ)],[v*sin(θ)],[u[0,0]],[u[1,0]]])

def xi(X,i):  return X[:,i%m].flatten().reshape(4,1)

m=6
np.random.seed(0)
dt = 0.05
ax=init_figure(-15,15,-15,15)
X=5*randn(4,m)
for t in arange(0,2,dt):
    clear(ax)
    X_=X.copy()
    for i in range(m):
        x=xi(X_,i)
        draw_tank(x[[0,1,2]],'red',0.25)
        u=array([[1],[0]])
        X[:,i]=(x+dt*f(x,u)).flatten()
    pause(0.01)
