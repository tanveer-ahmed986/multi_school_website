# Security Hardening Guide (T209-T216)

## Security Checklist

### Input Validation & Sanitization (T209) ✅
- [x] HTML sanitization for XSS prevention (`utils/security.py`)
- [x] Filename sanitization for path traversal prevention
- [x] JSON key sanitization
- [x] Email validation with regex
- [x] Subdomain validation (alphanumeric + hyphens only)
- [x] Hex color validation
- [x] File type validation (MIME type checking)
- [x] File size validation (10MB max default)

### SQL Injection Prevention (T210) ✅
- [x] ORM usage (SQLAlchemy) with parameterized queries
- [x] UUID validation before database queries
- [x] Input validation with Pydantic models
- [x] SQL injection pattern detection (defense-in-depth)
- [x] Row-Level Security (RLS) policies

### CORS Policies (T211) ✅
- [x] Strict origin whitelist (`cors_middleware.py`)
- [x] Credentials allowed for JWT cookies
- [x] Limited HTTP methods (GET, POST, PUT, DELETE, OPTIONS)
- [x] Specific allowed headers only
- [x] Preflight caching (1 hour)

### Rate Limiting (T212)

#### Backend Rate Limiting

Install dependencies:
```bash
pip install slowapi
```

Implementation (`middleware/rate_limit_middleware.py`):
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request

limiter = Limiter(key_func=get_remote_address)

def add_rate_limit_middleware(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Usage in routes
@app.get("/public/school")
@limiter.limit("100/minute")  # 100 requests per minute per IP
async def get_school(request: Request):
    # ...
```

#### Rate Limit Rules

**Public Endpoints**:
- `/public/*`: 100 requests/minute per IP
- `/auth/login`: 5 requests/minute per IP (brute force protection)
- `/auth/refresh`: 10 requests/minute per IP

**Authenticated Endpoints**:
- `/content/*`: 60 requests/minute per user
- `/schools/*`: 30 requests/minute per user (super admin)

**Global**:
- 1000 requests/minute per IP across all endpoints

#### Cloudflare Rate Limiting (Recommended)

Production deployments should use Cloudflare rate limiting:

```javascript
// Cloudflare Rate Limiting Rule
if (http.request.uri.path matches "^/auth/login")
  then rate limit 5 requests per minute per IP

if (http.request.uri.path matches "^/public/")
  then rate limit 100 requests per minute per IP
```

### CAPTCHA Integration (T213)

#### hCaptcha (Recommended - Privacy-focused)

1. **Sign up**: https://www.hcaptcha.com/
2. **Get site key and secret key**

Frontend integration (`frontend/src/components/common/CaptchaField.tsx`):
```typescript
import HCaptcha from '@hcaptcha/react-hcaptcha';

export function CaptchaField({ onVerify }) {
  return (
    <HCaptcha
      sitekey={process.env.NEXT_PUBLIC_HCAPTCHA_SITE_KEY}
      onVerify={(token) => onVerify(token)}
    />
  );
}
```

Backend verification (`backend/src/utils/captcha.py`):
```python
import httpx
import os

async def verify_captcha(token: str) -> bool:
    """Verify hCaptcha token."""
    secret = os.getenv("HCAPTCHA_SECRET_KEY")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://hcaptcha.com/siteverify",
            data={"secret": secret, "response": token}
        )
        result = response.json()
        return result.get("success", False)
```

**Apply CAPTCHA to**:
- Contact forms
- Public comment submission (if added)
- Login page (after 3 failed attempts)
- Password reset requests

#### Alternative: reCAPTCHA v3

```html
<script src="https://www.google.com/recaptcha/api.js?render=SITE_KEY"></script>
<script>
  grecaptcha.execute('SITE_KEY', {action: 'submit'}).then(function(token) {
    document.getElementById('captcha-token').value = token;
  });
</script>
```

### HTTPS Enforcement (T214) ✅

#### Production Deployment

**1. Obtain SSL Certificate**

Option A: Let's Encrypt (Free):
```bash
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

Option B: Cloudflare SSL (Automatic):
- Enable "Full (strict)" SSL mode in Cloudflare dashboard

**2. Configure NGINX**

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect all HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # HSTS header
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Proxy to backend
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Proxy to frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**3. Backend HTTPS redirect**

```python
# backend/src/middleware/security_middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Redirect HTTP to HTTPS in production
        if request.url.scheme == "http" and not request.url.hostname.startswith("localhost"):
            url = request.url.replace(scheme="https")
            return RedirectResponse(url, status_code=301)
        return await call_next(request)
```

### Content Security Policy (T215)

#### CSP Headers (Strict)

```python
# backend/src/middleware/security_middleware.py
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.hcaptcha.com https://*.hcaptcha.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://api.yourdomain.com; "
        "frame-src 'self' https://www.hcaptcha.com https://*.hcaptcha.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'self';"
    )

    # Other security headers (T214)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

    return response
```

#### Next.js CSP Configuration

```javascript
// frontend/next.config.js
const ContentSecurityPolicy = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline' https://www.hcaptcha.com;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  font-src 'self' https://fonts.gstatic.com;
  img-src 'self' data: https:;
  connect-src 'self' ${process.env.NEXT_PUBLIC_API_URL};
  frame-src 'self' https://www.hcaptcha.com;
`;

const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: ContentSecurityPolicy.replace(/\s{2,}/g, ' ').trim()
  },
  // ... other headers
];
```

### Security Scanning (T216)

#### OWASP ZAP (Zed Attack Proxy)

**Installation**:
```bash
# Docker
docker pull owasp/zap2docker-stable

# macOS
brew install zaproxy

# Linux
sudo apt-get install zaproxy
```

**Run automated scan**:
```bash
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://localhost:3000 \
  -r zap-report.html
```

**Scan types**:
- **Baseline scan**: Quick passive scan (~10 minutes)
- **Full scan**: Active scan with attacks (~1 hour)
- **API scan**: Scan API endpoints with OpenAPI spec

**Target**: Zero critical/high severity vulnerabilities

#### npm audit (Frontend)

```bash
cd frontend
npm audit

# Fix automatically
npm audit fix

# Force fix (may break dependencies)
npm audit fix --force
```

#### Safety (Python Backend)

```bash
pip install safety

# Check for known vulnerabilities
safety check

# Check requirements.txt
safety check -r requirements.txt
```

#### Snyk (Recommended for CI/CD)

```bash
npm install -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities
snyk test

# Monitor project
snyk monitor
```

**Add to CI/CD** (`.github/workflows/security.yml`):
```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Snyk Security Scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run npm audit
        run: npm audit --audit-level=high

      - name: Run OWASP ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'http://localhost:3000'
```

## Common Vulnerabilities Checklist

### OWASP Top 10 (2021)

- [x] **A01: Broken Access Control**: RLS policies, permission decorators, tenant middleware
- [x] **A02: Cryptographic Failures**: HTTPS, bcrypt password hashing, secure JWT
- [x] **A03: Injection**: Parameterized queries (ORM), input validation, sanitization
- [x] **A04: Insecure Design**: Security by design, defense-in-depth
- [x] **A05: Security Misconfiguration**: Secure defaults, CSP headers, HSTS
- [ ] **A06: Vulnerable Components**: Regular dependency updates, npm audit, safety
- [x] **A07: Authentication Failures**: JWT with refresh tokens, rate limiting on login
- [x] **A08: Software and Data Integrity**: File validation, checksum verification
- [x] **A09: Logging Failures**: Audit logs, request logging
- [x] **A10: SSRF**: Input validation, URL allowlist

## Security Incident Response

### If Security Breach Detected

1. **Immediate**: Revoke all refresh tokens, force re-login
2. **Isolate**: Disable affected school accounts
3. **Investigate**: Review audit logs, identify attack vector
4. **Patch**: Fix vulnerability, deploy hotfix
5. **Notify**: Inform affected users within 72 hours (GDPR compliance)
6. **Review**: Conduct post-mortem, update security policies

## Security Contact

For reporting security vulnerabilities:
- Email: security@yourdomain.com
- Response time: 24-48 hours

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP ZAP](https://www.zaproxy.org/)
- [Snyk](https://snyk.io/)
- [Let's Encrypt](https://letsencrypt.org/)
- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
