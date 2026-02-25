"""
QR Code Service — Generates QR codes for product traceability.
Each QR code links to the public product detail page.
"""

import os
import pyqrcode
import logging

logger = logging.getLogger(__name__)


def generate_product_qr(product, base_url='http://127.0.0.1:8000'):
    """
    Generate a QR code for a product that links to its detail page.

    Args:
        product: Product model instance
        base_url: Base URL of the application (updated when ngrok is active)

    Returns:
        Relative path to the generated QR code image, or empty string on failure.
    """
    try:
        from django.conf import settings

        # Build the product detail URL
        product_url = f"{base_url}/product/{product.pk}/"

        # Generate QR code
        qr = pyqrcode.create(product_url)

        # Ensure directory exists
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        os.makedirs(qr_dir, exist_ok=True)

        # Save QR code as PNG
        filename = f"product_{product.pk}.png"
        filepath = os.path.join(qr_dir, filename)
        qr.png(filepath, scale=6)

        return f"qrcodes/{filename}"

    except Exception as e:
        logger.error("Failed to generate QR code for product %s: %s", product.pk, str(e))
        return ""


def get_ngrok_url():
    """
    Get the current ngrok public URL if available.

    Returns:
        Public ngrok URL string, or None if ngrok is not running.
    """
    try:
        from pyngrok import ngrok
        tunnels = ngrok.get_tunnels()
        for tunnel in tunnels:
            if 'https' in tunnel.public_url:
                return tunnel.public_url
        if tunnels:
            return tunnels[0].public_url
    except Exception:
        pass
    return None
