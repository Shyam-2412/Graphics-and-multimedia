import matplotlib.pyplot as plt

rx = int(input("Enter the radius along x: "))
ry = int(input("Enter the radius along y: "))

x = 0
y = ry

p1 = (ry**2) + (0.25 * (rx**2)) - ((rx**2) * ry)

while (2 * (ry**2) * x <= 2 * (rx**2) * y):
    plt.plot(x, y, marker='o', color='red')
    plt.plot(-x, y, marker='o', color='red')
    plt.plot(x, -y, marker='o', color='red')
    plt.plot(-x, -y, marker='o', color='red')

    if p1 < 0:
        x += 1
        p1 = p1 + (2 * (ry**2) * x) + (ry**2)
    else:
        x += 1
        y -= 1
        p1 = p1 + (2 * (ry**2) * x) - (2 * (rx**2) * y) + (ry**2)

p2 = (ry**2) * ((x + 0.5)**2) + ((rx**2) * ((y - 1)**2)) - ((rx**2) * (ry**2))

while y >= 0:
    plt.plot(x, y, marker='o', color='red')
    plt.plot(-x, y, marker='o', color='red')
    plt.plot(x, -y, marker='o', color='red')
    plt.plot(-x, -y, marker='o', color='red')

    if p2 > 0:
        y -= 1
        p2 = p2 - (2 * (rx**2) * y) + (rx**2)
    else:
        x += 1
        y -= 1
        p2 = p2 + (2 * (ry**2) * x) - (2 * (rx**2) * y) + (rx**2)

plt.title("Ellipse drawn using Midpoint Ellipse Algorithm")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
