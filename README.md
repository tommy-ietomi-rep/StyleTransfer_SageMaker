# StyleTransfer (Local)

Neural Style Transfer (CNN) with PyTorch — runs entirely on your local machine.
No AWS / SageMaker account or S3 bucket is required.

Applies the artistic style of a reference image to a content image using a
pre-trained VGG19 network. The optimization is a simple gradient-descent loop
over a trainable target image, so it runs anywhere PyTorch is installed
(a GPU makes it much faster, but a CPU works too).

## Project Structure

```
.
├── StyleTransfer_Local.ipynb       # Main notebook (runs locally in Jupyter)
├── StyleTransfer_SageMaker.html    # Old exported HTML of the SageMaker version (reference only)
├── scripts/
│   └── train.py                    # Training script (also runnable standalone)
├── requirements.txt
└── data/                           # Local data directory (content + style images + result)
```

## How It Works

1. Place the content image (`mychild.jpg`) and style image (`illustration.jpg`)
   in the `data/` directory.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Open `StyleTransfer_Local.ipynb` in Jupyter and run the cells in order:
   - Loads and displays the content and style images.
   - Freezes a pre-trained VGG19 and uses it as a feature extractor.
   - Optimizes a target image so that it matches the content image's structure
     (`conv4_2` feature map) and the style image's texture (Gram matrices of
     `conv1_1`–`conv5_1`).
   - Saves the stylized result to `data/result.jpg` and displays it.

## Command Line Usage

The training can also be run directly without the notebook:

```bash
python scripts/train.py \
    --input_image_name mychild.jpg \
    --reference_image_name illustration.jpg \
    --epochs 500
```

Useful options:

| Argument                    | Default      | Description                                  |
|-----------------------------|--------------|----------------------------------------------|
| `--input_image_name`        | `input_image.jpg` | Content image file name (in `--data-dir`) |
| `--reference_image_name`    | `reference_image.jpg` | Style image file name (in `--data-dir`) |
| `--epochs`                  | `500`        | Number of optimization iterations            |
| `--data-dir`                | `./data`     | Directory containing the input images        |
| `--output-dir`              | `./data`     | Directory to save `result.jpg`               |
| `--seed`                    | `1`          | Random seed                                  |

## Requirements

- Python 3.9+
- `torch` / `torchvision`
- `Pillow`, `numpy`, `matplotlib`
- `ipykernel` / Jupyter (for the notebook)

## Notes

- The old SageMaker version of this project (notebook + workflow) has been
  replaced with a fully local version. `StyleTransfer_SageMaker.html` is the
  exported copy of the old notebook and is kept for reference only.
- The first run downloads the VGG19 pretrained weights from the internet.