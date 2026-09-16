# OpenCV Face & Eye Detection

A beginner/intermediate-friendly computer vision project that detects
human faces and eyes in images (or a live webcam feed) using OpenCV's
built-in Haar Cascade classifiers, draws bounding boxes around each
detection, and saves the annotated result to disk.

This README is written assuming **you have never seen this project
before**. Follow it top to bottom and you will be able to clone,
install, and run the project successfully.

---

## 1. Project Overview

The project takes an input image (or webcam frame), preprocesses it,
runs face detection, then searches for eyes *inside* each detected
face, and finally draws labeled bounding boxes around every face and
eye found. The annotated image is saved to an `output/` folder so
results are reproducible and easy to include in a report.

## 2. Problem Statement

Manually locating faces (and finer features like eyes) in an image is
trivial for a human but requires an automated visual pattern-matching
approach for a computer. The goal of this project is to build a
reliable, explainable pipeline that can automatically **detect and
localize human faces and eyes** in arbitrary photographs, using only
classical (non deep-learning) computer vision techniques so the
approach is transparent and runs comfortably on a normal laptop CPU
with no GPU and no internet-downloaded model weights.

## 3. Objectives

- Read and display images using OpenCV.
- Apply standard preprocessing (grayscale conversion, denoising,
  histogram equalization) to improve detection reliability.
- Detect faces using a Haar Cascade classifier.
- Detect eyes within each detected face region (feature extraction
  within a region of interest).
- Draw clearly labeled bounding boxes around every detected face and
  eye.
- Save the final annotated image to an output folder.
- Support both a batch "process all images in a folder" mode and a
  live webcam mode.
- Handle missing/invalid/corrupted input gracefully instead of
  crashing.

## 4. Features

- ✅ Face detection using Haar Cascades
- ✅ Eye detection restricted to each face's region (more accurate,
  fewer false positives than scanning the whole image)
- ✅ Image preprocessing pipeline: resize → grayscale → denoise →
  histogram equalization
- ✅ Bounding boxes + text labels drawn on the output image
- ✅ Batch mode: automatically processes every image in `input/`
- ✅ Single-image mode: process one specific file
- ✅ Live webcam mode
- ✅ Graceful error handling for missing/corrupt files or an
  unavailable webcam
- ✅ Timestamped output filenames so results are never overwritten
- ✅ No hardcoded, machine-specific file paths — works on any
  Windows/macOS/Linux machine

## 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.9+ | Programming language |
| OpenCV (`opencv-python`) | Image I/O, preprocessing, Haar Cascade detection, drawing |
| NumPy | Underlying array operations for image data |
| argparse (standard library) | Command-line interface |

## 6. Project / Folder Structure

```text
opencv-image-detection/
│
├── README.md                 <- This file
├── requirements.txt          <- Python dependencies
├── main.py                   <- Entry point / CLI (run this file)
├── src/
│   ├── __init__.py
│   ├── preprocessing.py      <- Resize, grayscale, denoise, equalize
│   ├── detector.py           <- FaceEyeDetector (Haar Cascade logic)
│   └── utils.py               <- File/folder helper functions
├── input/
│   └── README.md             <- Where to place your input images
├── output/                   <- Annotated results are saved here (auto-created)
├── screenshots/              <- Place report screenshots here
└── report/
    └── project_report.md     <- Full academic project report
```

## 7. Prerequisites

- A computer running Windows, macOS, or Linux (tested with Windows in
  mind, as requested).
- **Python 3.9 or newer** installed.
  - Check your version:
    ```bash
    python --version
    ```
  - If Python is not installed, download it from
    [python.org/downloads](https://www.python.org/downloads/) and
    make sure to tick **"Add Python to PATH"** during installation on
    Windows.
- A webcam is only required if you want to use `--mode webcam`. It is
  **not required** for image mode.

## 8. Setting Up the Project

### 8.1 Get the code

Either clone the repository:

```bash
git clone <your-repository-url>
cd opencv-image-detection
```

or simply download/copy the `opencv-image-detection/` folder onto
your computer and open a terminal inside it.

### 8.2 Create and activate a virtual environment

Using a virtual environment keeps this project's dependencies
isolated from other Python projects on your machine.

**Windows (Command Prompt / PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll know it worked when you see `(venv)` at the start of your
terminal prompt.

### 8.3 Install dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs `opencv-python` and `numpy` at the tested versions.

> No additional configuration, API keys, or external downloads are
> required — the Haar Cascade classifier files used for detection
> ship inside the `opencv-python` package itself.

## 9. Where to Place Input Images

Put one or more `.jpg`, `.jpeg`, `.png`, `.bmp`, or `.webp` images
inside the `input/` folder. See `input/README.md` for details. Use
clear, front-facing photos of people for the most reliable face/eye
detection results.

## 10. Exact Commands to Run the Project

Make sure your virtual environment is activated and you are in the
project's root folder (`opencv-image-detection/`) before running any
of these.

**Process every image inside `input/`:**
```bash
python main.py --mode image
```

**Process one specific image:**
```bash
python main.py --mode image --input input/your_image.jpg
```

**Process one image and also open a preview window:**
```bash
python main.py --mode image --input input/your_image.jpg --show
```

**Run live detection using your webcam (press `q` to quit):**
```bash
python main.py --mode webcam
```

**See all available options:**
```bash
python main.py --help
```

## 11. Expected Output

- For image mode: an annotated copy of each input image is saved
  inside `output/`, named like
  `your_image_detected_20260916_143210.jpg`, with green rectangles
  around detected faces (labeled "Face") and blue rectangles around
  detected eyes inside each face.
- The terminal also prints how many faces and eyes were found per
  image, e.g.:
  ```text
  [INFO] Processing: input/sample1.jpg
  [RESULT] Faces detected: 1 | Eyes detected: 2
  [INFO] Output saved to: output/sample1_detected_20260916_143210.jpg
  ```
- For webcam mode: a live window shows the camera feed with faces and
  eyes boxed and labeled in real time, plus a running count overlaid
  on screen, until you press `q`.

## 12. How the Detection Works

1. **Read the image** with `cv2.imread`.
2. **Preprocess**: resize (for consistent performance), convert to
   grayscale (Haar Cascades operate on grayscale intensity patterns,
   not color), apply a light Gaussian blur to reduce noise, then
   apply histogram equalization to normalize contrast/lighting.
3. **Face detection**: `cv2.CascadeClassifier.detectMultiScale()`
   slides a search window over the image at multiple scales, using a
   Haar Cascade model (`haarcascade_frontalface_default.xml`, bundled
   with OpenCV) trained to recognize face-like intensity patterns.
   It returns a list of `(x, y, width, height)` boxes.
4. **Eye detection**: for each detected face box, the region is
   cropped out and searched again with a second cascade
   (`haarcascade_eye.xml`), restricted to that smaller region. This
   is both faster and more accurate than searching the whole frame,
   since eyes only ever appear inside a face.
5. **Annotation**: `cv2.rectangle` and `cv2.putText` draw the
   bounding boxes and labels onto the original color image.
6. **Save**: the annotated image is written to `output/` with
   `cv2.imwrite`, using a timestamped filename.

## 13. Example Input/Output

| Input | Output |
|---|---|
| A plain front-facing photo of a person in `input/` | Same photo in `output/`, with a green box around the face labeled "Face" and blue boxes around each visible eye |

Add your own before/after screenshots to the `screenshots/` folder
and reference them here and in your report once you've run the
project on your own images.

## 14. Limitations

- Haar Cascades work best on **clear, front-facing, well-lit faces**;
  accuracy drops for extreme angles, heavy occlusion (sunglasses,
  masks), very small faces, or poor lighting.
- Eye detection can occasionally miss eyes that are closed, angled,
  or partially covered by hair/glasses glare.
- This is a classical computer-vision approach (not deep learning),
  so it will not match the accuracy of modern neural-network-based
  face detectors (e.g., MTCNN, RetinaFace) on difficult images — the
  trade-off is that it needs no dataset, training, or GPU.
- Webcam mode requires a functioning, accessible camera device.

## 15. Future Improvements

- Swap in a deep-learning-based detector (e.g., OpenCV's DNN face
  detector or MediaPipe) for higher accuracy on difficult images.
- Add command-line tunable parameters for `scaleFactor`/
  `minNeighbors` so users can trade off speed vs. sensitivity.
- Add automated unit tests using a small set of sample images with
  known expected face counts.
- Add support for detecting other objects (e.g., smiles, full body)
  using additional bundled Haar Cascades.
- Package the project as a simple GUI (e.g., using Tkinter or
  Streamlit) for non-technical users.

## 16. Credits / References

- OpenCV documentation: [https://docs.opencv.org/](https://docs.opencv.org/)
- OpenCV Cascade Classifier tutorial:
  [https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)
- Haar Cascade classifier files: bundled with the `opencv-python`
  package (`cv2.data.haarcascades`), originally from the OpenCV
  project (Viola-Jones object detection framework).

---

*Prepared as a college/course project demonstrating OpenCV
fundamentals: image I/O, preprocessing, detection, and annotation.*
