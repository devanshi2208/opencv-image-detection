"""
preprocessing.py
-----------------
Utility functions for image preprocessing steps used before running
detection algorithms. Keeping preprocessing separate from detection
logic makes the pipeline easier to read, test, and extend.
"""

import os
import cv2


def load_image(image_path: str):
    """
    Load an image from disk using OpenCV.

    Parameters
    ----------
    image_path : str
        Path to the image file.

    Returns
    -------
    numpy.ndarray or None
        The loaded BGR image, or None if the file could not be read
        (missing file, corrupted file, unsupported format, etc.).
    """
    if not os.path.isfile(image_path):
        print(f"[ERROR] Input image not found: {image_path}")
        return None

    image = cv2.imread(image_path)

    if image is None:
        # cv2.imread returns None (without raising) for unreadable,
        # corrupt, or unsupported files -- we must check explicitly.
        print(f"[ERROR] Could not read image (corrupt or unsupported format): {image_path}")
        return None

    return image


def resize_image(image, max_width: int = 900):
    """
    Resize an image so very large images are easier to display and
    process, while keeping the aspect ratio intact. Small images are
    left unchanged.

    Parameters
    ----------
    image : numpy.ndarray
        Input BGR image.
    max_width : int
        Maximum allowed width in pixels.

    Returns
    -------
    numpy.ndarray
        Resized (or original) image.
    """
    height, width = image.shape[:2]

    if width <= max_width:
        return image

    scale = max_width / float(width)
    new_dim = (max_width, int(height * scale))
    return cv2.resize(image, new_dim, interpolation=cv2.INTER_AREA)


def convert_to_grayscale(image):
    """Convert a BGR image to single-channel grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def equalize_histogram(gray_image):
    """
    Apply histogram equalization to improve contrast in the grayscale
    image. This generally improves Haar Cascade detection accuracy
    under poor or uneven lighting conditions.
    """
    return cv2.equalizeHist(gray_image)


def denoise_image(gray_image):
    """
    Apply a light Gaussian blur to reduce noise before detection.
    A small kernel is used so facial features are not smoothed away.
    """
    return cv2.GaussianBlur(gray_image, (3, 3), 0)


def preprocess_for_detection(image):
    """
    Full preprocessing pipeline used before running the detector:
        1. Resize (for consistent display/performance)
        2. Convert to grayscale
        3. Denoise (light Gaussian blur)
        4. Histogram-equalize (contrast improvement)

    Parameters
    ----------
    image : numpy.ndarray
        Original BGR image.

    Returns
    -------
    tuple(numpy.ndarray, numpy.ndarray)
        (resized_original_bgr_image, preprocessed_grayscale_image)
    """
    resized = resize_image(image)
    gray = convert_to_grayscale(resized)
    denoised = denoise_image(gray)
    equalized = equalize_histogram(denoised)
    return resized, equalized
