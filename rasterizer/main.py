from PIL import Image
import random
import time
import math
import objconverter
import mp4converter

width = 3440
height = 1440

print("Starting rasterizer...")

depths = [ [float('inf')] * width for _ in range(height) ]

def dot(a,b):
    return(a[0]*b[0]+a[1]*b[1])

def add_tuples(a,b):
    return(a[0]+b[0],a[1]+b[1])

def signed_triangle_area(a,b,p):
    dir = (a[0]-b[0],a[1]-b[1])
    perp_dir = (-dir[1],dir[0])
    ap_diff = (a[0]-p[0],a[1]-p[1])
    return(dot(ap_diff,perp_dir) / 2)

def point_in_triangle(a,b,c,p):
    areaab = signed_triangle_area(a,b,p)
    areabc = signed_triangle_area(b,c,p)
    areaca = signed_triangle_area(c,a,p)
    in_triangle = areaab >= 0 and areabc >= 0 and areaca >= 0
    inv_sum = 1/(areaab + areabc + areaca)
    weight_a = areabc * inv_sum
    weight_b = areaca * inv_sum
    weight_c = areaab * inv_sum
    return(in_triangle, (weight_a,weight_b,weight_c))

def draw_image(fov):
    triangle_points_2d = []
    for triangle in triangle_points:
        built_triangle = []
        for point in triangle:
            built_triangle.append(point_to_screenspace(point,fov))
        triangle_points_2d.append([built_triangle[0],built_triangle[1],built_triangle[2]])
    for triangle_i in range(len(triangle_points_2d)):
        if (triangle_points[triangle_i][0][2] > 0 or triangle_points[triangle_i][1][2] > 0 or triangle_points[triangle_i][2][2] > 0):
            continue
        min_x = int(max(min(triangle_points_2d[triangle_i][0][0],triangle_points_2d[triangle_i][1][0],triangle_points_2d[triangle_i][2][0],width-1),1))
        max_x = int(min(max(triangle_points_2d[triangle_i][0][0],triangle_points_2d[triangle_i][1][0],triangle_points_2d[triangle_i][2][0],1),width-1))
        min_y = int(max(min(triangle_points_2d[triangle_i][0][1],triangle_points_2d[triangle_i][1][1],triangle_points_2d[triangle_i][2][1],height-1),1))
        max_y = int(min(max(triangle_points_2d[triangle_i][0][1],triangle_points_2d[triangle_i][1][1],triangle_points_2d[triangle_i][2][1],1),height-1))
        for x in range(min_x,max_x+1):
            for y in range(min_y,max_y):
                in_triangle, depth_weights = point_in_triangle(triangle_points_2d[triangle_i][0],triangle_points_2d[triangle_i][1],triangle_points_2d[triangle_i][2],(x+0.5,y+0.5))
                z0 = -triangle_points[triangle_i][0][2]
                z1 = -triangle_points[triangle_i][1][2]
                z2 = -triangle_points[triangle_i][2][2]
                depth = 1/max((depth_weights[0]/z0 + depth_weights[1]/z1 + depth_weights[2]/z2) - 1e-6,0.000001)
                if in_triangle and depth <= depths[y][x]:
                    img.putpixel((x,y),triangle_colors[triangle_i])
                    depths[y][x] = depth

def point_to_screenspace(point,fov):

    screen_height_world = math.tan(fov/2)*2

    pixels_per_unit = height/screen_height_world/point[2]
    offset = (width//2,height//2)

    new_point = (point[0] * pixels_per_unit + offset[0], point[1] * pixels_per_unit + offset[1])
    return(new_point)

cube = objconverter.import_model("models/dragon.obj")

oringinal_triangle_points = cube.to_triangles()
triangle_points = [list(tri) for tri in oringinal_triangle_points]
triangle_colors = []

for i in range(len(triangle_points)):
    triangle_colors.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

def update_image(pitch,yaw,offset):
    i_hat = (math.sin(yaw), 0, -math.cos(yaw))
    j_hat = (math.cos(yaw)*math.sin(pitch), math.cos(pitch), math.sin(yaw)*math.sin(pitch))
    k_hat = (math.cos(yaw)*math.cos(pitch), -math.sin(pitch), math.sin(yaw)*math.cos(pitch))
    for triangle_i in range(len(oringinal_triangle_points)):
        new_triangle = []
        for point in oringinal_triangle_points[triangle_i]:
            x = point[0]*i_hat[0] + point[1]*j_hat[0] + point[2]*k_hat[0] + offset[0]
            y = point[0]*i_hat[1] + point[1]*j_hat[1] + point[2]*k_hat[1] + offset[1]
            z = point[0]*i_hat[2] + point[1]*j_hat[2] + point[2]*k_hat[2] - offset[2]
            new_triangle.append((x,y,z))
        triangle_points[triangle_i] = new_triangle

pitch = 0
yaw = 0

for i in range(5000):
    depths = [[float('inf')] * width for _ in range(height)]

    img = Image.new("RGB", (width,height), color=(0,-2,0))

    start = time.perf_counter()

    yaw += 00.05
    pitch += 0.01

    update_image(pitch,yaw,(0,-1,3))

    draw_image(90*math.pi/180)

    img.save(f"images2\\image{i:04d}.bmp", format="bmp")

    end = time.perf_counter()

    print(f"Image gen {i} done {end - start} seconds!")

mp4converter.export()