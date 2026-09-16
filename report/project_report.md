# Project Report

> **Note:** Sections marked **[ADJUST TO COURSE FORMAT]** should be
> checked against your specific course/assignment page — cover page
> requirements, exact section ordering, word/page limits, and
> citation style can vary by institution. The content below is
> written to be adapted quickly into whatever template your course
> requires.

---

## 1. Title

**Face and Eye Detection Using OpenCV Haar Cascade Classifiers**

**[ADJUST TO COURSE FORMAT]** — Add your name, roll/registration
number, course code, instructor name, and submission date here as
required by your institution's cover page.

---

## 2. Abstract

This project implements a face and eye detection system using the
OpenCV computer vision library in Python. The system reads an input
image (or live webcam feed), applies a preprocessing pipeline
(resizing, grayscale conversion, denoising, and histogram
equalization), and detects faces using a pretrained Haar Cascade
classifier. For each detected face, the system further searches
within that region to detect eyes, demonstrating region-restricted
feature extraction. Detected faces and eyes are annotated with
labeled bounding boxes and the resulting image is saved to disk. The
project is implemented as a modular, command-line Python application
that can process a single image, a folder of images, or a live
webcam stream, and is designed to run without a GPU or any additional
downloaded models, making it reproducible on any standard laptop.

---

## 3. Introduction

Computer vision enables machines to interpret and process visual
information from the world, and one of its most common applications
is detecting and localizing human faces within images. Face detection
underpins a wide range of real-world systems, including photo
organization software, video conferencing tools (auto-framing/
background blur), security and surveillance systems, and as a
preprocessing step for higher-level tasks such as face recognition or
emotion analysis. This project explores a classical, well-established
approach to this problem — the Haar Cascade classifier — implemented
using the OpenCV library, one of the most widely used open-source
computer vision toolkits.

---

## 4. Problem Statement

Given an arbitrary input image that may or may not contain one or
more human faces, automatically and reliably locate the position and
size of each face, and further locate the eyes within each face,
without any manual annotation or per-image tuning, and produce a
visual output that clearly marks each detection.

---

## 5. Objectives

1. Read and display images programmatically using OpenCV.
2. Apply an effective image preprocessing pipeline to improve
   detection robustness.
3. Detect human faces in an image using a Haar Cascade classifier.
4. Perform feature-level detection (eyes) restricted to each detected
   face's region of interest.
5. Visually annotate detections with bounding boxes and labels.
6. Save processed output images in an organized, reproducible folder
   structure.
7. Support both static-image and real-time webcam workflows.
8. Handle invalid, missing, or corrupted input gracefully.

---

## 6. Literature / Background

Face detection has been an active research area in computer vision
for decades. One of the most influential classical approaches is the
**Viola–Jones object detection framework** (2001), which introduced
Haar-like features combined with an AdaBoost-trained cascade of
classifiers to achieve fast, real-time object detection. This
approach became the basis for OpenCV's `CascadeClassifier`, which is
still widely used today for lightweight, CPU-only detection tasks
because it requires no GPU, no external model downloads, and runs
extremely quickly compared to modern deep-learning detectors.

More recent approaches (e.g., MTCNN, RetinaFace, and other CNN-based
detectors) achieve higher accuracy, especially on difficult poses,
lighting, and occlusion, but require significantly more computational
resources and, in many cases, internet access to download pretrained
model weights. For a college-level, CPU-only, offline-friendly
project, the Haar Cascade approach was chosen as the most practical
and pedagogically appropriate method: it directly demonstrates
classical computer vision concepts (sliding-window search, cascade
classification, region-of-interest restriction) without introducing
the added complexity of deep learning frameworks.

**[ADJUST TO COURSE FORMAT]** — If your course requires citations in
a specific style (APA/IEEE/etc.) or a literature review of multiple
academic papers, expand this section accordingly using the references
in Section 21.

---

## 7. Methodology

The project follows a straightforward image-processing pipeline,
implemented as a modular Python application:

1. **Input acquisition** — an image is loaded from disk (or a frame
   is captured from a webcam).
2. **Preprocessing** — the image is resized for consistent
   performance, converted from BGR color to grayscale (Haar Cascades
   operate on grayscale intensity patterns), lightly denoised with a
   Gaussian blur, and contrast-normalized with histogram
   equalization.
3. **Face detection** — the preprocessed grayscale image is passed to
   `cv2.CascadeClassifier.detectMultiScale()` using the bundled
   `haarcascade_frontalface_default.xml` model, which returns
   bounding boxes for each detected face.
4. **Eye detection (feature extraction)** — for each detected face
   box, the corresponding region of the grayscale image is cropped
   out and passed to a second cascade classifier
   (`haarcascade_eye.xml`) to detect eyes strictly within that
   region.
5. **Annotation** — bounding boxes and text labels are drawn on the
   original color image using `cv2.rectangle` and `cv2.putText`.
6. **Output** — the final annotated image is saved to the `output/`
   folder with a timestamped filename, and detection counts are
   printed to the console.

---

## 8. Technologies and Tools Used

| Category | Tool/Technology |
|---|---|
| Programming language | Python 3.9+ |
| Core CV library | OpenCV (`opencv-python`) |
| Numerical operations | NumPy |
| CLI interface | Python `argparse` (standard library) |
| Detection models | Haar Cascade XML classifiers bundled with OpenCV |
| Version control | Git / GitHub |

---

## 9. System / Project Architecture

```text
                ┌─────────────────┐
                │   Input Image /  │
                │  Webcam Frame    │
                └────────┬─────────┘
                         │
                         ▼
               ┌───────────────────┐
               │  Preprocessing     │
               │ (resize, gray,     │
               │  denoise, equalize)│
               └─────────┬──────────┘
                         │
                         ▼
               ┌───────────────────┐
               │   Face Detection   │
               │ (Haar Cascade)     │
               └─────────┬──────────┘
                         │  for each face
                         ▼
               ┌───────────────────┐
               │   Eye Detection    │
               │ (within face ROI)  │
               └─────────┬──────────┘
                         │
                         ▼
               ┌───────────────────┐
               │    Annotation      │
               │ (boxes + labels)   │
               └─────────┬──────────┘
                         │
                         ▼
               ┌───────────────────┐
               │   Save Output /    │
               │   Display Result   │
               └───────────────────┘
```

The codebase is organized into three logical modules under `src/`:
`preprocessing.py` (image I/O and preprocessing), `detector.py`
(the `FaceEyeDetector` class wrapping the Haar Cascade logic), and
`utils.py` (file/folder helper functions). `main.py` ties these
together behind a command-line interface supporting both batch-image
and live-webcam modes.

---

## 10. Implementation

The implementation is split across four Python files:

- **`main.py`** — the CLI entry point; parses arguments, loads the
  detector, and dispatches to either image-processing or webcam mode.
- **`src/preprocessing.py`** — `load_image()`, `resize_image()`,
  `convert_to_grayscale()`, `denoise_image()`,
  `equalize_histogram()`, and the combined
  `preprocess_for_detection()` pipeline function.
- **`src/detector.py`** — the `FaceEyeDetector` class, which loads
  the two Haar Cascade XML models on initialization and exposes
  `detect_faces()`, `detect_eyes_in_face()`, and
  `detect_and_annotate()`.
- **`src/utils.py`** — folder/file helpers: `list_images()`,
  `build_output_path()`, `save_image()`, and `ensure_dir()`.

See the repository's root `README.md` for the exact commands to run
each mode, and the source files themselves (fully commented) for
line-by-line implementation detail.

---

## 11. Algorithm / Working

**Haar Cascade detection (`detectMultiScale`) works as follows:**

1. The classifier encodes learned Haar-like rectangular features
   (patterns of light/dark regions) that are characteristic of faces
   (e.g., the eye region is typically darker than the cheek region
   below it).
2. A search window slides across the image at multiple positions and
   scales (`scaleFactor` controls how much the window shrinks between
   scales).
3. At each position, a cascade of increasingly complex classifiers
   quickly rejects non-face regions early, so only promising regions
   proceed through the full cascade — this is what makes the
   algorithm fast enough for real time use.
4. `minNeighbors` controls how many overlapping positive detections
   are required to retain a region as a genuine detection (higher
   values reduce false positives at some cost to recall).
5. The same algorithm is re-applied with a different trained cascade
   (`haarcascade_eye.xml`) restricted to each face's cropped region
   to detect eyes.

---

## 12. Dataset / Input Images

No external dataset or downloaded model weights are required. The two
Haar Cascade classifier files
(`haarcascade_frontalface_default.xml` and `haarcascade_eye.xml`) are
distributed as part of the `opencv-python` package itself
(`cv2.data.haarcascades`).

Input images are supplied by the user by placing personal or
course-approved sample photographs into the `input/` folder (see
`input/README.md`). For this report, `[ADD NUMBER]` sample images
were used, sourced from `[ADD SOURCE — e.g., "personal photographs
taken with permission" or a specific royalty-free image site]`.

**[ADJUST TO COURSE FORMAT]** — Fill in the exact number and source
of images you actually tested with, and confirm your course's policy
on using personal photographs versus royalty-free/public datasets.

---

## 13. Results

The system was tested on `[ADD NUMBER]` images containing a total of
`[ADD NUMBER]` faces. Faces were correctly detected in `[ADD NUMBER /
PERCENTAGE]` of cases, and eyes were correctly detected within
`[ADD NUMBER / PERCENTAGE]` of the correctly detected faces. Detection
was most reliable on clear, front-facing, well-lit photographs, and
less reliable on angled faces, low-light images, or faces partially
occluded by hair, glasses, or hands.

**[ADJUST TO COURSE FORMAT]** — Run the project on your own chosen
images and fill in the actual counts/percentages observed, ideally
summarized in a small results table.

| Image | Faces Detected | Eyes Detected | Notes |
|---|---|---|---|
| `sample1.jpg` | `[ADD]` | `[ADD]` | `[ADD]` |
| `sample2.jpg` | `[ADD]` | `[ADD]` | `[ADD]` |

---

## 14. Screenshots / Output

**[ADJUST TO COURSE FORMAT]** — Insert before/after image pairs here
(place the image files in the `screenshots/` folder and reference
them with Markdown image syntax, e.g. `![Detection result](../screenshots/result1.png)`).

---

## 15. Advantages

- No external dataset, training process, or internet-downloaded model
  weights are required — everything needed ships with OpenCV.
- Runs entirely on CPU, suitable for any standard laptop.
- Fast enough for real-time webcam use.
- Transparent, explainable algorithm — well suited to demonstrating
  core computer vision concepts in a course setting.
- Modular, well-commented codebase that is easy to extend.

## 16. Limitations

- Accuracy degrades on extreme head angles, poor lighting, small
  faces, or heavy occlusion.
- Classical Haar Cascades are outperformed in accuracy by modern
  deep-learning face detectors on difficult images.
- Eye detection can occasionally miss closed or partially obscured
  eyes.
- Requires a working webcam device for the real-time mode.

## 17. Applications

- Preprocessing step for face recognition or attendance systems.
- Auto-framing/cropping in photo and video applications.
- Basic security/surveillance motion-and-presence alerting.
- Educational demonstration of classical object detection concepts.

## 18. Future Scope

- Replace or augment Haar Cascades with a deep-learning-based
  detector for improved accuracy.
- Add configurable detection sensitivity via command-line arguments.
- Extend to detect additional features (smile detection, basic
  emotion classification).
- Build a simple graphical user interface for non-technical users.
- Add automated testing with a fixed set of benchmark images.

## 19. Conclusion

This project successfully demonstrates a complete, reproducible face
and eye detection pipeline built with OpenCV in Python. It covers the
full journey from raw image input through preprocessing, detection,
feature-region extraction, annotation, and output — using only
classical computer vision techniques that require no external
datasets or GPU resources. While Haar Cascades have well-understood
accuracy limitations compared to modern deep-learning detectors, they
remain an effective, fast, and pedagogically valuable approach for a
college-level computer vision project, and the modular code structure
leaves clear paths for future improvement.

## 20. References

1. OpenCV Documentation — https://docs.opencv.org/
2. OpenCV Cascade Classifier Tutorial —
   https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html
3. Viola, P., & Jones, M. (2001). *Rapid Object Detection using a
   Boosted Cascade of Simple Features.* IEEE CVPR.
4. NumPy Documentation — https://numpy.org/doc/

**[ADJUST TO COURSE FORMAT]** — Convert the reference list above into
your course's required citation style (APA/IEEE/MLA/etc.) if needed.
