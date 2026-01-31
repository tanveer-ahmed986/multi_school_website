# Technology Stack Research: Multi-School Website Platform

**Date**: 2026-01-31
**Feature**: 001-multi-school-platform
**Purpose**: Research and document technology stack decisions for implementation

---

## Research Questions

Based on Technical Context in plan.md, the following unknowns require research:

1. Backend framework choice (Python vs Node.js ecosystem)
2. Frontend framework choice (React/Next.js vs Vue/Nuxt vs other)
3. Database choice and multi-tenant strategy
4. Authentication implementation approach (JWT specifics)
5. File storage approach (filesystem vs cloud, migration path)
6. CDN and image optimization solution
7. Testing frameworks for TDD compliance

---

## 1. Backend Framework Decision

### Decision
**FastAPI (Python 3.11+)**

### Rationale
- **Async Performance**: Native async/await support meets <500ms API response requirement (p95)
- **OpenAPI Integration**: Automatic OpenAPI documentation generation supports contract-first development workflow
- **Type Safety**: Pydantic models provide strong type validation for school configurations, user inputs, and API contracts
- **Multi-Tenancy Ecosystem**: Excellent integration with SQLAlchemy for PostgreSQL row-level security implementation
- **JWT Authentication**: Simple integration with python-jose library for JWT with refresh tokens
- **Testing**: pytest ecosystem mature and well-documented for TDD workflow
- **Developer Experience**: Clean, readable code for educational platform domain logic

### Alternatives Considered

**Django (Python)**:
- **Pros**: Batteries-included ORM, admin panel, mature ecosystem
- **Cons**:
  - Django admin not needed (building custom admin panel per spec)
  - Heavier framework for API-focused architecture
  - Less performant for async workloads than FastAPI
  - More complex for contract-first OpenAPI development

**NestJS (Node.js/TypeScript)**:
- **Pros**: Full TypeScript stack, excellent for microservices, strong DI container
- **Cons**:
  - Less mature ecosystem for multi-tenant RLS patterns
  - Python has stronger data processing libraries (potential future: result analytics, AI features)
  - Team expertise consideration (if primarily Python-focused)

**Verdict**: FastAPI chosen for performance, type safety, and optimal multi-tenant architecture support.

---

## 2. Frontend Framework Decision

### Decision
**Next.js 14+ with App Router (React + TypeScript)**

### Rationale
- **SEO Optimization**: Built-in SSR/SSG critical for public school websites (organic search traffic)
- **Image Optimization**: Next.js Image component handles lazy loading, format conversion (WebP/AVIF), responsive images (meets FR-015)
- **Subdomain Routing**: Middleware can handle subdomain-based tenant routing cleanly
- **Performance**: Automatic code splitting, optimized bundles (meets <2s page load requirement)
- **Developer Experience**: TypeScript integration excellent, Hot Module Replacement (HMR) for fast development
- **Admin Dashboard Ecosystem**: Rich component libraries (Shadcn UI, React Admin, Headless UI)
- **Production Ready**: Vercel deployment option for easy scaling, or self-hosted

### Alternatives Considered

**Vue/Nuxt 3**:
- **Pros**: Simpler learning curve, excellent reactivity system
- **Cons**:
  - Smaller ecosystem for admin dashboard components
  - Less mature TypeScript integration than React
  - Fewer educational platform examples/templates

**Astro**:
- **Pros**: Excellent for static content, very fast
- **Cons**:
  - Limited interactivity for admin panel (requires islands architecture complexity)
  - Less suitable for multi-tenant dynamic routing

**Verdict**: Next.js chosen for SEO, image optimization, and rich admin component ecosystem.

---

## 3. Database Choice and Multi-Tenant Strategy

### Decision
**PostgreSQL 15+ with Row-Level Security (RLS)**

### Rationale
- **Native Row-Level Security**: PostgreSQL RLS provides database-level tenant isolation (critical for FR-003, FR-004)
- **JSONB Support**: Flexible storage for school configuration files (school.config.json) with queryable fields
- **Mature Ecosystem**: Excellent Python (SQLAlchemy, Alembic) and TypeScript (Prisma) ORM support
- **Horizontal Scaling**: Read replicas for public website load, write primary for admin operations
- **Constitutional Requirement**: Constitution explicitly recommends PostgreSQL for multi-tenant school platforms
- **Audit Logging**: Native support for triggers and audit tables (meets FR-045, FR-050)

### Multi-Tenant Isolation Strategy

**Row-Level Security (RLS) Implementation**:
```sql
-- Enable RLS on all tenant-specific tables
ALTER TABLE faculty ENABLE ROW LEVEL SECURITY;
ALTER TABLE results ENABLE ROW LEVEL SECURITY;
ALTER TABLE notices ENABLE ROW LEVEL SECURITY;
-- ... (all tenant tables)

-- Create RLS policy for SELECT
CREATE POLICY tenant_isolation_select ON faculty
  FOR SELECT
  USING (school_id = current_setting('app.current_school_id')::uuid);

-- Create RLS policy for INSERT
CREATE POLICY tenant_isolation_insert ON faculty
  FOR INSERT
  WITH CHECK (school_id = current_setting('app.current_school_id')::uuid);

-- Similar policies for UPDATE, DELETE
```

**Application-Level Flow**:
1. Middleware extracts subdomain from request header
2. Query `schools` table to resolve `school_id` from subdomain
3. Set PostgreSQL session variable: `SET app.current_school_id = '{school_id}'`
4. All subsequent queries automatically filtered by RLS policies

**Security Testing**:
- Integration tests verify School A admin cannot access School B data
- Attempt direct SQL injection to bypass RLS (should fail)
- Load testing with concurrent multi-tenant requests

### Alternatives Considered

**MongoDB (Document Store)**:
- **Pros**: Flexible schema for configuration files
- **Cons**:
  - No native row-level security (application-level filtering only - higher risk)
  - Harder to enforce referential integrity for relationships
  - Constitutional preference is PostgreSQL for school platforms

**MySQL**:
- **Pros**: Widely used, good performance
- **Cons**:
  - Row-level security support weaker than PostgreSQL
  - Less robust JSONB equivalent (JSON type less powerful)

**Verdict**: PostgreSQL with RLS chosen for constitutional alignment and superior multi-tenant isolation.

---

## 4. Authentication Implementation

### Decision
**JWT with Refresh Token Rotation**

### Rationale
- **Stateless**: Supports horizontal backend scaling (no session store required)
- **Multi-School Role Scoping**: Token claims can include `school_id` and `role` for authorization (meets FR-023)
- **Refresh Token Rotation**: Improves security by limiting access token lifespan (15 minutes) and rotating refresh tokens (7 days)
- **Constitutional Alignment**: Meets security best practices for school platforms
- **Simple Integration**: python-jose (backend), jose library (frontend)

### Token Structure

**Access Token Payload** (15-minute lifespan):
```json
{
  "sub": "user_id",
  "email": "user@school.com",
  "role": "SCHOOL_ADMIN",
  "school_id": "uuid-here",
  "exp": 1234567890
}
```

**Refresh Token** (7-day lifespan, HTTP-only cookie):
- Stored in database for revocation capability
- Rotated on every refresh request
- Invalidated on logout

### Security Measures
- Access tokens: Short lifespan (15 min) limits exposure window
- Refresh tokens: HTTP-only, Secure, SameSite cookies (prevents XSS theft)
- Token rotation: Old refresh tokens invalidated immediately
- Revocation list: Database table tracks invalidated tokens (logout, password change)

### Alternatives Considered

**Session-Based Authentication**:
- **Pros**: Simpler to implement, easier token revocation
- **Cons**:
  - Requires session store (Redis) - adds infrastructure complexity
  - Harder to scale horizontally (sticky sessions or shared session store)
  - Not stateless (complicates deployment)

**OAuth2 with Third-Party Provider (Google, Microsoft)**:
- **Pros**: Delegates authentication, reduces password management
- **Cons**:
  - External dependency (internet connectivity required)
  - Onboarding complexity (schools need Google Workspace/M365)
  - Not all schools may have existing SSO infrastructure

**Verdict**: JWT with refresh token rotation chosen for stateless scaling and multi-school role scoping.

---

## 5. File Storage Approach

### Decision
**File System Initially with Abstraction Layer for S3 Migration**

### Rationale
- **Onboarding Speed**: Meets <2 hour school onboarding target (SC-001) - no cloud account setup required
- **Simplicity**: Reduces infrastructure dependencies for MVP
- **Migration Path**: Abstraction layer (`FileStorageService` interface) enables S3 migration without code changes
- **Constitutional Justification**: Justified in Complexity Tracking (plan.md) as simplifying MVP

### File Storage Service Abstraction

**Interface Design**:
```python
# backend/src/services/file_storage_service.py

from abc import ABC, abstractmethod
from typing import BinaryIO

class FileStorageService(ABC):
    @abstractmethod
    async def upload_file(self, school_id: str, category: str, filename: str, file: BinaryIO) -> str:
        """Upload file and return URL"""
        pass

    @abstractmethod
    async def download_file(self, school_id: str, file_path: str) -> BinaryIO:
        """Download file by path"""
        pass

    @abstractmethod
    async def delete_file(self, school_id: str, file_path: str) -> bool:
        """Delete file"""
        pass

class LocalFileStorageService(FileStorageService):
    """File system implementation for MVP"""
    # Implementation uses /data/schools/{school_id}/... structure

class S3FileStorageService(FileStorageService):
    """S3 implementation for future migration"""
    # Implementation uses boto3 for AWS S3
```

**Dependency Injection**:
- Application configured to use `LocalFileStorageService` initially
- Switch to `S3FileStorageService` by changing configuration (no code changes)

### Cloud Migration Path

**Future S3 Implementation**:
- AWS S3 bucket with encryption at rest (AES-256)
- CloudFront CDN for global image delivery
- Signed URLs for secure file access (time-limited)
- S3 lifecycle policies for cost optimization (archive old results)

**Migration Steps** (when scaling beyond 50 schools):
1. Implement `S3FileStorageService` class
2. Upload existing files to S3 (one-time migration script)
3. Update configuration to use S3 service
4. Deploy with zero downtime

### Security Measures
- **File Type Validation**: Whitelist (jpg, png, webp) enforced at upload (FR-029)
- **File Size Limits**: 5MB max enforced client-side and server-side (FR-029)
- **Path Sanitization**: Prevent directory traversal attacks (../../etc/passwd)
- **Virus Scanning**: Consider ClamAV integration for production

### Alternatives Considered

**S3 from Day 1**:
- **Pros**: Production-ready, globally distributed, unlimited scaling
- **Cons**:
  - Increases onboarding complexity (AWS account, IAM, buckets)
  - Exceeds 2-hour onboarding target
  - Higher cost for MVP phase

**Dedicated Image Service (Cloudinary, Imgix)**:
- **Pros**: Advanced image transformations, built-in CDN
- **Cons**:
  - Additional cost (may exceed budget for MVP)
  - External dependency
  - Overkill for initial scale (10 schools)

**Verdict**: File system with abstraction layer chosen to meet onboarding target while preserving migration path.

---

## 6. CDN and Image Optimization

### Decision
**Next.js Image Component + Cloudflare CDN (or Vercel Edge)**

### Rationale
- **Next.js Image**: Automatic lazy loading, responsive images, format conversion (WebP/AVIF) (meets FR-015)
- **Cloudflare CDN**: Global edge network, generous free tier, DDoS protection
- **Performance**: Meets <1 second image load requirement (SC-009)
- **Developer Experience**: Zero configuration for Next.js Image component
- **Cost**: Cloudflare free tier sufficient for 10-50 schools

### Image Optimization Pipeline

**Client-Side** (Next.js):
```tsx
import Image from 'next/image'

// Automatic optimization: lazy loading, WebP/AVIF, responsive sizes
<Image
  src={galleryImage.url}
  alt={galleryImage.caption}
  width={800}
  height={600}
  loading="lazy"
  placeholder="blur"
/>
```

**Server-Side** (FastAPI):
- Upload validation: file type, size (FR-029)
- Optional: Image compression (Pillow library) before storage
- Generate responsive sizes (thumbnail, medium, large)

**CDN Configuration**:
- Cache-Control headers: `public, max-age=31536000` for images (1 year)
- Cloudflare caching: automatic with default settings
- Purge cache on image deletion/update

### Performance Targets
- First Contentful Paint (FCP): <1.8s
- Largest Contentful Paint (LCP): <2.5s (meets <2s page load for 95% of requests)
- Cumulative Layout Shift (CLS): <0.1 (Next.js Image prevents layout shift)

### Alternatives Considered

**Dedicated Image CDN (Cloudinary, Imgix)**:
- **Pros**: Advanced transformations (filters, overlays, AI cropping)
- **Cons**:
  - Additional cost ($0-$89/month starting)
  - Overkill for school website use cases (basic gallery, logos)

**Self-Hosted CDN (Nginx caching)**:
- **Pros**: Full control, no external dependency
- **Cons**:
  - Complex setup and maintenance
  - No global edge distribution (higher latency for distant users)

**Verdict**: Next.js Image + Cloudflare chosen for zero-configuration optimization and free global CDN.

---

## 7. Testing Frameworks for TDD Compliance

### Decision
**Backend**: pytest + pytest-asyncio + pytest-cov + httpx (for FastAPI testing)
**Frontend**: Vitest + Testing Library + Playwright

### Rationale

**Backend (pytest)**:
- **Industry Standard**: Python testing de facto standard
- **Async Support**: pytest-asyncio for testing FastAPI async routes
- **Coverage**: pytest-cov for enforcing ≥90% unit test coverage
- **FastAPI Integration**: httpx.AsyncClient for integration tests
- **Fixtures**: Powerful fixture system for database setup/teardown

**Frontend (Vitest + Playwright)**:
- **Vitest**: Faster than Jest (Vite-based), excellent TypeScript support, compatible with Jest ecosystem
- **Testing Library**: Component testing following best practices (user-centric queries)
- **Playwright**: E2E testing across browsers (Chromium, Firefox, WebKit), meets constitution requirement

### Test Pyramid Implementation

**Unit Tests (~70%)**:
- Backend: Service methods, validators, utilities
- Frontend: Utility functions, custom hooks, isolated components
- Target: ≥90% coverage for business logic

**Integration Tests (~20%)**:
- Backend: API endpoints with database interactions
- Frontend: Page-level component integration
- Target: ≥70% coverage for critical user journeys

**E2E Tests (~10%)**:
- Playwright tests for all P1 user stories:
  - Public website visitor flow (homepage, faculty, results, gallery, notices)
  - School admin content management flow
  - Super admin school onboarding flow
- Target: 100% coverage of P1 flows

### Testing Workflow (TDD)

**Red-Green-Refactor Cycle**:
1. **Red**: Write failing test for new feature
2. **Green**: Implement minimal code to pass test
3. **Refactor**: Improve code quality while keeping tests green

**Example Test Structure**:
```python
# backend/tests/unit/test_school_service.py

import pytest
from src.services.school_service import SchoolService

@pytest.mark.asyncio
async def test_create_school_generates_unique_id():
    # Red: Test written before implementation
    service = SchoolService()
    school = await service.create_school({
        "school_name": "Test School",
        "subdomain": "testschool"
    })
    assert school.school_id is not None
    assert len(str(school.school_id)) == 36  # UUID format
```

### CI/CD Integration

**GitHub Actions Workflow**:
```yaml
- name: Run Backend Tests
  run: |
    cd backend
    pytest --cov=src --cov-fail-under=90

- name: Run Frontend Tests
  run: |
    cd frontend
    npm run test:coverage
    npm run test:e2e
```

**Quality Gates**:
- All tests must pass before merge
- Coverage must meet thresholds (90% unit, 70% integration)
- E2E tests must pass for all P1 flows

### Alternatives Considered

**Backend (unittest)**:
- **Pros**: Python standard library (no dependency)
- **Cons**:
  - Less feature-rich than pytest
  - Verbose test syntax
  - Weaker async support

**Frontend (Jest)**:
- **Pros**: Most popular React testing framework
- **Cons**:
  - Slower than Vitest
  - More configuration required

**Verdict**: pytest (backend) and Vitest (frontend) chosen for performance and TDD-friendly features.

---

## Technology Stack Summary

| Category | Technology | Version | Rationale |
|----------|-----------|---------|-----------|
| **Backend Framework** | FastAPI | 0.104+ | Async performance, OpenAPI integration, type safety |
| **Frontend Framework** | Next.js | 14+ (App Router) | SSR/SSG for SEO, image optimization, subdomain routing |
| **Language (Frontend)** | TypeScript | 5.3+ | Type safety, developer experience |
| **Language (Backend)** | Python | 3.11+ | Multi-tenant ecosystem, FastAPI compatibility |
| **Database** | PostgreSQL | 15+ | Row-level security for multi-tenancy |
| **ORM (Backend)** | SQLAlchemy | 2.0+ | PostgreSQL RLS support, migration tooling |
| **ORM (Frontend)** | Prisma | 5.0+ (optional) | Type-safe database access if frontend needs direct DB |
| **Authentication** | JWT | python-jose | Stateless, horizontal scaling, role scoping |
| **File Storage** | File System → S3 | - | Abstraction layer enables migration |
| **CDN** | Cloudflare | Free tier | Global edge network, DDoS protection |
| **Image Optimization** | Next.js Image | Built-in | Lazy loading, WebP/AVIF, responsive |
| **Testing (Backend)** | pytest | 7.4+ | TDD workflow, async support, coverage |
| **Testing (Frontend)** | Vitest + Playwright | Latest | Fast unit tests, cross-browser E2E |

---

## Constitutional Alignment Verification

✅ **TDD Requirement**: pytest (backend) and Vitest (frontend) support Red-Green-Refactor workflow
✅ **Component Architecture**: Next.js (frontend) and FastAPI service layer (backend) are component-based
✅ **Accessibility**: Next.js supports semantic HTML, ARIA labels, keyboard navigation
✅ **Performance**: <2s page load target achievable with Next.js SSR + Cloudflare CDN
✅ **Security**: JWT auth, PostgreSQL RLS, input sanitization all supported by chosen stack
✅ **Multi-Tenant**: PostgreSQL RLS is constitutional recommendation for school platforms

---

## Next Steps

1. Set up development environment (see [quickstart.md](./quickstart.md))
2. Initialize database schema (see [data-model.md](./data-model.md))
3. Generate API contracts (see [contracts/](./contracts/))
4. Begin implementation tasks (run `/sp.tasks` command)
