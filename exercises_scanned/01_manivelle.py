from roblib import *
import matplotlib.pyplot as plt
import time 



# Bras du robot"
l1, l2 = 4, 4

# Disque à suivre
c = np.array([[3],[4]])
r = 1

# Modèle de la manivelle

def z_of(x):
    return l1 * np.array([[np.cos(x[0,0])],[np.sin(x[0,0])]])

def y_of(x):
    return z_of(x) + l2 * np.array([[np.cos(x[0,0]+x[1,0])],[np.sin(x[0,0]+x[1,0])]])

def A(x):
    x1 = x[0,0]; x2 = x[1,0]
    A = np.array([[-l1*np.sin(x1)-l2*np.sin(x1+x2), -l2*np.sin(x1+x2)],
                  [ l1*np.cos(x1)+l2*np.cos(x1+x2),  l2*np.cos(x1+x2)]])
    return A

# initialisation et update de la figure
def update_fig(x, seg_line, fig_target):
    z = z_of(x)
    y = y_of(x)
    # Mise à jour de la ligne brisée : (0,0) -> z -> y
    seg_line.set_data([0, z[0,0], y[0,0]], [0, z[1,0], y[1,0]])
    
    # Force le redessin spécifique de cette figure
    fig_target.canvas.draw()


# Mode interactif ON pour l'animation
plt.ion() 

dt = 0.05 # pas de temps de l'animation

# ---------------------------------------------------------
# FIGURE 1 : Trajectoire en boucle ouverte via commande constante
# ---------------------------------------------------------
print("Lancement Figure 1...")
fig1, ax1 = plt.subplots()
ax1.set_xlim(-10, 10); ax1.set_ylim(-10, 10)
ax1.set_aspect('equal')
ax1.grid(True)
ax1.set_title("Figure 1 : Commande constante")

seg1, = ax1.plot([], [], '-o', color='magenta', linewidth=2)
disk1 = plt.Circle((c[0,0], c[1,0]), r, color='cyan', alpha=0.5) # disque de référence à suivre
ax1.add_patch(disk1)

x = np.array([[-1],[2]]) # état initiale
u = np.array([[0],[0]]) # commande initale

for t in np.arange(0, 10, dt): 
    x = x + u*dt
    u = np.array([[1],[0.5]]) # commande constante
    
    update_fig(x, seg1, fig1) 
    plt.pause(0.01)


plt.close(fig1) 
print("Figure 1 fermée, attente de 2s...")
time.sleep(2.0) 

# ---------------------------------------------------------
# FIGURE 2 : Suivi de trajectoire par commande linéarisante
# ---------------------------------------------------------

print("Lancement Figure 2...")
fig2, ax2 = plt.subplots()

ax2.set_xlim(-10, 10); ax2.set_ylim(-10, 10)
ax2.set_aspect('equal')
ax2.grid(True)
ax2.set_title("Figure 2 : Suivi de trajectoire")

seg2, = ax2.plot([], [], '-o', color='magenta', linewidth=2)
disk2 = plt.Circle((c[0,0], c[1,0]), r, color='cyan', alpha=0.5)
ax2.add_patch(disk2)

# plt.show(block=False)
plt.pause(0.5) # On force l'affichage initial et on attend un peu pour laisser le temps à Matplotlib de créer le contexte graphique

print("Démarrage boucle Figure 2...")

x = np.array([[-1],[2]]) # état initiale
u = np.array([[0],[0]]) # commande initale
alpha_1 = 1 # gain de la partie proportionnelle de la loi de commande après placement de poles


for t in np.arange(0, 10, dt): 
    x = x + u*dt
    w = c + r*np.array([[np.cos(t)],[np.sin(t)]]) # consigne de position à suivre, dépend du temps
    wdot = np.array([[-r*np.sin(t)],[r*np.cos(t)]]) # dérivée de la consigne (wdot = dw/dt)
    v = alpha_1*(w - y_of(x)) + wdot # commande après linéarisation
    u = np.dot(np.linalg.inv(A(x)), v) #commande globale
    
    update_fig(x, seg2, fig2)
    plt.pause(0.01)


plt.close(fig2) 
time.sleep(2.0) 

# ---------------------------------------------------------
# FIGURE 3 : Test des points singuliers
# ---------------------------------------------------------


# Test de singularités
l1, l2 = 4*np.sqrt(2), 4
c = np.array([[4],[4]])
r = 4
x = np.array([[np.pi/4],[np.pi/4]]) # état initiale au point singulier (bras tendu vers le haut à 45°)


# Test de singularités 2
# l1, l2 = 4, 4
# c = np.array([[4*np.sqrt(2)],[4*np.sqrt(2)]])
# r = 1
# x = np.array([[np.pi/4],[np.pi/4]]) # état initiale au point singulier (bras tendu vers le haut à 45°)




print("Lancement Figure 3...") 

fig3, ax3 = plt.subplots() 
ax3.set_xlim(-10, 10); 
ax3.set_ylim(-10, 10) 
ax3.set_aspect('equal') 
ax3.grid(True) 
ax3.set_title("Figure 3 : Test des points singuliers") 

seg3, = ax3.plot([], [], '-o', color='magenta', linewidth=2) 
disk3 = plt.Circle((c[0,0], c[1,0]), r, color='cyan', alpha=0.5) 
ax3.add_patch(disk3) 

# plt.show(block=False) 
plt.pause(0.5) # On force l'affichage initial et on attend un peu pour laisser le temps à Matplotlib de créer le contexte graphique

print("Démarrage Figure 3...")

x = np.array([[-1],[2]]) # état initiale
u = np.array([[0],[0]]) # commande initale
alpha_1 = 1 # gain de la partie proportionnelle de la loi de commande après placement de poles


for t in np.arange(0, 20, dt): 
    x = x + u*dt
    w = c + r*np.array([[np.cos(t)],[np.sin(t)]]) # consigne de position à suivre, dépend du temps
    wdot = np.array([[-r*np.sin(t)],[r*np.cos(t)]]) # dérivée de la consigne (wdot = dw/dt)
    v = alpha_1*(w - y_of(x)) + wdot # commande après linéarisation
    u = np.dot(np.linalg.inv(A(x)), v) #commande globale
    
    update_fig(x, seg3, fig3)
    plt.pause(0.01)



plt.ioff()
plt.show()