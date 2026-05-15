from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
ax=figure3D()

m,g,b,d,l=10,9.81,2,1,1
I=array([[10,0,0],[0,10,0],[0,0,20]])
dt = 0.01  
B=array([[b,b,b,b],[-b*l,0,b*l,0],[0,-b*l,0,b*l],[-d,d,-d,d]])


def clock_quadri(p,R,vr,wr,w):
    w2=w*abs(w)
    τ=B@w2.flatten()
    p=p+dt*R@vr
    vr=vr+dt*(-adjoint(wr)@vr+inv(R)@array([[0],[0],[g]])+array([[0],[0],[-τ[0]/m]]))
    R=R@expw(dt*wr)
    wr=wr+dt*(inv(I)@(-adjoint(wr)@I@wr+τ[1:4].reshape(3,1)))
    return p,R,vr,wr

    
def control(p,R,vr,wr):

    zd = -15
    vd = 10
    # wrd = array([[0],[0],[0]])
    v_vdp = f_vanderpol(p)

    dp = R@vr
    t0 = -60*(zd - p[2,0]) + 20*vr[2,0] #+ m*g 


    phid = 0.5*tanh(5*sawtooth(arctan2(v_vdp[1,0], v_vdp[0,0] ) - arctan2(dp[1,0],dp[0,0]))) #arctan2(vr[1,0],vr[0,0])
    thetad = 0.5*arctan(vd-vr[0,0])
    psid=arctan2(dp[1,0],dp[0,0])
 

    Rd = eulermat(phid,thetad,psid) # la matrice de rotation désirée dans le repère de Euler.
    # adj_wrd = adjoint(wrd)
    ER = Rd.T @ R - R.T @ Rd # fonctionne bien pour la majorité des cas de trajectoires simples ou statiques, avec un bon paramétrage des constantes
    # ER = (Rd-R) # très instable pour le suivi avec van der pol
    adj_wrd = 30*inv(R)@ER

    # Extraction du vecteur (opération vex)
    wrd = array([[adj_wrd[2, 1]], 
                 [adj_wrd[0, 2]], 
                 [adj_wrd[1, 0]]])

    # R=expw(dt*wrd)@Rd
    # wrd = array([[0],[0],[0]])
    # wrd=50*inv(R)@(array([[phid-phi],[thetad-theta],[psid-psi]]))

    Kp = 50
    t123 = np.cross(wr,I@wr,axis=0) + Kp*I@(wrd - wr) #  adjoint(wr) @ (I @ wr) + Kp * (I @ (wrd - wr))

    td = array([[t0], t123[0], t123[1], t123[2]])

    w = sqrt(abs(inv(B)@td)) * sign(inv(B)@td)

    # wr=array([[6],[6],[5],[5]])

    return w


def f_vanderpol(p):
    x,y,z = p.flatten()
    dx = y
    dy = -(0.001*(x**2)-1)*y-x
    return array([[dx],[dy]])

p = array([[0], [0], [-5]])  #x,y,z (front,right,down) -> position d'équilibre instable avec van der pol
p = array([[-40.0], [0.0], [-5.0]])  

R = eye(3)
vr = array([[0], [0], [0]])
wr = array([[0], [0], [0]])
α=array([[0,0,0,0]]).T #angles for the blades

historique_p = [] # Pour stocker la trajectoire
ax_lim = 100

for t in arange(0,15,dt):
    w=control(p, R, vr, wr)
    p, R, vr, wr = clock_quadri(p, R, vr, wr, w)
    historique_p.append(p.flatten())
    
    if int(t/dt) % 10 == 0:

        clean3D(ax, -ax_lim, ax_lim, -ax_lim, ax_lim, 0, ax_lim)
        draw_quadrotor3D(ax, p, R, α, 5 * l)

        traj = np.array(historique_p)
        ax.plot(-traj[:,0], traj[:,1], -traj[:,2], color='blue')
        # ax.view_init(elev=0, azim=-90) # vue de côté (plan xz)

        
        pause(0.001)

    α = α + dt * 30 * w
pause(1)


