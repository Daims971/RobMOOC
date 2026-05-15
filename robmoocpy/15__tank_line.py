from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

# def f(X,u):
#     θ=X[2,0]
#     return array([[cos(θ)], [sin(θ)],[u]])

def f(X,u):
    X=X.flatten()
    u=u.flatten()
    x,y,θ,v = X[0], X[1], X[2], X[3]

    return array([[v*cos(θ)], [v*sin(θ)],[u[1]], [u[0]-v]])


X=array([[-20],[-10],[4],[0]])
u=array([[1],[0.1]])
a,b = array([[-30],[-4]]), array([[30],[6]])

a1=3
a2=1
b1=1
b2=2

vd=50
θd=arctan2(b[1,0]-a[1,0], b[0,0]-a[0,0])

ab=array([[b[0,0]-a[0,0]],[b[1,0]-a[1,0]]])
nab=sqrt(ab[0,0]**2 + ab[1,0]**2)
iab= array([[ab[0,0]/nab],[ab[1,0]/nab]])

am=array([[X[0,0]-a[0,0]],[X[1,0]-a[1,0]]])
print("am=",am)

mh= np.dot(am.T,iab)
print("mh=",mh)

mh_bis = np.dot(am.flatten(),iab.flatten())
print("mh_bis=",mh_bis)

E =[]
i=0

#### ------------- Random line building

A = []
B = []

a0 = array([[-30],[-4]])
Aj = [a0]

line_size = 15
jmax=5
for j in arange(0,jmax):
    xaj=np.random.uniform(-line_size,line_size)
    yaj=np.random.uniform(-line_size,line_size)
    xbj=np.random.uniform(-line_size,line_size)
    ybj=np.random.uniform(-line_size,line_size)

    # print("a=",[xaj,yaj])
    # print("b=",[xbj,ybj])

    A.append([xaj,yaj])
    B.append([xbj,ybj])

    print("A=",A)

    bj = array([[xbj], [ybj]])
    # bj = [xbj, ybj]
    Aj.append(bj)
    # Aj = hstack((Aj,bj))

# print("Aj=",Aj)
# print("Aj[0]=",Aj[0])
# print("array([[A[0][0]],[A[0][1]]])=",array([[A[0][0]],[A[0][1]]]))


#### ------------- Robot building

m= 4 # number of robots
# X=array([[-20],[-10],[4],[0]])
XX=array([-20*ones(m),-10*ones(m),4*ones(m),0*ones(m)])
print("XX=",XX)

MJ =zeros(m) # save the line number j that a robot i_m follows. This will allow each robot to follow its own line
# print("MJ=",MJ)
MJ=MJ.flatten().astype(int)
# print("MJ=",MJ)

Vd = np.linspace(10,vd,m) # speed target for each robot
print("Vd=",Vd)



#### ------------- Simulation

dt= 0.1
T = 100
j=0

ax=init_figure(-40,40,-40,40)

for t in arange(0,T,dt):
    clear(ax)
    
    for i in range(len(Aj)-1):
        a = Aj[i]
        b = Aj[i+1]
        plot2D(hstack((a,b)),'green')
        plot2D(a,'go')
        plot2D(b,'go')

    for i in range(m):
        # print("i=",i)

        if MJ[i] >= jmax:
            break

        else:
            X=XX[:,i].reshape(4,1)
            draw_tank(X,'darkblue')
            
            a = Aj[MJ[i]]
            b = Aj[MJ[i]+1]

            plot2D(hstack((a,b)),'red')
            plot2D(a,'ro')
            plot2D(b,'ro')

            ab=array([[b[0,0]-a[0,0]],[b[1,0]-a[1,0]]])

            nab=sqrt(ab[0,0]**2 + ab[1,0]**2) # norm of the vector ab
            iab= array([[ab[0,0]/nab],[ab[1,0]/nab]]) # unit vector in the direction of ab
            # print("iab=",iab)

            jab = array([[-iab[1,0]], [iab[0,0]]]) # unit normal vector of iab

            am=array([[X[0,0]-a[0,0]],[X[1,0]-a[1,0]]])
            # print("am=",am)

            mh= np.dot(am.T,iab)
            # print("mh=",mh)

            nam = sqrt(am[0,0]**2 + am[1,0]**2)

            # e = sqrt( nam**2 - np.dot(am.flatten(),iab.flatten())**2)
            # e = np.linalg.det([iab, am])
            e = np.dot(am.T, jab)[0,0]

            # E.append(e)

            θd = arctan2(b[1,0]-a[1,0], b[0,0]-a[0,0]) - arctan(e)

            mb = array([[b[0,0]-X[0,0]],[b[1,0]-X[1,0]]])

            if np.dot(ab.T,mb) < 0:
                u1 = 0
                u2 = 0
                # if i == m-1:
                    # j=j+1
                MJ[i] = MJ[i]+1
                if MJ[i] >= jmax:
                    break
            else:
                if (i<m-1) and (MJ[i] == MJ[i+1]): # wait a robot i to finish a line to start robot i+1
                    u1=0
                    u2=0
                else:
                    u1= a1*tanh(Vd[i]-X[3,0]) #-tanh((m-i)/m)
                    u2= a2*sawtooth(θd-X[2,0])
                    # u2= a2*(θd-X[2,0])

            u=array([[u1],[u2]])

            X   = X+dt*f(X,u)
            XX[:,i] = X.flatten() # Update the state in XX for the next iteration


# figure()
# plot(arange(0,T,dt),E)
# time_array = arange(0, T, dt) # On prends les N premiers éléments du temps, ou on s'assure que tout match
# plot(time_array[:len(E)], E) 

# show()