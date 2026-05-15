from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(x,u,ax,ax_lim):
    x,u        = x.flatten(),u.flatten()
    plane    = array([[0,  0, 6, 0,  0, 0,   0,   1, 6, 0],
                      [0, -1, 0, 1, -1, 0,   0,   0, 0, 0],
                      [0,  0, 0, 0,  0, 0,   1, 0.2, 0, 0],
                      [1,  1, 1, 1,  1, 1,   1,   1, 1, 1]])
    e        = 0.5
    flap  = array([[-e,  0, 0, -e, -e],[-e, -e, e,  e, -e],
                      [ 0,  0, 0,  0,  0],[ 1,  1, 1,  1,  1]])
    
    R        = hstack((     eulermat(-x[3],-x[4],x[5]),
                            array([[x[0],x[1],-x[2]]]).T
                     ))
    R        = vstack((R,array([[0, 0, 0, 1]])))
    
    def draw_flap(ua,s):
        R1  = hstack((eulermat(0,ua,0),array([[0,s,0]]).T))
        R1  = vstack((R1,array([[0,0,0,1]])))
        flap1  = R @ R1 @ flap
        ax.plot(flap1[0,:],flap1[1,:],flap1[2,:],'red')    
        return
    
    plane    = R @ plane
    # clean3D(ax,-1,14,-7,7,-1,14)
    clean3D(ax,-ax_lim,ax_lim,-ax_lim,ax_lim,-ax_lim,ax_lim)
    draw_flap(-u[1]+u[2],1-e)    #left flap
    draw_flap(-u[1]-u[2],e-1)    #right flap
    ax.plot(plane[0,:],plane[1,:],plane[2,:],'blue')          # drone
    ax.plot(plane[0,:],plane[1,:],0*plane[2,:],'black')       # ombre du drone
    ax.plot(Cx0,Cy0,Cz0,'green')                              # cercle consigne


def f(x,u):
    v     = x[6:9]
    w     = x[9:12]
    x,u=x.flatten(),u.flatten()
    V     = norm(v)
    α = arctan(x[8]/x[6])
    β  = arcsin(x[7]/V)
    φ,θ,ψ = x[3],x[4],x[5]
    cf,sf,ct,st,tt,ca,sa,cb,sb = cos(φ),sin(φ),cos(θ),sin(θ),tan(θ),cos(α),sin(α),cos(β),sin(β)
    Fa= 0.002*(V**2)*array([[-ca*cb,ca*sb,sa],[sb,cb,0],[-sa*cb,sa*sb,-ca]])  \
            @  \
            array([[4+(-0.3+10*α+10*w[1,0]/V+2*u[2]+0.3*u[1])**2+abs(u[1])+3*abs(u[2])],
                   [-50*β + 10*(w[2,0]-0.3*w[0,0])/V],
                   [10+500*α+400*w[1,0]/V+50*u[2]+10*u[1]]])
    
    return vstack((
                         eulermat(φ,θ,ψ) @ v,
                         eulerderivative(φ,θ,ψ)@ w,                  
                         9.81*array([[-st],[ct*sf],[ct*cf]])+Fa+array([[u[0]],[0],[0]]) - cross(w.T,v.T).T,
                         array([ -w[2]*w[1]+0.1*(V**2)*(-β -2*u[2]+(-5*w[0]+w[2])/V),
                                w[2]*w[0]+0.1*(V**2)*(-0.1-2*α+0.2*u[2]-3*u[1]-30*w[1]/V),
                                0.1*w[0]*w[1]+0.1*(V**2)*(β+0.5*u[2]+0.5*(w[0]-2*w[2])/V)])
                         ))
    
def control(x,vbar,thetabar,psibar):
    x = x.flatten()

    v     = x[6:9]
    w     = x[9:12]
    V     = norm(v)
    α = arctan(x[8]/x[6])
    β  = arcsin(x[7]/V)
    φ,θ,ψ = x[3],x[4],x[5]

    u1max,u2max,u3max = 10,0.6,0.2

    u1 = (u1max/2)*((2/pi)*arctan(vbar-V)+1) # u1 in [0,10]
    u2 = -(u2max/2)*(2/pi)*(arctan(4*(thetabar-θ))+np.abs(sin(φ))) #-0.3
    
    phibar = (1/2)*arctan(2*sawtooth((psibar-ψ)/1)) # phibar in [-0.5,0.5]
    # phibar = (1/2)*((2/pi)*arctan(psibar-ψ)) # 

    u3 = -(u3max/2)*(2/pi)*(arctan(phibar-φ)) # or psibar for the start gain
    return array([[u1],[u2],[u3]])

def control_cons(x,vbar,zbar,rbar):
    x = x.flatten()

    px,py,pz = x[0:3]
    thetabar = -0.2*arctan((zbar-pz)/10)
    d = sqrt((px**2)+(py**2))
    psibar = arctan2(py,px) + pi/2+ arctan((rbar-d)/30)

    return thetabar,psibar


x    = array([[1, 0, 0, 0, 0.1, 0, 20, 0, 0, 0, 10, 0]]).T #[x;y;z;φ;θ;ψ;v;w]
dt   = 0.005
vbar,zbar,rbar = 15,-50,100  
a    = arange(0,2*pi+0.1, 0.1)
Cx0,Cy0,Cz0 = rbar*np.cos(a),rbar*np.sin(a),[-zbar]*len(a) #circle to follow

thetabar = 0
psibar= 1

# x_history = []

# i=0
# ax=figure3D()
# for t in arange (0,20,dt):
#     #u=array([[10],[-0.3],[0.2]])
#     thetabar,psibar = control_cons(x,vbar,zbar,rbar)
#     u = control(x,vbar,thetabar,psibar)
#     x = x +dt*f(x,u)
#     # draw(x,u,ax,120)
#     # On ne dessine qu'une itération sur 10 (soit toutes les 0.05 secondes) pour alléger la simulation
#     if i % 400 == 0:
#         draw(x,u,ax,120)

#         # #Trace la trajectoire (historique des positions x, y, z) pour voir "tous les points"
        
#         # x_history.append(x)
#         # traj = np.array(x_history[:i]) # Prend l'historique jusqu'au point actuel
#         # if len(traj) > 0:
#         #     ax.plot(traj[:,0,0], traj[:,1,0], traj[:,2,0], color='gray', linestyle='--')
    
# #     ax.view_init(elev=90, azim=-90) # vue de dessus

#     pause(0.01)
#     i += 1



"""

Si le calcul est trop intense, on enregistre les données dans une liste (x_history, u_history) à chaque itération,
 puis on fait une seconde boucle pour l'affichage (animation) à partir de ces données pré-calculées.
"""

# 1. ÉTAPE DE CALCUL (rapide)
x_history = []
u_history = []
u_cons_history = []

print("Calcul en cours...")
for t in arange (0, 200, dt):
    thetabar,psibar = control_cons(x,vbar,zbar,rbar)
    u = control(x, vbar, thetabar, psibar)
    x = x + dt*f(x,u)
    u_cons_history.append([thetabar,psibar])
    u_history.append(u)
    x_history.append(x)

print("Calcul terminé. Lancement de l'animation...")

# 2. ÉTAPE D'AFFICHAGE (animation)
ax=figure3D()
# ax.view_init(elev=90, azim=-90) # vue de dessus
# On itère sur les données enregistrées avec un pas spécifique pour fluidifier
for i in range(0, len(x_history), 200):
    # ax.cla() # Efface explicitement les anciens tracés de la mémoire

    draw(x_history[i], u_history[i], ax, 120)

    # Trace la trajectoire (historique des positions x, y, z) pour voir "tous les points"
    traj = np.array(x_history[:i]) # Prend l'historique jusqu'au point actuel
    if len(traj) > 0:
        ax.plot(traj[:,0,0], traj[:,1,0], traj[:,2,0], color='gray', linestyle='--')
    
    # ax.view_init(elev=90, azim=-90) # vue de dessus

    pause(0.01)
