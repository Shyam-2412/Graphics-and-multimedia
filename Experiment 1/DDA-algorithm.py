import matplotlib.pyplot as plt

x0 = int(input("Enter x0: "))
y0 = int(input("Enter y0: "))
x1 = int(input("Enter x1: "))
y1 = int(input("Enter y1: "))

dx = x1 - x0
dy = y1 - y0
steps = max(abs(dx), abs(dy))
x_inc = dx / steps
y_inc = dy / steps

x = x0
y = y0

x_points = []
y_points = []

for i in range(steps + 1):
    x_points.append(round(x))
    y_points.append(round(y))
    x += x_inc
    y += y_inc

plt.plot(x_points, y_points, marker='o')
plt.title("Line drawn using DDA Algorithm")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.grid(True)
plt.show()
