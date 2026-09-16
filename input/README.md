# input/ folder

Place the image(s) you want to run detection on inside this folder.

- Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`
- Use clear, front-facing photos of people for best results (this
  project uses face + eye detection).
- You can add as many images as you like — if you run
  `python main.py --mode image` without `--input`, every image in
  this folder will be processed automatically, one after another.
- To process just one image, use:
  `python main.py --mode image --input input/your_image_name.jpg`

This file (and `.gitkeep`) exists only so the empty folder is tracked
by Git. Feel free to delete them once you've added your own images —
they are not required by the code.
