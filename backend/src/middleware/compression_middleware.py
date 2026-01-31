"""
Compression Middleware (T205)

Implements gzip compression for API responses to reduce bandwidth.
Compresses responses larger than 1KB.
"""

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware


def add_compression_middleware(app: FastAPI) -> None:
    """
    Add gzip compression middleware to FastAPI app.

    Compresses responses when:
    - Client supports gzip (Accept-Encoding: gzip)
    - Response size > minimum_size (1000 bytes = 1KB)

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,  # Only compress responses larger than 1KB
        compresslevel=6,    # Compression level (1-9, 6 is balanced)
    )
    print("✓ Response compression enabled (gzip, min size: 1KB)")
