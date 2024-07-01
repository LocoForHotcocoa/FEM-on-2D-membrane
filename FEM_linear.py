import numpy as np
import numpy.linalg as lin
import matplotlib.pyplot as plt
import matplotlib.animation as ani

import os
import math

# important! put file path for ffmpeg here 
plt.rcParams['animation.ffmpeg_path'] = '/Users/matthewbradley/Downloads/ffmpeg'

# Amount of elements
N = 20

# Amount of nodes
n = N + 1

# Element size
h = 1.0/N

# Constant
c = 1

# Delta time
dt = 0.001

# Amount of iterations
iterations = 20000

# Stepsize, how many iterations per frame in animation
stepSize = 100


# Time coefficient matrix
T = np.zeros((n, n))

T[0, 0] = 1; # Left boundary
T[N, N] = 1; # Right boundary

for i in range(1, N):
    for j in range(0, N+1):
        if(i==j):
            T[i, j] = (2.0/3.0)*h
        if(abs(i-j) == 1):
            T[i, j] = (1.0/6.0)*h

# Space coefficient matrix
S = np.zeros((n, n))

for i in range(1, N):
    for j in range(0, N+1):
        if(i==j):
            S[i, j] = (2.0/h)
        if(abs(i-j)== 1):
            S[i, j] = -(1.0/h)


# A single time step from U(t) -> U(t+dt) and U'(t) -> U'(t+dt)
def iteration(v, vDer):
    vNew = v + dt*vDer
    q = -c*c*S@v
    r = lin.solve(T, q)
    vDerNew = vDer + dt*r
    return (vNew, vDerNew)

# The real solution
def realU(x, t):
    return np.cos(2*np.pi*t)*np.sin(2*np.pi*x)

# The initial value of the finite element problem
u = np.zeros((n, 1))
uDer = np.zeros((n, 1))

for i in range(0, n):
    x = i*h
    u[i] = realU(x, 0)
    

# calculating all values
data = []
data.append(u)

for i in range(0, iterations):
    (uNew, uDerNew) = iteration(u, uDer)
    u = uNew
    uDer = uDerNew
    if iterations % stepSize == 0:
        data.append(u)

spacing = np.linspace(0.0, 1.0, n) # for FEM solution
bigspacing = np.linspace(0.0, 1.0, 100) # for real solution

#-----------------------------------------------------------------

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 1), ylim=(-1.7, 1.7))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    line.set_data(spacing, data[i])
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = ani.FuncAnimation(fig, animate, init_func=init,
                               frames=iterations, interval=2, blit=True)

plt.show()