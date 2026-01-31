"""
Cache Service (T203)

Per-school caching implementation with Redis support.
Caches frequently accessed data (school config, public content).
"""

import json
import os
from typing import Any, Optional
from datetime import timedelta

# Redis is optional - gracefully degrade if not available
try:
    import redis
    from redis import Redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    Redis = Any  # Type hint fallback


class CacheService:
    """
    Caching service with Redis backend.
    Falls back to no caching if Redis is unavailable.
    """

    def __init__(self):
        self.client: Optional[Redis] = None
        self.enabled = False

        if REDIS_AVAILABLE:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            try:
                self.client = redis.from_url(redis_url, decode_responses=True)
                # Test connection
                self.client.ping()
                self.enabled = True
                print(f"✓ Redis cache enabled: {redis_url}")
            except Exception as e:
                print(f"⚠ Redis unavailable, caching disabled: {e}")
                self.enabled = False
        else:
            print("⚠ Redis not installed, caching disabled")

    def _make_key(self, school_id: str, resource: str) -> str:
        """Generate cache key with school namespace."""
        return f"school:{school_id}:{resource}"

    async def get(self, school_id: str, resource: str) -> Optional[Any]:
        """
        Get cached value for a school resource.

        Args:
            school_id: School UUID
            resource: Resource name (e.g., 'config', 'faculty', 'notices')

        Returns:
            Cached value or None if not found
        """
        if not self.enabled or not self.client:
            return None

        try:
            key = self._make_key(school_id, resource)
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    async def set(
        self,
        school_id: str,
        resource: str,
        value: Any,
        ttl: int = 300  # 5 minutes default
    ) -> bool:
        """
        Set cached value for a school resource.

        Args:
            school_id: School UUID
            resource: Resource name
            value: Value to cache (must be JSON serializable)
            ttl: Time to live in seconds

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            return False

        try:
            key = self._make_key(school_id, resource)
            serialized = json.dumps(value, default=str)
            self.client.setex(key, timedelta(seconds=ttl), serialized)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False

    async def delete(self, school_id: str, resource: str) -> bool:
        """
        Delete cached value for a school resource.

        Args:
            school_id: School UUID
            resource: Resource name

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            return False

        try:
            key = self._make_key(school_id, resource)
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False

    async def clear_school(self, school_id: str) -> bool:
        """
        Clear all cache entries for a school.

        Args:
            school_id: School UUID

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            return False

        try:
            pattern = f"school:{school_id}:*"
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
            return True
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False


# Global cache instance
cache = CacheService()


# Cache TTL constants (in seconds)
class CacheTTL:
    SCHOOL_CONFIG = 3600  # 1 hour
    PUBLIC_CONTENT = 300  # 5 minutes
    FACULTY = 600  # 10 minutes
    RESULTS = 1800  # 30 minutes
    NOTICES = 300  # 5 minutes
    GALLERY = 600  # 10 minutes
