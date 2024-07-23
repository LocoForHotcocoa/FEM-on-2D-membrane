import numpy as np
import numpy.linalg as lin
import meshpy.triangle as triangle
import math
import os

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import matplotlib.animation as ani


# constants

numTriangles = 30
c = 4
dt = 0.001
iterations = 20000
stepSize = 50

save = True # choose to save the animation as a file
dirname = 'animations' # folder name to store animations
filename = f'FEM_wave_equation_tri_{numTriangles}_i_{iterations}_dt_{dt}_c_{c}.mp4' # animation file name

fps = int(1/(dt*stepSize))

#
## Mesh Creation ---------------------------------------------------------------------------------------------------- ##
#

def round_trip_connect(start, end):
	result = []
	for i in range(start, end):
		result.append((i, i+1))
	result.append((end, start))
	return result

# Points list defines boundary
print('defining boundary...\n')
points = []
points.extend((np.cos(angle),  np.sin(angle)) for angle in np.linspace(0, 2*np.pi, numTriangles, endpoint=False))

info = triangle.MeshInfo()
info.set_points(points)
info.set_facets(round_trip_connect(0, len(points)-1))


#Here you build mesh
print('building mesh...\n')
mesh = triangle.build(info, max_volume=1e-2, min_angle=25)


# Extract vertices and triangles
vertices = np.array(mesh.points)
triangles = np.array(mesh.elements)

# make things easy, list of all x and y coordinates
xs = vertices[:,0]
ys = vertices[:,1]

# extract boundary points. 0 = inside, 1 = on boundary
bs = np.array(mesh.point_markers)

#
## Math ---------------------------------------------------------------------------------------------------- ##
#

print('populating matrices...\n')


# number of elements
N = len(triangles)

# number of points
n = len(vertices)

# local basis integrals

A = [[1/12 , -1/24, -1/24],
	 [-1/24, 1/4  , 1/8  ],
	 [-1/24, 1/8  , 1/12]]


Ad = [[1   , -1/2, -1/2],
	  [-1/2, 1/2 , 0   ],
	  [-1/2, 0   , 1/2 ]]

T = np.zeros((n, n))
S = np.zeros((n, n))

for [ind1, ind2, ind3] in triangles:
    inds = [ind1, ind2, ind3]
    J = (xs[ind2]-xs[ind1])*(ys[ind3]-ys[ind1]) - (xs[ind3] - xs[ind1])*(ys[ind2] - ys[ind1])
    for i in range(0, 3):
        for j in range(0, 3):
            T[inds[i], inds[j]] += J*A[i][j]
            S[inds[i], inds[j]] += J*Ad[i][j]
            
for i in range(0, n):
    if(bs[i]):
        for j in range(0, n):
            S[i,j] = 0
            if(i == j):
                T[i, j] = 1
            else:
                T[i, j] = 0


def iteration(v, vDer):
	vNew = v + dt*vDer
	q = -c*c*S@v
	r = lin.solve(T, q)
	vDerNew = vDer + dt*r
	return (vNew, vDerNew)

# initial value

def initialU(x, y):
	return math.e - math.exp(x*x + y*y)

u = np.zeros((n, 1))
uDer = np.zeros((n, 1))

for i in range(0, n):
	if(not bs[i]):
		u[i] = initialU(xs[i], ys[i])
	else:
		u[i] = 0
	uDer[i] = 0
      
# iteration
print('iterating FEM...\n')

data = []
data.append(u)

for i in range(0, iterations):
	(uNew, uDerNew) = iteration(u, uDer)
	u = uNew
	uDer = uDerNew
	if i % stepSize == 0:
		data.append(u)


print('plotting solution...\n')
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

z = [val[0] for val in data[0]]
surf = ax.plot_trisurf(xs, ys, z, triangles=triangles, cmap=plt.cm.YlGnBu_r)

# --------------------------------------------------------
# animation

def animate(i):
	ax.clear()
	ax.set_zlim([-2,2]) # arbitrary, you can change this if you want
	ax.set_xlabel("x")
	ax.set_ylabel("y")
	ax.set_zlabel("u")
	z = [val[0] for val in data[i]]

	surf = ax.plot_trisurf(xs, ys, z, triangles=triangles, cmap=plt.cm.YlGnBu_r)
	return surf,

anim = ani.FuncAnimation(fig, animate, frames=math.floor(iterations / stepSize),
                         interval=2, blit=False)


if save == True:
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    writer=ani.FFMpegWriter(bitrate=5000, fps=fps)
    anim.save(dirname + '/' + filename, writer=writer)
    print(f'saving animation to {dirname}/{filename}')

plt.show()


