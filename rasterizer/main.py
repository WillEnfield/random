from PIL import Image
import random
import time

start = time.perf_counter()

width = 3440
height = 1440

triangle_point_1 = (random.randint(1,width),random.randint(1,height))
triangle_point_2 = (random.randint(1,width),random.randint(1,height))
triangle_point_3 = (random.randint(1,width),random.randint(1,height))

def dot(a,b):
    return(a[0]*b[0]+a[1]*b[1])

def get_pixel(x,y):
    if point_in_triangle(triangle_point_1,triangle_point_2,triangle_point_3,(x,y)):
        img.putpixel((x,y),(255,255,255))
    else:
        img.putpixel((x,y),(0,0,0))

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


img = Image.new("RGB", (width,height), color=(0,255,0))


for x in range(width):
    for y in range(height):
        get_pixel(x,y)

img.putpixel(triangle_point_1,(255,0,0))
img.putpixel(triangle_point_2,(0,255,0))
img.putpixel(triangle_point_3,(0,0,255))

img.save("image.bmp", format="bmp")

end = time.perf_counter()

print(f"Image gen done in  {end - start} seconds!")