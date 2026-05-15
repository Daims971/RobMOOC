from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x1,x2):        
    return -(x1**3+x2**2*x1-x1+x2),-(x2**3+x1**2*x2-x1-x2)

def R_polaire(theta,a,b):
    return array([[a*cos(theta),-b*sin(theta)],[a*sin(theta),b*cos(theta)]])

@np.vectorize
def fA(x1,x2):

    R = R_polaire(pi/4,1,1) # rotation
    E = R_polaire(0,2,1) # ellipse
    S = R_polaire(0,1,-1) #symetry

    A = R@E@S

    B=inv(A)

    
    # xy = stack([x1, x2])                  # (2,) ou (2,17,17)
    # y  = tensordot(B, xy, axes=1)         # (2,) ou (2,17,17)

    # z1, z2 = f(y[0], y[1])

    # z = stack([z1, z2])                   # (2,) ou (2,17,17)
    # v  = tensordot(A, z, axes=1)          # (2,) ou (2,17,17)

    # return v[0], v[1]  
        
    y=B.dot(array([[x1],[x2]]))
    z1,z2 = f(y[0,0],y[1,0])
    z_vector = array([[z1], [z2]])
    v = A.dot(z_vector)
    return v[0,0],v[1,0]

xmin,xmax,ymin,ymax=-2.5,2.5,-2.5,2.5 
ax=init_figure(xmin,xmax,ymin,ymax)
draw_field(ax,fA,xmin,xmax,ymin,ymax,0.3)    
dt=0.05
x=array([[0],[1]])
for t in arange(0,10,dt):
    x1,x2=x[0,0],x[1,0]
    # dx1,dx2=f(x1,x2)
    dx1,dx2=fA(x1,x2)
    x=x+dt*array([[dx1],[dx2]])
    ax.scatter(x1,x2,1.6,color='red')

pause(0.5*5)
    
    






