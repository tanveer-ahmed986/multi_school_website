"""
CORS Middleware (T211)

Configure Cross-Origin Resource Sharing policies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os


def add_cors_middleware(app: FastAPI) -> None:
    """
    Add CORS middleware to FastAPI app with secure defaults.

    Args:
        app: FastAPI application instance
    """
    # Get allowed origins from environment
    allowed_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000")
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]

    # Production: Only allow specific domains
    # Development: Allow localhost for testing
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,  # Allow cookies for JWT refresh tokens
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-CSRF-Token",
            "X-Request-ID",
        ],
        expose_headers=["X-Process-Time", "X-Request-ID"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )

    print(f"✓ CORS configured: {allowed_origins}")
