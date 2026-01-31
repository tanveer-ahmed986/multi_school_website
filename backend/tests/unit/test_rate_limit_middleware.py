"""Unit tests for RateLimitMiddleware (T048)."""
from collections import defaultdict
import pytest
from src.middleware.rate_limit_middleware import check_rate_limit


@pytest.mark.unit
class TestRateLimitMiddleware:
    def test_check_rate_limit_under_limit_returns_true(self):
        store = defaultdict(lambda: (0, 0.0))
        key = "ip:127.0.0.1"
        assert check_rate_limit(store, key, max_requests=10, window_seconds=60) is True
        assert store[key][0] <= 10

    def test_check_rate_limit_over_limit_returns_false(self):
        store = defaultdict(lambda: (0, 0.0))
        key = "ip:127.0.0.1"
        for _ in range(5):
            check_rate_limit(store, key, max_requests=5, window_seconds=60)
        assert check_rate_limit(store, key, max_requests=5, window_seconds=60) is False
