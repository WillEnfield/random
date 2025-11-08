from PIL import Image
import random
import time

width = 688
height = 288

triangle_count = 100

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
    if trueab == truebc and truebc == trueca:
        return(True)
    else:
        return(False)

def draw_image():
    for triangle_i in range(triangle_count):
        min_x = max(min(triangle_points[triangle_i][0][0],triangle_points[triangle_i][1][0],triangle_points[triangle_i][2][0],width-1),1)
        max_x = min(max(triangle_points[triangle_i][0][0],triangle_points[triangle_i][1][0],triangle_points[triangle_i][2][0],1),width-1)
        min_y = max(min(triangle_points[triangle_i][0][1],triangle_points[triangle_i][1][1],triangle_points[triangle_i][2][1],height)-1,1)
        max_y = min(max(triangle_points[triangle_i][0][1],triangle_points[triangle_i][1][1],triangle_points[triangle_i][2][1],1),height-1)
        for x in range(min_x,max_x+1):
            for y in range(min_y,max_y):
                if point_in_triangle(triangle_points[triangle_i][0],triangle_points[triangle_i][1],triangle_points[triangle_i][2],(x,y)):
                    img.putpixel((x,y),triangle_colors[triangle_i])

triangle_points = []
triangle_velocities = []
triangle_colors = []

for i in range(triangle_count):
    triangle_points.append([(random.randint(int(width/2),width),random.randint(int(height/2),height)),(random.randint(int(width/2),width),random.randint(int(height/2),height)),(random.randint(int(width/2),width),random.randint(int(height/2),height))])
    triangle_velocities.append((random.randint(-10,-1),random.randint(-10,-1)))
    triangle_colors.append((random.randint(1,255),random.randint(1,255),random.randint(1,255)))


for i in range(100000000):
    img = Image.new("RGB", (width,height), color=(0,0,0))

    start = time.perf_counter()

    draw_image()

    for triangle_i in range(triangle_count):
        velocity = triangle_velocities[triangle_i]
        reverse_x = False
        reverse_y = False
        for point_i in range(3):
            triangle_points[triangle_i][point_i] = add_tuples(triangle_points[triangle_i][point_i], velocity)

            if triangle_points[triangle_i][point_i][0] > width or triangle_points[triangle_i][point_i][0] < 0:
                triangle_velocities[triangle_i] = (-triangle_velocities[triangle_i][0], triangle_velocities[triangle_i][1])

            if triangle_points[triangle_i][point_i][1] > height or triangle_points[triangle_i][point_i][1] < 0:
                triangle_velocities[triangle_i] = (triangle_velocities[triangle_i][0], -triangle_velocities[triangle_i][1])


    img.save(f"images\image{i:05d}.bmp", format="bmp")

    end = time.perf_counter()

    print(f"Image gen {i} done in  {end - start} seconds!")