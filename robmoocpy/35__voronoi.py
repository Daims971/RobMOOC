from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

ax=init_figure(-5,15,-5,15)
m=3
p=10*rand(2,m)

#### 3) Calcul of circumscribed circle of the points

n = m-len(p.T[1]) # number of points 1 to reach a square matrix for A to be able to inverse it
ones_matrix = np.ones((m, n)) # matrix of ones to complete A with the last column of 1
A = np.hstack((2*p.T, ones_matrix))

# row_norms = np.linalg.norm(p.T, axis=1)  # shape (m,)
# norm_a_vect = row_norms[:, None]* row_norms[:, None]  # shape (m, 1)
norm_a_vect_carree = np.sum(p.T**2, axis=1)[:, None]
Cbar = inv(A)@norm_a_vect_carree
c = Cbar[:-1]
r = sqrt(norm(c)**2 + Cbar[-1,0])

draw_disk(ax,c.flatten()[0:2],r,'lightblue')
plot(p[0,:],p[1,:],'ob')
pause(1)

#### 4) Triangulation

dt = 0.1
tmax = 10
T = arange(0,tmax,dt)
def trace_circle(c, r, t):
    cx, cy = c[0,0], c[1,0]  
    x = cx + r*np.cos(t)
    y = cy + r*np.sin(t)
    return array([x, y])      # shape (2, len(t))

ax=init_figure(-5,15,-5,15)
m=10
p=10*rand(2,m)

n = m-len(p.T[1]) 
ones_matrix = np.ones((3, 1))

C=[]
K=[]

for i in range(m-2):
    for j in range(i+1,m-1):
        for k in range(j+1,m):
            A=p.T[[i,j,k],:] # selected triangle
            B=np.hstack((2*A, ones_matrix))
            norm_a_vect_carree = np.sum(A**2, axis=1)[:, None]
            Cbar = inv(B)@norm_a_vect_carree
            # Cbar = norm_a_vect_carree/B
            c = Cbar[:-1]
            r = sqrt(norm(c)**2 + Cbar[-1,0])

            valid_triangle = True
            for l in range(m):
                if l not in [i,j,k]:
                    if norm(p[:,l:l+1] - c) < r:
                        valid_triangle = False
                        break
            if not valid_triangle:
                continue

            if valid_triangle:
                # C= [C,c]
                C.append(c)
                # K= [K,[i,j,k]]
                K.append([i,j,k])

                draw_disk(ax,c.flatten()[0:2],r,'lightblue',0.8)
                trace = trace_circle(c,r,T)
                plot(trace[0,:],trace[1,:],'--g', linewidth = 0.3)
                # plot(A[:,0], A[:,1], 'or')
                draw_polygon(ax, A, 'r')  
                # xs = [A[0,0], A[1,0], A[2,0], A[0,0]] # segments fermés 
                # ys = [A[0,1], A[1,1], A[2,1], A[0,1]]
                # plot(xs, ys, 'r-')    

                plot(p[0,:],p[1,:],'ob')
                pause(0.1)
pause(2)


for i in range(len(K)):
    for j in range(i+1,len(K)):
        if len(set(K[i]) & set(K[j])) == 2: # if they share 2 vertices, they are neighbors
            print(f"Triangle {i} and Triangle {j} are neighbors.")
            plot([C[i][0,0], C[j][0,0]], [C[i][1,0], C[j][1,0]], 'r-', linewidth=2)
pause(3)