import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy import cos, sin

img = mpimg.imread("BlackWhiteHeartTest.jpg")

# Convert to grayscale
image = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])

height = min(image.shape)

for i in range(height):
    for j in range(height):
        image[i][j] = 0.1*(256-image[i][j])

def mapIndicesToCoords(i, j):
    return ((2*j/height)-1, 1-(2*i/height))

def mapCoordsToIndices(x, y):
    return (height*(y+1)//2, height*(-x+1)//2)

def generateCircle(radius=1, center=(0,0), numpoints=2**5):
    points = []
    angle = 2*np.pi/numpoints
    for i in range(numpoints):
        points.append((center[0]+radius*cos(i*angle), center[1]+radius*sin(i*angle)))
    return points

numpoints = 2**5
circle = generateCircle(numpoints=numpoints)

fig, ax = plt.subplots()

def sumOfLine(line):
    res = 0
    for i in len(line):
        res += image[line[i][0]][line[i][1]]

def substractLine(line):
    for i in len(line):
        image[line[i][0]][line[i][1]] -= 1

def generateLines():
    res = []
    while(sum(image) > 0):
        linePoints = ((0,0),(0,0))
        max = -np.infty
        linePixels = []
        for i in range(numpoints):
            for j in range(i+1, numpoints):
                line = []
                x0, y0 = circle[i]
                x1, y1 = circle[j]
                i0, j0 = mapCoordsToIndices(x0, y0)
                i1, j1 = mapCoordsToIndices(x1, y1)
                if j1 == j0:
                    for index in range(i0, i1+1):
                        line.append((index, j0))
                else:
                    slope = (i1-i0)/(j1-j0)
                    for index in range(i0, i1+1):
                        line.append((index, slope*index + i0))
                if sumOfLine(line) > max:
                    linePoints = ((x0, y0), (x1, y1))
                    linePixels = line
        substractLine(linePixels)
        res.append(linePoints)



for (x, y) in circle:
    plt.plot(x, y, 'bo')
for i in range(height):
    for j in range(height):
        if(image[i][j] > 10):
            x, y = mapIndicesToCoords(i, j)
            plt.plot(x, y, 'bo')
plt.show()