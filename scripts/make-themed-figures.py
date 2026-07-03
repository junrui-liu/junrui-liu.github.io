"""Make light/dark transparent variants of white-background figures.

Usage: python3 scripts/make-themed-figures.py [--trim] INPUT.png OUTBASE
Writes OUTBASE-light.png and OUTBASE-dark.png.

Light: color-to-alpha against white (GIMP algorithm) — anti-aliasing moves
into the alpha channel, colored elements keep their hue.
Dark: same, but low-saturation (grayscale) ink is recolored to the site's
dark-mode text color, and pastel colors get an alpha boost so they stay
vivid instead of going muddy on a dark background.

White that is enclosed by colored regions (e.g. percentage labels inside
pie slices) is kept opaque white rather than made transparent; only white
connected to the image border counts as background.
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

DARK_INK = np.array([0xD9, 0xD2, 0xC4], dtype=np.float64)  # theme --text-color


def color_to_alpha_white(rgb):
    """rgb float64 HxWx3 in [0,1] -> (rgb', alpha) with white made transparent."""
    alpha = (1.0 - rgb).max(axis=2)  # distance from white, per pixel
    safe = np.maximum(alpha, 1e-6)[..., None]
    new_rgb = (rgb - (1.0 - safe)) / safe
    new_rgb = np.clip(new_rgb, 0.0, 1.0)
    new_rgb[alpha == 0] = 0.0
    return new_rgb, alpha


def enclosed_white_mask(alpha, chroma):
    """White regions not connected to the border, if bounded mostly by
    saturated color (pie-slice labels) rather than by ink (letter counters)."""
    whiteish = alpha < 0.06
    border_seed = np.zeros_like(whiteish)
    border_seed[0, :] = border_seed[-1, :] = True
    border_seed[:, 0] = border_seed[:, -1] = True
    background = ndimage.binary_propagation(border_seed & whiteish, mask=whiteish)
    interior = whiteish & ~background
    keep = np.zeros_like(interior)
    labels, n = ndimage.label(interior)
    colored = chroma > 0.25
    for i in range(1, n + 1):
        region = labels == i
        ring = ndimage.binary_dilation(region, iterations=2) & ~region
        if ring.any() and colored[ring].mean() > 0.5:
            keep |= region
    return keep


def process(path_in, out_base, trim=False):
    im = Image.open(path_in).convert("RGBA")
    arr = np.asarray(im).astype(np.float64) / 255.0
    rgb, src_a = arr[..., :3], arr[..., 3]

    new_rgb, alpha = color_to_alpha_white(rgb)
    alpha = alpha * src_a  # respect any existing transparency

    # Absolute chroma, not relative saturation: near-black ink with a slight
    # color cast (e.g. Google's #202124) unmixes to a tiny but fully
    # "saturated" residue, so a ratio-based measure would misread it as color.
    chroma = new_rgb.max(axis=2) - new_rgb.min(axis=2)

    white_text = enclosed_white_mask(alpha, chroma)

    light_rgb = np.where(white_text[..., None], 1.0, new_rgb)
    light_alpha = np.where(white_text, 1.0, alpha)
    light = np.dstack([light_rgb, light_alpha])

    # Dark variant: recolor grayscale ink to light, keep colored pixels.
    grayness = np.clip(1.0 - chroma / 0.25, 0.0, 1.0)[..., None]  # 1 = grayscale
    dark_rgb = new_rgb * (1 - grayness) + (DARK_INK / 255.0) * grayness
    # Pastel colors owe their lightness to white-blending, which became
    # transparency; boost their alpha so they don't go muddy on dark.
    colored = 1.0 - grayness[..., 0]
    boosted = 1.0 - (1.0 - alpha) ** 2
    dark_alpha = alpha * (1 - colored) + boosted * colored
    dark_rgb = np.where(white_text[..., None], 1.0, dark_rgb)
    dark_alpha = np.where(white_text, 1.0, dark_alpha)
    dark = np.dstack([dark_rgb, dark_alpha])

    if trim:
        ys, xs = np.where(light_alpha > 0.02)
        pad = 12
        y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, light.shape[0])
        x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, light.shape[1])
        light, dark = light[y0:y1, x0:x1], dark[y0:y1, x0:x1]

    for img, suffix in ((light, "light"), (dark, "dark")):
        path = f"{out_base}-{suffix}.png"
        Image.fromarray((img * 255).round().astype(np.uint8), "RGBA").save(path)
        print(f"wrote {path}")


if __name__ == "__main__":
    args = sys.argv[1:]
    trim = "--trim" in args
    args = [a for a in args if a != "--trim"]
    process(args[0], args[1], trim=trim)
