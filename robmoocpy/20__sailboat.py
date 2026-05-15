from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

         
    
def f(x,u):
    x,u=x.flatten(),u.flatten()
    θ=x[2]; v=x[3]; w=x[4]; δr=u[0]; δsmax=u[1];
    w_ap = array([[awind*cos(ψ-θ) - v],[awind*sin(ψ-θ)]])
    ψ_ap = angle(w_ap)
    a_ap=norm(w_ap)
    sigma = cos(ψ_ap) + cos(δsmax)
    if sigma < 0 :
        δs = pi + ψ_ap
    else :
        δs = -sign(sin(ψ_ap))*δsmax
    fr = p4*v*sin(δr)
    fs = p3*a_ap* sin(δs - ψ_ap)
    dx=v*cos(θ) + p0*awind*cos(ψ)
    dy=v*sin(θ) + p0*awind*sin(ψ)
    dv=(fs*sin(δs)-fr*sin(δr)-p1*v**2)/p8
    dw=(fs*(p5-p6*cos(δs)) - p7*fr*cos(δr) - p2*w*v)/p9
    xdot=array([ [dx],[dy],[w],[dv],[dw]])
    return xdot,δs    

    
def control(x,ab,r,psi,q):

    """

    ab: target_line defined by two points a and b
    a = array([[-50],[-100]])   
    b = array([[50],[100]])
    ab = [a,b]

    r: cutting distance to the target line

    """
    
    x=x.flatten()
    θ=x[2]; v=x[3]; w=x[4]; #δr=u[0]; δsmax=u[1];
    
    #1 cross product between i_ab and (x-a)
    a = ab[0].flatten()
    b = ab[1].flatten()
    i_ab = ((b-a) / np.linalg.norm(b-a)) # director vector from a to b
    am = x[0:2] - a  # vector from a to the boat position
    e = i_ab[0]*am[1] - i_ab[1]*am[0] #1 cross product between i_ab and (x-a)
    #2
    if np.abs(e) > r: 
        q=sign(e)
    # else:
    #     q=1 # could be needed a value othewise there will be an error in the simulation

    #3
    phi = arctan2((b-a)[1],(b-a)[0]) 
    #4
    theta_bar = phi - arctan(e/r) 
    #5 6 7
    gamma = pi/4 # no-go zone angle
    if (cos(psi - theta_bar) + cos(gamma) <0) or ( ((np.abs(e)-r)<0) and (cos(psi-phi)+cos(gamma)<0)):
        theta_bar = -psi - q*gamma
    #8
    δrmax = 1
    δr = (δrmax/pi)*sawtooth(θ-theta_bar)
    #9
    beta=pi/4
    eta=log(pi/(2*beta))/log(2)
    δsmax = (pi/2)*((cos(psi-theta_bar)+1)/2)**eta

    u=array([[δr],[δsmax]])
    return u,q
    
    
p0,p1,p2,p3,p4,p5,p6,p7,p8,p9 = 0.1,1,6000,1000,2000,1,1,2,300,10000
x = array([[10,-40,-3,1,0]]).T   #x=(x,y,θ,v,w)

dt = 0.1
awind,ψ = 2,-2  
a = array([[-50],[-100]])   
b = array([[50],[100]])
b = array([[50],[10]])
r=10
q=1
                  
ax=init_figure(-100,100,-60,60)

for t in arange(0,80,0.1):
    clear(ax)
    plot([a[0,0],b[0,0]],[a[1,0],b[1,0]],'red')
    # u=array([[0],[1]])
    u,q = control(x,[a,b],r,ψ,q)
    xdot,δs=f(x,u)
    x = x + dt*xdot
    draw_sailboat(x,δs,u[0,0],ψ,awind)


"""
4)




"""