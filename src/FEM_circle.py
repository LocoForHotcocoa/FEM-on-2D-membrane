import numpy as np
import numpy.linalg as lin
import meshpy.triangle as triangle
import math
import os

from tools.FEM_methods import *
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import matplotlib.animation as ani

def animate_2D(iterations, c, numTriangles, dt, dir, show, save):
      
	# constants
	# numTriangles = 30
	# c = 4
	# dt = 0.001

	# iterations = 20000
	stepSize = 50

	# save = True # choose to save the animation as a file
	# dir = 'animations' # folder name to store animations
	filename = f'FEM_tri_{numTriangles}_i_{iterations}_dt_{dt}_c_{c}.mp4' # animation file name

	fps = int(1/(dt*stepSize))


	#
	## Mesh Creation ---------------------------------------------------------------------------------------------------- ##
	#

	mesh = create_mesh(numTriangles)


	# Extract list of vertices and triangles from mesh
	vertices = np.array(mesh.points)
	triangles = np.array(mesh.elements)

	# make things easy, seperate (x,y) tuple into seperate list of xs and ys for each vertex
	xs = vertices[:,0]
	ys = vertices[:,1]

	# extract boundary point information. for each vertex, 0 = inside, 1 = on boundary
	bs = np.array(mesh.point_markers)

	#
	## Math ---------------------------------------------------------------------------------------------------- ##
	#
	# our canonical element is the triangle that spans the points:
	# (0,0), (0,1), and (1,0)
	#
	# in this element, we use a set of 
	# 3 canonical basis functions phi(x,y) where:
	# phi_1 = 1 - x - y
	# phi_2 = x
	# phi_3 = y
	#
	# then, over our canonical element:
	#
	#	integral of (phi_i * phi_j * dA)
	#	gives us A[i,j]:
	A = [[1/12 , -1/24, -1/24],
		[-1/24, 1/4  , 1/8  ],
		[-1/24, 1/8  , 1/12]]
	
	# 	and integral of (np.dot(grad(phi_i), grad(phi_j)) * dA)
	#	gives us Ad[i,j]:
	Ad = [[1   , -1/2, -1/2],
		 [-1/2, 1/2 , 0   ],
		 [-1/2, 0   , 1/2 ]]
	# to transform any element into the canonical element, we need this:
	# J = (x2 - x1)(y3 - y1) - (x3 - x1)(y2 - y1)
	# this is discussed further in the referenced paper

	# all we need to do is create (n,n) T & S matrices
	# (n = # of vertices in mesh), and iterate over all triangles. 
	#
	# vertices that are shared with multiple triangles will have their T & S values summed.
	#
	# T[n,m] += J*A[i,j]
	# S[n,m] += J*Ad[i,j]

	print('populating matrices...\n')
	
	# number of elements
	N = len(triangles)

	# number of points
	n = len(vertices)

	# local basis integrals


	T = np.zeros((n, n))
	S = np.zeros((n, n))

	for [ind1, ind2, ind3] in triangles:

		# (ind1, ind2, ind3) are the indices for each point on 1 triangle.
		# xs[ind] and ys[ind] will give x and y values for that index.

		inds = [ind1, ind2, ind3]
		# calculate J for this specific triangle
		J = (xs[ind2]-xs[ind1])*(ys[ind3]-ys[ind1]) - (xs[ind3] - xs[ind1])*(ys[ind2] - ys[ind1])

		# now cycle through each (i,j) pair in A, Ad 
		# to update T, S with the specific J for the current element
		for i in range(0, 3):
			for j in range(0, 3):
				T[inds[i], inds[j]] += J*A[i][j]
				S[inds[i], inds[j]] += J*Ad[i][j]
				

	# boundary condition:
	# if point is on boundary (bs[i] = 1), 
	# then set S[i:] = 0, T[i:] = 0, T[i,i] = 1
	for i in range(0, n):
		if(bs[i]):
			for j in range(0, n):
				S[i,j] = 0
				if(i == j):
					T[i, j] = 1
				else:
					T[i, j] = 0

	# iterate through time using first order approximation
	def iteration(v, vDer):
		vNew = v + dt*vDer
		q = -c*c*S@v
		r = lin.solve(T, q)
		vDerNew = vDer + dt*r
		return (vNew, vDerNew)

	# initial value function u(x,0)
	# TODO: need to find a way to vary this function or make it a user input
	def initialU(x, y):
		return math.e - math.exp(x*x + y*y)

	u = np.zeros((n, 1))
	uDer = np.zeros((n, 1))

	# filling in initial data for each element, 
	# making sure that u[boundary] == 0.
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

	# populating data for entire timespan of simulation
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


	if save:
		if not os.path.exists(dir):
			os.mkdir(dir)

		writer=ani.FFMpegWriter(bitrate=5000, fps=fps)
		anim.save(dir + '/' + filename, writer=writer)
		print(f'saving animation to {dir}/{filename}')

	if show:
		plt.show()


