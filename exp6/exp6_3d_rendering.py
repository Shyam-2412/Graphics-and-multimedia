import pygame
import numpy as np
import math
import sys

def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def calculate_normal(v1, v2, v3):
    edge1 = np.array(v2) - np.array(v1)
    edge2 = np.array(v3) - np.array(v1)
    normal = np.cross(edge1, edge2)
    return normalize_vector(normal)

def calculate_lighting(normal, light_direction, light_intensity=1.0):
    dot_product = np.dot(normal, light_direction)
    return max(0, dot_product) * light_intensity

class Object3D:
    def __init__(self, vertices, faces):
        self.vertices = np.array(vertices, dtype=float)
        self.faces = faces
        self.angle_x = 0
        self.angle_y = 0
    
    def rotate(self, angle_x, angle_y):
        self.angle_x += angle_x
        self.angle_y += angle_y
        
        cos_x, sin_x = math.cos(self.angle_x), math.sin(self.angle_x)
        cos_y, sin_y = math.cos(self.angle_y), math.sin(self.angle_y)
        
        rotation_x = np.array([
            [1, 0, 0],
            [0, cos_x, -sin_x],
            [0, sin_x, cos_x]
        ])
        
        rotation_y = np.array([
            [cos_y, 0, sin_y],
            [0, 1, 0],
            [-sin_y, 0, cos_y]
        ])
        
        rotation_matrix = np.dot(rotation_y, rotation_x)
        return np.dot(self.vertices, rotation_matrix.T)
    
    def project_to_2d(self, vertices_3d, width, height, distance=5):
        projected = []
        for vertex in vertices_3d:
            x, y, z = vertex
            z_offset = z + distance
            if z_offset != 0:
                screen_x = int((x * 300) / z_offset + width // 2)
                screen_y = int((-y * 300) / z_offset + height // 2)
            else:
                screen_x = int(x * 300 + width // 2)
                screen_y = int(-y * 300 + height // 2)
            projected.append((screen_x, screen_y))
        return projected

def create_cube():
    vertices = [
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ]
    
    faces = [
        [0, 1, 2, 3], [4, 7, 6, 5], [0, 4, 5, 1],
        [2, 6, 7, 3], [0, 3, 7, 4], [1, 5, 6, 2]
    ]
    
    return Object3D(vertices, faces)

def create_sphere(radius=1, segments=16):
    vertices = []
    faces = []
    
    for i in range(segments + 1):
        lat = math.pi * i / segments - math.pi / 2
        for j in range(segments):
            lon = 2 * math.pi * j / segments
            x = radius * math.cos(lat) * math.cos(lon)
            y = radius * math.sin(lat)
            z = radius * math.cos(lat) * math.sin(lon)
            vertices.append([x, y, z])
    
    for i in range(segments):
        for j in range(segments):
            current = i * segments + j
            next_row = (i + 1) * segments + j
            next_col = i * segments + (j + 1) % segments
            next_both = (i + 1) * segments + (j + 1) % segments
            
            if i < segments:
                faces.append([current, next_row, next_both, next_col])
    
    return Object3D(vertices, faces)

def draw_filled_polygon(screen, points, color):
    if len(points) >= 3:
        pygame.draw.polygon(screen, color, points)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("3D Rendering with Shading")
clock = pygame.time.Clock()

cube = create_cube()
sphere = create_sphere()
current_object = cube
object_name = "Cube"

light_direction = normalize_vector(np.array([1, 1, 1]))
wireframe_mode = False
auto_rotate = True

base_colors = {
    "Cube": [(255, 100, 100), (100, 255, 100), (100, 100, 255), 
             (255, 255, 100), (255, 100, 255), (100, 255, 255)],
    "Sphere": [(200, 100, 50)] * 100
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_object = cube
                object_name = "Cube"
            elif event.key == pygame.K_2:
                current_object = sphere
                object_name = "Sphere"
            elif event.key == pygame.K_w:
                wireframe_mode = not wireframe_mode
            elif event.key == pygame.K_SPACE:
                auto_rotate = not auto_rotate
    
    keys = pygame.key.get_pressed()
    rotation_speed = 0.02
    
    if keys[pygame.K_LEFT] or auto_rotate:
        current_object.rotate(0, -rotation_speed)
    if keys[pygame.K_RIGHT]:
        current_object.rotate(0, rotation_speed)
    if keys[pygame.K_UP]:
        current_object.rotate(-rotation_speed, 0)
    if keys[pygame.K_DOWN]:
        current_object.rotate(rotation_speed, 0)
    
    screen.fill((20, 20, 30))
    
    rotated_vertices = current_object.rotate(0, 0)
    projected_vertices = current_object.project_to_2d(rotated_vertices, 800, 600)
    
    face_data = []
    for i, face in enumerate(current_object.faces):
        if len(face) >= 3:
            v1 = rotated_vertices[face[0]]
            v2 = rotated_vertices[face[1]]
            v3 = rotated_vertices[face[2]]
            
            normal = calculate_normal(v1, v2, v3)
            
            if normal[2] > 0:
                continue
            
            center_z = sum(rotated_vertices[vertex_idx][2] for vertex_idx in face) / len(face)
            
            lighting = calculate_lighting(normal, light_direction)
            
            if object_name == "Cube" and i < len(base_colors[object_name]):
                base_color = base_colors[object_name][i]
            else:
                base_color = base_colors[object_name][0]
            
            shaded_color = tuple(int(c * (0.3 + 0.7 * lighting)) for c in base_color)
            
            face_points = [projected_vertices[vertex_idx] for vertex_idx in face]
            
            face_data.append((center_z, face_points, shaded_color))
    
    face_data.sort(key=lambda x: x[0], reverse=True)
    
    for center_z, face_points, color in face_data:
        if wireframe_mode:
            if len(face_points) >= 3:
                pygame.draw.polygon(screen, (255, 255, 255), face_points, 2)
        else:
            draw_filled_polygon(screen, face_points, color)
            if len(face_points) >= 3:
                pygame.draw.polygon(screen, (50, 50, 50), face_points, 1)
    
    font = pygame.font.Font(None, 36)
    text = font.render(f"Object: {object_name}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    
    mode_text = "Wireframe" if wireframe_mode else "Solid"
    mode_surface = font.render(f"Mode: {mode_text}", True, (255, 255, 255))
    screen.blit(mode_surface, (10, 50))
    
    controls = [
        "Controls:",
        "1 - Cube",
        "2 - Sphere", 
        "Arrow Keys - Rotate",
        "W - Toggle Wireframe",
        "SPACE - Auto-rotate"
    ]
    
    y_offset = 100
    for control in controls:
        text = pygame.font.Font(None, 24).render(control, True, (200, 200, 200))
        screen.blit(text, (10, y_offset))
        y_offset += 25
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()