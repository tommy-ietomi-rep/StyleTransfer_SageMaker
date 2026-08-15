# Common Commands

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run training
```bash
python scripts/train.py \
    --input_image_name mychild.jpg \
    --reference_image_name illustration.jpg \
    --epochs 500
```

### Main options (see `python scripts/train.py --help`)
| Argument | Default | Description |
|---|---|---|
| `--input_image_name` | `input_image.jpg` | Content image (inside `--data-dir`) |
| `--reference_image_name` | `reference_image.jpg` | Style image (inside `--data-dir`) |
| `--epochs` | `500` | Number of optimization iterations |
| `--data-dir` | `./data` | Input image directory |
| `--output-dir` | `./data` | Output directory (`result.jpg`) |
| `--seed` | `1` | Random seed |

## Verification
- Run and confirm `data/result.jpg` is generated and opens as an image.
- Syntax check: `python -m py_compile scripts/train.py`
- Always verify with one of the above after making changes.
