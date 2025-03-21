import numpy as np
import numpy.linalg as lin
import meshpy.triangle as triangle


# mesh creation

def create_mesh(numTriangles):

    def round_trip_connect(start, end):
        result = [(i, i + 1) for i in range(start, end)]
        result.append((end, start))
        return result

    # Generate boundary points in a circular shape
    numBoundaryPoints = int(2 * np.sqrt(numTriangles))
    points = [(np.cos(angle), np.sin(angle)) for angle in np.linspace(0, 2*np.pi, numBoundaryPoints, endpoint=False)]

    # Define mesh info
    info = triangle.MeshInfo()
    info.set_points(points)
    info.set_facets(round_trip_connect(0, len(points) - 1))

    # Estimate max_volume based on desired triangle count
    area_estimate = np.pi  # Approximate area of the circular domain
    max_volume = area_estimate / numTriangles  # Average triangle area

    # Build the mesh
    mesh = triangle.build(info, max_volume=max_volume, min_angle=30)

    print(f"Generated {len(mesh.elements)} triangles (target: {numTriangles})")

    return mesh