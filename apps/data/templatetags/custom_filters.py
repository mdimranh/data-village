# custom_filters.py

from django import template

register = template.Library()


@register.filter
def filesizeformat(value):
    """
    Format the value as a human-readable file size (e.g. '13 KB', '4.1 MB', '102 Bytes').
    """
    try:
        value = float(value)
    except (TypeError, ValueError, UnicodeDecodeError):
        return "0 Bytes"

    base = 1024
    prefixes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    for i, prefix in enumerate(prefixes):
        if abs(value) < base or i == len(prefixes) - 1:
            return "{:.1f} {}".format(value, prefix)
        value /= base
