"""Utility functions for the controllers."""

import re
import mimetypes
import base64

from odoo.tools.image import image_data_uri


def clean_html(html):
    """Remove HTML tags from a string."""
    clean = re.compile("<.*?>")
    return re.sub(clean, "", html)


def get_image_from_base64(image):
    """Get an image from a base64 string.
    - Return the image as a binary image.
    """
    image = base64.b64decode(image)
    return image


def get_image_format(image):
    """Get the format of an image.
    - Return the format of the image.
    """
    image_data = image_data_uri(image)
    image_format = mimetypes.guess_type(image_data)[0]
    return image_format
