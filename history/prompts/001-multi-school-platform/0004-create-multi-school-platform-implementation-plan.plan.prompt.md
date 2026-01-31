---
id: 0004
title: Create Multi-School Platform Implementation Plan
stage: plan
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-multi-school-platform
branch: 001-multi-school-platform
user: tanveer-ahmed986
command: /sp.plan make plan for execution
labels: ["planning", "architecture", "multi-tenant", "database-design", "api-design"]
links:
  spec: specs/001-multi-school-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-multi-school-platform/plan.md
  - specs/001-multi-school-platform/research.md
  - specs/001-multi-school-platform/data-model.md
  - specs/001-multi-school-platform/quickstart.md
  - specs/001-multi-school-platform/contracts/auth.openapi.yaml
  - specs/001-multi-school-platform/contracts/schools.openapi.yaml
  - specs/001-multi-school-platform/contracts/content.openapi.yaml
  - specs/001-multi-school-platform/contracts/public.openapi.yaml
tests:
  - null
---

## Prompt

User invoked `/sp.plan make plan for execution` to create a comprehensive implementation plan for the multi-school website platform based on the clarified specification.

User context: "make plan for execution"

## Response snapshot

Created complete Phase 0 (Research) and Phase 1 (Design & Contracts) planning artifacts following the spec-driven development workflow.

**Planning Artifacts Created**:

1. **plan.md** - Main implementation plan:
   - Summary: Multi-tenant platform with subdomain-based routing, JWT auth, PostgreSQL RLS
   - Technical Context: FastAPI (backend), Next.js (frontend), PostgreSQL 15+, TypeScript/Python
   - Constitution Check: Validated against all core principles (TDD, component architecture, accessibility, security, multi-tenancy, RBAC)
   - Project Structure: Web application with separate backend/frontend
   - Complexity Tracking: Justified file-based storage (vs S3) for <2 hour onboarding target
   - Critical Success Factors: 100% tenant isolation, <2s page load, ≥90% test coverage

2. **research.md** - Technology stack research (Phase 0):
   - Backend: FastAPI chosen over Django/NestJS (async performance, OpenAPI, multi-tenant ecosystem)
   - Frontend: Next.js chosen over Vue/Astro (SEO, image optimization, admin components)
   - Database: PostgreSQL with RLS chosen (constitutional requirement, superior multi-tenant isolation)
   - Auth: JWT with refresh rotation chosen (stateless scaling, role scoping)
   - Storage: File system initially with S3 abstraction layer (onboarding speed, migration path)
   - CDN: Next.js Image + Cloudflare (zero-config optimization, free tier)
   - Testing: pytest (backend), Vitest + Playwright (frontend) for TDD compliance
   - All decisions include rationale and rejected alternatives

3. **data-model.md** - Database schema (Phase 1):
   - 7 core entities: School, User, Faculty, Result, Notice, GalleryImage, PrincipalProfile
   - 2 supporting tables: AuditLog (compliance), RefreshTokens (JWT management)
   - Complete schema with PostgreSQL types, constraints, validation rules
   - Row-Level Security (RLS) policies for all tenant-specific tables
   - Multi-tenant isolation strategy: session variable (`app.current_school_id`)
   - Performance indexes: foreign keys, composite indexes, partial indexes
   - Alembic migration structure
   - Security test examples for tenant isolation verification

4. **contracts/** - OpenAPI 3.0.3 API specifications (Phase 1):
   - **auth.openapi.yaml**: Login, refresh, logout, profile, school selector (7 endpoints)
   - **schools.openapi.yaml**: School CRUD, statistics, admin management (Super Admin only, 8 endpoints)
   - **content.openapi.yaml**: Faculty, results, notices, gallery, principal, branding (School Admin/Staff, 18 endpoints)
   - **public.openapi.yaml**: Public website data retrieval by subdomain (6 endpoints)
   - All endpoints include: request/response schemas, status codes, authentication requirements, examples

5. **quickstart.md** - Developer setup guide (Phase 1):
   - Prerequisites (Python 3.11+, Node.js 18+, PostgreSQL 15+)
   - Database setup (local and Docker options)
   - Backend setup (FastAPI, virtual environment, Alembic migrations, seed data)
   - Frontend setup (Next.js, subdomain routing configuration)
   - Test school onboarding walkthrough (API commands with curl examples)
   - Running tests (pytest coverage ≥90%, Vitest, Playwright E2E)
   - TDD Red-Green-Refactor workflow
   - Common development tasks (migrations, endpoints, debugging)
   - Comprehensive troubleshooting section

**Architecture Highlights**:

**Multi-Tenant Isolation**:
- PostgreSQL Row-Level Security (RLS) enforces tenant boundaries at database level
- Session variable approach: `SET app.current_school_id = '{uuid}'` per request
- Middleware extracts subdomain → resolves school_id → sets session context
- All queries automatically filtered by RLS policies
- Security tests verify 100% isolation (School A cannot access School B data)

**Authentication & Authorization**:
- JWT with refresh token rotation (15-min access, 7-day refresh)
- Token claims include: user_id, email, role, school_id
- HTTP-only cookies for refresh tokens (XSS protection)
- Token revocation on logout via database table
- Multi-school role scoping: users select school context after login (FR-023)

**Technology Stack Rationale**:
- **FastAPI**: Async performance (<500ms API p95), native OpenAPI, strong typing with Pydantic
- **Next.js 14+**: SSR/SSG for SEO, built-in image optimization, subdomain middleware
- **PostgreSQL 15+ with RLS**: Constitutional requirement, native multi-tenant isolation
- **File system → S3**: Abstraction layer enables migration without code changes

**Constitutional Alignment**:
- ✅ TDD: pytest (backend), Vitest (frontend) support Red-Green-Refactor
- ✅ Component Architecture: Next.js components, FastAPI service layer
- ✅ Accessibility: WCAG 2.1 AA (SC-011), semantic HTML, keyboard nav
- ✅ Performance: <2s page load, CDN, caching, lazy loading
- ✅ Security: HTTPS, input sanitization, CSRF, rate limiting, audit logs
- ✅ Multi-Tenant: PostgreSQL RLS is constitutional standard for school platforms
- ⚠️ File storage initially (justified: <2 hour onboarding target, S3 migration path documented)

**Project Structure**:
- Backend: `backend/src/{models, services, api, middleware, database, utils}`
- Frontend: `frontend/src/{components, app, services, hooks, types}`
- Tests: Unit (≥90%), integration (≥70%), E2E (100% P1 flows)
- Data: `data/schools/{school_id}/{config, faculty, results, gallery, notices, management}`

**API Contracts**:
- 39 total endpoints across 4 OpenAPI specs
- Authentication: 7 endpoints (login, refresh, logout, profile, school selector)
- School management: 8 endpoints (Super Admin only)
- Content management: 18 endpoints (School Admin/Staff with role-based access)
- Public website: 6 endpoints (subdomain-based data retrieval)

## Outcome

- ✅ Impact: Complete Phase 0 (Research) and Phase 1 (Design & Contracts) artifacts created. All technology stack decisions documented with rationale. Database schema defines 7 entities with RLS policies. API contracts specify 39 endpoints. Developer setup guide enables immediate environment setup. Ready for Phase 2 (/sp.tasks).
- 🧪 Tests: No tests at planning stage. Test strategy defined: ≥90% unit, ≥70% integration, 100% E2E for P1 flows. Security tests for tenant isolation. TDD workflow (Red-Green-Refactor) documented in quickstart.md.
- 📁 Files: Created 8 planning artifacts (plan.md, research.md, data-model.md, quickstart.md, 4 OpenAPI contracts)
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks from plan. Then begin TDD implementation starting with P1 user stories.
- 🧠 Reflection: Plan successfully balances MVP simplicity (file storage) with production scalability (S3 migration path, PostgreSQL RLS, horizontal scaling). Multi-tenant architecture thoroughly researched and designed. Constitutional compliance verified for all principles. File storage initially justified in Complexity Tracking. Technology choices optimize for spec requirements (FastAPI async for performance, Next.js for SEO, PostgreSQL RLS for security).

## Evaluation notes (flywheel)

- Failure modes observed: Initial planning agent encountered read-only mode limitation. Recovered by creating files directly using Write tool. All 8 artifacts successfully created.
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all core principles met, 1 justified complexity). Technology decisions - PASS (all choices have documented rationale and rejected alternatives). Multi-tenant isolation - PASS (RLS policies defined, security tests specified).
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 (research) and Phase 1 (design/contracts) completion
- Next experiment (smallest change to try): Validate in /sp.tasks whether generated tasks align with TDD workflow and test pyramid requirements. Consider if contract-first approach reduces implementation ambiguity.
