"""
main.py
-------
Entry point for the OpenCV Face & Eye Detection project.

Usage examples (run from the project root folder):

    Process every image inside the input/ folder:
        python main.py --mode image

    Process a single specific image:
        python main.py --mode image --input input/sample1.jpg

    Process a single image AND display the result in a window:
        python main.py --mode image --input input/sample1.jpg --show

    Run live detection using your webcam (press 'q' to quit):
        python main.py --mode webcam

Run `python main.py --help` to see all available options.
"""

import argparse
import sys

import cv2

from src.preprocessing import preprocess_for_detection, load_image, \
    resize_image, convert_to_grayscale, denoise_image, equalize_histogram
from src.detector import FaceEyeDetector
from src.utils import list_images, build_output_path, save_image, ensure_dir

DEFAULT_INPUT_DIR = "input"
DEFAULT_OUTPUT_DIR = "output"


def process_single_image(detector, image_path, output_dir, show_window):
    """Run the full detection pipeline on one image file and save the result."""
    print(f"\n[INFO] Processing: {image_path}")
    image = load_image(image_path)

    if image is None:
        # Skip gracefully instead of crashing the whole batch run
        print(f"[WARN] Skipping invalid/missing image: {image_path}")
        return

    resized_bgr, preprocessed_gray = preprocess_for_detection(image)
    annotated, num_faces, num_eyes = detector.detect_and_annotate(
        resized_bgr, preprocessed_gray
    )

    print(f"[RESULT] Faces detected: {num_faces} | Eyes detected: {num_eyes}")

    output_path = build_output_path(output_dir, image_path)
    save_image(annotated, output_path)

    if show_window:
        cv2.imshow("Detection Result - press any key to continue", annotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def run_image_mode(args, detector):
    ensure_dir(args.output)

    if args.input:
        # A single specific image was supplied
        process_single_image(detector, args.input, args.output, args.show)
        return

    # No specific file given -> process every image inside input/
    image_paths = list_images(args.input_dir)

    if not image_paths:
        print(f"[ERROR] No images found in '{args.input_dir}/'. "
              f"Please add at least one .jpg/.png image there and try again "
              f"(see input/README.md).")
        sys.exit(1)

    print(f"[INFO] Found {len(image_paths)} image(s) in '{args.input_dir}/'.")
    for path in image_paths:
        process_single_image(detector, path, args.output, args.show)


def run_webcam_mode(args, detector):
    """
    Run real-time face & eye detection using the default webcam.
    Press 'q' in the display window to quit.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Could not access the webcam. Check that a camera "
              "is connected, drivers are installed, and it is not already "
              "in use by another application.")
        sys.exit(1)

    print("[INFO] Webcam started. Press 'q' in the video window to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read frame from webcam.")
            break

        frame = resize_image(frame, max_width=800)
        gray = convert_to_grayscale(frame)
        gray = denoise_image(gray)
        gray = equalize_histogram(gray)

        annotated, num_faces, num_eyes = detector.detect_and_annotate(frame, gray)

        cv2.putText(annotated, f"Faces: {num_faces}  Eyes: {num_eyes}",
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("Live Face & Eye Detection (press 'q' to quit)", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def parse_args():
    parser = argparse.ArgumentParser(
        description="OpenCV Face & Eye Detection Project"
    )
    parser.add_argument(
        "--mode", choices=["image", "webcam"], default="image",
        help="Detection mode: 'image' processes files, 'webcam' uses a "
             "live camera feed (default: image)"
    )
    parser.add_argument(
        "--input", type=str, default=None,
        help="Path to a single input image. If omitted, every image inside "
             "--input-dir is processed instead."
    )
    parser.add_argument(
        "--input-dir", type=str, default=DEFAULT_INPUT_DIR,
        help=f"Folder containing input images (default: {DEFAULT_INPUT_DIR}/)"
    )
    parser.add_argument(
        "--output", type=str, default=DEFAULT_OUTPUT_DIR,
        help=f"Folder where output images are saved (default: {DEFAULT_OUTPUT_DIR}/)"
    )
    parser.add_argument(
        "--show", action="store_true",
        help="Display each result in a window after processing (image mode only)."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        detector = FaceEyeDetector()
    except IOError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    if args.mode == "image":
        run_image_mode(args, detector)
    else:
        run_webcam_mode(args, detector)

    print("\n[DONE] Processing complete.")


if __name__ == "__main__":
    main()
