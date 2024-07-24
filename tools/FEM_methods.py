import numpy as np
import numpy.linalg as lin
import meshpy.triangle as triangle


# mesh creation

def create_mesh(numTriangles):

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
	return mesh