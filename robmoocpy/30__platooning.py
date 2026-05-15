from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(x,col):
    θ = x[0,0]/r
    a=array([[r*cos(θ)],[r*sin(θ)],[θ+pi/2]])
    draw_tank(a,col)
        

def xi(X,i):  
    return X[:,i%m].flatten().reshape(2,1)


def circular_dist(xi,xj):
    d = xj-xi
    sigma = r*(pi+sawtooth(d[0,0]/r - pi))
    return sigma

def g(xi,xj):
    d=xj-xi
    sigma = circular_dist(xi,xj)
    return array([[sigma],[d[1,0]]])

def f(x,u):
    x=x.flatten()
    v = x[1]
    return array([ [v], [u]])

def control(xi,yi):
    yi = yi.flatten()
    k1,k2,k3 = 1,1,1
    d0 = L/m
    v0 = 10

    u = k1*(yi[0] - d0) + k2*(yi[1]) + k3*(v0-xi[1,0])

    return u



L=100
r=L/(2*pi)
m = 10

dr = -7
X = zeros([2,m])
for i in range(m):
    dr = dr - 7*abs(rand())-4 # 4 : approximation de la taille du robot
    X[0,i] = dr #-7*i

dt = 0.05
# xa=array([[25],[0]])   

ax=init_figure(-20,20,-20,20)
for t in arange(0,10,dt):
    clear(ax)
    draw_disk(ax,array([[0],[0]]),r+3,'lightblue')
    draw_disk(ax,array([[0],[0]]),r-3,'white')


    for i in range(m):
        xa = xi(X,i)
        xb = xi(X,i-1)
        yi=g(xa,xb)
        u = control(xa,yi)
        xa = xa + dt*f(xa,u)
        X[:,i%m] = xa.flatten()
        
        draw(xa,'black')

    pause(0.01)
pause(2)


## Eighvalues calculation for question 4:

A = np.array([
    [0, 0, 0, -1, 0, 0, 1],
    [0, 0, 0, 1, -1, 0, 0],
    [0, 0, 0, 0, 1, -1, 1],
    [1, 0, 0, -2, 0, 0, 1],
    [0, 1, 0, 1, -2, 0, 0],
    [0, 0, 1, 0, 1, -2, 0],
    [-1, -1, -1, 0, 0, 1, -2]
])

vp, _ = np.linalg.eig(A)
print("Eigenvalues of A:", vp)