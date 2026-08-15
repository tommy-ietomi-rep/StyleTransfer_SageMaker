# StyleTransfer_SageMaker

Neural Style Transfer (CNN) on AWS SageMaker.

Applies the artistic style of a reference image to a content image using a
pre-trained VGG19 network, with the optimization run as a SageMaker training job.

## Project Structure

```
.
├── StyleTransfer_SageMaker.ipynb   # Main notebook (SageMaker SDK v2 compatible)
├── StyleTransfer_SageMaker.html    # Exported HTML version of the notebook
├── scripts/
│   └── train.py                    # Training script executed on SageMaker
└── data/                           # Local data directory (content + style images)
```

## How It Works

1. Place the content image (`mychild.jpg`) and style image (`illustration.jpg`)
   in the `data/` directory.
2. Run the notebook cells in order:
   - It uploads the images to an S3 bucket.
   - It launches a SageMaker PyTorch training job that runs `scripts/train.py`.
   - `train.py` optimizes a target image so that it matches the content image's
     structure (`conv4_2` feature map) and the style image's texture
     (Gram matrices of `conv1_1`–`conv5_1`) using a frozen pre-trained VGG19.
   - The stylized result (`result.jpg`) is saved to S3 as a model artifact.
3. The notebook downloads `model.tar.gz` from S3, extracts it, and displays
   the result next to the original content image.

## Requirements

- An AWS account with SageMaker access
- A SageMaker notebook instance, or a local environment with:
  - `boto3`
  - `sagemaker` (Python SDK v2)
  - `torch` / `torchvision` (latest)
  - `Pillow`, `matplotlib`, `numpy`

## Configuration

The estimator is configured in the notebook:

| Parameter             | Value            | Notes                                       |
|-----------------------|------------------|---------------------------------------------|
| `framework_version`   | `2.0.1`          | PyTorch version used by SageMaker           |
| `py_version`          | `py310`          | Python 3.10                                 |
| `instance_type`       | `ml.p2.xlarge`   | GPU instance (change if unavailable in your region, e.g. `ml.g4dn.xlarge` or `ml.p3.xlarge`) |
| `epochs`              | `500`            | Style transfer optimization iterations      |

## Notes

- The `StyleTransfer_SageMaker.html` file is an old exported copy of the
  original notebook and is kept for reference only.
- The project originally used SageMaker SDK v1 API parameters such as
  `train_instance_type` / `train_instance_count`, which are deprecated.
  The notebook has been updated to the SageMaker SDK v2 API
  (`instance_type` / `instance_count`, `TrainingInput`, `framework_version`).