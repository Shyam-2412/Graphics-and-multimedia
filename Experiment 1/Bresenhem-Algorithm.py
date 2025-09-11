import matplotlib.pyplot as plt

def bresenham(x1, y1, x2, y2):
    x_points = []
    y_points = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x, y = x1, y1

    sx = 1 if x2 > x1 else -1  
    sy = 1 if y2 > y1 else -1  

    if dy <= dx:
        p = 2*dy - dx
        for _ in range(dx + 1):
            x_points.append(x)
            y_points.append(y)
            print(f"({x}, {y})")
            if p >= 0:
                y += sy
                p -= 2*dx
            x += sx
            p += 2*dy
    else:
        p = 2*dx - dy
        for _ in range(dy + 1):
            x_points.append(x)
            y_points.append(y)
            print(f"({x}, {y})")
            if p >= 0:
                x += sx
                p -= 2*dy
            y += sy
            p += 2*dx

    return x_points, y_points


x1 = int(input("Enter x1: "))
y1 = int(input("Enter y1: "))
x2 = int(input("Enter x2: "))
y2 = int(input("Enter y2: "))

x_points, y_points = bresenham(x1, y1, x2, y2)

plt.plot(x_points, y_points, marker='o')
plt.title("Bresenham's Line Algorithm")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.grid(True)
plt.show()
