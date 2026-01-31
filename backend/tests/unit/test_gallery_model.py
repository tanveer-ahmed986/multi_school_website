"""Unit tests for GalleryImage model (T021)."""
import uuid
import pytest
from src.models.gallery import GalleryImage


@pytest.mark.unit
class TestGalleryImageModel:
    def test_table_name(self):
        assert GalleryImage.__tablename__ == "gallery_images"

    def test_has_required_columns(self):
        assert hasattr(GalleryImage, "image_id")
        assert hasattr(GalleryImage, "school_id")
        assert hasattr(GalleryImage, "category")
        assert hasattr(GalleryImage, "image_url")
        assert hasattr(GalleryImage, "file_size_bytes")
        assert hasattr(GalleryImage, "uploaded_by")

    def test_instantiate_with_required_fields(self):
        school_id = uuid.uuid4()
        user_id = uuid.uuid4()
        g = GalleryImage(
            school_id=school_id,
            category="sports",
            image_url="/data/schools/xyz/photo.jpg",
            file_size_bytes=102400,
            uploaded_by=user_id,
        )
        assert g.school_id == school_id
        assert g.category == "sports"
        assert g.image_url == "/data/schools/xyz/photo.jpg"
        assert g.file_size_bytes == 102400
        assert g.is_visible is True
        assert g.display_order == 0
