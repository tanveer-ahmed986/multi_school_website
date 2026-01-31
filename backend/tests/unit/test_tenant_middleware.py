"""Unit tests for TenantMiddleware (T044)."""
import pytest
from src.middleware.tenant_middleware import extract_subdomain


@pytest.mark.unit
class TestExtractSubdomain:
    def test_localhost_with_subdomain(self):
        assert extract_subdomain("springfield.localhost") == "springfield"
        assert extract_subdomain("demo.localhost") == "demo"

    def test_localhost_without_subdomain(self):
        assert extract_subdomain("localhost") is None

    def test_host_with_port(self):
        assert extract_subdomain("springfield.localhost:3000") == "springfield"

    def test_production_style_host(self):
        assert extract_subdomain("schoolA.example.com") == "schoolA"
        assert extract_subdomain("www.example.com") is None or extract_subdomain("www.example.com") != "www"

    def test_base_domain_parameter(self):
        assert extract_subdomain("springfield.example.com", base_domain="example.com") == "springfield"
        assert extract_subdomain("other.org", base_domain="example.com") is None
