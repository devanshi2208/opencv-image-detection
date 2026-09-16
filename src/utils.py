"""
utils.py
--------
Small helper functions shared across the project: directory
management, output file naming, and locating input images.
"""

import os
import glob
from datetime import datetime

import cv2

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def ensure_dir(path: str):
    """Create a directory (including parents) if it doesn't exist."""
    if path:
        os.makedirs(path, exist_ok=True)


def list_images(folder: str):
    """
    Return a sorted list of all image file paths inside a folder.

    Parameters
    ----------
    folder : str
        Directory to search (non-recursive).

    Returns
    -------
    list of str
    """
    if not os.path.isdir(folder):
        return []

    files = []
    for ext in IMAGE_EXTENSIONS:
        files.extend(glob.glob(os.path.join(folder, f"*{ext}")))
        files.extend(glob.glob(os.path.join(folder, f"*{ext.upper()}")))

    return sorted(set(files))


def build_output_path(output_dir: str, input_path: str):
    """
    Build an output file path based on the input filename, with a
    timestamp appended so repeated runs never overwrite each other.
    """
    ensure_dir(output_dir)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_name = f"{base_name}_detected_{timestamp}.jpg"
    return os.path.join(output_dir, output_name)


def save_image(image, output_path: str) -> bool:
    """Save an image to disk, returning True on success."""
    ensure_dir(os.path.dirname(output_path))
    success = cv2.imwrite(output_path, image)
    if success:
        print(f"[INFO] Output saved to: {output_path}")
    else:
        print(f"[ERROR] Failed to save output image to: {output_path}")
    return success
