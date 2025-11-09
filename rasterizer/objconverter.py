import os

class Model:

    def __init__(self):
        self.points = []
        self.faces = [] # defined as point indices

    def to_triangles(self):
        triangles = []
        for face in self.faces:
            for i in range(1, len(face) - 1):
                triangles.append((
                    self.points[face[0]],
                    self.points[face[i]],
                    self.points[face[i + 1]]
                    ))
        return(triangles)

def import_model(file_path):
    model = Model()
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == 'v':
                x, y, z = map(float, parts[1:4])
                model.points.append((x, y, z))
            elif parts[0] == 'f':
                indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                model.faces.append(indices)
    return model