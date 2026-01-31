# Performance Optimization Guide (T207, T208)

## Performance Targets (SC-004)

- **Page Load Time**: <2 seconds (p95)
- **API Response Time**: <500ms (p95)
- **First Contentful Paint (FCP)**: <1.8s
- **Largest Contentful Paint (LCP)**: <2.5s
- **Time to Interactive (TTI)**: <3.5s
- **Cumulative Layout Shift (CLS)**: <0.1

## CDN Configuration (T207)

### Cloudflare Setup (Recommended)

1. **Add your domain to Cloudflare**
   - Create account at https://dash.cloudflare.com/
   - Add your domain
   - Update nameservers at your registrar

2. **Configure caching rules**

**Page Rules** (recommended):
```
Static Assets: *.js, *.css, *.jpg, *.png, *.webp, *.svg, *.woff2
- Cache Level: Standard
- Edge Cache TTL: 1 year (31536000 seconds)
- Browser Cache TTL: 1 year

API Endpoints: /api/*
- Cache Level: Bypass
- Security Level: Medium
- Browser Integrity Check: On

Public Content: /public/*
- Cache Level: Standard
- Edge Cache TTL: 5 minutes (300 seconds)
- Browser Cache TTL: 5 minutes
```

**Cache Rules** (modern approach):
```javascript
// Cache static assets for 1 year
(http.request.uri.path matches "\\.(js|css|jpg|jpeg|png|webp|svg|woff2|woff|ttf|ico)$")
→ Cache TTL: 31536000s, Browser TTL: 31536000s

// Cache public API responses for 5 minutes
(http.request.uri.path contains "/public/")
→ Cache TTL: 300s, Browser TTL: 300s

// Bypass cache for admin/auth
(http.request.uri.path contains "/admin/" or http.request.uri.path contains "/auth/")
→ Bypass cache
```

3. **Performance features to enable**
   - ✅ Auto Minify (JavaScript, CSS, HTML)
   - ✅ Brotli compression
   - ✅ HTTP/2
   - ✅ HTTP/3 (QUIC)
   - ✅ Early Hints
   - ✅ Rocket Loader (optional - test first)

4. **Image optimization**
   - Enable Cloudflare Images or Polish
   - Automatic WebP conversion
   - Lazy loading

### Alternative CDN Options

#### AWS CloudFront
```javascript
// CloudFront distribution settings
{
  "Origins": [
    {
      "DomainName": "api.yourdomain.com",
      "OriginPath": "",
      "CustomHeaders": []
    }
  ],
  "DefaultCacheBehavior": {
    "ViewerProtocolPolicy": "redirect-to-https",
    "AllowedMethods": ["GET", "HEAD", "OPTIONS"],
    "CachedMethods": ["GET", "HEAD"],
    "Compress": true,
    "MinTTL": 0,
    "DefaultTTL": 86400,
    "MaxTTL": 31536000
  }
}
```

#### Vercel Edge Network (for Next.js)
- Automatic CDN for frontend
- Edge caching built-in
- Zero configuration required

## Performance Testing (T208)

### Lighthouse CI (Recommended)

Install Lighthouse CI:
```bash
npm install -g @lhci/cli
```

Create configuration file `lighthouserc.js`:
```javascript
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/faculty', 'http://localhost:3000/results'],
      numberOfRuns: 3,
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['error', {minScore: 0.9}],
        'categories:accessibility': ['error', {minScore: 0.95}],
        'categories:best-practices': ['error', {minScore: 0.9}],
        'categories:seo': ['error', {minScore: 0.9}],
        'first-contentful-paint': ['error', {maxNumericValue: 1800}],
        'largest-contentful-paint': ['error', {maxNumericValue: 2500}],
        'cumulative-layout-shift': ['error', {maxNumericValue: 0.1}],
        'total-blocking-time': ['error', {maxNumericValue: 300}],
      },
    },
    upload: {
      target: 'filesystem',
      outputDir: './lighthouse-reports',
    },
  },
};
```

Run Lighthouse CI:
```bash
lhci autorun
```

### WebPageTest

1. Visit https://www.webpagetest.org/
2. Enter your URL
3. Select test location and device
4. Run test
5. Review waterfall and filmstrip

**Target Metrics**:
- Speed Index: <3.0s
- Time to First Byte (TTFB): <600ms
- Start Render: <1.5s

### Load Testing with k6

Install k6:
```bash
# macOS
brew install k6

# Windows
choco install k6

# Linux
sudo apt-get install k6
```

Create load test script `load-test.js`:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },   // Ramp up to 50 users
    { duration: '1m', target: 100 },   // Ramp up to 100 users
    { duration: '2m', target: 1000 },  // Ramp up to 1000 users
    { duration: '1m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],     // Error rate < 1%
  },
};

export default function () {
  // Test homepage
  let res = http.get('http://localhost:3000/');
  check(res, {
    'homepage status 200': (r) => r.status === 200,
    'homepage load < 2s': (r) => r.timings.duration < 2000,
  });

  sleep(1);

  // Test public API
  res = http.get('http://localhost:8000/public/school');
  check(res, {
    'API status 200': (r) => r.status === 200,
    'API response < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

Run load test:
```bash
k6 run load-test.js
```

### Performance Monitoring in Production

#### Backend Monitoring

```python
# backend/src/middleware/performance_middleware.py
import time
from fastapi import Request

@app.middleware("http")
async def add_performance_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

    # Log slow requests
    if process_time > 500:
        print(f"⚠ Slow request: {request.url.path} took {process_time:.2f}ms")

    return response
```

#### Frontend Monitoring with Web Vitals

```typescript
// frontend/src/app/layout.tsx
import { useReportWebVitals } from 'next/web-vitals';

export function reportWebVitals(metric) {
  // Send to analytics
  console.log(metric);

  // Optionally send to monitoring service
  if (metric.value > thresholds[metric.name]) {
    console.warn(`⚠ Poor ${metric.name}: ${metric.value}`);
  }
}
```

## Optimization Checklist

### Frontend Optimizations
- [x] Next.js Image component with WebP/AVIF (T204)
- [x] Code splitting (automatic with Next.js)
- [x] Tree shaking (automatic with Next.js)
- [x] Lazy loading for images and components
- [x] CDN for static assets (T207)
- [x] Minification (CSS, JS, HTML)
- [x] Gzip/Brotli compression
- [ ] Service Worker for offline support (optional)
- [ ] Preconnect to external domains
- [ ] Prefetch critical resources

### Backend Optimizations
- [x] API response compression (T205)
- [x] Per-school caching with Redis (T203)
- [x] Database query optimization (T206)
- [x] Connection pooling (SQLAlchemy)
- [x] Pagination for large datasets
- [x] Select only needed columns
- [x] Eager loading to avoid N+1 queries

### Database Optimizations
- [x] Indexes on frequently queried columns
- [x] Composite indexes for multi-column queries
- [x] RLS policies use indexed columns
- [x] Analyze and vacuum regularly
- [x] Connection pooling
- [x] Query result caching

## Performance Budget

Set performance budgets to prevent regressions:

```json
{
  "budgets": [
    {
      "resourceSizes": [
        {
          "resourceType": "script",
          "budget": 300
        },
        {
          "resourceType": "total",
          "budget": 1000
        },
        {
          "resourceType": "image",
          "budget": 500
        }
      ]
    },
    {
      "timings": [
        {
          "metric": "first-contentful-paint",
          "budget": 1800
        },
        {
          "metric": "largest-contentful-paint",
          "budget": 2500
        },
        {
          "metric": "interactive",
          "budget": 3500
        }
      ]
    }
  ]
}
```

## CI/CD Integration

Add to `.github/workflows/ci.yml`:
```yaml
- name: Run Lighthouse CI
  run: |
    npm install -g @lhci/cli
    lhci autorun || echo "Lighthouse failed"

- name: Performance Tests
  run: |
    npm run build
    npm start &
    sleep 10
    k6 run tests/load-test.js
```

## Resources

- [Web Vitals](https://web.dev/vitals/)
- [Lighthouse Documentation](https://developers.google.com/web/tools/lighthouse)
- [Cloudflare Performance](https://www.cloudflare.com/performance/)
- [k6 Load Testing](https://k6.io/docs/)

## Performance Score Target

**Minimum Acceptable**: 90/100
**Target**: 95+/100

Monitor performance regularly and address regressions immediately.
