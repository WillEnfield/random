from PIL import Image
import numpy as np
import pygame
import random
import time
import math
import models

pygame.init()

width = 344
height = 144

screen = pygame.display.set_mode((width*10, height*10))

print("Starting rasterizer...")

depths = np.full((height, width), float('inf'), dtype=np.float32)

def dot(a,b):
    return(a[0]*b[0]+a[1]*b[1])

def add_tuples(a,b):
    return(a[0]+b[0],a[1]+b[1])

def add_tuples_3d(a,b):
    return(a[0]+b[0],a[1]+b[1],a[2]+b[2])

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

def draw_image(fov,camera_offset):
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    triangle_points_2d = []
    triangle_bounds = []
    for triangle in triangle_points:
        built_triangle = []
        for point in triangle:
            built_triangle.append(point_to_screenspace(add_tuples_3d(point,camera_offset),fov))
        triangle_points_2d.append([built_triangle[0],built_triangle[1],built_triangle[2]])

        min_x = int(max(min(built_triangle[0][0], 
                            built_triangle[1][0], 
                            built_triangle[2][0], width-1), 1))
        max_x = int(min(max(built_triangle[0][0], 
                            built_triangle[1][0], 
                            built_triangle[2][0], 1), width-1))
        min_y = int(max(min(built_triangle[0][1], 
                            built_triangle[1][1], 
                            built_triangle[2][1], height-1), 1))
        max_y = int(min(max(built_triangle[0][1], 
                            built_triangle[1][1], 
                            built_triangle[2][1], 1), height-1))
        
        triangle_bounds.append((min_x,max_x,min_y,max_y))
    for triangle_i in range(len(triangle_points_2d)):
        p0, p1, p2 = triangle_points[triangle_i]
        if p0[2] > 0 or p1[2] > 0 or p2[2] > 0:
            continue
        
        min_x, max_x, min_y, max_y = triangle_bounds[triangle_i]

        z0, z1, z2 = -p0[2], -p1[2], -p2[2]

        for x in range(min_x,max_x+1):
            for y in range(min_y,max_y):
                in_triangle, depth_weights = point_in_triangle(triangle_points_2d[triangle_i][0],triangle_points_2d[triangle_i][1],triangle_points_2d[triangle_i][2],(x+0.5,y+0.5))
                if not in_triangle:
                    continue
                depth = 1/max((depth_weights[0]/z0 + depth_weights[1]/z1 + depth_weights[2]/z2) - 1e-6,0.000001)
                if  depth <= depths[y][x]:
                    img_array[y][x] = triangle_colors[triangle_i]
                    depths[y][x] = depth
    return(img_array)

def point_to_screenspace(point,fov):

    screen_height_world = math.tan(fov/2)*2

    pixels_per_unit = height/screen_height_world/point[2]
    offset = (width//2,height//2)

    new_point = (point[0] * pixels_per_unit + offset[0], point[1] * pixels_per_unit + offset[1])
    return(new_point)

def pil_to_pygame_surface(pil_image):
    return pygame.image.fromstring(
        pil_image.tobytes(),
        pil_image.size,
        pil_image.mode
    )

monkey = models.import_model("models/dragon.obj")
cube = models.import_model("models/cube.obj")

models = [monkey, cube]

oringinal_triangle_points = monkey.to_triangles() + cube.to_triangles()
triangle_points = [list(tri) for tri in oringinal_triangle_points]
triangle_colors = []

for i in range(len(triangle_points)):
    triangle_colors.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

i = 0

running = True
performances = []


movement_vec = (0,0,0)
camera_offset = (0,0,0)

while running:
    i += 1

    movement_vec = (0,0,0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
                movement_vec = add_tuples_3d(movement_vec,(0,0,-0.1))
        if keys[pygame.K_w]:
                movement_vec = add_tuples_3d(movement_vec,(0,0,0.1))
        if keys[pygame.K_a]:
                movement_vec = add_tuples_3d(movement_vec,(-0.1,0,0))
        if keys[pygame.K_d]:
                movement_vec = add_tuples_3d(movement_vec,(0.1,0,0))
        if keys[pygame.K_e]:
                movement_vec = add_tuples_3d(movement_vec,(0,-0.1,0))
        if keys[pygame.K_q]:
                movement_vec = add_tuples_3d(movement_vec,(0,0.1,0))
        
    camera_offset = add_tuples_3d(camera_offset, movement_vec)

    depths = np.full((height, width), float('inf'), dtype=np.float32)


    start = time.perf_counter()

    triangle_points = monkey.rotate(0,0.01*i).shift((0, 0, 3)).to_triangles() + cube.shift((math.sin(i/40)+3,0,math.cos(i/40)+3)).to_triangles()

    img_array = draw_image(90*math.pi/180,camera_offset)

    img = Image.fromarray(img_array, 'RGB')

    pygame_surface = pil_to_pygame_surface(img)
    scaled_surface = pygame.transform.scale(pygame_surface, (width*10, height*10))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()

    end = time.perf_counter()
    
    performance = end - start

    performances.append(performance)

    print(f"Image gen {i} done {performance} seconds!")


print("Avergage performance:", sum(performances)/len(performances))
pygame.quit()