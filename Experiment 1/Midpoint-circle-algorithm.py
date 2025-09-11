# Midpoint Circle Algorithm

import matplotlib.pyplot as plt

x0=int(input("Enter x0:"))
y0=int(input("Enter y0:"))
r=int(input("Enter Radius:"))

p = 1 - r

x=0
y=r

x_points=[]
y_points=[]

x_points.extend([x+x0,x+x0,-x+x0,-x+x0,y+x0,y+x0,-y+x0,-y+x0])
    
y_points.extend([y+y0,-y+y0,y+y0,-y+y0,x+y0,-x+y0,x+y0,-x+y0])

while(x<y):
    if(p<0):
        p=p+(2*(x+1))+1
        x=x+1
    else:
        p=p+(2*(x+1))+1-(2*(y-1))
        x=x+1
        y=y-1
        
    x_points.extend([x+x0,x+x0,-x+x0,-x+x0,y+x0,y+x0,-y+x0,-y+x0])
    
    y_points.extend([y+y0,-y+y0,y+y0,-y+y0,x+y0,-x+y0,x+y0,-x+y0])
    
    #print("(",x,",",y,")")



plt.plot(x_points,y_points,'s')
plt.plot(x0,y0,'ro')
plt.title("Midpoint Circle Algorithm")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.grid(True)
plt.show()


# x_points.extend([x+x0,x+x0,-x+x0,-x+x0,y+x0,y+x0,-y+x0,-y+x0])
    
# y_points.extend([y+y0,-y+y0,y+y0,-y+y0,x+y0,-x+y0,x+y0,-x+y0])
