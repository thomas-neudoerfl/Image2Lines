import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy import cos, sin
from math import floor

img = mpimg.imread("BlackWhiteHeartTest.jpg")

# Convert to grayscale
global image
image = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])

height = min(image.shape)
numpoints = 2**6
maxvalue = 42
factor = maxvalue/256

def cleanImage():
    global image
    for i in range(height):
        for j in range(height):
            x, y = mapIndicesToCoords(i, j)
            if x**2 + y**2 > 1:
                image[i][j] = 0
            else:
                image[i][j] = factor*(256-image[i][j])

def mapIndicesToCoords(i, j):
    return ((2*j/height)-1, 1-(2*i/height))

def mapCoordsToIndices(x, y):
    return (min(height-1, int((height*(1-y))/2)), min(height-1, int((height*(x+1))/2)))

def generateCircle(radius=1, center=(0,0), numpoints=2**5):
    points = []
    angle = 2*np.pi/numpoints
    for i in range(numpoints):
        points.append((center[0]+radius*cos(i*angle), center[1]+radius*sin(i*angle)))
    return points


def sumOfLine(line):
    global image
    res = 0
    for pixel in line:
        res += image[pixel[0]][pixel[1]]
    return res

def substractLine(line):
    global image
    for pixel in line:
        image[pixel[0]][pixel[1]] -= 1

def generateLines():
    global image
    res = []
    counter = 0
    while(np.sum(image) > 0):
        counter += 1
        print(counter, ": ", np.sum(image))
        linePoints = ((0,0),(0,0))
        maxSum = -np.infty
        linePixels = []
        for i in range(numpoints-1):
            for j in range(i+1, numpoints):
                line = []
                x0, y0 = circle[i]
                x1, y1 = circle[j]
                pointA = mapCoordsToIndices(x0, y0)
                pointB = mapCoordsToIndices(x1, y1)
                if pointA[0]>pointB[0]:
                    pointA, pointB = pointB, pointA
                i0, j0 = pointA
                i1, j1 = pointB

                if i1 == i0:
                    jmin = min(j0, j1)
                    jmax = max(j0, j1)
                    for jndex in range(jmin, jmax+1):
                        line.append((i0, jndex))
                else:
                    slope = (j1-j0)/(i1-i0)
                    for index in range(i0, i1+1):
                        line.append((index, min(height-1, floor(slope*index + j0 - slope*i0))))
                if len(line) > 0 and sumOfLine(line)/len(line) > maxSum:
                    maxSum = sumOfLine(line)/len(line)
                    linePoints = (([x0, x1]), ([y0, y1]))
                    linePixels = line
        substractLine(linePixels)
        res.append(linePoints)
    return res


cleanImage()

circle = generateCircle(numpoints=numpoints)

fig, ax = plt.subplots()

lines = generateLines()

for x, y in lines:
    plt.plot(x, y, 'b-')

for (x, y) in circle:
    plt.plot(x, y, 'bo')
"""
for i in range(height):
    for j in range(height):
        if(image[i][j] > 1):
            x, y = mapIndicesToCoords(i, j)
            plt.plot(x, y, 'bo')
"""
plt.show()