import tensorflow as tf
from roblib import *
import os

def draw_boat(X,t,col='darkblue'):
    if (t-t//1>0.01): return()
    draw_tank(X,col,0.25,0.3)
    plot([-30,30], [0,0], 'red')
    pause(0.001)

def control(X):
    x,y,θ,v=tolist(X)
    u=array([[tanh(1-v)],[-0.1]])
    return u

def control_2(X):
    x,y,θ,v=tolist(X)
    A=array([[1,1],[1, -1]])
    V=array([[tanh(1-v)],[sin(-tanh(y/10)-θ)]])
    u=(1/3)*np.dot(A,V)
    
    return u

def make_phi_hat():
    local_path = os.path.dirname(os.path.abspath(__file__)) # os.getcwd() #
    model_path = os.path.join(local_path, 'phi_hat_model.keras')
    data_path = os.path.join(local_path, 'deepboatdata.txt')

    if os.path.exists(model_path):
        print("Loading existing model...",flush=True)
        return tf.keras.models.load_model(model_path)
    
    else:
        if os.path.exists(data_path):
            print("Training new model...",flush=True)
            
            phi_hat_model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(5,)),
                tf.keras.layers.Dense(16, activation='relu'),
                tf.keras.layers.Dense(16, activation='relu'),
                tf.keras.layers.Dense(16, activation='relu'),
                tf.keras.layers.Dense(3)
            ])

            phi_hat_model.compile(optimizer='adam', loss='mse')
            exp_data = np.loadtxt(data_path)
            X_train = exp_data[:, :5]
            y_train = exp_data[:, 5:]
            phi_hat_model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)

            # we should save the generated model to use it later
            phi_hat_model.save(model_path)

            return phi_hat_model
    
        elif not os.path.exists(data_path):
            print("Error: deepboatdata.txt not found.",flush=True)
            return None

def phi_hat(vx,vy,w,u1,u2, phi_hat_model):
    input_data = np.array([[vx, vy, w, u1, u2]])
    dvx, dvy, dw = phi_hat_model.predict(input_data, verbose=0)[0]
    # sortie = tolist(phi_hat_model.predict(input_data).flatten())
    return dvx, dvy, dw


def f_deepboat(X,u, phi_hat_model):
    x,y,theta,vx,vy,w = tolist(X)
    u1,u2 = tolist(u)
    dvx, dvy, dw = phi_hat(vx,vy,w,u1,u2, phi_hat_model)

    R_theta = array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
    dpos = np.dot(R_theta, array([[vx],[vy]]))
    dx, dy = tolist(dpos)
    dtheta = w

    return array([[dx],[dy],[dtheta],[dvx],[dvy],[dw]])
    

#**************************************************************************************************

def SimuDubins():
    def f_dubins(X,u):
        u1,u2=tolist(u)
        θ,v=tolist(X[2:4])
        dX=array([[v*cos(θ)],[v*sin(θ)],[u1-u2],[u1+u2]])
        return dX
    X=array([[-30],[-10],[-1],[0]])  #x,y,theta,v
    for t in arange(0,50,dt):
        draw_boat(X,t)
        u=control_2(X) #x,y,θ,v
        X=X+dt*f_dubins(X,u)


def SimuModelApprox():
    phi_hat_model = make_phi_hat()
    
    X=array([[-30],[-10],[-1],[0],[0],[0]])  #x,y,theta,vx,vy,w
    for t in arange(0,50,dt):
        draw_boat(X,t,'yellow')
        u=control_2(X[0:4]) #x,y,θ,v
        X=X+dt*f_deepboat(X,u,phi_hat_model)


def SimuModelReal():
    def f_real(X,u):
        
        x,y,theta,vx,vy,w = tolist(X)
        u1,u2 = tolist(u)

        R_theta = array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        dpos = np.dot(R_theta, array([[vx],[vy]]))
        dx, dy = tolist(dpos)
        dtheta = w

        dvx = -(1/20)*vx + u1 + (4/5)*u2
        dvy = -(1/10)*vy - w*vx
        dw = u1-(4/5)*u2-3*w

        dX=array([[dx],[dy],[dtheta],[dvx],[dvy],[dw]])
        return dX
    
    X=array([[-30],[-10],[-1],[0],[0],[0]])  #x,y,theta,vx,vy,w
    for t in arange(0,50,dt):
        draw_boat(X,t,'green')
        u=control_2(X[0:4]) #x,y,θ,v
        X=X+dt*f_real(X,u)


dt=0.1
ax=init_figure(-35,20,-20,20)

SimuDubins() #blue

pause(2)

SimuModelApprox() #yellow

pause(2)

SimuModelReal() #green

# pause(10)
show()
