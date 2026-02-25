"""
Image Generator — Creates beautiful gradient placeholder images for products.
Uses Pillow to generate category-specific images with icons.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random


# Category color schemes (gradient start, gradient end, icon emoji text)
CATEGORY_STYLES = {
    'Fruits': {
        'colors': [(255, 107, 107), (255, 165, 0)],    # Red → Orange
        'icon': 'F',
        'bg_shapes': [(255, 130, 100), (255, 180, 50)],
    },
    'Vegetables': {
        'colors': [(46, 139, 87), (107, 203, 119)],     # Green → Light Green
        'icon': 'V',
        'bg_shapes': [(60, 160, 90), (130, 210, 140)],
    },
    'Grains': {
        'colors': [(184, 134, 11), (218, 165, 32)],     # Dark Gold → Gold
        'icon': 'G',
        'bg_shapes': [(195, 145, 30), (225, 180, 60)],
    },
    'Dairy': {
        'colors': [(70, 130, 180), (135, 206, 250)],    # Steel Blue → Light Blue
        'icon': 'D',
        'bg_shapes': [(90, 150, 200), (150, 210, 250)],
    },
    'Other': {
        'colors': [(128, 0, 128), (186, 85, 211)],      # Purple → Medium Orchid
        'icon': 'O',
        'bg_shapes': [(140, 20, 140), (200, 100, 220)],
    },
}


def _interpolate_color(c1, c2, t):
    """Linearly interpolate between two RGB colors."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def generate_product_image(product_name, category, output_dir, index=0):
    """
    Generate a beautiful gradient placeholder image for a product.
    
    Returns:
        Relative path (from MEDIA_ROOT) to the generated image.
    """
    width, height = 600, 400
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    style = CATEGORY_STYLES.get(category, CATEGORY_STYLES['Other'])
    c1, c2 = style['colors']

    # Draw gradient background
    for y in range(height):
        t = y / height
        color = _interpolate_color(c1, c2, t)
        draw.line([(0, y), (width, y)], fill=color)

    # Draw decorative circles
    random.seed(index + hash(product_name))
    shape_colors = style['bg_shapes']
    for _ in range(6):
        cx = random.randint(0, width)
        cy = random.randint(0, height)
        r = random.randint(30, 120)
        opacity_color = _interpolate_color(shape_colors[0], shape_colors[1], random.random())
        # Semi-transparent effect by blending
        alpha = random.randint(40, 100)
        blended = tuple(int(opacity_color[i] * alpha / 255 + c2[i] * (255 - alpha) / 255) for i in range(3))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=blended)

    # Draw product name text
    # Use a default font at various sizes
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except (OSError, IOError):
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except (OSError, IOError):
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # Category label at top
    cat_text = category.upper()
    draw.text((30, 20), cat_text, fill=(255, 255, 255, 180), font=font_small)

    # Product name centered
    # Simple centering
    name_lines = product_name.split('(')[0].strip()
    if len(name_lines) > 20:
        # Split into two lines
        words = name_lines.split()
        mid = len(words) // 2
        line1 = ' '.join(words[:mid])
        line2 = ' '.join(words[mid:])
        draw.text((30, height // 2 - 40), line1, fill=(255, 255, 255), font=font_large)
        draw.text((30, height // 2 + 10), line2, fill=(255, 255, 255), font=font_large)
    else:
        draw.text((30, height // 2 - 20), name_lines, fill=(255, 255, 255), font=font_large)

    # Small decorative line
    draw.rectangle([30, height - 60, 150, height - 57], fill=(255, 255, 255, 200))
    draw.text((30, height - 50), "AgriChain", fill=(255, 255, 255, 150), font=font_small)

    # Save image
    os.makedirs(output_dir, exist_ok=True)
    filename = f"product_{index}.jpg"
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, 'JPEG', quality=85)

    return f"products/{filename}"
