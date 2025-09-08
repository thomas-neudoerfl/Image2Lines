import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin

def generateCircle(radius=1, center=(0,0), numpoints=2**5):
    points = []
    angle = 2*np.pi/numpoints
    for i in range(numpoints):
        points.append((center[0]+radius*cos(i*angle), center[1]+radius*sin(i*angle)))
    return points

circle = generateCircle()


fig, ax = plt.subplots()
for (x, y) in circle:
    plt.plot(x, y, 'bo')
plt.show()