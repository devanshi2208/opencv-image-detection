"""
detector.py
-----------
Face and eye detection using OpenCV's built-in Haar Cascade
classifiers.

Why Haar Cascades for this project:
- They ship with OpenCV (cv2.data.haarcascades), so no external
  dataset download or model training is required.
- They run fast enough for real time use on a normal laptop CPU.
- They are well documented and a standard, well-understood starting
  point for learning object detection concepts (sliding window +
  cascade classifier), which suits a college-level project.

The detector first finds faces in the image, then searches for eyes
only inside each detected face's region of interest (ROI). This is
both faster and far more accurate than searching the whole image for
eyes directly.
"""

import os
import cv2


class FaceEyeDetector:
    def __init__(self, face_cascade_path: str = None, eye_cascade_path: str = None):
        """
        Load the Haar Cascade classifiers.

        If no explicit paths are supplied, the classifiers bundled
        with the installed OpenCV package are used
        (cv2.data.haarcascades). This keeps the project free of any
        hardcoded, machine-specific paths.
        """
        base_path = cv2.data.haarcascades

        face_path = face_cascade_path or os.path.join(
            base_path, "haarcascade_frontalface_default.xml"
        )
        eye_path = eye_cascade_path or os.path.join(
            base_path, "haarcascade_eye.xml"
        )

        self.face_cascade = cv2.CascadeClassifier(face_path)
        self.eye_cascade = cv2.CascadeClassifier(eye_path)

        if self.face_cascade.empty():
            raise IOError(f"Failed to load face cascade from: {face_path}")
        if self.eye_cascade.empty():
            raise IOError(f"Failed to load eye cascade from: {eye_path}")

    def detect_faces(self, gray_image,
                      scale_factor: float = 1.1,
                      min_neighbors: int = 5,
                      min_size=(30, 30)):
        """
        Detect faces in a preprocessed grayscale image.

        Returns
        -------
        list of (x, y, w, h) tuples, one per detected face.
        """
        faces = self.face_cascade.detectMultiScale(
            gray_image,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_size
        )
        return faces

    def detect_eyes_in_face(self, gray_face_roi,
                             scale_factor: float = 1.1,
                             min_neighbors: int = 8,
                             min_size=(15, 15)):
        """
        Detect eyes within a single face's grayscale region of
        interest (ROI). Restricting the search to the face ROI
        (rather than the whole frame) both speeds up detection and
        greatly reduces false positives.
        """
        eyes = self.eye_cascade.detectMultiScale(
            gray_face_roi,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_size
        )
        return eyes

    def detect_and_annotate(self, bgr_image, gray_image):
        """
        Run the full detection pipeline on one image and draw
        bounding boxes + labels for every face and eye found.

        Parameters
        ----------
        bgr_image : numpy.ndarray
            The color image to draw annotations on (modified in
            place and also returned).
        gray_image : numpy.ndarray
            The preprocessed grayscale version used for detection.

        Returns
        -------
        tuple(numpy.ndarray, int, int)
            (annotated_bgr_image, num_faces, num_eyes)
        """
        faces = self.detect_faces(gray_image)
        total_eyes = 0

        for (x, y, w, h) in faces:
            # Draw bounding box + label around the detected face
            cv2.rectangle(bgr_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(bgr_image, "Face", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Restrict eye search to this face's region only
            face_gray_roi = gray_image[y:y + h, x:x + w]
            face_color_roi = bgr_image[y:y + h, x:x + w]

            eyes = self.detect_eyes_in_face(face_gray_roi)
            total_eyes += len(eyes)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face_color_roi, (ex, ey),
                              (ex + ew, ey + eh), (255, 0, 0), 2)

        return bgr_image, len(faces), total_eyes
