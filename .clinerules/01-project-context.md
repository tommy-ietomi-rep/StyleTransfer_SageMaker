# Project Context

## Purpose
This project implements **Neural Style Transfer** using a pre-trained VGG19 as the
feature extractor, running entirely on a local machine. It applies the artistic
style of a reference image to a content image and produces a stylized result.

## Tech Stack
- Python 3.9+
- PyTorch / torchvision (pre-trained VGG19, features only)
- Pillow / numpy / matplotlib
- Jupyter Notebook (ipykernel)
- Dev environment: VSCode DevContainer (`.devcontainer/`)

## Directory Layout
| Path | Description |
|---|---|
| `scripts/train.py` | Training script (also runnable standalone) |
| `StyleTransfer_Local.ipynb` | Local-run notebook |
| `StyleTransfer_SageMaker.html` | Old SageMaker export (reference only — **do not edit**) |
| `data/` | Input images (content/style) and `result.jpg` |
| `doc/` | Reference materials (PDFs, etc.) |
| `verilog/` | FPGA learning samples (outside the main scope) |
| `.clinerules/` | Agent working rules (these files) |

## Important Notes
- `StyleTransfer_SageMaker.html` is a reference copy of the old version; never edit it.
- `data/result.jpg` is a build output and is gitignored.
- VGG19 pretrained weights are downloaded from the internet on first run.
