import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy import cos, sin

img = mpimg.imread("BlackWhiteHeartTest.jpg")

# Convert to grayscale
image = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
height = min(image.shape)

def mapIndicesToCoords(i, j):
    return ((2*j/height)-1, 1-(2*i/height))

def mapCoordsToIndeces(x, y):
    return (height*(y+1)//2, height*(x+1)//2)

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
for i in range(height):
    for j in range(height):
        if(image[i][j] < 100):
            x, y = mapIndicesToCoords(i, j)
            plt.plot(x, y, 'bo')
plt.show()