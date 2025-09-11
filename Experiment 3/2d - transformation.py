import numpy as np
import matplotlib.pyplot as plt

# Draw a closed shape and label it
def draw_shape(points, label, color):
    x, y = zip(*points)
    x += (x[0],)
    y += (y[0],)
    plt.plot(x, y, color=color, label=label)

# Translation matrix
def translate(points, tx, ty):
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]])
    return apply_transform(points, T)

# Scaling matrix
def scale(points, sx, sy):
    S = np.array([[sx, 0, 0],
                  [0, sy, 0],
                  [0, 0, 1]])
    return apply_transform(points, S)

# Rotation matrix
def rotate(points, angle_deg):
    angle_rad = np.radians(angle_deg)
    R = np.array([[np.cos(angle_rad), -np.sin(angle_rad), 0],
                  [np.sin(angle_rad),  np.cos(angle_rad), 0],
                  [0, 0, 1]])
    return apply_transform(points, R)

# Apply transformation matrix to each point
def apply_transform(points, matrix):
    transformed = []
    for x, y in points:
        vec = np.array([x, y, 1])
        result = matrix @ vec
        transformed.append((result[0], result[1]))
    return transformed
# Original triangle
triangle = [(0, 0), (100, 0), (50, 80)]

translated = translate(triangle, 120, 50)
scaled = scale(triangle, 1.5, 1.5)
rotated = rotate(triangle, 45)

# Plot
plt.figure(figsize=(8, 8))
draw_shape(triangle, "Original", 'blue')
draw_shape(translated, "Translated", 'green')
draw_shape(scaled, "Scaled", 'orange')
draw_shape(rotated, "Rotated", 'red')
plt.title("2D Transformations")
plt.legend()
plt.grid(True)
plt.axis("equal")
plt.show() 
