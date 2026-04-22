from PIL import Image
import numpy as np
import pygame
import math
import random

pygame.init()

width = 344
height = 144
aspect = width / height

max_bounces = 3

screen = pygame.display.set_mode((3440, 1440))

class Material():
    def __init__(self, color, emission_color, emission_strength):
        self.color = color
        self.emission_color = emission_color
        self.emission_strength = emission_strength

class Sphere():
    def __init__(self, loc, radius, material):
        self.loc = loc
        self.radius = radius
        self.material = material

def normalize(vec):
    len = (vec[0]**2 + vec[1]**2 + vec[2]**2) ** 0.5
    return (vec[0] / len, vec[1] / len, vec[2] / len)

def dot(vec, vec2):
    return vec[0] * vec2[0] + vec[1] * vec2[1] + vec[2] * vec2[2]

def add_t(vec, vec2):
    return(vec[0] + vec2[0], vec[1] + vec2[1], vec[2] + vec2[2])

def sub_t(vec, vec2):
    return(vec[0] - vec2[0], vec[1] - vec2[1], vec[2] - vec2[2])

def mul_t(vec, vec2):
    return(vec[0] * vec2[0], vec[1] * vec2[1], vec[2] * vec2[2])

def div_t_f(vec, scalar):
     return(vec[0] / scalar, vec[1] / scalar, vec[2] / scalar)

def mul_t_f(vec, scalar):
    return(vec[0] * scalar, vec[1] * scalar, vec[2] * scalar)

def gaussian_random():
    theta = 2 * 3.1415926 * random.random()
    rho = (-2 * math.log(random.random()))**0.5
    return(rho * math.cos(theta))

def random_direction():
    angle = normalize((
            gaussian_random() * 2 - 1,
            gaussian_random() * 2 - 1,
            gaussian_random() * 2 - 1
            ))
    return(angle)

def sphere_intersection(ray_origin, ray_dir, sphere):
    offset_origin = (ray_origin[0] - sphere.loc[0], ray_origin[1] - sphere.loc[1], ray_origin[2] - sphere.loc[2])

    a = dot(ray_dir, ray_dir)
    b = 2 * dot(offset_origin, ray_dir)
    c = dot(offset_origin, offset_origin) - sphere.radius *  sphere.radius
    discriminant = b * b - 4 * a * c

    if discriminant >= 0:
        distance = (-b - math.sqrt(discriminant)) / (2*a)

        if distance >= 0:
            hit_point = add_t(ray_origin, mul_t_f(ray_dir, distance))
            normal = normalize(sub_t(hit_point, sphere.loc))
            return((distance, hit_point, normal, sphere))

    return None

def closest_intercection(ray_origin, ray_dir):
    spheres = [
        Sphere((0,-0.5,6), 2, Material((0,255,255), (0,0,0), 0)),
        Sphere((0,2,6), 0.5, Material((0,255,0), (0,0,0), 0)),
        Sphere((200,0,0), 150, Material((255,255,255), (255, 255, 255), 1))
    ]

    closest_intercection = (float("inf"), None, None)

    for sphere in spheres:
        intercection = sphere_intersection(ray_origin, ray_dir, sphere)
        if intercection != None:
            if intercection[0] < closest_intercection[0]:
                closest_intercection = intercection
    
    return(None if closest_intercection == (float("inf"), None, None) else closest_intercection)

def pixel(ray_origin, ray_dir, old_pixel, i):

    weight = 1 / (i + 1)

    new_color = mul_t_f(trace(ray_origin, ray_dir), weight)
    old_color = mul_t_f(old_pixel, 1 - weight)
    color = add_t(new_color, old_color)
    color = (int(color[0]), int(color[1]), int(color[2]))
    
    return(color)

def rotate(vec, pitch, yaw, roll):
    x, y, z = vec

    cos_y, sin_y = math.cos(yaw), math.sin(yaw)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y

    cos_p, sin_p = math.cos(pitch), math.sin(pitch)
    y, z = y * cos_p - z * sin_p, y * sin_p + z * cos_p

    cos_r, sin_r = math.cos(roll), math.sin(roll)
    x, y = x * cos_r - y * sin_r, x * sin_r + y * cos_r

    return (x, y, z)

def calculate_ray_direction(x, y, camera_dir, camera_fov):
    x = (2 * (x / width) - 1) * aspect
    y = (1 - 2 * (y / height))

    f = math.tan(camera_fov / 2)
    
    d_cam = normalize((x * f, y * f, 1))

    d_world = rotate(d_cam, camera_dir[0], camera_dir[1], camera_dir[2])

    return normalize(d_world)

def trace(ray_origin, ray_direction):

    incoming_light = (0,0,0)
    ray_color = (1, 1, 1)

    for i in range(max_bounces):
        hit = closest_intercection(ray_origin, ray_direction)
        if hit != None:
            ray_origin = hit[1]
            ray_direction = normalize(add_t(random_direction(), hit[2]))

            material = hit[3].material

            emitted_light = mul_t_f(div_t_f(material.emission_color, 255), material.emission_strength)
            incoming_light = add_t(mul_t(emitted_light, ray_color), emitted_light)

            ray_color = mul_t(div_t_f(material.color, 255), ray_color)
        else:
            break
    
    incoming_light = mul_t_f(incoming_light, 255)
    return(incoming_light)

def draw_image(camera_loc, camera_dir, fov, old_img, i):

    img_array = np.zeros((height, width, 3), dtype=np.float64)

    for y in range(height):
        for x in range(width):
            ray_dir = calculate_ray_direction(x, y, camera_dir, fov)
            color = pixel(camera_loc, ray_dir, old_img[y,x], i)
            img_array[y, x] = color
    return img_array

def pil_to_pygame_surface(pil_image):
    return pygame.image.fromstring(
        pil_image.tobytes(),
        pil_image.size,
        pil_image.mode
    )

def main():
    running = True
    i = 0
    img_array = np.zeros((height, width, 3), dtype=np.float64)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        img_array = draw_image((0, 0, 0), (0,0,0), math.pi/3, img_array, i)

        display_img = np.clip(img_array, 0, 255).astype(np.uint8)

        img = Image.fromarray(display_img, 'RGB')

        pygame_surface = pil_to_pygame_surface(img)
        scaled_surface = pygame.transform.scale(pygame_surface, (3440, 1440))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

        i += 1
    
    pygame.quit()

main()