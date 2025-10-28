import pygame
import numpy as np
import math
import sys

class Object3D:
    def __init__(self, vertices, edges):
        self.original_vertices = np.array(vertices)
        self.vertices = np.copy(self.original_vertices)
        self.edges = edges
    
    def translate(self, dx, dy, dz):
        translation_matrix = np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])
        self.apply_transformation(translation_matrix)
    
    def scale(self, sx, sy, sz):
        scale_matrix = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
        self.apply_transformation(scale_matrix)
    
    def rotate_x(self, angle):
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        rotation_matrix = np.array([
            [1, 0, 0, 0],
            [0, cos_a, -sin_a, 0],
            [0, sin_a, cos_a, 0],
            [0, 0, 0, 1]
        ])
        self.apply_transformation(rotation_matrix)
    
    def rotate_y(self, angle):
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        rotation_matrix = np.array([
            [cos_a, 0, sin_a, 0],
            [0, 1, 0, 0],
            [-sin_a, 0, cos_a, 0],
            [0, 0, 0, 1]
        ])
        self.apply_transformation(rotation_matrix)
    
    def rotate_z(self, angle):
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        rotation_matrix = np.array([
            [cos_a, -sin_a, 0, 0],
            [sin_a, cos_a, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.apply_transformation(rotation_matrix)
    
    def apply_transformation(self, matrix):
        homogeneous_vertices = np.column_stack([self.vertices, np.ones(len(self.vertices))])
        transformed = np.dot(homogeneous_vertices, matrix.T)
        self.vertices = transformed[:, :3]
    
    def project_to_2d(self, width, height, distance=5):
        projected = []
        for vertex in self.vertices:
            x, y, z = vertex
            if z + distance != 0:
                screen_x = int((x * distance) / (z + distance) * 200 + width // 2)
                screen_y = int((y * distance) / (z + distance) * 200 + height // 2)
            else:
                screen_x = int(x * 200 + width // 2)
                screen_y = int(y * 200 + height // 2)
            projected.append((screen_x, screen_y))
        return projected
    
    def reset(self):
        self.vertices = np.copy(self.original_vertices)

cube_vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
]

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

pyramid_vertices = [
    [0, 1, 0], [-1, -1, 1], [1, -1, 1], [1, -1, -1], [-1, -1, -1]
]

pyramid_edges = [
    (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 2), (2, 3), (3, 4), (4, 1)
]

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("3D Transformations")
clock = pygame.time.Clock()

cube = Object3D(cube_vertices, cube_edges)
pyramid = Object3D(pyramid_vertices, pyramid_edges)
current_object = cube
object_name = "Cube"

rotation_x = 0
rotation_y = 0
auto_rotate = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_object.reset()
                rotation_x = rotation_y = 0
            elif event.key == pygame.K_t:
                current_object.translate(0.5, 0, 0)
            elif event.key == pygame.K_g:
                current_object.translate(-0.5, 0, 0)
            elif event.key == pygame.K_y:
                current_object.translate(0, 0.5, 0)
            elif event.key == pygame.K_h:
                current_object.translate(0, -0.5, 0)
            elif event.key == pygame.K_u:
                current_object.translate(0, 0, 0.5)
            elif event.key == pygame.K_j:
                current_object.translate(0, 0, -0.5)
            elif event.key == pygame.K_EQUALS:
                current_object.scale(1.1, 1.1, 1.1)
            elif event.key == pygame.K_MINUS:
                current_object.scale(0.9, 0.9, 0.9)
            elif event.key == pygame.K_SPACE:
                auto_rotate = not auto_rotate
            elif event.key == pygame.K_1:
                current_object = cube
                object_name = "Cube"
            elif event.key == pygame.K_2:
                current_object = pyramid
                object_name = "Pyramid"
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rotation_y -= 0.05
        current_object.rotate_y(-0.05)
    if keys[pygame.K_RIGHT]:
        rotation_y += 0.05
        current_object.rotate_y(0.05)
    if keys[pygame.K_UP]:
        rotation_x -= 0.05
        current_object.rotate_x(-0.05)
    if keys[pygame.K_DOWN]:
        rotation_x += 0.05
        current_object.rotate_x(0.05)
    
    if auto_rotate:
        current_object.rotate_y(0.02)
        current_object.rotate_x(0.01)
    
    screen.fill((0, 0, 0))
    
    projected_vertices = current_object.project_to_2d(800, 600)
    
    for edge in current_object.edges:
        start_pos = projected_vertices[edge[0]]
        end_pos = projected_vertices[edge[1]]
        pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 2)
    
    for i, pos in enumerate(projected_vertices):
        pygame.draw.circle(screen, (255, 0, 0), pos, 4)
    
    font = pygame.font.Font(None, 36)
    text = font.render(f"Object: {object_name}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    
    controls = [
        "Controls:",
        "Arrow Keys - Rotate",
        "T/G - Translate X",
        "Y/H - Translate Y", 
        "U/J - Translate Z",
        "+/- - Scale",
        "R - Reset",
        "SPACE - Auto-rotate",
        "1 - Cube, 2 - Pyramid"
    ]
    
    y_offset = 50
    for control in controls:
        text = pygame.font.Font(None, 24).render(control, True, (200, 200, 200))
        screen.blit(text, (10, y_offset))
        y_offset += 25
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()