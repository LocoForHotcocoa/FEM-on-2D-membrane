import meshpy.triangle as triangle
import numpy as np

def round_trip_connect(start, end):
	result = []
	for i in range(start, end):
		result.append((i, i+1))
	result.append((end, start))
	return result

# Points list defines boundary
print('defining boundary...')
points = []
points.extend((np.cos(angle),  np.sin(angle)) for angle in np.linspace(0, 2*np.pi, 30, endpoint=False))

info = triangle.MeshInfo()
info.set_points(points)
info.set_facets(round_trip_connect(0, len(points)-1))


#Here you build mesh
print('building mesh...')
mesh = triangle.build(info, max_volume=1e-3, min_angle=25)


# Extract vertices and triangles
vertices = mesh.points
triangles = mesh.elements

triangle_list = []
# Print vertices of each triangle
for triangle_indices in triangles:
    triangle_vertices = [vertices[index] for index in triangle_indices]
    triangle_list.append(triangle_vertices)

print(triangle_list)