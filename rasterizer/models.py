import math


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

    def shift(self, offset):
        shifted_model = Model()
        for point in self.points:
            shifted_model.points.append((
                point[0] + offset[0],
                point[1] + offset[1],
                point[2] - offset[2]
            ))
        shifted_model.faces = self.faces.copy()
        return(shifted_model)
    
    def rotate(self, pitch, yaw):
        i_hat = (math.cos(yaw), 0, -math.sin(yaw))
        j_hat = (math.sin(yaw)*math.sin(pitch), math.cos(pitch), math.cos(yaw)*math.sin(pitch))
        k_hat = (math.sin(yaw)*math.cos(pitch), -math.sin(pitch), math.cos(yaw)*math.cos(pitch))
        rotated_model = Model()
        for point in self.points:
            x = point[0]*i_hat[0] + point[1]*j_hat[0] + point[2]*k_hat[0]
            y = point[0]*i_hat[1] + point[1]*j_hat[1] + point[2]*k_hat[1]
            z = point[0]*i_hat[2] + point[1]*j_hat[2] + point[2]*k_hat[2]
            rotated_model.points.append((x,y,z))
        rotated_model.faces = self.faces.copy()
        return(rotated_model)


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