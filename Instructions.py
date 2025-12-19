import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF

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

# Add a GUI that adds the last drawn line for visual feedback

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    format_instructions()