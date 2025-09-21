import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
from skimage.draw import line as bresenham_line
import numpy as np
from numpy import cos, sin
from tkinter import filedialog
import os

class StringArt:
    def __init__(self, img_path):
        global image
        img = mpimg.imread(img_path)
        image = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
        
        self.height = min(image.shape)
        self.numpoints = 4*60
        self.maxvalue = 12
        self.factor = self.maxvalue/256
        self.circle = []
        self.cache = {}

    def cleanImage(self):
        global image
        for i in range(self.height):
            for j in range(self.height):
                x, y = self.mapIndicesToCoords(i, j)
                if x**2 + y**2 > 1:
                    image[i][j] = 0
                else:
                    image[i][j] = self.factor*(256-image[i][j])

    def mapIndicesToCoords(self, i, j):
        return ((2*j/self.height)-1, 1-(2*i/self.height))

    def mapCoordsToIndices(self, x, y):
        return (min(self.height-1, int((self.height*(1-y))/2)),
                min(self.height-1, int((self.height*(x+1))/2)))

    def generateCircle(self, radius=1, center=(0,0), numpoints=2**5):
        points = []
        angle = 2*np.pi/numpoints
        for i in range(numpoints):
            points.append((center[0]+radius*cos(i*angle), center[1]+radius*sin(i*angle)))
        return points

    def sumOfLine(self, line):
        global image
        res = 0
        for pixel in line:
            res += image[pixel[0]][pixel[1]]
        return res

    def subtractLine(self, rr, cc):
        global image
        image[rr, cc] = image[rr, cc] - 1

    def precomputeLines(self):
        cache = {}
        for i in range(self.numpoints):
            for j in range(i + 1, self.numpoints):
                x0, y0 = self.circle[i]
                x1, y1 = self.circle[j]
                pointA = self.mapCoordsToIndices(x0, y0)
                pointB = self.mapCoordsToIndices(x1, y1)
                if pointA[0]>pointB[0]:
                    pointA, pointB = pointB, pointA
                i0, j0 = pointA
                i1, j1 = pointB
                rr, cc = bresenham_line(i0, j0, i1, j1)
                cache[(i, j)] = (rr, cc)
        return cache

    def line_score(self, rr, cc):
        return np.mean(image[rr, cc]) if len(rr) > 0 else -np.inf  

    def bestLineFromPoint(self, pointIndex, minIndex = 0, cache=[], instructions= []):
        maxSum = -np.infty
        linePoints = (([0, 0]), ([0, 0]))
        linePixels = []
        nextPoint = -1
        for j in range(minIndex, self.numpoints):
            if j == pointIndex or (pointIndex, j) in instructions or (j, pointIndex) in instructions:
                continue
            rr, cc = cache[(min(pointIndex, j), max(pointIndex, j))]
            tmaxSum = np.mean(image[rr, cc]) if len(rr) > 0 else -np.inf  
            if tmaxSum > maxSum:
                maxSum = tmaxSum
                x0, y0 = self.circle[pointIndex]
                x1, y1 = self.circle[j]
                linePoints = (([x0, x1]), ([y0, y1]))
                linePixels = rr, cc
                nextPoint = j
        return maxSum, linePoints, linePixels, nextPoint

    def generateLines(self, cache):
        global image
        pointIndex = -1
        maxSum = -np.infty
        cc, rr = None, None
        startIndex = None
        instructions = []
        res = []
        for i in range(self.numpoints-1):
            tmaxSum, newlinePoints, line, nextPoint = self.bestLineFromPoint(i, i+1, cache)
            if len(line) > 0 and tmaxSum > maxSum:
                maxSum = tmaxSum
                linePoints = newlinePoints
                cc, rr = line
                pointIndex = nextPoint
                startIndex = i
        res.append(linePoints)
        self.subtractLine(cc, rr)
        instructions.append((startIndex, pointIndex))
        #yield linePoints, instructions

        counter = 0
        csum = np.sum(image)
        while csum > 0:
            counter+=1
            print(counter, ": ", csum)
            tmaxSum, tlinePoints, line, nextPoint = self.bestLineFromPoint(pointIndex=pointIndex, cache=cache, instructions=instructions)
            instructions.append((pointIndex, nextPoint))
            linePoints = tlinePoints
            cc, rr = line
            pointIndex = nextPoint
            self.subtractLine(cc, rr)
            csum = np.sum(image)
            res.append(linePoints)
        #yield linePoints, instructions
        return res, instructions

    def generateInstructions(self, instructions):
        filePath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")])
        with open(filePath, 'w') as file:
            file.write(str(instructions))

    def generateFromInstructions(self, instructions, cache):
        lines = []
        for (i, j) in instructions:
            rr, cc = cache[(min(i, j), max(i, j))]
            self.subtractLine(rr, cc)
            x0, y0 = self.circle[i]
            x1, y1 = self.circle[j]
            lines.append((([x0, x1]), ([y0, y1])))
        return lines

def animate():
    sa = StringArt("Pablo1.jpg")
    #sa = StringArt("BlackWhiteHeartTest.jpg")
    sa.cleanImage()
    sa.circle = sa.generateCircle(numpoints=sa.numpoints)
    sa.cache = sa.precomputeLines()

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    plt.axis('off')

    # Draw circle points once
    for (x, y) in sa.circle:
        ax.plot(x, y, 'bo', markersize=2)

    # Convert generator to iterator
    line_generator = sa.generateLines(sa.cache)

    # Keep track of all drawn lines
    drawn_lines = []

    def update(frame):
        try:
            x, y = next(line_generator)   # get next line
            line, = ax.plot(x, y, color='black', linewidth=0.08)
            drawn_lines.append(line)
            return drawn_lines   # return ALL lines so far
        except StopIteration:
            return drawn_lines

    ani = FuncAnimation(fig, update, blit=True, interval=50, repeat=False)
    plt.show()

def plotFromInstructions():
    sa = StringArt("Pablo1.jpg")
    #sa = StringArt("BlackWhiteHeartTest.jpg")
    sa.cleanImage()
    sa.circle = sa.generateCircle(numpoints=sa.numpoints)
    sa.cache = sa.precomputeLines()

    filePath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    with open(filePath, 'r') as file:
        instructions = eval(file.read())

    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    lines = sa.generateFromInstructions(instructions, sa.cache)

    plt.axis('off')
    for x, y in lines:
        plt.plot(x, y, color='black', linewidth=0.1)
    for (x, y) in sa.circle:
        plt.plot(x, y, 'bo')
    plt.show()

def main():
    sa = StringArt("Pablo1.jpg")
    #sa = StringArt("BlackWhiteHeartTest.jpg")
    sa.cleanImage()
    sa.circle = sa.generateCircle(numpoints=sa.numpoints)
    sa.cache = sa.precomputeLines()

    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    lines, instructions = sa.generateLines(sa.cache)
     
    sa.generateInstructions(instructions)

    plt.axis('off')
    for x, y in lines:
        plt.plot(x, y, color='black', linewidth=0.1)
    for (x, y) in sa.circle:
        plt.plot(x, y, 'bo')
    plt.show()    


if __name__ == "__main__":
    #main()
    plotFromInstructions()
