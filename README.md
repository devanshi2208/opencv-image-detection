# OpenCV Face & Eye Detection

A Python-based computer vision project that uses OpenCV to detect human faces and eyes in images. The project uses Haar Cascade classifiers to identify faces and eyes, draw bounding boxes around them, and save the processed image.

## 1. Project Overview

This project demonstrates basic image detection using OpenCV.

The program takes an input image, processes it, detects faces in the image, and then detects eyes within the detected face regions. The detected faces and eyes are highlighted using bounding boxes and labels.

The project also supports live detection using a webcam.

## 2. Problem Statement

Detecting faces and facial features manually in an image can be time-consuming when working with multiple images. This project aims to automate the process of detecting human faces and eyes using computer vision techniques.

The project uses Haar Cascade classifiers provided by OpenCV, making it possible to perform detection without requiring a GPU or training a deep learning model.

## 3. Objectives

* To understand the basics of computer vision using OpenCV.
* To read and process images using Python.
* To convert images into grayscale for detection.
* To detect human faces using Haar Cascade classifiers.
* To detect eyes within detected face regions.
* To draw bounding boxes around detected faces and eyes.
* To save the processed images.
* To support detection using both images and a webcam.
* To handle invalid or missing input files without crashing.

## 4. Features

* Face detection using Haar Cascade classifiers.
* Eye detection inside detected face regions.
* Image preprocessing before detection.
* Bounding boxes and labels for detected faces and eyes.
* Processing of multiple images from the input folder.
* Option to process a single image.
* Live face and eye detection using a webcam.
* Automatically saves detection results in the output folder.
* Uses relative file paths instead of machine-specific paths.
* Simple command-line interface.

## 5. Technologies Used

| Technology | Purpose                                 |
| ---------- | --------------------------------------- |
| Python     | Main programming language               |
| OpenCV     | Image processing and face/eye detection |
| NumPy      | Image and array operations              |
| argparse   | Command-line arguments                  |

## 6. Project Structure

```text
opencv-image-detection/
│
├── README.md
├── requirements.txt
├── main.py
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── detector.py
│   └── utils.py
│
├── input/
│   └── README.md
│
├── output/
│
├── screenshots/
│
└── report/
    └── project_report.md
```

### Description of Important Files

* `main.py` - Main file used to run the project.
* `preprocessing.py` - Contains image preprocessing functions.
* `detector.py` - Contains face and eye detection logic.
* `utils.py` - Contains file and folder handling functions.
* `requirements.txt` - Contains the Python dependencies required by the project.
* `input/` - Folder where input images are placed.
* `output/` - Folder where processed images are saved.
* `screenshots/` - Folder for project screenshots.
* `report/` - Folder containing the project report.

## 7. Prerequisites

Before running the project, make sure you have:

* Python 3.9 or newer
* Git (optional)
* A working webcam if you want to use webcam mode

Check your Python version:

```bash
python --version
```

If Python is not installed, download it from:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

On Windows, make sure to select **Add Python to PATH** during installation.

## 8. Getting the Project

The project repository is available on GitHub:

[https://github.com/devanshi2208/opencv-image-detection](https://github.com/devanshi2208/opencv-image-detection)

To clone the repository, open a terminal and run:

```bash
git clone https://github.com/devanshi2208/opencv-image-detection.git
```

Then enter the project folder:

```bash
cd opencv-image-detection
```

## 9. Setting Up the Environment

Using a virtual environment is recommended so that the project's dependencies remain separate from other Python projects.

### Windows

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

After activation, `(venv)` should appear at the beginning of the terminal.

### macOS/Linux

Create the virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

## 10. Installing Dependencies

After activating the virtual environment, install the required packages:

```bash
pip install -r requirements.txt
```

The main dependencies are OpenCV and NumPy.

No API key or external service is required for this project.

The Haar Cascade files used for detection are available through the OpenCV package.

## 11. Adding Input Images

Place the images you want to process inside the `input/` folder.

Supported formats include:

```text
.jpg
.jpeg
.png
.bmp
.webp
```

For better results, use clear and well-lit images where the face is visible.

Example:

```text
input/
└── sample.jpg
```

## 12. Running the Project

Make sure the virtual environment is activated and you are inside the project folder.

### Process All Images

To process all supported images inside the `input/` folder:

```bash
python main.py --mode image
```

### Process One Specific Image

```bash
python main.py --mode image --input input/sample.jpg
```

### Display the Result

To process an image and display the result:

```bash
python main.py --mode image --input input/sample.jpg --show
```

### Run Webcam Detection

To start live face and eye detection using your webcam:

```bash
python main.py --mode webcam
```

Press `q` to close the webcam window.

### View Available Options

```bash
python main.py --help
```

## 13. How the Project Works

The project follows these steps:

### Step 1: Read the Image

The input image is loaded using OpenCV's `cv2.imread()` function.

### Step 2: Preprocess the Image

The image is resized and converted to grayscale. Noise reduction and histogram equalization are also applied to improve the detection process.

### Step 3: Detect Faces

A Haar Cascade classifier is used to detect faces.

OpenCV's `detectMultiScale()` method searches the image at different scales and returns the locations of detected faces.

### Step 4: Detect Eyes

After detecting a face, the program searches for eyes within that face region.

This reduces unnecessary detections because the eye detector focuses only on the detected face.

### Step 5: Draw Bounding Boxes

Bounding boxes and labels are drawn around detected faces and eyes using OpenCV functions such as:

```python
cv2.rectangle()
cv2.putText()
```

### Step 6: Save the Result

The processed image is saved inside the `output/` folder.

## 14. Expected Output

For image detection, the program creates an annotated version of the input image.

The output contains:

* A bounding box around each detected face.
* A label for the detected face.
* Bounding boxes around detected eyes.
* Information about the number of detected faces and eyes in the terminal.

Example terminal output:

```text
[INFO] Processing: input/sample.jpg
[RESULT] Faces detected: 1 | Eyes detected: 2
[INFO] Output saved to: output/sample_detected.jpg
```

The output filename may contain a timestamp so that previous results are not overwritten.

## 15. Example Result

After running the project, the output image will contain bounding boxes around detected faces and eyes.

Add your own screenshots of the input and output after testing the project.

For example:

```text
screenshots/
├── input_image.png
└── detection_result.png
```

You can display a result screenshot in this README using:

```markdown
![Detection Result](screenshots/detection_result.png)
```

## 16. Limitations

* Haar Cascade detection works best with clear, front-facing faces.
* Poor lighting can reduce detection performance.
* Faces at extreme angles may not be detected correctly.
* Sunglasses, masks, hair, or other objects covering the face can affect detection.
* Eye detection may not work correctly when eyes are closed or partially covered.
* Haar Cascades may produce false detections in some images.
* Webcam mode requires a working camera.

## 17. Applications

Face and eye detection can be used as a basic component in applications such as:

* Computer vision projects
* Image analysis
* Human-computer interaction
* Basic attendance systems
* Camera-based applications
* Facial feature detection
* Educational computer vision applications

## 18. Future Improvements

The project can be improved by:

* Using modern deep-learning-based face detection models.
* Improving detection for different face angles and lighting conditions.
* Adding detection for additional facial features.
* Adding a graphical user interface.
* Adding automated tests for different input images.
* Adding adjustable detection parameters.
* Extending the project to detect other objects.

## 19. GitHub Repository

The complete project is available here:

[https://github.com/devanshi2208/opencv-image-detection](https://github.com/devanshi2208/opencv-image-detection)

## 20. References

* OpenCV Documentation:
  [https://docs.opencv.org/](https://docs.opencv.org/)

* OpenCV Cascade Classifier Documentation:
  [https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)

* OpenCV Official Website:
  [https://opencv.org/](https://opencv.org/)

## 21. Project Report

A structured project report is included in the `report/` folder.

The report covers the project background, objectives, methodology, implementation, results, limitations, applications, and future scope.

---

**This project was created as a college/course project to demonstrate fundamental concepts of image processing and object detection using OpenCV.**
