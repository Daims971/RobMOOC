from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x,u  = x.flatten(), u.flatten()
    v,θ = x[2],x[3]    
    return array([[v*cos(θ)],[v*sin(θ)],[u[0]],[u[1]]])
    

# def f1(x1,x2):  
#     return -x1,-x2


# def f1(x1, x2):  
#     p = array([[x1], [x2]])
    
#     d = norm(p - qhat)
#     # Protection pour éviter une division par zéro si la grille tombe pile sur qhat
#     if d < 0.1:
#         d = 0.1
        
#     w = vhat - 2*(p - phat) + (p - qhat)/(d**3)
    
#     return w[0,0], w[1,0]


def f1(x1, x2):
    # On extrait les composantes des vecteurs cibles
    ph_x, ph_y = phat[0,0], phat[1,0]
    qh_x, qh_y = qhat[0,0], qhat[1,0]
    vh_x, vh_y = vhat[0,0], vhat[1,0]
    
    # x1 et x2 sont des matrices de points. 
    # On calcule la distance à qhat pour chaque point de l'espace.
    d = sqrt((x1 - qh_x)**2 + (x2 - qh_y)**2)
    
    # On limite la distance minimale pour éviter une division par zéro ou 
    # des flèches immenses au centre de l'obstacle
    # d[d < 0.1] = 0.1
    
    # Calcul composante par composante du vecteur ew
    wx = vh_x - 2*(x1 - ph_x) + (x1 - qh_x)/(d**3)
    wy = vh_y - 2*(x2 - ph_y) + (x2 - qh_y)/(d**3)
    
    return wx, wy

def control(x,w):
    
    x,w  = x.flatten(), w.flatten()
    v,theta = x[2],x[3]

    k1 = 1
    k2 = 3

    vbar=norm(w)
    thetabar = arctan2(w[1],w[0])

    u1 = k1*(vbar - v)
    u2 = k2*2*arctan(tan((thetabar-theta)/2))

    return array([[u1],[u2]])

    
x    = array([[4,-3,1,2]]).T #x,y,v,θ

case = 1

dt   = 0.1
s=8
ax=init_figure(-s,s,-s,s)
for t in arange(0,10,dt):
    clear(ax)

    if case == 1:
        phat = array([[1],[2]]) 
        qhat = array([[3],[4]]) 
        vhat = array([[0],[0]]) # derivate of phat
    elif case == 2:
        phat = array([[t],[t]])
        qhat = array([[4],[5]]) 
        vhat = array([[1],[1]]) # derivate of phat
    elif case == 3:
        phat = array([[cos(t/10)],[2*sin(t/10)]]) 
        qhat = array([[2*cos(t/5)],[2*sin(t/5)]])
        vhat = array([[-0.1*sin(t/10)],[0.2*cos(t/10)]]) # derivate of phat


    draw_disk(ax,qhat,0.3,"magenta")
    draw_disk(ax,phat,0.2,"green")

    p = x[0:2]
    w = vhat  -2*(p-phat) + (p-qhat)/(norm(p-qhat)**3)
    u=control(x,w)
    # u=array([[0],[0.3]])

    x=x+dt*f(x,u)    
    draw_tank(x[[0,1,3]],'red',0.2) # x,y,θ
    draw_field(ax,f1,-s,s,-s,s,0.4)

pause(1)    


