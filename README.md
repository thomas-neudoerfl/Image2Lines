# String Art Generator 

This project recreates the effect of **string art** (drawings made by connecting points on a circular frame with straight lines) using image processing and a greedy algorithm.

It takes an image, simplifies it into a grayscale intensity map, and then iteratively draws lines between pegs on a circle to approximate the original image. The result looks like an image "stitched" with thread.

---

## Features

* Converts any image into a **string art representation**.
* Uses **Bresenham’s line algorithm** for efficient pixel traversal.
* Supports both **static output** (final drawing) and **animated rendering** (watch the art being created line by line).
* Exports **line instructions** as a text file => can be used to physically recreate the artwork.

---

## Requirements

* Python 3.8+
* Libraries:

  ```bash
  pip install matplotlib scikit-image numpy tkinter
  ```

---

## Usage

Run the main script:

```bash
python LinesAndDotsTest.py
```

This will launch a graphical user interface (GUI) for generating string art from images.

### Workflow

1. **Select Image**: Click the "Select .jpg File" button to choose an image file for processing.
2. **Adjust Line Width**: Use the "Line Width" slider to set the thickness of the lines before or after generating the plot.
3. **Generate String Art**: The program will process the image, generate circle points, and display the string art visualization in a matplotlib window.
4. **Update Line Width**: After the plot is generated, you can further adjust the line thickness by moving the slider and clicking the "Update Line Width" button in the main window. The plot will update in real time.
5. **Export Instructions**: After generation, you can save the list of line instructions for physical recreation by clicking the "Instructions" button in the success dialog.
6. **Regenerate from Instructions**: Use the "Regenerate" button to load a previously saved instructions file and visualize the corresponding string art.

The interface also includes a progress bar to indicate processing status and an exit button to close the application.

---

## Example Output

* **Final drawing:** clean string art visualization.
* **Animation:** progressive construction of the image.
* **Instructions file:** a sequence of peg-to-peg connections for physical recreation.

---

## Notes

* Images work best in **black & white** or high-contrast mode.
* You can adjust parameters like:

  * `numpoints`: number of circle pegs
  * `maxvalue`: contrast scaling
  * `linewidth`: thickness of drawn lines


