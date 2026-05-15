from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


def f(x,u):
    x = x.flatten()
    θ = x[2]
    return array([[cos(θ)],[sin(θ)],[u]])

def control(x,thetabar):
    x = x.flatten()
    u=2*arctan(tan((thetabar-x[2])/2))/pi
    return u
    

def plot_dubins_path(a,b,ca,cb,da,db,beta_a,beta_b):
    # plot the Dubins path from a to b with turning radius r
    
    # xa = xa.flatten()
    # xb = xb.flatten()
    # ca = ca.flatten()
    # cb = cb.flatten()
    # da = da.flatten()
    # db = db.flatten()

    draw_arc(ca,a,beta_a,'blue')
    draw_arc(cb,db,beta_b,'green')
    plot([da[0],db[0]],[da[1],db[1]],'red')
    plot(ca[0],ca[1],'blue')
    plot(cb[0],cb[1],'green')


def calculate_L(xa,xb,r):
    # calculate the length of the Dubins path from a to b with turning radius r
    
    xa = xa.flatten()
    xb = xb.flatten()

    a = array([[xa[0]],[xa[1]]])
    b = array([[xb[0]],[xb[1]]])

    ca = a + r*array([[cos(xa[2]-pi/2)],[sin(xa[2]-pi/2)]])
    cb = b + r*array([[cos(xb[2]+pi/2)],[sin(xb[2]+pi/2)]])

    m = norm(cb-ca)/2

    l2 = m**2 - r**2
    if l2<0:
        return inf
    else:
        l = sqrt(l2)
    
    alpha = arctan(l/r)

    R_alpha = array([[cos(alpha),-sin(alpha)],[sin(alpha),cos(alpha)]])
    da = ca + r*R_alpha@(cb-ca)/norm(cb-ca)
    db = cb+ca-da
    
    # ca = ca.flatten()
    # cb = cb.flatten()
    # da = da.flatten()
    # db = db.flatten()

    ca_col, cb_col = ca, cb          # (2,1)
    da_col, db_col = da, db          # (2,1)

    # flatten the columns to get 1D arrays for beta calculation : (2,)
    ca = ca_col.flatten()
    cb = cb_col.flatten()
    da = da_col.flatten()
    db = db_col.flatten()

    angle_aca = arctan2((xa[1]-ca[1]),(xa[0]-ca[0]))
    angle_cada = arctan2((da[1]-ca[1]),(da[0]-ca[0]))

    angle_cbdb = arctan2((db[1]-cb[1]),(db[0]-cb[0]))
    angle_cbb = arctan2((xb[1]-cb[1]),(xb[0]-cb[0]))

    beta_a = sawtooth(angle_cada - angle_aca)
    beta_b = sawtooth(angle_cbb - angle_cbdb)

    # beta_a = float(beta_a)
    # beta_b = float(beta_b)

    L = -r*beta_a + r*beta_b + 2*l

    # plot_dubins_path(xa,xb,ca,cb,da,db,beta_a,beta_b)
    plot_dubins_path(a, b, ca_col, cb_col, da_col, db_col, beta_a, beta_b)

    return L


def calculate_L_eps(xa,xb,r,eps_a,eps_b):
    # calculate the length of the Dubins path from a to b with turning radius r
    
    xa = xa.flatten()
    xb = xb.flatten()

    a = array([[xa[0]],[xa[1]]])
    b = array([[xb[0]],[xb[1]]])

    ca = a + 1*r*array([[cos(xa[2]+eps_a*pi/2)],[sin(xa[2]+eps_a*pi/2)]])
    cb = b + 1*r*array([[cos(xb[2]+eps_b*pi/2)],[sin(xb[2]+eps_b*pi/2)]])

    m = norm(cb-ca)/2

    if eps_a*eps_b == -1:

        l2 = m**2 - r**2
        if l2<0:
            return inf
        else:
            l = sqrt(l2)
        
        alpha = -eps_a*arctan(l/r)

    elif eps_a*eps_b == 1:
        l = m
        alpha = -eps_a*pi/2
    

    R_alpha = array([[cos(alpha),-sin(alpha)],[sin(alpha),cos(alpha)]])
    da = ca + r*R_alpha@(cb-ca)/norm(cb-ca)
    # db = cb - (ca-da)*eps_a*eps_b

    # ✅ CORRECTION 2 : db se calcule différemment selon le type de tangente
    if eps_a * eps_b == -1:  # Tangente interne
        db = cb + ca - da
    else:  # Tangente externe
        db = da + (cb - ca)  # vecteur de translation identique
    
    # ca = ca.flatten()
    # cb = cb.flatten()
    # da = da.flatten()
    # db = db.flatten()

    ca_col, cb_col = ca, cb          # (2,1)
    da_col, db_col = da, db          # (2,1)

    # flatten the columns to get 1D arrays for beta calculation : (2,)
    ca = ca_col.flatten()
    cb = cb_col.flatten()
    da = da_col.flatten()
    db = db_col.flatten()

    angle_caa = arctan2((xa[1]-ca[1]),(xa[0]-ca[0]))
    angle_cada = arctan2((da[1]-ca[1]),(da[0]-ca[0]))

    angle_cbb = arctan2((xb[1]-cb[1]),(xb[0]-cb[0]))
    angle_cbdb = arctan2((db[1]-cb[1]),(db[0]-cb[0]))

    beta_a = eps_a*sawtooth(1*(angle_cada - angle_caa))
    beta_b = eps_b*sawtooth(1*(angle_cbb - angle_cbdb))

    # beta_a = float(beta_a)
    # beta_b = float(beta_b)

    L_eps = r*abs(beta_a) + r*abs(beta_b) + 2*l

    # plot_dubins_path(xa,xb,ca,cb,da,db,beta_a,beta_b)
    plot_dubins_path(a, b, ca_col, cb_col, da_col, db_col, beta_a, beta_b)

    return L_eps

    


# x   = array([[0],[0],[0.1]])


r=10 #turning radius or angle
a,b,ech = array([[-25,0,pi/2]]).T, array([[25,0,pi/2]]).T, 40      #simu 1
ax=init_figure(-ech,ech,-ech,ech)
clear(ax)
draw_tank(a,"black")
draw_tank(b,"blue")

# draw_arc(array([[0],[5]]),array([[4],[6]]),r,'red') # center, start, angle, color

# draw_arc(array([[0],[5]]),array([[4],[15]]),r,'red') # center, start, angle, color

xa = a
xb = b
L = calculate_L(xa,xb,r)
# L_eps = calculate_L_eps(xa,xb,r,1,1)

find_min_path = False
if find_min_path == True:
    L_dubins = []
    for i in [-1,1]:
        for j in [-1,1]:
            L_ij = calculate_L_eps(xa,xb,r,i,j)
            L_dubins.append(L_ij)
            print(f"L_{i}{j} = {L_ij:.2f}")

    # Lmin = [min(L_d) for L_d in L_dubins if L_d>=0 ]

    L_pos = [L_d for L_d in L_dubins if L_d>=0 ]

    print(f"Minimum Dubins path length: {min(L_pos):.2f}")
    print("Path number ij for minimum Dubins path length:",L_dubins.index(min(L_dubins)))



pause(5)
# show()
