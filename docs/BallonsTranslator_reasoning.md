# BallonsTranslator. Reasoning Log

## Initial Assessment

BallonsTranslator is a manga and comic image translation tool that combines OCR, text region detection, inpainting, and machine translation. The upstream project is a desktop GUI application built on PyQt6. It also exposes a `--headless` flag on `launch.py` that bypasses the event loop and runs batch translation without a display, which makes it deployable in Docker without a full virtual framebuffer.

## What Was Checked

1. **README.md**: Describes the app primarily as a desktop tool. The headless flag is documented for CI and server use.

2. **launch.py**: Accepts `--headless` and `--exec_dirs`. In headless mode the PyQt6 application object is still created but the event loop is never started, so PyQt6 must be installed but no display server is needed.

3. **requirements.txt (upstream)**: Contains a large set of dependencies including PyTorch, torchvision, transformers, ultralytics (YOLO-based detection), OpenCV, PyQt6, MeCab, DeepL, and OpenAI. Several entries are Windows-only or require special build flags.

4. **pillow-jxl-plugin**: Listed in requirements but requires Pillow to be compiled with JXL support, which is not available in `python:3.11-slim`. Excluded.

5. **GPU footprint**: Ultralytics and transformers pull in PyTorch as a transitive dependency. Without explicit intervention the default pip resolver would install the CUDA build of PyTorch, which is several gigabytes and unnecessary for this deployment. Installing CPU-only torch first via `--index-url https://download.pytorch.org/whl/cpu` pins the resolver before other packages run.

## Decisions Made

### No upstream Dockerfile
The upstream repo has no Dockerfile. The Dockerfile was written from scratch.

### CPU-only PyTorch
GPU is not needed for OCR, inpainting, or translation on a research deployment machine. Installing CPU torch first forces the resolver to accept the CPU build when transformers and ultralytics later declare torch as a dependency.

### PyQt6 in offscreen mode
PyQt6 requires an X11 display even when the application does not open a window, because the platform plugin loads at import time. Setting `QT_QPA_PLATFORM=offscreen` instructs Qt to use the virtual offscreen platform plugin. The minimal X11 libraries (`libxcb1`, `libx11-6`) are still required by the offscreen plugin itself.

### MeCab installation
`mecab-python3` (pulled in by fugashi) requires the MeCab runtime and a dictionary. The `mecab`, `libmecab-dev`, and `mecab-ipadic-utf8` packages are installed from apt.

### Non-root user
`appuser` (UID 1000) is created and owns `/app`. This follows standard container hardening practice.

### HEALTHCHECK without HTTP
There is no HTTP server in this image. The healthcheck imports `torch` and `cv2` as a proxy for successful environment setup. If either import fails the container is considered unhealthy.

### Volume mounts declared
`/input` and `/output` are declared as VOLUME mount points so callers know where to bind their host directories.

## Testing

### Tests Performed
1. **Import check** (`python -c "import torch; import cv2"`): Both modules loaded. Pass.
2. **Entry point smoke test** (`docker run ... --help`): `launch.py` printed usage. Pass.

### What Was Not Tested
- Actual batch translation (requires manga images and optionally an API key for non-free backends).
- DeepL and OpenAI translation backends (require keys, not tested).
- GPU acceleration path.

## Gotchas

1. **CUDA torch installed by default**: If `torch` is not installed before running `pip install -r requirements.txt`, the CUDA variant (several GB) gets pulled in. Explicitly installing CPU torch first prevents this.

2. **PyQt6 offscreen plugin needs X11 libraries**: Even with `QT_QPA_PLATFORM=offscreen`, Qt loads the XCB plugin at startup and links against `libxcb1` and `libx11-6`. Without these the import fails with a missing shared library error.

3. **pillow-jxl-plugin incompatible**: The upstream requirements list this package but it only installs if Pillow was built with JXL support. The `python:3.11-slim` base does not have the necessary libjxl dev headers. Excluding it has no functional impact because JPEG-XL is not a common manga image format.

4. **numpy<2 required**: Several dependencies in this era (transformers, ultralytics, OpenCV) are not compatible with numpy 2.x. The constraint `numpy<2` pins this.
