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
from fpdf import FPDF
from LinesAndDotsTest import StringArt

def format_instructions():
    # Open a file dialog to select the instructions file
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        print("No file selected.")
        return

    # Read the instructions from the file
    with open(file_path, 'r') as file:
        try:
            instructions = eval(file.read())  # Convert string to list of tuples
        except Exception as e:
            print(f"Error reading instructions: {e}")
            return

    # Format the instructions
    formatted_instructions = []
    for i, (start, end) in enumerate(instructions, start=1):
        formatted_instructions.append(f"{i}. Start: {start}, End: {end}")

    # Create a PDF instance
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add formatted instructions to the PDF
    for line in formatted_instructions:
        pdf.cell(0, 10, txt=line, ln=True)

    # Save the PDF
    save_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[("PDF files", "*.pdf")])
    if not save_path:
        print("No save location selected.")
        return

    pdf.output(save_path)

    print(f"Formatted instructions saved to {save_path}")

def update_main_linewidth():
    global instructions, fig, linewidth_var
    if instructions and fig:
        new_lw = linewidth_var.get()
        for line in instructions:
            line.set_linewidth(new_lw)
        fig.canvas.draw_idle()

def update_main_numlines():
    global instructions, fig, numlines_var
    if instructions and fig:
        num_lines = numlines_var.get()
        for idx, line in enumerate(instructions):
            line.set_visible(idx < num_lines)
        fig.canvas.draw_idle()

        
# Add a GUI that adds the last drawn line for visual feedback
def draw_next_line():
    global fig, linewidth_var, numlines_var, progress, instructions
    

def exit_program():
    root.destroy()
    quit()

def main():
        
    global root, progress, linewidth_var, line_objects, fig, numlines_var, numpoints, instructions
    
    root = tk.Tk()
    root.title("String Art Generator")

    title_label = tk.Label(root, text="String Art Generator", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    next_button = tk.Button(button_frame, text="Next", command=draw_next_line, width=15)
    next_button.pack(side=tk.LEFT, padx=10)
    
    format_instructions_button = tk.Button(button_frame, text="Generate .pdf", command=format_instructions, width=15, bg="green", fg="white")
    format_instructions_button.pack(side=tk.LEFT, padx=10)
    
    exit_button = tk.Button(button_frame, text="Exit", command=exit_program, width=15, bg="red", fg="white")
    exit_button.pack(side=tk.LEFT, padx=10)


    numlines_var = tk.IntVar(value=0)
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
    
    sa = StringArt(True)
    filePath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    with open(filePath, 'r') as file:
        instructions = eval(file.read())

    numlines = instructions.__len__()
    numpoints = max(max(i, j) for (i, j) in instructions) + 1

    sa.circle = sa.generateCircle(numpoints=sa.numpoints)
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    plt.axis('off')
    for (x, y) in sa.circle:
        plt.plot(x, y, 'bo')
    plt.show()

    root.mainloop()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()