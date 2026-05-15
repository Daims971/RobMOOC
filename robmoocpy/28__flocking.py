from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x=x.flatten()
    θ = x[2]
    return array([[cos(θ)], [sin(θ)], [u]])


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


ax=init_figure(-60,60,-60,60)
m   = 20
X   = 20*randn(3,m)
dt  = 0.2

k1,k2,k3 = 1,0.005,20

for t in arange(0,5*10,dt):
    clear(ax)

    for i in range(m):
        xi=X[:,i].flatten()
        xi=xi.reshape(3,1)

        vhat = array([[0],[0]]) # derivate of phat
        dp = array([[0],[0]]) # variation of phat
        dq = array([[0],[0]]) # variation of qhat

        for j in range(m):
            if i != j:
                xj=X[:,j].flatten()
                xj=xj.reshape(3,1)
                
                # alignment
                vhat = vhat + array([[cos(xj[2,0])],[sin(xj[2,0])]]) # speed

                # cohesion
                dpi = xi[0:2] - xj[0:2]
                dp = dp + dpi
                # dp = dp / norm(dp)

                # repulsion
                dqi = dpi/(norm(dpi)**3)
                dq = dq + dqi


        wi = k1*vhat - 2*k2*dp + k3*dq
        # wi = wi / (m-1)
        # wi = wi / norm(wi) * 1 # normalize and set speed to 1
        wi = wi.flatten()
        thetai = arctan2(wi[1],wi[0])
        u = 2*arctan(tan((thetai-xi[2,0])/2))

        # u=0
        xi=xi+f(xi,u)*dt        
        X[:,i]  = xi.flatten()        
        
        draw_tank(xi,'b')

        
        # if int(t/dt) % 10 == 0:
        #     clear(ax)
        #     draw_tank(xi,'b')


