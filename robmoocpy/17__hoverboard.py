from roblib import *

def draw_hoverboard(ax,x,β,col,w):
    def draw_wheel(x,y,θ,ρ,col='darkblue',w=1):
        wheel = zeros((3, 0))
        for i in range(18):
            k = i*pi/8
            rayon = array([[ρ*cos(k)], [ρ*sin(k)], [1]])
            wheel = hstack((wheel, rayon, array([[0], [0], [1]]), rayon))
        wheel = array([[cos(θ),-sin(θ),x], [sin(θ),cos(θ),y], [0,0,1]]) @ wheel
        plot2D(wheel, col,w)
    def draw_board(x,y,θ,β,col='red',w=1):
        board = array([[-1,1,0,0],[0,0,0,3],[1,1,1,1]])
        board=tran2H(x,y)@rot2H(θ+β)@board
        plot2D(board, col,w)
    s,θ,ds,dθ=list(x[0:4,0])
    M = add1(array([[0,0.6,1,0,-1,-0.6,0], [0,0.6,5,5.4,5,0.6,0]]))
    M = tran2H(-ρ*s,ρ)@rot2H(θ)@M
    ax.plot([-10,20],[0,0],col)
    plot2D(M,col,w)
    draw_wheel(-ρ*s,ρ,s,ρ,'darkblue',w)
    draw_board(-ρ*s,ρ,θ,β,'red',w=1)
    pause(0.01)

def f(x,u):
    s,θ,v,w=list(x[0:4,0])
    den=μ4+μ3**2*sin(θ)**2
    dv = (μ3*(μ2*w**2-μg*cos(θ))*sin(θ)+(μ2+μ3*cos(θ))*u)/den
    dw = ((μ1*μg-μ3**2*w**2*cos(θ))*sin(θ)-(μ1+μ3*cos(θ))*u)/den
    return array([[v],[w],[dv],[dw]])

def g(x,u,β):
    s,θ,v,w=list(x[0:4,0])
    dv = f(x,u)[0,0]
    δ=θ+β
    am=array([[cos(δ),sin(δ)],[-sin(δ),cos(δ)]])@array([[dv],[g0]])
    return am,w

m,M,l,g0,ρ=10,1,1,9.81,1
μ1,μ2,μ3,μg=(3/2)*M*ρ**2+m*ρ**2,2*m*l**2,ρ*m*l,g0*l*m
μ4=3*ρ**2*m*M*l**2+ρ**2*m**2*l**2
dt=0.05

ax = init_figure(-5,5, -2,7)
x=array([[0],[0.1],[0],[0]])
for t in arange(0,2,dt):
    s,θ,v,w=list(x[0:4,0])
    β=0.1
    u=0
    am,wm=g(x,u,β)
    x=x+dt*f(x+(dt/2)*f(x,u),u)
    clear(ax)
    draw_hoverboard(ax,x,β,'black',1)
pause(1)

