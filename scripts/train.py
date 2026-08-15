"""
Neural Style Transfer training script for AWS SageMaker.

Applies the artistic style of a reference image to a content image using a
pre-trained VGG19 network (features only) as the feature extractor.

Input images are read from the SageMaker training channel
(/opt/ml/input/data/training) and the stylized result (result.jpg) is
saved to /opt/ml/model, which SageMaker uploads to S3 as the model artifact.
"""

import argparse
import os

import numpy as np
import PIL.Image
import torch
import torch.optim as optim
from torchvision import transforms, models


# --- Style transfer constants -------------------------------------------------
# VGG19 feature layers used for style/content extraction
STYLE_LAYERS = {
    '0': 'conv1_1',
    '5': 'conv2_1',
    '10': 'conv3_1',
    '19': 'conv4_1',
    '21': 'conv4_2',  # content representation
    '28': 'conv5_1',
}

STYLE_WEIGHTS = {
    'conv1_1': 1.,
    'conv2_1': 0.75,
    'conv3_1': 0.2,
    'conv4_1': 0.2,
    'conv5_1': 0.2,
}

CONTENT_WEIGHT = 1      # alpha
STYLE_WEIGHT = 1e6      # beta


def load_image(img_path, max_size=400, shape=None):
    """Load an image, resize it, and normalize it for VGG19 input."""
    image = PIL.Image.open(img_path).convert('RGB')

    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)

    if shape is not None:
        size = shape

    in_transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225)),
    ])
    image = in_transform(image)[:3, :, :].unsqueeze(0)
    return image


def im_convert(tensor):
    """Convert a normalized tensor back to a displayable image (0-1 range)."""
    image = tensor.to("cpu").clone().detach().numpy().squeeze()
    image = image.transpose(1, 2, 0)
    image = image * np.array((0.229, 0.224, 0.225)) + np.array((0.485, 0.456, 0.406))
    image = image.clip(0, 1)
    return image


def get_features(image, model, layers=None):
    """Extract intermediate feature maps from the VGG19 feature network."""
    if layers is None:
        layers = STYLE_LAYERS

    features = {}
    x = image
    for name, layer in model._modules.items():
        x = layer(x)
        if name in layers:
            features[layers[name]] = x
    return features


def gram_matrix(tensor):
    """Compute the Gram matrix of a feature map (style representation)."""
    _, d, h, w = tensor.size()
    tensor = tensor.view(d, h * w)
    return torch.mm(tensor, tensor.t())


def train(model, target, content_features, style_features, style_grams,
          epochs, optimizer):
    """Optimize the target image to match content + style."""
    show_every = max(1, epochs // 10)

    for ii in range(1, epochs + 1):
        target_features = get_features(target, model)

        # Content loss (conv4_2 only)
        content_loss = torch.mean(
            (target_features['conv4_2'] - content_features['conv4_2']) ** 2)

        # Style loss (Gram matrices of style layers)
        style_loss = 0
        for layer in STYLE_WEIGHTS:
            target_feature = target_features[layer]
            target_gram = gram_matrix(target_feature)
            _, d, h, w = target_feature.shape
            style_gram = style_grams[layer]
            layer_style_loss = STYLE_WEIGHTS[layer] * torch.mean(
                (target_gram - style_gram) ** 2)
            style_loss += layer_style_loss / (d * h * w)

        total_loss = CONTENT_WEIGHT * content_loss + STYLE_WEIGHT * style_loss

        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        if ii % show_every == 0:
            print(f"epoch {ii:4d}/{epochs} | total loss: {total_loss.item():.4f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=500,
                        help='number of epochs (default: 500)')
    parser.add_argument('--input_image_name', type=str, default='input_image.jpg',
                        help='content image file name')
    parser.add_argument('--reference_image_name', type=str, default='reference_image.jpg',
                        help='style image file name')
    parser.add_argument('--seed', type=int, default=1,
                        help='random seed (default: 1)')
    parser.add_argument('--model-dir', type=str,
                        default=os.environ.get('SM_MODEL_DIR', '/opt/ml/model'),
                        help='directory to save the result (SageMaker: SM_MODEL_DIR)')
    parser.add_argument('--data-dir', type=str,
                        default=os.environ.get('SM_CHANNEL_TRAINING', './data'),
                        help='directory containing the input images '
                             '(SageMaker: SM_CHANNEL_TRAINING)')
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    torch.manual_seed(args.seed)

    # --- Pre-trained VGG19 as a fixed feature extractor -------------------
    # Modern torchvision API: weights are specified explicitly.
    vgg = models.vgg19(weights=models.VGG19_Weights.IMAGENET1K_V1).features
    for param in vgg.parameters():
        param.requires_grad_(False)
    vgg.to(device)
    vgg.eval()

    # --- Load content and style images ------------------------------------
    content = load_image(os.path.join(args.data_dir, args.input_image_name)).to(device)
    # Resize style to match content (makes the code easier)
    style = load_image(os.path.join(args.data_dir, args.reference_image_name),
                       shape=content.shape[-2:]).to(device)

    content_features = get_features(content, vgg)
    style_features = get_features(style, vgg)
    style_grams = {layer: gram_matrix(style_features[layer])
                   for layer in style_features}

    # Target image = content image copy, optimized via gradient descent
    target = content.clone().requires_grad_(True).to(device)

    optimizer = torch.optim.Adam([target], lr=0.003)

    # --- Run style transfer ------------------------------------------------
    train(vgg, target, content_features, style_features, style_grams,
          args.epochs, optimizer)

    # --- Save the result ----------------------------------------------------
    os.makedirs(args.model_dir, exist_ok=True)
    result = PIL.Image.fromarray(np.uint8(im_convert(target) * 255))
    result_path = os.path.join(args.model_dir, 'result.jpg')
    result.save(result_path)
    print(f"Saved result image to {result_path}")