import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
from skimage.draw import line as bresenham_line
import numpy as np
from numpy import cos, sin
import tkinter as tk
from tkinter import filedialog, ttk
import os
from skimage.transform import resize
import threading

class StringArt:
    def __init__(self, from_instructions=False):
        global image, real_radius, total_length
        if not from_instructions:
            img_path = filedialog.askopenfilename(filetypes=[("Image Files", ["*.jpg", "*.jpeg", "*.png"])] )
            img = mpimg.imread(img_path)
            image = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
            self.height = min(image.shape)
        else:
            print("Invalid image path provided.")
            img, image = None, None
            self.height = 1

        real_radius = 20.6
        total_length = 0
        self.numpoints = 4*60
        self.numlines = 3000
        self.resolution = 288
        self.maxvalue = 12
        self.factor = self.maxvalue/256
        self.circle = []
        self.cache = {}

    def cleanImage(self):
        global image
        if self.height > self.resolution:
            scale = self.resolution / self.height
            new_size = (int(image.shape[0] * scale), int(image.shape[1] * scale))
            image = resize(image, new_size, preserve_range=True, anti_aliasing=True).astype(image.dtype)
            self.height = min(image.shape)
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
        maxSum = -np.inf
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

    def UpdateRealLengthOfLine(self, LinePoints):
        global real_radius, total_length
        x0, x1 = LinePoints[0]
        y0, y1 = LinePoints[1]
        length = np.sqrt((x1 - x0)**2 + (y1 - y0)**2) * real_radius
        total_length += length
    
    def generateLines(self, cache):
        global image, progress
        pointIndex = -1
        maxSum = -np.inf
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
        self.UpdateRealLengthOfLine(linePoints)
        print(linePoints)
        self.subtractLine(cc, rr)
        instructions.append((startIndex, pointIndex))
        #yield linePoints, instructions

        counter = 0
        progress.set(0)                 
        while counter < self.numlines and counter < self.numpoints*(self.numpoints-1)/2:
            counter+=1
            if counter % 100 == 0:
                progress.set((counter/self.numlines)*100)
                print(counter/self.numlines)
            root.update_idletasks()
            tmaxSum, tlinePoints, line, nextPoint = self.bestLineFromPoint(pointIndex=pointIndex, cache=cache, instructions=instructions)
            instructions.append((pointIndex, nextPoint))
            linePoints = tlinePoints
            if not line or len(line) != 2 or len(line[0]) == 0 or len(line[1]) == 0:
                break
            cc, rr = line
            pointIndex = nextPoint
            self.subtractLine(cc, rr)
            #currSum = np.sum(image)
            res.append(linePoints)
            self.UpdateRealLengthOfLine(linePoints)
        #yield linePoints, instructions
        return res, instructions

    def generateInstructions(self, instructions):
        filePath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")])
        with open(filePath, 'w') as file:
            file.write(str(instructions))

    def generateFromInstructions(self, instructions):
        lines = []
        for (i, j) in instructions:
            x0, y0 = self.circle[i]
            x1, y1 = self.circle[j]
            lines.append((([x0, x1]), ([y0, y1])))
        return lines


def exit_program():
    root.destroy()
    quit()
    
def plotFromInstructions():
    sa = StringArt(True)
    
    filePath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    with open(filePath, 'r') as file:
        instructions = eval(file.read())
    sa.numlines = instructions.__len__()
    sa.numpoints = max(max(i, j) for (i, j) in instructions) + 1

    sa.circle = sa.generateCircle(numpoints=sa.numpoints)
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    lines = sa.generateFromInstructions(instructions)

    plt.axis('off')
    for x, y in lines:
        plt.plot(x, y, color='black', linewidth=0.1)
    for (x, y) in sa.circle:
        plt.plot(x, y, 'bo')
    plt.show()


def plotStringArt():
    global progress, linewidth_var, line_objects, fig, numlines_var, resolution_var, numpoints_var, total_length
    def worker():
        sa = StringArt()
        sa.numlines = numlines_var.get()
        sa.resolution = resolution_var.get()
        sa.numpoints = numpoints_var.get()
        sa.cleanImage()
        sa.circle = sa.generateCircle(numpoints=sa.numpoints)
        sa.cache = sa.precomputeLines()
        def update_progress(val):
            progress.set(val)
            root.update_idletasks()
        global progress
        old_progress_set = progress.set
        def patched_set(val):
            root.after(0, lambda: old_progress_set(val))
        progress.set = patched_set
        lines, instructions = sa.generateLines(sa.cache)
        progress.set = old_progress_set
        root.after(0, lambda: show_results(lines, instructions, sa))
    def show_results(lines, instructions, sa):
        global line_objects, fig, linewidth_var
        print(f"Total length of string used: {total_length:.2f} cm")
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        plt.axis('off')
        lw = linewidth_var.get()
        line_objects = []
        for x, y in lines:
            line, = ax.plot(x, y, color='black', linewidth=lw)
            line_objects.append(line)
        for (x, y) in sa.circle:
            ax.plot(x, y, 'bo')
        plt.show()
        success_dialog = tk.Toplevel()
        success_dialog.title("Success")
        path_label = tk.Label(success_dialog, text=f"Generate instructions", wraplength=400)
        path_label.pack(pady=10)
        button_frame = tk.Frame(success_dialog)
        button_frame.pack(pady=10)
        def openInstructions():
            sa.generateInstructions(instructions)
            success_dialog.destroy()
        open_button = tk.Button(button_frame, text="Instructions", command=openInstructions)
        open_button.pack(side=tk.LEFT, padx=10)
        close_button = tk.Button(button_frame, text="Close", command=success_dialog.destroy)
        close_button.pack(side=tk.RIGHT, padx=10)
        progress.set(0)
        root.update_idletasks()
    threading.Thread(target=worker).start()

def update_main_linewidth():
    global line_objects, fig, linewidth_var
    if line_objects and fig:
        new_lw = linewidth_var.get()
        for line in line_objects:
            line.set_linewidth(new_lw)
        fig.canvas.draw_idle()

def update_main_numlines():
    global line_objects, fig, numlines_var
    if line_objects and fig:
        num_lines = numlines_var.get()
        for idx, line in enumerate(line_objects):
            line.set_visible(idx < num_lines)
        fig.canvas.draw_idle()

def main():
        
    global root, progress, linewidth_var, line_objects, fig, numlines_var, resolution_var, numpoints_var, total_length
    root = tk.Tk()
    root.title("String Art Generator")
    
    title_label = tk.Label(root, text="String Art Generator", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    instructions_button = tk.Button(button_frame, text="Regenerate", command=plotFromInstructions, width=15)
    instructions_button.pack(side=tk.LEFT, padx=10)
    
    select_button = tk.Button(button_frame, text="Select .jpg File", command=plotStringArt, width=15, bg="green", fg="white")
    select_button.pack(side=tk.LEFT, padx=10)
    
    exit_button = tk.Button(button_frame, text="Exit", command=exit_program, width=15, bg="red", fg="white")
    exit_button.pack(side=tk.LEFT, padx=10)

    numpoints_var = tk.IntVar(value=240)
    numpoints_label = tk.Label(root, text="Number of Points:")
    numpoints_label.pack()
    numpoints_frame = tk.Frame(root)
    numpoints_frame.pack(fill=tk.X, padx=20)
    numpoints_slider = tk.Scale(numpoints_frame, variable=numpoints_var, from_=10, to=1000, resolution=1, orient=tk.HORIZONTAL)
    numpoints_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
    numpoints_entry = tk.Entry(numpoints_frame, width=6)
    numpoints_entry.pack(side=tk.RIGHT)
    numpoints_entry.insert(0, str(numpoints_var.get()))
    def update_numpoints_from_entry(event):
        try:
            val = int(numpoints_entry.get())
            numpoints_var.set(val)
        except ValueError:
            pass
    numpoints_entry.bind('<Return>', update_numpoints_from_entry)
    def update_numpoints_entry(*args):
        numpoints_entry.delete(0, tk.END)
        numpoints_entry.insert(0, str(numpoints_var.get()))
    numpoints_var.trace_add('write', update_numpoints_entry)

    resolution_var = tk.IntVar(value=288)
    resolution_label = tk.Label(root, text="Resolution:")
    resolution_label.pack()
    resolution_frame = tk.Frame(root)
    resolution_frame.pack(fill=tk.X, padx=20)
    resolution_slider = tk.Scale(resolution_frame, variable=resolution_var, from_=10, to=1000, resolution=10, orient=tk.HORIZONTAL)
    resolution_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
    resolution_entry = tk.Entry(resolution_frame, width=6)
    resolution_entry.pack(side=tk.RIGHT)
    resolution_entry.insert(0, str(resolution_var.get()))
    def update_resolution_from_entry(event):
        try:
            val = int(resolution_entry.get())
            resolution_var.set(val)
        except ValueError:
            pass
    resolution_entry.bind('<Return>', update_resolution_from_entry)
    def update_resolution_entry(*args):
        resolution_entry.delete(0, tk.END)
        resolution_entry.insert(0, str(resolution_var.get()))
    resolution_var.trace_add('write', update_resolution_entry)

    numlines_var = tk.IntVar(value=3000)
    numlines_label = tk.Label(root, text="Number of Lines:")
    numlines_label.pack()
    numlines_frame = tk.Frame(root)
    numlines_frame.pack(fill=tk.X, padx=20)
    numlines_slider = tk.Scale(numlines_frame, variable=numlines_var, from_=0, to=10000, resolution=10, orient=tk.HORIZONTAL)
    numlines_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
    numlines_entry = tk.Entry(numlines_frame, width=6)
    numlines_entry.pack(side=tk.RIGHT)
    numlines_entry.insert(0, str(numlines_var.get()))
    def update_numlines_from_entry(event):
        try:
            val = int(numlines_entry.get())
            numlines_var.set(val)
        except ValueError:
            pass
    numlines_entry.bind('<Return>', update_numlines_from_entry)
    def update_numlines_entry(*args):
        numlines_entry.delete(0, tk.END)
        numlines_entry.insert(0, str(numlines_var.get()))
    numlines_var.trace_add('write', update_numlines_entry)

    linewidth_var = tk.DoubleVar(value=0.1)
    linewidth_label = tk.Label(root, text="Line Width:")
    linewidth_label.pack()
    linewidth_frame = tk.Frame(root)
    linewidth_frame.pack(fill=tk.X, padx=20)
    linewidth_slider = tk.Scale(linewidth_frame, variable=linewidth_var, from_=0.01, to=2.0, resolution=0.01, orient=tk.HORIZONTAL)
    linewidth_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
    linewidth_entry = tk.Entry(linewidth_frame, width=6)
    linewidth_entry.pack(side=tk.RIGHT)
    linewidth_entry.insert(0, str(linewidth_var.get()))
    def update_linewidth_from_entry(event):
        try:
            val = float(linewidth_entry.get())
            linewidth_var.set(val)
        except ValueError:
            pass
    linewidth_entry.bind('<Return>', update_linewidth_from_entry)
    def update_linewidth_entry(*args):
        linewidth_entry.delete(0, tk.END)
        linewidth_entry.insert(0, str(linewidth_var.get()))
    linewidth_var.trace_add('write', update_linewidth_entry)

    update_main_lw_button = tk.Button(root, text="Update Line Width", command=update_main_linewidth)
    update_main_lw_button.pack(pady=5)
    update_main_numlines_button = tk.Button(root, text="Update Number of Lines", command=update_main_numlines)
    update_main_numlines_button.pack(pady=5)

    progress = tk.IntVar()
    progressbar = ttk.Progressbar(variable=progress)
    progressbar.pack(pady=10, fill=tk.X, padx=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
