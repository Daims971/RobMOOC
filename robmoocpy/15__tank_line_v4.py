from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

# def f(X,u):
#     θ=X[2,0]
#     return array([[cos(θ)], [sin(θ)],[u]])

def f(X,u):
    X=X.flatten()
    u=u.flatten()
    x,y,θ,v = X[0], X[1], X[2], X[3]

    
    return array([[v*cos(θ)], [v*sin(θ)],[u[1]], [u[0]-v]])


# X=array([[-20],[-10],[4]])
# u=1

X=array([[-20],[-10],[4],[0]])
u=array([[1],[0.1]])
dt= 0.1
a,b = array([[-30],[-4]]), array([[30],[6]])

a1=3
a2=1
b1=1
b2=2

print("X=",X)
print("X[3,0]=",X[3,0])

vd=50
θd=arctan2(b[1,0]-a[1,0], b[0,0]-a[0,0])

ab=array([[b[0,0]-a[0,0]],[b[1,0]-a[1,0]]])
nab=sqrt(ab[0,0]**2 + ab[1,0]**2)
iab= array([[ab[0,0]/nab],[ab[1,0]/nab]])

print("iab=",iab)


am=array([[X[0,0]-a[0,0]],[X[1,0]-a[1,0]]])
print("am=",am)

mh= np.dot(am.T,iab)
print("mh=",mh)

mh_bis = np.dot(am.flatten(),iab.flatten())
print("mh_bis=",mh_bis)

E =[]
THETA =[0]
i=0


A = []
B = []


a0 = array([[-30],[-4]])
Aj = [a0]

line_size = 15

jmax=10
for j in arange(0,jmax):
    xaj=np.random.uniform(-line_size,line_size)
    yaj=np.random.uniform(-line_size,line_size)
    xbj=np.random.uniform(-line_size,line_size)
    ybj=np.random.uniform(-line_size,line_size)

    print("a=",[xaj,yaj])
    print("b=",[xbj,ybj])

    A.append([xaj,yaj])
    B.append([xbj,ybj])

    print("A=",A)

    bj = array([[xbj], [ybj]])
    # bj = [xbj, ybj]
    Aj.append(bj)
    # Aj = hstack((Aj,bj))

print("Aj=",Aj)
print("Aj[0]=",Aj[0])
print("array([[A[0][0]],[A[0][1]]])=",array([[A[0][0]],[A[0][1]]]))



# X=array([[-20],[-10],[4],[0]])
m= 6 # number of robots
# X=array([4*arange(0,m),zeros(m),ones(m),3*ones(m),zeros(m)])
X=array([4*arange(0,m),-20*ones(m),-10*ones(m),4*ones(m),0*ones(m)])



T = 40
j=0

ax=init_figure(-40,40,-40,40)

for t in arange(0,T,dt):
    clear(ax)
    draw_tank(X,'darkblue')
    
    if j >= jmax:
        break
    # a = array([[A[j][0]],[A[j][1]]])
    # b = array([[B[j][0]],[B[j][1]]])

    
    for i in range(len(Aj)-1):
        a = Aj[i]
        b = Aj[i+1]
        plot2D(hstack((a,b)),'green')
        plot2D(a,'go')
        plot2D(b,'go')

    a = Aj[j]
    b = Aj[j+1]
    plot2D(hstack((a,b)),'red')
    plot2D(a,'ro')
    plot2D(b,'ro')
    # plot2D(hstack((a,b)),'red')
    # plot2D(a,'ro')
    # plot2D(b,'ro')    


        # θd=arctan2(b[1,0]-a[1,0], b[0,0]-a[0,0])

    ab=array([[b[0,0]-a[0,0]],[b[1,0]-a[1,0]]])
    nab=sqrt(ab[0,0]**2 + ab[1,0]**2)
    iab= array([[ab[0,0]/nab],[ab[1,0]/nab]])

    # print("iab=",iab)

    am=array([[X[0,0]-a[0,0]],[X[1,0]-a[1,0]]])
    # print("am=",am)

    mh= np.dot(am.T,iab)
    # print("mh=",mh)

    mh_bis = np.dot(am.flatten(),iab.flatten())
    # print("mh_bis=",mh_bis)

    # psi_d = arctan2(X[1,0]-a[1,0], X[0,0]-a[0,0])
    # delta_d=sqrt((X[0,0]-a[0,0])**2 + (X[1,0]-a[1,0])**2)
    # e_d = delta_d*sin(psi_d)

    am=array([[X[0,0]-a[0,0]],[X[1,0]-a[1,0]]])
    nam = sqrt(am[0,0]**2 + am[1,0]**2)

    n_ab = array([[-iab[1,0]], [iab[0,0]]]) 

    # e = sqrt( nam**2 - np.dot(am.flatten(),iab.flatten())**2)
    # e = np.linalg.det([iab, am])
    e = np.dot(am.T, n_ab)[0,0]
    E.append(e)

    # THETA.append(X[2,0])

    # e=0
    θd = arctan2(b[1,0]-a[1,0], b[0,0]-a[0,0]) - arctan(e) #+ pi/2

    mb = array([[b[0,0]-X[0,0]],[b[1,0]-X[1,0]]])


    if np.dot(ab.T,mb) < 0:
        u1 = 0
        u2 = 0
        j=j+1
        if j >= jmax:
            break
    else:
        u1= a1*tanh(vd-X[3,0])
        u2= a2*sawtooth(θd-X[2,0])
        u2= a2*(θd-X[2,0])
        # u2= a2*sawtooth(θd-X[2,0]) + b2*(sin(X[2,0]))
        # u2=arctan((tan(θd-X[2,0]))/2) - arctan(e)
        # u2=arctan((tan(θd-X[2,0]))/2) 
        # u2= a2*sawtooth(θd-X[2,0]) +b2*(sin(X[2,0]-THETA[i]))/dt
        # u2=arctan2((tan(θd-X[2,0]))/2,1) 


    u=array([[u1],[u2]])

    X   = X+dt*f(X,u)
    i=i+1

figure()
# plot(arange(0,T,dt),E)
time_array = arange(0, T, dt) # On prends les N premiers éléments du temps, ou on s'assure que tout match
plot(time_array[:len(E)], E) 

show()