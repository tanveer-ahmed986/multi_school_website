# Implementation Plan: Multi-School Website Platform

**Branch**: `001-multi-school-platform` | **Date**: 2026-01-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-multi-school-platform/spec.md`

## Summary

A configuration-driven multi-tenant website platform serving multiple schools from a single codebase. Each school operates as an isolated tenant with subdomain-based routing (e.g., schoolA.domain.com), custom branding, and independent content management. The platform prioritizes rapid school onboarding (under 2 hours), strict data isolation through PostgreSQL row-level security, and role-based access control for Super Admin, School Admin, and Staff roles. Technical approach uses Next.js 14+ (frontend), FastAPI (backend), PostgreSQL 15+ with RLS for multi-tenancy, JWT authentication with refresh tokens, and file-based storage initially with S3 migration path.

## Technical Context

**Language/Version**: TypeScript 5.3+ (Frontend), Python 3.11+ (Backend)
**Primary Dependencies**: Next.js 14+, FastAPI 0.104+, PostgreSQL 15+, Prisma ORM, SQLAlchemy
**Storage**: PostgreSQL with row-level security (RLS) for multi-tenancy, File system initially (S3 migration path)
**Testing**: Vitest + Testing Library + Playwright (Frontend), pytest + pytest-asyncio (Backend)
**Target Platform**: Web (Linux server, Node.js 18+ runtime)
**Project Type**: Web application (separate backend and frontend)
**Performance Goals**: <2s page load (p95), 1000 concurrent users, <500ms API response (p95)
**Constraints**: <2 hour school onboarding, 100% data isolation validation, WCAG 2.1 AA compliance
**Scale/Scope**: Initial support for 10 schools, 10GB storage/school, target 50 schools

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

### Alignment with Constitution Principles

✅ **TDD Requirement (Core Principle I)**: All code must be developed with tests first (Red-Green-Refactor)
- Unit test coverage ≥90% for business logic (services, models, utilities)
- Integration test coverage ≥70% for critical user journeys (FR-001 to FR-051)
- E2E tests for all P1 user flows (public website visitor, admin content management, school onboarding)
- Test pyramid enforced: ~70% unit, ~20% integration, ~10% E2E

✅ **Component-Based Architecture (Core Principle II)**:
- Frontend: Reusable UI components (Header, Footer, Gallery, ResultsTable, NoticeBoard, etc.)
- Backend: Service layer with single responsibility (SchoolService, UserService, AuthService, ContentService, FileStorageService)
- Each component independently testable

✅ **Responsive & Accessible Design (Core Principle III)**:
- WCAG 2.1 Level AA compliance required (SC-011 from spec)
- Mobile-first responsive (320px to 4K) - SC-006
- Screen reader support, keyboard navigation, semantic HTML
- 4.5:1 contrast ratios minimum
- Touch targets ≥44px x 44px

✅ **Performance & Optimization (Core Principle IV)**:
- <2s page load target (SC-004) meets <3s constitution requirement
- CDN for static assets (FR-047)
- Per-school caching (FR-046)
- Image lazy loading and optimization (FR-015)
- Database query optimization with proper indexing

✅ **Security & Privacy (Core Principle V)**:
- HTTPS enforcement (FR-038)
- Input sanitization for XSS/SQL injection prevention (FR-039)
- CSRF protection on state-changing operations (FR-040)
- Rate limiting on public endpoints (FR-041)
- CAPTCHA on public forms (FR-042)
- Audit logging for all admin actions (FR-045, FR-050)
- JWT with refresh token rotation (FR-017)

✅ **Multi-Tenant Architecture (School Websites Section)**:
- PostgreSQL row-level security (RLS) for strict tenant isolation
- Tenant identification via subdomain (FR-001)
- Backend validation on every data access (FR-004)
- Session-based tenant context (`SET app.current_school_id`)
- Comprehensive tenant isolation security testing

✅ **Role-Based Access Control (School Websites Section)**:
- Super Admin: Platform-wide school management (FR-018)
- School Admin: Single school full access, cannot cross boundaries (FR-019, FR-020)
- Staff: Limited permissions - notices and gallery only (FR-021)
- Backend API-level enforcement (FR-022)
- Multi-school email scoping with role selector (FR-023)

✅ **Data Privacy & Compliance (School Websites Section)**:
- Student result data protected with audit logging (FR-026, FR-050)
- Comprehensive audit trail for all modifications (FR-050)
- Backup and recovery policies (FR-049, FR-051)

### Constitution Concerns & Justifications

⚠️ **File-Based Storage Initially** (Constitution recommends cloud storage)

**Justification**:
- Simplifies initial school onboarding to meet <2 hour target (SC-001)
- Reduces external dependencies and cloud account requirements for MVP
- Migration path to S3 documented in assumptions
- Abstraction layer (FileStorageService interface) designed to enable S3 migration without code changes

**Mitigation**:
- FileStorageService abstraction hides implementation details
- Cloud storage migration planned as future enhancement
- Storage limits enforced (10GB per school) to prevent scaling issues

## Project Structure

### Documentation (this feature)

```text
specs/001-multi-school-platform/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: Technology stack decisions
├── data-model.md        # Phase 1: Database schema & entities
├── quickstart.md        # Phase 1: Developer setup guide
├── contracts/           # Phase 1: API contracts
│   ├── auth.openapi.yaml
│   ├── schools.openapi.yaml
│   ├── content.openapi.yaml
│   └── public.openapi.yaml
└── tasks.md             # Phase 2: Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/              # SQLAlchemy models
│   │   ├── school.py        # School entity
│   │   ├── user.py          # User entity (Super Admin, School Admin, Staff)
│   │   ├── faculty.py       # Faculty member entity
│   │   ├── result.py        # Student result entity
│   │   ├── notice.py        # Notice/announcement entity
│   │   ├── gallery.py       # Gallery image entity
│   │   └── principal.py     # Principal profile entity
│   ├── services/            # Business logic layer
│   │   ├── school_service.py        # School CRUD, onboarding workflow
│   │   ├── auth_service.py          # JWT generation, refresh, validation
│   │   ├── content_service.py       # Faculty, results, notices, gallery, principal
│   │   ├── file_storage_service.py  # File upload/download abstraction (S3 migration path)
│   │   └── tenant_service.py        # Subdomain resolution, tenant context
│   ├── api/                 # FastAPI routes
│   │   ├── auth.py          # Login, refresh, logout, role selector
│   │   ├── schools.py       # School management (Super Admin only)
│   │   ├── content.py       # Content CRUD (School Admin, Staff)
│   │   └── public.py        # Public website data retrieval
│   ├── middleware/          # Request/response processing
│   │   ├── tenant_middleware.py     # Subdomain extraction, tenant context
│   │   ├── auth_middleware.py       # JWT validation, user injection
│   │   ├── csrf_middleware.py       # CSRF token validation
│   │   └── rate_limit_middleware.py # Rate limiting
│   ├── database/
│   │   ├── connection.py    # PostgreSQL connection pool
│   │   └── migrations/      # Alembic migrations
│   └── utils/
│       ├── validators.py    # Input validation (email, file types, etc.)
│       ├── jwt_utils.py     # JWT encoding/decoding
│       └── file_utils.py    # File size validation, sanitization
├── tests/
│   ├── unit/                # Unit tests for services, models, utils
│   │   ├── test_school_service.py
│   │   ├── test_auth_service.py
│   │   └── test_validators.py
│   ├── integration/         # API integration tests
│   │   ├── test_auth_api.py
│   │   ├── test_schools_api.py
│   │   ├── test_content_api.py
│   │   └── test_public_api.py
│   └── security/            # Tenant isolation & security tests
│       ├── test_tenant_isolation.py  # Verify school A cannot access school B data
│       └── test_authorization.py     # Role-based access enforcement
├── alembic/                 # Database migrations
├── requirements.txt
└── .env.example

frontend/
├── src/
│   ├── components/
│   │   ├── common/          # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Spinner.tsx
│   │   ├── layout/          # Layout components (tenant-aware)
│   │   │   ├── Header.tsx           # Dynamic logo, colors from config
│   │   │   ├── Footer.tsx
│   │   │   └── Navigation.tsx
│   │   ├── admin/           # Admin panel components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── ContentEditor.tsx
│   │   │   ├── FileUploader.tsx
│   │   │   ├── FacultyManager.tsx
│   │   │   ├── ResultUploader.tsx
│   │   │   ├── NoticeEditor.tsx
│   │   │   └── GalleryManager.tsx
│   │   └── public/          # Public website components
│   │       ├── Hero.tsx
│   │       ├── NoticeBoard.tsx
│   │       ├── GalleryGrid.tsx
│   │       ├── ResultsTable.tsx
│   │       └── FacultyCard.tsx
│   ├── app/                 # Next.js App Router pages
│   │   ├── (admin)/         # Admin panel routes
│   │   │   ├── login/
│   │   │   ├── dashboard/
│   │   │   └── [...features]/
│   │   └── (public)/        # Public website routes
│   │       ├── page.tsx     # Homepage
│   │       ├── faculty/
│   │       ├── results/
│   │       ├── gallery/
│   │       └── notices/
│   ├── services/            # API client services
│   │   ├── authService.ts          # Login, refresh, logout
│   │   ├── schoolService.ts        # School management (Super Admin)
│   │   ├── contentService.ts       # Content CRUD (School Admin/Staff)
│   │   └── publicService.ts        # Public website data
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.ts              # Authentication state
│   │   ├── useTenant.ts            # Current school context
│   │   └── useSchoolConfig.ts      # School branding/configuration
│   ├── styles/
│   │   ├── globals.css
│   │   └── tailwind.config.ts      # Tailwind with dynamic theming
│   ├── utils/
│   │   ├── validators.ts    # Client-side validation
│   │   └── formatters.ts    # Date, number formatting
│   └── types/               # TypeScript interfaces
│       ├── School.ts
│       ├── User.ts
│       ├── Faculty.ts
│       ├── Result.ts
│       ├── Notice.ts
│       ├── Gallery.ts
│       └── Principal.ts
├── tests/
│   ├── unit/                # Component unit tests
│   ├── integration/         # Page integration tests
│   └── e2e/                 # Playwright E2E tests
│       ├── public-visitor.spec.ts   # User Story 1
│       ├── school-admin.spec.ts     # User Story 2
│       └── super-admin.spec.ts      # User Story 3
├── public/
├── package.json
└── .env.example

data/                        # File-based data storage (deployment only, not in repo)
└── schools/
    └── {school_id}/
        ├── config/
        │   └── school.config.json
        ├── faculty/
        │   └── faculty.json
        ├── results/
        │   └── {year}/{class}.json
        ├── gallery/
        │   └── {category}/images/
        ├── notices/
        │   └── notices.json
        └── management/
            └── principal.json
```

**Structure Decision**: Web application structure selected because the platform requires:
1. **Separate backend** for multi-tenant data isolation enforcement, authentication, and business logic
2. **Separate frontend** for public website rendering (SSR/SSG for SEO) and admin panel (CSR for interactivity)
3. **Clear separation** enables independent scaling: frontend via CDN/edge, backend via horizontal scaling

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| File-based storage initially | Simplifies school onboarding (under 2 hours target - SC-001), reduces external dependencies for MVP, lowers infrastructure complexity | Cloud storage (S3) adds AWS account configuration complexity, increases onboarding time beyond 2-hour target, requires additional security configuration (IAM roles, bucket policies) |

---

## Implementation Workflow

### Phase 0: Research & Architecture
**Status**: Complete (see [research.md](./research.md))
- Technology stack decisions with rationale
- Multi-tenant architecture design
- Security and compliance review

### Phase 1: Design & Contracts
**Status**: Complete (this plan + supporting docs)
- Database schema design (see [data-model.md](./data-model.md))
- API contracts (see [contracts/](./contracts/))
- Developer environment setup (see [quickstart.md](./quickstart.md))

### Phase 2: Implementation Tasks
**Status**: Pending - run `/sp.tasks` command
- Generate dependency-ordered tasks from this plan
- Red-Green-Refactor cycles for each feature
- Tasks will cover User Stories 1-5 from specification

---

## Critical Success Factors

1. **Multi-Tenant Isolation**: PostgreSQL RLS policies must prevent cross-school data access (SC-005: 100% prevention)
2. **Onboarding Speed**: School onboarding workflow must complete in <2 hours (SC-001)
3. **Performance**: Page load <2s (SC-004), API response <500ms
4. **Security**: Zero critical/high vulnerabilities in security scans (SC-013)
5. **Test Coverage**: Unit ≥90%, Integration ≥70%, E2E for all P1 flows

---

## Next Steps

1. **Run `/sp.tasks`** to generate implementation tasks from this plan
2. **Set up development environment** following [quickstart.md](./quickstart.md)
3. **Begin Red-Green-Refactor cycles** starting with highest priority user stories (P1)
4. **Continuous validation** against constitution principles and success criteria
