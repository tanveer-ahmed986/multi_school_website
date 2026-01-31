"""
Input validators: email, subdomain, hex color, file type/size.
"""
import re
from typing import Optional

# Subdomain: lowercase alphanumeric and hyphens, 3-50 chars
SUBDOMAIN_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,48}[a-z0-9]$|^[a-z0-9]{2,50}$")
HEX_COLOR_RE = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
# Simplified email: local@domain
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
DEFAULT_MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB


def validate_email(value: str) -> str:
    """Validate email format. Returns normalized value or raises ValueError."""
    if not value or not value.strip():
        raise ValueError("Invalid email")
    v = value.strip()
    if len(v) > 255:
        raise ValueError("Invalid email")
    if not EMAIL_RE.match(v):
        raise ValueError("Invalid email")
    return v


def validate_subdomain(value: str) -> str:
    """Validate and normalize subdomain: lowercase, 3-50 chars, alphanumeric and hyphens."""
    if not value or not value.strip():
        raise ValueError("Invalid subdomain")
    v = value.strip().lower()
    if len(v) < 3 or len(v) > 50:
        raise ValueError("Invalid subdomain")
    # Only a-z, 0-9, hyphen; no underscore or other chars
    if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]{3,}$", v):
        raise ValueError("Invalid subdomain")
    if v.startswith("-") or v.endswith("-") or "--" in v:
        raise ValueError("Invalid subdomain")
    return v


def validate_hex_color(value: str) -> str:
    """Validate #RRGGBB or #RGB hex color."""
    if not value or not value.strip():
        raise ValueError("Invalid hex color")
    v = value.strip()
    if not HEX_COLOR_RE.match(v):
        raise ValueError("Invalid hex color")
    return v


def validate_file_type(filename: str, allowed: Optional[set] = None) -> bool:
    """Return True if filename has an allowed image extension (jpg, png, webp)."""
    allowed = allowed or ALLOWED_IMAGE_EXTENSIONS
    if not filename:
        return False
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in allowed


def validate_file_size(size_bytes: int, max_bytes: Optional[int] = None) -> bool:
    """Return True if size_bytes <= max_bytes. Raises ValueError for negative size."""
    max_bytes = max_bytes or DEFAULT_MAX_FILE_SIZE_BYTES
    if size_bytes < 0:
        raise ValueError("File size must be non-negative")
    return size_bytes <= max_bytes
