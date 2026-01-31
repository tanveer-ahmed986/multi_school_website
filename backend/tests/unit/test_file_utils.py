"""Unit tests for file utilities (T038)."""
import pytest
from src.utils.file_utils import (
    sanitize_path,
    validate_upload_file_type,
    validate_upload_file_size,
    ALLOWED_IMAGE_EXTENSIONS,
    DEFAULT_MAX_FILE_SIZE_BYTES,
)


@pytest.mark.unit
class TestSanitizePath:
    def test_removes_path_traversal(self):
        assert ".." not in sanitize_path("../../../etc/passwd")
        assert sanitize_path("..\\..\\windows\\system32") != "..\\..\\windows\\system32"

    def test_allows_safe_relative_path(self):
        safe = "schools/abc-123/config/logo.png"
        assert sanitize_path(safe) == safe or "logo.png" in sanitize_path(safe)

    def test_returns_basename_or_safe_path(self):
        result = sanitize_path("faculty/photo.jpg")
        assert "photo" in result or "jpg" in result
        assert ".." not in result


@pytest.mark.unit
class TestValidateUploadFileType:
    def test_accepts_allowed_extensions(self):
        for ext in [".jpg", ".jpeg", ".png", ".webp"]:
            assert validate_upload_file_type(f"file{ext}") is True
        assert validate_upload_file_type("FILE.JPG") is True

    def test_rejects_disallowed(self):
        assert validate_upload_file_type("file.exe") is False
        assert validate_upload_file_type("file.sh") is False
        assert validate_upload_file_type("file") is False


@pytest.mark.unit
class TestValidateUploadFileSize:
    def test_accepts_within_limit(self):
        assert validate_upload_file_size(1024) is True
        assert validate_upload_file_size(DEFAULT_MAX_FILE_SIZE_BYTES) is True

    def test_rejects_over_limit(self):
        assert validate_upload_file_size(DEFAULT_MAX_FILE_SIZE_BYTES + 1) is False

    def test_custom_max(self):
        assert validate_upload_file_size(100, max_bytes=200) is True
        assert validate_upload_file_size(300, max_bytes=200) is False
