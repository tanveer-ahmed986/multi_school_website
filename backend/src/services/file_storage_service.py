"""
File storage service with abstraction for S3 migration.

Provides interface and local file system implementation.
(T134-T135 - Implementation)
"""
from abc import ABC, abstractmethod
from typing import BinaryIO, Optional
import os
import shutil
from pathlib import Path
from uuid import UUID


class FileStorageService(ABC):
    """Abstract interface for file storage operations."""

    @abstractmethod
    async def upload_file(
        self, school_id: UUID, category: str, filename: str, file: BinaryIO
    ) -> str:
        """Upload file and return URL/path."""
        pass

    @abstractmethod
    async def download_file(self, school_id: UUID, file_path: str) -> BinaryIO:
        """Download file by path."""
        pass

    @abstractmethod
    async def delete_file(self, school_id: UUID, file_path: str) -> bool:
        """Delete file."""
        pass


class LocalFileStorageService(FileStorageService):
    """
    Local file system implementation for MVP.

    File structure: /data/schools/{school_id}/{category}/{filename}

    Migration to S3: Replace this class with S3FileStorageService
    without changing application code.
    """

    def __init__(self, base_path: str = "./data/schools"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent directory traversal attacks."""
        # Remove any path separators
        filename = os.path.basename(filename)
        # Remove any potentially dangerous characters
        safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.")
        return "".join(c for c in filename if c in safe_chars)

    def _get_school_path(self, school_id: UUID, category: str) -> Path:
        """Get directory path for school and category."""
        school_path = self.base_path / str(school_id) / category
        school_path.mkdir(parents=True, exist_ok=True)
        return school_path

    async def upload_file(
        self, school_id: UUID, category: str, filename: str, file: BinaryIO
    ) -> str:
        """
        Upload file to local file system.

        Args:
            school_id: School UUID
            category: Category (faculty, results, gallery, etc.)
            filename: Original filename
            file: File-like object

        Returns:
            Relative file path for storage in database
        """
        safe_filename = self._sanitize_filename(filename)
        school_path = self._get_school_path(school_id, category)
        file_path = school_path / safe_filename

        # Write file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)

        # Return relative path for database storage
        return f"/data/schools/{school_id}/{category}/{safe_filename}"

    async def download_file(self, school_id: UUID, file_path: str) -> BinaryIO:
        """
        Download file from local file system.

        Args:
            school_id: School UUID (for validation)
            file_path: Relative file path from database

        Returns:
            File-like object

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        # Validate file path starts with correct school_id
        if not file_path.startswith(f"/data/schools/{school_id}/"):
            raise PermissionError("Cannot access files from other schools")

        full_path = Path("." + file_path)

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return open(full_path, "rb")

    async def delete_file(self, school_id: UUID, file_path: str) -> bool:
        """
        Delete file from local file system.

        Args:
            school_id: School UUID (for validation)
            file_path: Relative file path from database

        Returns:
            True if deleted, False if file didn't exist
        """
        # Validate file path starts with correct school_id
        if not file_path.startswith(f"/data/schools/{school_id}/"):
            raise PermissionError("Cannot delete files from other schools")

        full_path = Path("." + file_path)

        if full_path.exists():
            full_path.unlink()
            return True

        return False

    def get_storage_usage(self, school_id: UUID) -> int:
        """
        Calculate total storage usage for a school.

        Args:
            school_id: School UUID

        Returns:
            Total bytes used
        """
        school_path = self.base_path / str(school_id)

        if not school_path.exists():
            return 0

        total_size = 0
        for file_path in school_path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size

        return total_size


# Singleton instance
_file_storage_service: Optional[FileStorageService] = None


def get_file_storage_service() -> FileStorageService:
    """Get file storage service instance (dependency injection)."""
    global _file_storage_service

    if _file_storage_service is None:
        # For MVP, use local file storage
        # To migrate to S3, replace with: S3FileStorageService()
        _file_storage_service = LocalFileStorageService()

    return _file_storage_service
