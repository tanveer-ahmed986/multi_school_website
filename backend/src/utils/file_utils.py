"""
File utilities: path sanitization, file type/size validation for uploads.
"""
import os
import re
from typing import Optional

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
DEFAULT_MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB


def sanitize_path(path_string: str) -> str:
    """Remove path traversal and dangerous segments; return safe relative path or basename."""
    if not path_string or not path_string.strip():
        return ""
    # Normalize and remove ..
    normalized = os.path.normpath(path_string.strip()).replace("\\", "/")
    # Remove any leading slashes or drive letters
    normalized = normalized.lstrip("/").lstrip("\\")
    if normalized.startswith("..") or "/.." in normalized or ".." in normalized:
        # Fall back to basename only
        normalized = os.path.basename(path_string)
    # Allow only alphanumeric, hyphen, underscore, dot, slash
    if not re.match(r"^[a-zA-Z0-9_\-./]+$", normalized):
        return os.path.basename(path_string) if path_string else ""
    return normalized


def validate_upload_file_type(filename: str, allowed: Optional[set] = None) -> bool:
    """Return True if filename has an allowed image extension."""
    allowed = allowed or ALLOWED_IMAGE_EXTENSIONS
    if not filename or not filename.strip():
        return False
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in allowed


def validate_upload_file_size(size_bytes: int, max_bytes: Optional[int] = None) -> bool:
    """Return True if size_bytes <= max_bytes (default 5MB)."""
    max_bytes = max_bytes or DEFAULT_MAX_FILE_SIZE_BYTES
    return 0 <= size_bytes <= max_bytes
