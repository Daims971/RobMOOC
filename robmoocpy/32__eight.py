from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def φ0(p1,p2):        
    return -(p1**3+p2**2*p1-p1+p2),-(p2**3+p1**2*p2-p1-p2)
    

# c = [2,0]
c = array([[2],[0]])
rho=2
eps=1

D = array([[rho,0],[0,rho*eps]])

# @np.vectorize
# def φ(p1,p2):
#     # p = array([[p1],[p2]])
#     dp1, dp2 = φ0(p1,p2)
#     dp = array([[dp1],[dp2]])

#     gdp = D@dp + c

#     gdp = gdp.flatten()

#     return gdp[0], gdp[1]

@np.vectorize
def φ(p1,p2):
    
    B=inv(D)

    y=B.dot(array([[p1],[p2]]) -c )
    z1,z2 = φ0(y[0,0],y[1,0])
    z_vector = array([[z1], [z2]])
    v = D@z_vector
    return v[0,0],v[1,0]


def Jphi0(p):
    p1, p2 = p.flatten()
    jphi0 = array([[-3*p1**2 - p2**2 + 1, -2*p1*p2 - 1],
                  [-2*p1*p2 - 1, -3*p2**2 - p1**2 + 1]])

    return jphi0

def dphi(x):
    p1, p2, θ = x.flatten()
    c1, c2 = c.flatten()
    z = inv(D) @ array([[p1 - c1], [p2 - c2]])
    dv = D @ Jphi0(z) @ inv(D) @ array([[cos(θ)], [sin(θ)]])
    return dv.flatten()

def control(x):
    dphi1, dphi2 = dphi(x)
    x1, x2, x3 = x.flatten()
    phi1, phi2 = φ(x1, x2)
    u = -sawtooth(x3 - arctan2(phi2, phi1)) - ((phi2 * dphi1 - phi1 * dphi2) / (phi1**2 + phi2**2))
    return u


def f(x, u):
    θ = x[2, 0]
    return array([[cos(θ)], [sin(θ)], [u]])

#### 1) Vector field

# dt,s= 0.1,5       
# ax=init_figure(-s,s,-s,s)
# # draw_field(ax,φ0,-s,s,-s,s,0.51)
# draw_field(ax,φ,-s,s,-s,s,0.51)


#### 2) COntrol law

# x = array([[0],[0],[0]])

# dt = 0.1
# s=5
# ax=init_figure(-s,s,-s,s)
# for t in arange(0, 20, dt):
#     clear(ax)
#     draw_tank(x, 'darkblue', 0.1, 2)
#     # D = array([[r, 0], [0, r * eps]])
#     u = control(x)
#     x = x + dt * f(x, u)
#     draw_field(ax,φ,-s,s,-s,s,0.51)
#     pause(0.05)

# pause(1)    
    


#### 3) State machine

x = array([[1],[-4],[0]])
q = 0

dt = 0.1
s=5
ax=init_figure(-s,s,-s,s)

for t in np.arange(0, 40, dt):
    clear(ax)
    if q == 0:
        c1, c2, rho, eps = 2, 0, 2, 1
        draw_tank(x, 'darkblue', 0.1, 2)
    if q == 1:
        draw_tank(x, 'red', 0.1, 2)
        c1, c2, rho, eps = 2, 0, 2, 1
    if q == 2:
        draw_tank(x, 'green', 0.1, 2)
        c1, c2, rho, eps = -2, 0, 2, -1
    if q == 3:
        draw_tank(x, 'magenta', 0.1, 2)
        c1, c2, rho, eps = -2, 0, 2, -1

    c = np.array([[c1],[c2]])   
    D = np.array([[rho, 0], [0, rho * eps]])
    x1, x2 = x[0:2, 0].flatten()
    u = control(x)
    x = x + dt * f(x, u)

    if ((q % 2 == 0) & (x2 > 0.5)) | ((q % 2 == 1) & (x2 < 0)):
        q = (q + 1) % 4

    draw_field(ax,φ,-s,s,-s,s,0.51)
    pause(0.05)

# plt.show()
pause(1)