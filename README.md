# String Art Generator 🎨🧵

This project recreates the effect of **string art** (drawings made by connecting points on a circular frame with straight lines) using image processing and a greedy algorithm.

It takes an image, simplifies it into a grayscale intensity map, and then iteratively draws lines between pegs on a circle to approximate the original image. The result looks like an image "stitched" with thread.

---

## ✨ Features

* Converts any image into a **string art representation**.
* Uses **Bresenham’s line algorithm** for efficient pixel traversal.
* Supports both **static output** (final drawing) and **animated rendering** (watch the art being created line by line).
* Exports **line instructions** as a text file => can be used to physically recreate the artwork.

---

## ⚙️ Requirements

* Python 3.8+
* Libraries:

  ```bash
  pip install matplotlib scikit-image numpy tkinter
  ```

---

## 🚀 Usage

Run the main script:

```bash
python string_art.py
```

* By default, it loads `Pablo1.jpg` (replace with your own image).
* The program processes the image, generates circle points, and finds the best sequence of lines.
* The final string art visualization will be displayed with `matplotlib`.
* It will prompt you to save the **list of line instructions**.

To watch the artwork appear line by line:

```python
animate()
```

---

## 📂 Example Output

* **Final drawing:** clean string art visualization.
* **Animation:** progressive construction of the image.
* **Instructions file:** a sequence of peg-to-peg connections for physical recreation.

---

## 🧩 Notes

* Images work best in **black & white** or high-contrast mode.
* You can adjust parameters like:

  * `numpoints`: number of circle pegs
  * `maxvalue`: contrast scaling
  * `linewidth`: thickness of drawn lines


