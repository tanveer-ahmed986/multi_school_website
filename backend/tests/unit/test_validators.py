"""Unit tests for input validators (T036)."""
import pytest
from src.utils.validators import (
    validate_email,
    validate_subdomain,
    validate_hex_color,
    validate_file_type,
    validate_file_size,
)


@pytest.mark.unit
class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("admin@school.edu") == "admin@school.edu"
        assert validate_email("user+tag@example.com") == "user+tag@example.com"

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError, match="Invalid email"):
            validate_email("notanemail")
        with pytest.raises(ValueError, match="Invalid email"):
            validate_email("@nodomain.com")
        with pytest.raises(ValueError, match="Invalid email"):
            validate_email("")


@pytest.mark.unit
class TestValidateSubdomain:
    def test_valid_subdomain(self):
        assert validate_subdomain("springfield") == "springfield"
        assert validate_subdomain("school-a") == "school-a"
        assert validate_subdomain("abc") == "abc"

    def test_normalizes_lowercase(self):
        assert validate_subdomain("SpringField") == "springfield"

    def test_invalid_subdomain_raises(self):
        with pytest.raises(ValueError, match="Invalid subdomain"):
            validate_subdomain("ab")  # too short
        with pytest.raises(ValueError, match="Invalid subdomain"):
            validate_subdomain("a" * 51)  # too long
        with pytest.raises(ValueError, match="Invalid subdomain"):
            validate_subdomain("school_a")  # underscore not allowed
        with pytest.raises(ValueError, match="Invalid subdomain"):
            validate_subdomain("")


@pytest.mark.unit
class TestValidateHexColor:
    def test_valid_hex_color(self):
        assert validate_hex_color("#0A3D62") == "#0A3D62"
        assert validate_hex_color("#ffffff") == "#ffffff"
        assert validate_hex_color("#ABC") == "#ABC"

    def test_invalid_hex_color_raises(self):
        with pytest.raises(ValueError, match="Invalid hex color"):
            validate_hex_color("0A3D62")  # missing #
        with pytest.raises(ValueError, match="Invalid hex color"):
            validate_hex_color("#GGGGGG")
        with pytest.raises(ValueError, match="Invalid hex color"):
            validate_hex_color("#12")  # wrong length


@pytest.mark.unit
class TestValidateFileType:
    def test_allowed_types(self):
        assert validate_file_type("photo.jpg") is True
        assert validate_file_type("image.png") is True
        assert validate_file_type("pic.webp") is True
        assert validate_file_type("PHOTO.JPG") is True

    def test_disallowed_types(self):
        assert validate_file_type("file.exe") is False
        assert validate_file_type("script.sh") is False
        assert validate_file_type("doc.pdf") is False


@pytest.mark.unit
class TestValidateFileSize:
    def test_within_limit(self):
        assert validate_file_size(1024, max_bytes=5 * 1024 * 1024) is True
        assert validate_file_size(0, max_bytes=100) is True

    def test_exceeds_limit(self):
        assert validate_file_size(6 * 1024 * 1024, max_bytes=5 * 1024 * 1024) is False

    def test_raises_for_negative(self):
        with pytest.raises(ValueError, match="size"):
            validate_file_size(-1, max_bytes=1000)
