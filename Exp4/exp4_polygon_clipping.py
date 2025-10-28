import pygame
import sys

def cohen_sutherland_line_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8
    
    def compute_code(x, y):
        code = INSIDE
        if x < xmin:
            code |= LEFT
        elif x > xmax:
            code |= RIGHT
        if y < ymin:
            code |= BOTTOM
        elif y > ymax:
            code |= TOP
        return code
    
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)
    accept = False
    
    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        elif code1 & code2 != 0:
            break
        else:
            x = 0.0
            y = 0.0
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2
                
            if code_out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin
                
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)
    
    if accept:
        return [(int(x1), int(y1)), (int(x2), int(y2))]
    return None

def sutherland_hodgman_clip(polygon, clip_window):
    def is_inside(point, edge_start, edge_end):
        return ((edge_end[0] - edge_start[0]) * (point[1] - edge_start[1]) - 
                (edge_end[1] - edge_start[1]) * (point[0] - edge_start[0])) >= 0
    
    def intersection(p1, p2, edge_start, edge_end):
        dc = [edge_start[0] - edge_end[0], edge_start[1] - edge_end[1]]
        dp = [p1[0] - p2[0], p1[1] - p2[1]]
        n1 = edge_start[0] * edge_end[1] - edge_start[1] * edge_end[0]
        n2 = p1[0] * p2[1] - p1[1] * p2[0]
        n3 = dc[0] * dp[1] - dc[1] * dp[0]
        return [(n1 * dp[0] - n2 * dc[0]) / n3, (n1 * dp[1] - n2 * dc[1]) / n3]
    
    output_list = polygon
    xmin, ymin, xmax, ymax = clip_window
    clip_edges = [
        [(xmin, ymin), (xmin, ymax)],
        [(xmin, ymax), (xmax, ymax)],
        [(xmax, ymax), (xmax, ymin)],
        [(xmax, ymin), (xmin, ymin)]
    ]
    
    for edge in clip_edges:
        if not output_list:
            break
        input_list = output_list
        output_list = []
        
        if input_list:
            s = input_list[-1]
            for e in input_list:
                if is_inside(e, edge[0], edge[1]):
                    if not is_inside(s, edge[0], edge[1]):
                        output_list.append(intersection(s, e, edge[0], edge[1]))
                    output_list.append(e)
                elif is_inside(s, edge[0], edge[1]):
                    output_list.append(intersection(s, e, edge[0], edge[1]))
                s = e
    
    return output_list

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Polygon Clipping")

polygon = [(100, 100), (200, 150), (300, 100), (250, 200), (150, 200)]
clip_window = (200, 150, 500, 400)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    
    pygame.draw.polygon(screen, (255, 0, 0), polygon, 2)
    pygame.draw.rect(screen, (0, 255, 0), clip_window, 2)
    
    clipped_polygon = sutherland_hodgman_clip(polygon, clip_window)
    if clipped_polygon and len(clipped_polygon) > 2:
        pygame.draw.polygon(screen, (0, 0, 255), clipped_polygon, 3)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()