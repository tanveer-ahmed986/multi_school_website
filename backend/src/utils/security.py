"""
Security Utilities (T209, T210)

Input sanitization, XSS prevention, and SQL injection prevention.
"""

import re
import html
from typing import Any, Dict, List, Optional
import bleach


def sanitize_html(text: str, allowed_tags: Optional[List[str]] = None) -> str:
    """
    Sanitize HTML input to prevent XSS attacks (T209).

    Args:
        text: HTML string to sanitize
        allowed_tags: List of allowed HTML tags (default: none)

    Returns:
        Sanitized HTML string
    """
    if allowed_tags is None:
        # No HTML allowed by default
        return html.escape(text)

    # Allow specific tags with bleach
    return bleach.clean(
        text,
        tags=allowed_tags,
        attributes={},  # No attributes allowed
        strip=True,
    )


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal attacks (T209).

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove path separators and null bytes
    filename = filename.replace('..', '').replace('/', '').replace('\\', '').replace('\x00', '')

    # Remove special characters, keep only alphanumeric, dash, underscore, dot
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

    # Limit length
    if len(filename) > 255:
        filename = filename[:255]

    return filename


def validate_uuid(uuid_string: str) -> bool:
    """
    Validate UUID format to prevent injection (T210).

    Args:
        uuid_string: UUID string to validate

    Returns:
        True if valid UUID format
    """
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    return bool(uuid_pattern.match(uuid_string))


def validate_email(email: str) -> bool:
    """
    Validate email format (basic validation).

    Args:
        email: Email address to validate

    Returns:
        True if valid email format
    """
    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    return bool(email_pattern.match(email))


def validate_subdomain(subdomain: str) -> bool:
    """
    Validate subdomain format.

    Args:
        subdomain: Subdomain to validate

    Returns:
        True if valid subdomain format
    """
    # Lowercase alphanumeric and hyphens only, 3-50 chars
    subdomain_pattern = re.compile(r'^[a-z0-9][a-z0-9-]{1,48}[a-z0-9]$')
    return bool(subdomain_pattern.match(subdomain))


def validate_hex_color(color: str) -> bool:
    """
    Validate hex color format.

    Args:
        color: Hex color code

    Returns:
        True if valid hex color
    """
    color_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
    return bool(color_pattern.match(color))


def sanitize_json_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize JSON keys to prevent injection.

    Args:
        data: Dictionary with potentially unsafe keys

    Returns:
        Dictionary with sanitized keys
    """
    sanitized = {}
    for key, value in data.items():
        # Only allow alphanumeric keys and underscores
        safe_key = re.sub(r'[^a-zA-Z0-9_]', '_', key)
        if isinstance(value, dict):
            sanitized[safe_key] = sanitize_json_keys(value)
        elif isinstance(value, list):
            sanitized[safe_key] = [
                sanitize_json_keys(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[safe_key] = value
    return sanitized


def detect_sql_injection_patterns(text: str) -> bool:
    """
    Detect common SQL injection patterns (T210).
    Note: This is a safety check. Use parameterized queries (ORM) as primary defense.

    Args:
        text: Text to check for SQL injection patterns

    Returns:
        True if suspicious patterns detected
    """
    # Common SQL injection patterns
    suspicious_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION)\b)",
        r"(--|;|'|\")",
        r"(\bOR\b.*=.*)",
        r"(\bAND\b.*=.*)",
        r"(1=1|1='1')",
    ]

    text_upper = text.upper()
    for pattern in suspicious_patterns:
        if re.search(pattern, text_upper, re.IGNORECASE):
            return True

    return False


# File upload validation
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/jpg', 'image/png', 'image/webp'}
ALLOWED_DOCUMENT_TYPES = {'application/pdf'}
MAX_FILE_SIZE_MB = 10


def validate_file_type(content_type: str, allowed_types: set) -> bool:
    """
    Validate file MIME type.

    Args:
        content_type: File MIME type
        allowed_types: Set of allowed MIME types

    Returns:
        True if file type is allowed
    """
    return content_type in allowed_types


def validate_file_size(file_size: int, max_size_mb: int = MAX_FILE_SIZE_MB) -> bool:
    """
    Validate file size.

    Args:
        file_size: File size in bytes
        max_size_mb: Maximum allowed size in MB

    Returns:
        True if file size is within limit
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes
