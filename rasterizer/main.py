from PIL import Image
import random
import time
import math
import objconverter

width = 3440
height = 1440

def dot(a,b):
    return(a[0]*b[0]+a[1]*b[1])

def add_tuples(a,b):
    return(a[0]+b[0],a[1]+b[1])

def point_on_right_side_of_line(a,b,p):
    dir = (a[0]-b[0],a[1]-b[1])
    perp_dir = (-dir[1],dir[0])
    ap_diff = (a[0]-p[0],a[1]-p[1])
    return(dot(ap_diff,perp_dir) >= 0)

def point_in_triangle(a,b,c,p):
    trueab = point_on_right_side_of_line(a,b,p)
    truebc = point_on_right_side_of_line(b,c,p)
    trueca = point_on_right_side_of_line(c,a,p)
    if trueab and truebc and trueca:
        return(True)
    else:
        return(False)

def draw_image():
    triangle_points_2d = []
    for triangle in triangle_points:
        triangle_points_2d.append(triangle_3d_to_screenspace(triangle))
    for triangle_i in range(len(triangle_points_2d)):
        min_x = int(max(min(triangle_points_2d[triangle_i][0][0],triangle_points_2d[triangle_i][1][0],triangle_points_2d[triangle_i][2][0],width),0))
        max_x = int(min(max(triangle_points_2d[triangle_i][0][0],triangle_points_2d[triangle_i][1][0],triangle_points_2d[triangle_i][2][0],0),width))
        min_y = int(max(min(triangle_points_2d[triangle_i][0][1],triangle_points_2d[triangle_i][1][1],triangle_points_2d[triangle_i][2][1],height),0))
        max_y = int(min(max(triangle_points_2d[triangle_i][0][1],triangle_points_2d[triangle_i][1][1],triangle_points_2d[triangle_i][2][1],0),height))
        for x in range(min_x,max_x+1):
            for y in range(min_y,max_y):
                if point_in_triangle(triangle_points_2d[triangle_i][0],triangle_points_2d[triangle_i][1],triangle_points_2d[triangle_i][2],(x,y)):
                    img.putpixel((x,y),triangle_colors[triangle_i])

def triangle_3d_to_screenspace(triangle):
    pixels_per_unit = 250
    offset = (width//2,height//2)
    new_triangle = []
    for point in triangle:
        new_triangle.append((point[0] * pixels_per_unit+offset[0], point[1] * pixels_per_unit+offset[1]))
    return(new_triangle)

cube = objconverter.import_model("models/cube.obj")

oringinal_triangle_points = cube.to_triangles()
triangle_points = [list(tri) for tri in oringinal_triangle_points]
triangle_colors = []

for i in range(len(triangle_points)):
    triangle_colors.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

def update_image(pitch,yaw):
    i_hat = (math.sin(yaw), 0, -math.cos(yaw))
    j_hat = (math.cos(yaw)*math.sin(pitch), math.cos(pitch), math.sin(yaw)*math.sin(pitch))
    k_hat = (math.cos(yaw)*math.cos(pitch), -math.sin(pitch), math.sin(yaw)*math.cos(pitch))
    for triangle_i in range(len(oringinal_triangle_points)):
        new_triangle = []
        for point in oringinal_triangle_points[triangle_i]:
            x = point[0]*i_hat[0] + point[1]*j_hat[0] + point[2]*k_hat[0]
            y = point[0]*i_hat[1] + point[1]*j_hat[1] + point[2]*k_hat[1]
            z = point[0]*i_hat[2] + point[1]*j_hat[2] + point[2]*k_hat[2]
            new_triangle.append((x,y,z))
        triangle_points[triangle_i] = new_triangle

pitch = 0
yaw = 0

for i in range(500):
    img = Image.new("RGB", (width,height), color=(0,0,0))

    start = time.perf_counter()

    draw_image()

    yaw += 0.05
    pitch += 0.01
    update_image(pitch,yaw)

    img.save(f"images\image{i:05d}.bmp", format="bmp")

    end = time.perf_counter()

    print(f"Image gen {i} done in  {end - start} seconds!")