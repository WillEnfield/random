import numpy as np
from PIL import Image
import pygame

pygame.init()

width = 344
height = 144

monitor_width = 3440
monitor_height = 1440

screen = pygame.display.set_mode((monitor_width, monitor_height))

class game_of_life_board:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), bool)
    
    def update(self):
        new_board = np.zeros((self.height, self.width), bool)
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                if self.board[y, x]:
                    if neighbors == 2 or neighbors == 3:
                        new_board[y, x] = True
                    else:
                        new_board[y, x] = False
                else:
                    if neighbors == 3:
                        new_board[y, x] = True
        self.board = new_board
    
    def count_neighbors(self, x, y):
        count = 0
        for ny in range(y-1, y+2):
            for nx in range(x-1, x+2):
                nx = nx % self.width
                ny = ny % self.height
                if (nx, ny) != (x, y) and self.board[ny, nx]:
                    count += 1
        return count

    def print_board(self):
        for row in self.board:
            print(''.join(['█' if cell else '░' for cell in row]))
    
    def to_image(self):
        img = Image.new('RGB', (self.width, self.height), (13, 2, 33))
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y, x]:
                    img.putpixel((x, y), (194, 231, 217))
        return img
    
    def randomize(self, density=0.5):
        self.board = np.random.rand(self.height, self.width) < density

def pil_to_pygame_surface(pil_image):
    return pygame.image.fromstring(
        pil_image.tobytes(),
        pil_image.size,
        pil_image.mode
    )

board = game_of_life_board(width, height)
board.board[0, 0] = True
board.board[1, 1] = True
board.board[1, 2] = True
board.board[2, 0] = True
board.board[2, 1] = True


iteration = 0

running = True

speed = 1

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = not running
            elif event.key == pygame.K_r:
                random_density = input("Enter density (0.0 - 1.0): ")
                try:
                    random_density = float(random_density)
                except ValueError:
                    print("Invalid density.")
                board.randomize(random_density)
            elif event.key == pygame.K_c:
                board.board = np.zeros((height, width), bool)
            elif event.key == pygame.K_s:
                speed = input("Enter speed: ")
                try:
                    speed = int(speed)
                except ValueError:
                    print("Invalid speed.")
            elif event.key == pygame.K_g:
                mouse_pixel_pos = (pygame.mouse.get_pos()[0] * width // monitor_width, pygame.mouse.get_pos()[1] * height // monitor_height)
                board.board[mouse_pixel_pos[1], mouse_pixel_pos[0]] = True
                board.board[mouse_pixel_pos[1] + 1, mouse_pixel_pos[0] + 1] = True
                board.board[mouse_pixel_pos[1] + 1, mouse_pixel_pos[0] + 2] = True
                board.board[mouse_pixel_pos[1] + 2, mouse_pixel_pos[0]] = True
                board.board[mouse_pixel_pos[1] + 2, mouse_pixel_pos[0] + 1] = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pixel_pos = (pygame.mouse.get_pos()[0] * width // monitor_width, pygame.mouse.get_pos()[1] * height // monitor_height)
                board.board[mouse_pixel_pos[1], mouse_pixel_pos[0]] = not board.board[mouse_pixel_pos[1], mouse_pixel_pos[0]]
    
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        break

    if running:
        iteration += 1
        if iteration % speed == 0:
            board.update()

    pygame_surface = pil_to_pygame_surface(board.to_image())
    scaled_surface = pygame.transform.scale(pygame_surface, (monitor_width, monitor_height))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()