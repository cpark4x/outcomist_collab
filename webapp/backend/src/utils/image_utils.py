"""Image utility functions for MIME type detection and normalization."""

import base64
import logging
from io import BytesIO
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


def detect_image_type(data: bytes) -> str | None:
    """Detect actual image format from bytes using Pillow.

    Args:
        data: Image bytes

    Returns:
        Image format string (e.g., 'jpeg', 'png') or None if not an image
    """
    try:
        img = Image.open(BytesIO(data))
        # PIL format to lowercase standard format names
        format_map = {
            "JPEG": "jpeg",
            "PNG": "png",
            "GIF": "gif",
            "WEBP": "webp",
            "BMP": "bmp",
            "TIFF": "tiff",
        }
        return format_map.get(img.format, img.format.lower() if img.format else None)
    except Exception:
        return None


def normalize_image_format(data: bytes, target_format: str = "jpeg") -> tuple[bytes, str]:
    """Convert image to target format and return correct MIME type.

    This ensures the image data matches the declared MIME type.
    Handles RGBA to RGB conversion for JPEG compatibility.

    Args:
        data: Original image bytes
        target_format: Target format ('jpeg', 'png', 'webp', etc.)

    Returns:
        Tuple of (normalized_bytes, mime_type)

    Raises:
        ValueError: If image cannot be processed
    """
    try:
        img = Image.open(BytesIO(data))

        # Convert RGBA/LA/P to RGB for JPEG (JPEG doesn't support transparency)
        if target_format.lower() in ("jpeg", "jpg") and img.mode in ("RGBA", "LA", "P"):
            rgb_img = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "RGBA":
                rgb_img.paste(img, mask=img.split()[-1])
            elif img.mode in ("LA", "P"):
                rgb_img.paste(img)
            img = rgb_img

        # Convert to target format
        output = BytesIO()
        save_format = "JPEG" if target_format.lower() == "jpg" else target_format.upper()
        img.save(output, format=save_format)

        # Return normalized bytes and MIME type
        normalized_format = "jpeg" if target_format.lower() == "jpg" else target_format.lower()
        return output.getvalue(), f"image/{normalized_format}"

    except Exception as e:
        raise ValueError(f"Failed to normalize image to {target_format}: {e}") from e


def get_correct_mime_type(filename: str, data: bytes) -> str:
    """Get correct MIME type based on actual image data.

    Args:
        filename: File name (used as fallback)
        data: File bytes

    Returns:
        Correct MIME type string
    """
    # Try to detect from actual data
    detected = detect_image_type(data)
    if detected:
        # Map imghdr types to MIME types
        mime_map = {
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
            "bmp": "image/bmp",
            "tiff": "image/tiff",
        }
        return mime_map.get(detected, "application/octet-stream")

    # Fallback to extension-based detection
    ext = Path(filename).suffix.lower().lstrip(".")
    ext_mime_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        "bmp": "image/bmp",
        "svg": "image/svg+xml",
    }
    return ext_mime_map.get(ext, "application/octet-stream")


def validate_and_fix_image_mime(
    data: bytes, declared_mime: str, filename: str = "image"
) -> tuple[bytes, str]:
    """Validate image MIME type and fix if mismatched.

    Args:
        data: Image bytes
        declared_mime: Declared MIME type (e.g., 'image/jpeg')
        filename: Filename for fallback detection

    Returns:
        Tuple of (possibly_normalized_bytes, correct_mime_type)
    """
    # Detect actual type
    actual_mime = get_correct_mime_type(filename, data)

    # If types match, return as-is
    if actual_mime == declared_mime:
        return data, declared_mime

    # If mismatch, try to normalize to declared format
    if declared_mime.startswith("image/"):
        target_format = declared_mime.split("/")[1]
        try:
            normalized_data, normalized_mime = normalize_image_format(data, target_format)
            logger.info(
                f"Normalized image from {actual_mime} to {normalized_mime} (declared: {declared_mime})"
            )
            return normalized_data, normalized_mime
        except ValueError as e:
            logger.warning(f"Could not normalize image to {declared_mime}: {e}")

    # If normalization fails, return with actual detected type
    logger.warning(f"MIME type mismatch: declared={declared_mime}, actual={actual_mime}. Using actual type.")
    return data, actual_mime


def validate_base64_image(b64_data: str, declared_mime: str) -> tuple[str, str] | None:
    """Validate and fix base64-encoded image for Claude API.

    Args:
        b64_data: Base64-encoded image string
        declared_mime: Declared MIME type

    Returns:
        Tuple of (fixed_base64, correct_mime) or None if image is invalid
    """
    try:
        # Decode base64
        img_bytes = base64.b64decode(b64_data)

        # Validate and fix
        fixed_bytes, correct_mime = validate_and_fix_image_mime(img_bytes, declared_mime)

        # Re-encode
        fixed_b64 = base64.b64encode(fixed_bytes).decode("ascii")

        return fixed_b64, correct_mime

    except Exception as e:
        logger.error(f"Failed to validate base64 image: {e}")
        return None
