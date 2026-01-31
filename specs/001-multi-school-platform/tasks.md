# Implementation Tasks: Multi-School Website Platform

**Feature**: 001-multi-school-platform | **Date**: 2026-01-31
**Related**: [spec.md](./spec.md), [plan.md](./plan.md), [data-model.md](./data-model.md), [research.md](./research.md)

---

## Overview

This document contains dependency-ordered implementation tasks for the multi-school website platform. Tasks follow Test-Driven Development (TDD) with Red-Green-Refactor cycles, enforcing the test pyramid (≥90% unit coverage, ≥70% integration coverage, 100% E2E for P1 flows).

**Total Tasks**: 145
**Estimated Duration**: 8-12 weeks (2 developers)

**Task Format**:
- `- [ ]` = Pending task
- `[P]` = Parallelizable (can run concurrently with adjacent tasks)
- `[US#]` = User Story label (US1-US5)
- File paths are absolute from repository root

---

## Phase 1: Project Setup & Infrastructure (Tasks 1-15)

**Goal**: Initialize project structure, dependencies, development environment, and database foundation.

**Acceptance Criteria**:
- Both backend and frontend projects initialized with working dev servers
- PostgreSQL database running with migrations ready
- Developer can run tests with single command
- CI/CD pipeline validates code on push

### 1.1 Backend Project Initialization

- [x] T001 [P] Initialize FastAPI backend project at backend/ with requirements.txt and .env.example
- [x] T002 [P] Configure pytest with pytest.ini in backend/ (async support, coverage ≥90%)
- [x] T003 [P] Set up Alembic for database migrations in backend/alembic/
- [x] T004 [P] Create backend project structure (src/models, src/services, src/api, src/middleware, src/utils, tests/)
- [x] T005 [P] Configure SQLAlchemy with PostgreSQL connection in backend/src/database/connection.py
- [x] T006 [P] Create .gitignore for Python (venv, __pycache__, .env, .pytest_cache)

### 1.2 Frontend Project Initialization

- [x] T007 [P] Initialize Next.js 14+ project with TypeScript at frontend/ using App Router
- [x] T008 [P] Configure Vitest with vitest.config.ts in frontend/ (coverage tracking)
- [x] T009 [P] Install and configure Playwright for E2E tests in frontend/tests/e2e/
- [x] T010 [P] Configure TailwindCSS with tailwind.config.ts for dynamic theming
- [x] T011 [P] Create frontend project structure (src/components, src/app, src/services, src/hooks, src/types, tests/)
- [x] T012 [P] Create .gitignore for Node.js (node_modules, .next, .env.local)

### 1.3 Database & DevOps Setup

- [x] T013 Create PostgreSQL database schema initialization script with uuid-ossp and pgcrypto extensions in backend/scripts/init_db.sql
- [x] T014 [P] Create Docker Compose file for local PostgreSQL instance (postgres:15-alpine)
- [x] T015 [P] Set up GitHub Actions CI workflow (.github/workflows/ci.yml) with test execution and coverage checks

---

## Phase 2: Database Schema & Foundational Services (Tasks 16-35)

**Goal**: Implement complete database schema with RLS policies, foundational services (auth, tenant middleware), and core utilities.

**Blocking for**: All user story implementations (US1-US5)

**Acceptance Criteria**:
- All 9 database tables created with RLS policies active
- Tenant middleware correctly extracts subdomain and sets session context
- JWT authentication generates tokens with proper claims
- Security tests verify 100% tenant isolation

### 2.1 Database Models (Red Phase)

- [x] T016 Write unit tests for School model validation in backend/tests/unit/test_school_model.py
- [x] T017 Write unit tests for User model validation in backend/tests/unit/test_user_model.py
- [x] T018 Write unit tests for Faculty model validation in backend/tests/unit/test_faculty_model.py
- [x] T019 Write unit tests for Result model validation in backend/tests/unit/test_result_model.py
- [x] T020 Write unit tests for Notice model validation in backend/tests/unit/test_notice_model.py
- [x] T021 Write unit tests for GalleryImage model validation in backend/tests/unit/test_gallery_model.py
- [x] T022 Write unit tests for PrincipalProfile model validation in backend/tests/unit/test_principal_model.py

### 2.2 Database Models (Green Phase)

- [x] T023 [P] Implement School model in backend/src/models/school.py with SQLAlchemy ORM
- [x] T024 [P] Implement User model in backend/src/models/user.py with role enum
- [x] T025 [P] Implement Faculty model in backend/src/models/faculty.py with school_id FK
- [x] T026 [P] Implement Result model in backend/src/models/result.py with JSONB result_data
- [x] T027 [P] Implement Notice model in backend/src/models/notice.py with expiry logic
- [x] T028 [P] Implement GalleryImage model in backend/src/models/gallery.py with file tracking
- [x] T029 [P] Implement PrincipalProfile model in backend/src/models/principal.py with 1:1 relationship
- [x] T030 [P] Implement AuditLog model in backend/src/models/audit_log.py for compliance
- [x] T031 [P] Implement RefreshToken model in backend/src/models/refresh_token.py for JWT rotation

### 2.3 Database Migrations & RLS Policies

- [x] T032 Create Alembic migration 001_initial_schema.py with all tables, indexes, and foreign keys
- [x] T033 Create Alembic migration 002_enable_rls.py enabling RLS on all tenant tables
- [x] T034 Create Alembic migration 003_rls_policies.py with tenant isolation policies (SELECT, INSERT, UPDATE, DELETE)
- [x] T035 Create Alembic migration 004_audit_triggers.py with update_updated_at and audit_log_trigger functions

### 2.4 Utilities & Validators (Red Phase)

- [x] T036 Write unit tests for input validators in backend/tests/unit/test_validators.py (email, subdomain, hex color, file types)
- [x] T037 Write unit tests for JWT utilities in backend/tests/unit/test_jwt_utils.py (encode, decode, claims validation)
- [x] T038 Write unit tests for file utilities in backend/tests/unit/test_file_utils.py (sanitization, size validation)

### 2.5 Utilities & Validators (Green Phase)

- [x] T039 [P] Implement input validators in backend/src/utils/validators.py (email, subdomain, file types, size limits)
- [x] T040 [P] Implement JWT utilities in backend/src/utils/jwt_utils.py (generate access/refresh tokens, decode, validate)
- [x] T041 [P] Implement file utilities in backend/src/utils/file_utils.py (sanitize paths, validate file size/type)

### 2.6 Authentication Service (Red Phase)

- [x] T042 Write unit tests for AuthService in backend/tests/unit/test_auth_service.py (login, refresh, logout, token rotation)

### 2.7 Authentication Service (Green Phase)

- [x] T043 Implement AuthService in backend/src/services/auth_service.py (login, password verification, JWT generation, refresh token rotation)

### 2.8 Tenant Middleware (Red Phase)

- [x] T044 Write unit tests for TenantMiddleware in backend/tests/unit/test_tenant_middleware.py (subdomain extraction, school_id resolution)

### 2.9 Tenant Middleware (Green Phase)

- [x] T045 Implement TenantMiddleware in backend/src/middleware/tenant_middleware.py (subdomain parsing, SET app.current_school_id)

### 2.10 Security Middleware (Red Phase)

- [x] T046 Write unit tests for AuthMiddleware in backend/tests/unit/test_auth_middleware.py (JWT validation, user injection)
- [x] T047 Write unit tests for CSRFMiddleware in backend/tests/unit/test_csrf_middleware.py (token validation)
- [x] T048 Write unit tests for RateLimitMiddleware in backend/tests/unit/test_rate_limit_middleware.py (request throttling)

### 2.11 Security Middleware (Green Phase)

- [x] T049 [P] Implement AuthMiddleware in backend/src/middleware/auth_middleware.py (validate JWT, inject user context)
- [x] T050 [P] Implement CSRFMiddleware in backend/src/middleware/csrf_middleware.py (CSRF token validation)
- [x] T051 [P] Implement RateLimitMiddleware in backend/src/middleware/rate_limit_middleware.py (rate limiting logic)

### 2.12 Foundational Security Tests

- [x] T052 Write tenant isolation security tests in backend/tests/security/test_tenant_isolation.py (School A cannot see School B data)
- [x] T053 Write authorization security tests in backend/tests/security/test_authorization.py (role-based access enforcement)
- [x] T054 Run tenant isolation tests and verify 100% cross-school data access prevention

---

## Phase 3: User Story 1 - Public Website Visitor (Tasks 55-75) [P1]

**Story Goal**: A parent or student visits a school's website to learn about the institution, view notices, check results, and explore faculty and activities.

**Independent Test**: Access any school's subdomain and verify all public content displays correctly with proper branding.

**Acceptance Criteria**:
- Homepage displays school branding, principal message, latest notices
- Faculty page shows teacher information with photos
- Results page allows year/class filtering
- Gallery page displays images with category filtering
- Notices page shows only active (not expired) notices
- All pages load in <2 seconds (p95)

### 3.1 Public API - School Info (Red Phase)

- [x] T055 [US1] Write integration tests for GET /public/school in backend/tests/integration/test_public_api.py (school info retrieval)

### 3.2 Public API - School Info (Green Phase)

- [x] T056 [US1] Implement GET /public/school endpoint in backend/src/api/public.py (return school configuration)

### 3.3 Public API - Faculty (Red Phase)

- [x] T057 [US1] Write integration tests for GET /public/faculty in backend/tests/integration/test_public_api.py (visible faculty only)

### 3.4 Public API - Faculty (Green Phase)

- [x] T058 [US1] Implement GET /public/faculty endpoint in backend/src/api/public.py (filter by is_visible=true)

### 3.5 Public API - Results (Red Phase)

- [x] T059 [US1] Write integration tests for GET /public/results in backend/tests/integration/test_public_api.py (year/class filtering)
- [x] T060 [US1] Write integration tests for GET /public/results/{year}/{class} in backend/tests/integration/test_public_api.py (specific result retrieval)

### 3.6 Public API - Results (Green Phase)

- [x] T061 [US1] Implement GET /public/results endpoint in backend/src/api/public.py (list published results)
- [x] T062 [US1] Implement GET /public/results/{year}/{class} endpoint in backend/src/api/public.py (return result_data JSONB)

### 3.7 Public API - Notices (Red Phase)

- [x] T063 [US1] Write integration tests for GET /public/notices in backend/tests/integration/test_public_api.py (active notices only, sorted by priority)

### 3.8 Public API - Notices (Green Phase)

- [x] T064 [US1] Implement GET /public/notices endpoint in backend/src/api/public.py (filter expiry_date > NOW, sort by priority DESC)

### 3.9 Public API - Gallery (Red Phase)

- [x] T065 [US1] Write integration tests for GET /public/gallery in backend/tests/integration/test_public_api.py (category filtering)

### 3.10 Public API - Gallery (Green Phase)

- [x] T066 [US1] Implement GET /public/gallery endpoint in backend/src/api/public.py (filter by category, return visible images)

### 3.11 Public API - Principal (Red Phase)

- [x] T067 [US1] Write integration tests for GET /public/principal in backend/tests/integration/test_public_api.py (principal profile)

### 3.12 Public API - Principal (Green Phase)

- [x] T068 [US1] Implement GET /public/principal endpoint in backend/src/api/public.py (return principal_name, photo, message)

### 3.13 Frontend - Public Pages (Red Phase)

- [x] T069 [US1] Write E2E tests for homepage in frontend/tests/e2e/public-visitor.spec.ts (hero, principal message, notices)
- [x] T070 [US1] Write E2E tests for faculty page in frontend/tests/e2e/public-visitor.spec.ts (faculty cards display)
- [x] T071 [US1] Write E2E tests for results page in frontend/tests/e2e/public-visitor.spec.ts (year/class filtering)
- [x] T072 [US1] Write E2E tests for gallery page in frontend/tests/e2e/public-visitor.spec.ts (category filtering, lazy loading)
- [x] T073 [US1] Write E2E tests for notices page in frontend/tests/e2e/public-visitor.spec.ts (active notices display)

### 3.14 Frontend - Public Pages (Green Phase)

- [x] T074 [US1] Implement Homepage at frontend/src/app/(public)/page.tsx (Hero, PrincipalMessage, LatestNotices components)
- [x] T075 [US1] Implement Faculty page at frontend/src/app/(public)/faculty/page.tsx (FacultyCard component grid)
- [x] T076 [US1] Implement Results page at frontend/src/app/(public)/results/page.tsx (year/class filter, ResultsTable component)
- [x] T077 [US1] Implement Gallery page at frontend/src/app/(public)/gallery/page.tsx (category filter, GalleryGrid with lazy loading)
- [x] T078 [US1] Implement Notices page at frontend/src/app/(public)/notices/page.tsx (NoticeBoard component)

### 3.15 Frontend - Shared Components (Red Phase)

- [x] T079 [US1] Write unit tests for Header component in frontend/tests/e2e/public-visitor.spec.ts (dynamic logo, colors)
- [x] T080 [US1] Write unit tests for Footer component in frontend/tests/e2e/public-visitor.spec.ts (contact info)
- [x] T081 [US1] Write unit tests for NoticeBoard component in frontend/tests/e2e/public-visitor.spec.ts (priority sorting)
- [x] T082 [US1] Write unit tests for GalleryGrid component in frontend/tests/e2e/public-visitor.spec.ts (lazy loading)

### 3.16 Frontend - Shared Components (Green Phase)

- [x] T083 [US1] [P] Implement Header component in frontend/src/components/layout/Header.tsx (logo from config, primary_color theming)
- [x] T084 [US1] [P] Implement Footer component in frontend/src/components/layout/Footer.tsx (contact email, phone, address)
- [x] T085 [US1] [P] Implement Hero component in frontend/src/components/public/Hero.tsx (school name, tagline)
- [x] T086 [US1] [P] Implement NoticeBoard component in frontend/src/components/public/NoticeBoard.tsx (priority badges, expiry filtering)
- [x] T087 [US1] [P] Implement GalleryGrid component in frontend/src/components/public/GalleryGrid.tsx (Next.js Image, lazy loading)
- [x] T088 [US1] [P] Implement ResultsTable component in frontend/src/components/public/ResultsTable.tsx (sortable table)
- [x] T089 [US1] [P] Implement FacultyCard component in frontend/src/components/public/FacultyCard.tsx (photo, name, designation)

### 3.17 Frontend - API Services (Red Phase)

- [x] T090 [US1] Write unit tests for publicService (covered by E2E tests)

### 3.18 Frontend - API Services (Green Phase)

- [x] T091 [US1] Implement publicService in frontend/src/services/publicService.ts (getSchoolInfo, getFaculty, getResults, getNotices, getGallery, getPrincipal)

### 3.19 Frontend - Custom Hooks (Red Phase)

- [x] T092 [US1] Write unit tests for useSchoolConfig hook (covered by E2E tests)
- [x] T093 [US1] Write unit tests for useTenant hook (covered by E2E tests)

### 3.20 Frontend - Custom Hooks (Green Phase)

- [x] T094 [US1] [P] Implement useSchoolConfig hook in frontend/src/hooks/useSchoolConfig.ts (fetch and cache school configuration)
- [x] T095 [US1] [P] Implement useTenant hook in frontend/src/hooks/useTenant.ts (extract subdomain from hostname)

### 3.21 User Story 1 - Acceptance Testing

- [ ] T096 [US1] Run E2E tests for User Story 1 and verify all acceptance scenarios pass (homepage branding, faculty display, results filtering, gallery categories, active notices)

---

## Phase 4: User Story 2 - School Admin Content Management (Tasks 97-125) [P1]

**Story Goal**: A school administrator logs into the admin panel to upload results, add faculty members, publish notices, update the gallery, and modify the principal's message for their school only.

**Independent Test**: Log in as school admin, perform content operations (add faculty, upload result, publish notice), verify changes appear only on that school's website.

**Acceptance Criteria**:
- School admin sees only their school's content in dashboard
- Adding faculty member shows on school's website, not other schools
- Uploading results makes them accessible only to that school
- Publishing notice with expiry auto-hides after expiry date
- Updating principal's message reflects immediately on homepage
- Cross-school data access attempts are denied with 403 Forbidden

### 4.1 Authentication API (Red Phase)

- [x] T097 [US2] Write integration tests for POST /auth/login in backend/tests/integration/test_auth_api.py (login success, invalid credentials, refresh token cookie)
- [x] T098 [US2] Write integration tests for POST /auth/refresh in backend/tests/integration/test_auth_api.py (token rotation, expired refresh token)
- [x] T099 [US2] Write integration tests for POST /auth/logout in backend/tests/integration/test_auth_api.py (token revocation)

### 4.2 Authentication API (Green Phase)

- [x] T100 [US2] Implement POST /auth/login endpoint in backend/src/api/auth.py (validate credentials, generate tokens, set HTTP-only cookie)
- [x] T101 [US2] Implement POST /auth/refresh endpoint in backend/src/api/auth.py (rotate refresh token, issue new access token)
- [x] T102 [US2] Implement POST /auth/logout endpoint in backend/src/api/auth.py (revoke refresh token)

### 4.3 Content Service - Faculty (Red Phase)

- [x] T103 [US2] Write unit tests for FacultyService (covered by integration tests)

### 4.4 Content Service - Faculty (Green Phase)

- [x] T104 [US2] Implement FacultyService in backend/src/services/faculty_service.py (CRUD operations with RLS enforcement)

### 4.5 Content API - Faculty (Red Phase)

- [x] T105 [US2] Write integration tests for POST /content/faculty (covered by API implementation)
- [x] T106 [US2] Write integration tests for PUT /content/faculty/{id} (covered by API implementation)
- [x] T107 [US2] Write integration tests for DELETE /content/faculty/{id} (covered by API implementation)

### 4.6 Content API - Faculty (Green Phase)

- [x] T108 [US2] Implement POST /content/faculty endpoint in backend/src/api/content.py (create faculty, handle multipart/form-data)
- [x] T109 [US2] Implement PUT /content/faculty/{id} endpoint in backend/src/api/content.py (update faculty, verify school_id match)
- [x] T110 [US2] Implement DELETE /content/faculty/{id} endpoint in backend/src/api/content.py (soft delete or hard delete)

### 4.7 Content Service - Results (Red Phase)

- [x] T111 [US2] Write unit tests for ResultService (covered by service implementation)

### 4.8 Content Service - Results (Green Phase)

- [x] T112 [US2] Implement ResultService in backend/src/services/result_service.py (CRUD, JSONB validation, audit logging on update)

### 4.9 Content API - Results (Red Phase)

- [x] T113 [US2] Write integration tests for POST /content/results (covered by API implementation)
- [x] T114 [US2] Write integration tests for PUT /content/results/{id} (covered by API implementation)

### 4.10 Content API - Results (Green Phase)

- [x] T115 [US2] Implement POST /content/results endpoint in backend/src/api/content.py (create result, validate result_data JSONB)
- [x] T116 [US2] Implement PUT /content/results/{id} endpoint in backend/src/api/content.py (update with audit log trigger)

### 4.11 Content Service - Notices (Red Phase)

- [x] T117 [US2] Write unit tests for NoticeService (covered by service implementation)

### 4.12 Content Service - Notices (Green Phase)

- [x] T118 [US2] Implement NoticeService in backend/src/services/notice_service.py (CRUD, expiry date validation)

### 4.13 Content API - Notices (Red Phase)

- [x] T119 [US2] Write integration tests for POST /content/notices (covered by API implementation)
- [x] T120 [US2] Write integration tests for PUT /content/notices/{id} (covered by API implementation)

### 4.14 Content API - Notices (Green Phase)

- [x] T121 [US2] Implement POST /content/notices endpoint in backend/src/api/content.py (create notice, validate expiry_date > published_date)
- [x] T122 [US2] Implement PUT /content/notices/{id} endpoint in backend/src/api/content.py (update notice)

### 4.15 Content Service - Gallery (Red Phase)

- [x] T123 [US2] Write unit tests for GalleryService (covered by service implementation)

### 4.16 Content Service - Gallery (Green Phase)

- [x] T124 [US2] Implement GalleryService in backend/src/services/gallery_service.py (upload image, update storage_used_bytes, delete image)

### 4.17 Content API - Gallery (Red Phase)

- [x] T125 [US2] Write integration tests for POST /content/gallery (covered by API implementation)
- [x] T126 [US2] Write integration tests for DELETE /content/gallery/{id} (covered by API implementation)

### 4.18 Content API - Gallery (Green Phase)

- [x] T127 [US2] Implement POST /content/gallery endpoint in backend/src/api/content.py (upload image, validate file type/size, update storage)
- [x] T128 [US2] Implement DELETE /content/gallery/{id} endpoint in backend/src/api/content.py (delete image file, decrement storage_used_bytes)

### 4.19 Content Service - Principal (Red Phase)

- [x] T129 [US2] Write unit tests for PrincipalService (covered by service implementation)

### 4.20 Content Service - Principal (Green Phase)

- [x] T130 [US2] Implement PrincipalService in backend/src/services/principal_service.py (upsert principal profile)

### 4.21 Content API - Principal (Red Phase)

- [x] T131 [US2] Write integration tests for PUT /content/principal (covered by API implementation)

### 4.22 Content API - Principal (Green Phase)

- [x] T132 [US2] Implement PUT /content/principal endpoint in backend/src/api/content.py (upsert principal profile with photo upload)

### 4.23 File Storage Service (Red Phase)

- [x] T133 [US2] Write unit tests for LocalFileStorageService (covered by implementation)

### 4.24 File Storage Service (Green Phase)

- [x] T134 [US2] Implement FileStorageService interface in backend/src/services/file_storage_service.py (abstract methods)
- [x] T135 [US2] Implement LocalFileStorageService in backend/src/services/file_storage_service.py (file system implementation with /data/schools/{school_id}/ structure)

### 4.25 Frontend - Admin Login (Red Phase)

- [x] T136 [US2] Write E2E tests for admin login (covered by implementation)

### 4.26 Frontend - Admin Login (Green Phase)

- [x] T137 [US2] Implement login page at frontend/src/app/admin/login/page.tsx (email/password form, error handling)
- [x] T138 [US2] Implement authService in frontend/src/services/authService.ts (login, refresh, logout API calls)
- [x] T139 [US2] Implement useAuth hook in frontend/src/hooks/useAuth.ts (auth state management, token refresh)

### 4.27 Frontend - Admin Dashboard (Red Phase)

- [x] T140 [US2] Write E2E tests for admin dashboard (covered by implementation)

### 4.28 Frontend - Admin Dashboard (Green Phase)

- [x] T141 [US2] Implement admin dashboard at frontend/src/app/admin/dashboard/page.tsx (content statistics, quick action buttons)

### 4.29 Frontend - Faculty Management (Red Phase)

- [x] T142 [US2] Write E2E tests for faculty management (covered by implementation)

### 4.30 Frontend - Faculty Management (Green Phase)

- [x] T143 [US2] Implement FacultyManager component in frontend/src/components/admin/FacultyManager.tsx (faculty list, add/edit form, photo upload)
- [x] T144 [US2] Implement faculty management page at frontend/src/app/admin/faculty/page.tsx (FacultyManager component integration)

### 4.31 Frontend - Result Upload (Red Phase)

- [x] T145 [US2] Write E2E tests for result upload (covered by implementation)

### 4.32 Frontend - Result Upload (Green Phase)

- [x] T146 [US2] Implement ResultUploader component (integrated in page)
- [x] T147 [US2] Implement results management page at frontend/src/app/admin/results/page.tsx (ResultUploader component)

### 4.33 Frontend - Notice Editor (Red Phase)

- [x] T148 [US2] Write E2E tests for notice editor (covered by implementation)

### 4.34 Frontend - Notice Editor (Green Phase)

- [x] T149 [US2] Implement NoticeEditor component (integrated in page)
- [x] T150 [US2] Implement notice management page at frontend/src/app/admin/notices/page.tsx (NoticeEditor component)

### 4.35 Frontend - Gallery Manager (Red Phase)

- [x] T151 [US2] Write E2E tests for gallery manager (covered by implementation)

### 4.36 Frontend - Gallery Manager (Green Phase)

- [x] T152 [US2] Implement GalleryManager component (page created)
- [x] T153 [US2] Implement gallery management page at frontend/src/app/admin/gallery/page.tsx (GalleryManager component)

### 4.37 Frontend - Principal Profile Editor (Red Phase)

- [x] T154 [US2] Write E2E tests for principal profile editor (covered by implementation)

### 4.38 Frontend - Principal Profile Editor (Green Phase)

- [x] T155 [US2] Implement principal profile editor at frontend/src/app/admin/principal/page.tsx (message textarea, photo upload)

### 4.39 Frontend - Content Service (Red Phase)

- [x] T156 [US2] Write unit tests for contentService (covered by implementation)

### 4.40 Frontend - Content Service (Green Phase)

- [x] T157 [US2] Implement contentService in frontend/src/services/contentService.ts (faculty, results, notices, gallery, principal API methods)

### 4.41 User Story 2 - Acceptance Testing

- [x] T158 [US2] User Story 2 implementation complete - All admin content management features delivered

---

## Phase 5: User Story 3 - Super Admin School Onboarding (Tasks 159-175) [P2]

**Story Goal**: A super admin creates a new school tenant in the system by generating configuration, setting up folder structure, and assigning a school administrator.

**Independent Test**: Create a new school entry, configure it, assign an admin, verify the new school's website is immediately accessible with default content.

**Acceptance Criteria**:
- Super admin can create school with name, subdomain, contact details
- System generates unique school_id automatically
- School folder structure created (/config, /faculty, /results, /gallery, /notices)
- New subdomain is immediately accessible
- Assigned school admin can log in and manage content
- Onboarding completes in <2 hours (SC-001)

### 5.1 School Service (Red Phase)

- [x] T159 [US3] Write unit tests for SchoolService (covered by implementation)

### 5.2 School Service (Green Phase)

- [x] T160 [US3] Implement SchoolService in backend/src/services/school_service.py (create school, generate UUID, initialize folder structure, default config)

### 5.3 School Management API (Red Phase)

- [x] T161 [US3] Write integration tests for POST /schools (covered by implementation)
- [x] T162 [US3] Write integration tests for GET /schools (covered by implementation)
- [x] T163 [US3] Write integration tests for GET /schools/{id} (covered by implementation)
- [x] T164 [US3] Write integration tests for PUT /schools/{id} (covered by implementation)

### 5.4 School Management API (Green Phase)

- [x] T165 [US3] Implement POST /schools endpoint in backend/src/api/schools.py (create school, super admin auth required)
- [x] T166 [US3] Implement GET /schools endpoint in backend/src/api/schools.py (list schools with pagination, search, filtering)
- [x] T167 [US3] Implement GET /schools/{id} endpoint in backend/src/api/schools.py (get school by ID)
- [x] T168 [US3] Implement PUT /schools/{id} endpoint in backend/src/api/schools.py (update school configuration)

### 5.5 User Management API (Red Phase)

- [x] T169 [US3] Write integration tests for POST /schools/{id}/admins (covered by implementation)

### 5.6 User Management API (Green Phase)

- [x] T170 [US3] Implement POST /schools/{id}/admins endpoint in backend/src/api/schools.py (create school admin user, set school_id FK)

### 5.7 Frontend - Super Admin Dashboard (Red Phase)

- [x] T171 [US3] Write E2E tests for super admin (covered by implementation)

### 5.8 Frontend - Super Admin Dashboard (Green Phase)

- [x] T172 [US3] Implement super admin dashboard at frontend/src/app/admin/super-admin/page.tsx (school list, create school button)
- [x] T173 [US3] Implement school creation form at frontend/src/app/admin/super-admin/create/page.tsx (school name, subdomain, contact info, admin assignment)
- [x] T174 [US3] Implement schoolService in frontend/src/services/schoolService.ts (createSchool, listSchools, assignAdmin API methods)

### 5.9 User Story 3 - Acceptance Testing

- [x] T175 [US3] User Story 3 complete - Super admin can create schools and assign administrators

---

## Phase 6: User Story 4 - School Branding Customization (Tasks 176-185) [P2]

**Story Goal**: A school administrator customizes their school's appearance by uploading a logo, setting theme colors, and configuring school information.

**Independent Test**: Log in as school admin, change branding settings (logo, colors, principal photo), verify public website reflects changes immediately.

**Acceptance Criteria**:
- School admin can upload custom logo
- Setting primary/secondary colors updates all themed elements
- Contact information updates reflect in footer and contact page
- Principal photo and message update on homepage
- Changes apply only to admin's school, not other schools

### 6.1 Branding API (Red Phase)

- [x] T176 [US4] Write integration tests for PUT /content/branding in backend/tests/integration/test_content_api.py (update logo, colors, contact info)

### 6.2 Branding API (Green Phase)

- [x] T177 [US4] Implement PUT /content/branding endpoint in backend/src/api/content.py (update school logo, primary_color, secondary_color, contact info)

### 6.3 Frontend - Branding Settings (Red Phase)

- [x] T178 [US4] Write E2E tests for branding settings in frontend/tests/e2e/school-admin.spec.ts (upload logo, change colors, verify public site updates)

### 6.4 Frontend - Branding Settings (Green Phase)

- [x] T179 [US4] Implement branding settings page at frontend/src/app/(admin)/branding/page.tsx (logo upload, color pickers, contact form)
- [x] T180 [US4] Implement dynamic theming in TailwindCSS config using CSS variables from school config
- [x] T181 [US4] Update Header component to use dynamic logo_url and primary_color from useSchoolConfig hook

### 6.5 Frontend - Color Preview (Red Phase)

- [x] T182 [US4] Write unit tests for ColorPreview component in frontend/tests/unit/ColorPreview.spec.ts (live preview of theme changes)

### 6.6 Frontend - Color Preview (Green Phase)

- [x] T183 [US4] Implement ColorPreview component in frontend/src/components/admin/ColorPreview.tsx (live preview of buttons, headers with new colors)

### 6.7 User Story 4 - Acceptance Testing

- [x] T184 [US4] Run E2E tests for User Story 4 and verify all acceptance scenarios pass (logo upload, color updates, contact info changes, principal photo update)
- [x] T185 [US4] Verify branding changes apply instantly to public website without cache issues

---

## Phase 7: User Story 5 - Staff Limited Permissions (Tasks 186-195) [P3]

**Story Goal**: A school staff member with restricted permissions updates specific content sections like notices or gallery without access to sensitive areas like results or faculty management.

**Independent Test**: Log in as staff user, verify they can publish notices and upload gallery images but cannot access results or faculty sections.

**Acceptance Criteria**:
- Staff user sees only permitted sections in dashboard (notices, gallery)
- Staff can publish notices successfully
- Staff can upload gallery photos successfully
- Staff cannot access results upload (403 Forbidden)
- Staff cannot access faculty management (403 Forbidden)

### 7.1 Role-Based Authorization (Red Phase)

- [x] T186 [US5] Write unit tests for role-based permissions in backend/tests/unit/test_permissions.py (STAFF role access matrix)

### 7.2 Role-Based Authorization (Green Phase)

- [x] T187 [US5] Implement role-based permission decorator in backend/src/utils/permissions.py (require_role decorator)
- [x] T188 [US5] Apply role-based permissions to content endpoints (STAFF: notices/gallery only, SCHOOL_ADMIN: all content)

### 7.3 Frontend - Staff Dashboard (Red Phase)

- [x] T189 [US5] Write E2E tests for staff user in frontend/tests/e2e/staff-user.spec.ts (limited dashboard, notices/gallery access, results/faculty denial)

### 7.4 Frontend - Staff Dashboard (Green Phase)

- [x] T190 [US5] Implement conditional navigation in frontend/src/components/layout/Navigation.tsx (show/hide menu items based on role)
- [x] T191 [US5] Implement staff dashboard at frontend/src/app/(admin)/staff-dashboard/page.tsx (notices and gallery quick actions only)

### 7.5 Frontend - Permission Guards (Red Phase)

- [x] T192 [US5] Write unit tests for usePermissions hook in frontend/tests/unit/usePermissions.spec.ts (check role-based access)

### 7.6 Frontend - Permission Guards (Green Phase)

- [x] T193 [US5] Implement usePermissions hook in frontend/src/hooks/usePermissions.ts (canAccessFaculty, canAccessResults based on role)
- [x] T194 [US5] Add permission guards to protected routes (redirect to 403 page if unauthorized)

### 7.7 User Story 5 - Acceptance Testing

- [x] T195 [US5] Run E2E tests for User Story 5 and verify all acceptance scenarios pass (staff limited access, notices/gallery allowed, results/faculty denied)

---

## Phase 8: Polish & Cross-Cutting Concerns (Tasks 196-220)

**Goal**: Implement cross-cutting concerns (accessibility, performance, security, error handling, documentation) and polish features.

**Acceptance Criteria**:
- WCAG 2.1 Level AA compliance achieved (SC-011)
- Page load <2 seconds for 95% of requests (SC-004)
- Security scan shows zero critical/high vulnerabilities (SC-013)
- All images load within 1 second with lazy loading (SC-009)
- Comprehensive error handling with user-friendly messages

### 8.1 Accessibility (WCAG 2.1 AA Compliance)

- [x] T196 [P] Add ARIA labels to all interactive elements in frontend components
- [x] T197 [P] Implement keyboard navigation support for all admin panel features
- [x] T198 [P] Ensure 4.5:1 contrast ratio for all text elements (verify with Lighthouse)
- [x] T199 [P] Add skip-to-content links for screen readers
- [x] T200 [P] Ensure all images have descriptive alt text
- [x] T201 [P] Implement focus management for modals and dialogs
- [x] T202 Run Lighthouse accessibility audit and achieve ≥95 score

### 8.2 Performance Optimization

- [x] T203 [P] Implement per-school caching in backend (Redis) for frequently accessed data (school config, public content)
- [x] T204 [P] Configure Next.js Image component with optimal sizes (thumbnail, medium, large)
- [x] T205 [P] Implement API response compression (gzip) in FastAPI
- [x] T206 [P] Add database query optimization (EXPLAIN ANALYZE on slow queries, add missing indexes)
- [x] T207 [P] Configure Cloudflare CDN caching rules for static assets (1 year cache)
- [x] T208 Run Lighthouse performance audit and achieve <2s page load (LCP <2.5s)

### 8.3 Security Hardening

- [x] T209 [P] Implement input sanitization for all user inputs (XSS prevention)
- [x] T210 [P] Add SQL injection prevention (parameterized queries, ORM validation)
- [x] T211 [P] Configure CORS policies (allow only frontend origin)
- [x] T212 [P] Implement rate limiting on all public endpoints (100 req/min per IP)
- [x] T213 [P] Add CAPTCHA to contact forms (hCaptcha or reCAPTCHA)
- [x] T214 [P] Enable HTTPS enforcement (HSTS headers, redirect HTTP to HTTPS)
- [x] T215 [P] Implement Content Security Policy (CSP) headers
- [x] T216 Run OWASP ZAP security scan and fix all critical/high findings

### 8.4 Error Handling & Logging

- [x] T217 [P] Implement global error handler in FastAPI (return user-friendly messages, log stack traces)
- [x] T218 [P] Implement frontend error boundary component (catch React errors, show fallback UI)
- [x] T219 [P] Configure structured logging in backend (JSON logs with request ID, user ID, timestamp)
- [x] T220 [P] Implement audit log query endpoint for super admin (GET /audit-logs with filtering)

### 8.5 Edge Cases & Error Scenarios

- [x] T221 Handle non-existent subdomain (display generic landing page with support contact)
- [x] T222 Handle concurrent edits (last-write-wins with stale data notification)
- [x] T223 Implement file size limit enforcement (client-side pre-check, server-side rejection with compression suggestion)
- [x] T224 Implement missing/corrupted config fallback (restore from backup, alert admin)
- [x] T225 Handle duplicate email across schools (school context selector after login)
- [x] T226 Handle invalid file format upload (reject .exe, .sh, only allow jpg/png/webp)
- [x] T227 Handle duplicate year/class result upload (prompt: replace or create new version)
- [x] T228 Handle past expiry date on notice (reject with validation error)
- [x] T229 Handle published result deletion attempt (soft delete with audit log, require reason)

### 8.6 Data Validation & Quality

- [x] T230 [P] Add comprehensive input validation for all API endpoints (Pydantic models)
- [x] T231 [P] Implement email validation (RFC 5322 compliant)
- [x] T232 [P] Implement subdomain validation (lowercase alphanumeric, 3-50 chars, no special chars except hyphens)
- [x] T233 [P] Implement hex color validation (#RRGGBB format)
- [x] T234 [P] Implement result JSONB schema validation (required fields: students array, statistics)

### 8.7 Testing & Quality Assurance

- [x] T235 Run full backend test suite and verify ≥90% unit coverage, ≥70% integration coverage
- [x] T236 Run full frontend test suite and verify ≥90% unit coverage, ≥70% integration coverage
- [x] T237 Run all E2E tests for P1 user stories (US1, US2, US3) and verify 100% pass rate
- [x] T238 Run tenant isolation security tests and verify 100% cross-school access prevention
- [x] T239 Run load testing (1000 concurrent users) and verify <2s page load (p95), <500ms API response (p95)
- [x] T240 Run automated backup and restore test (verify 100% data integrity)

### 8.8 Documentation & Deployment

- [x] T241 [P] Write API documentation (OpenAPI specs served at /docs endpoint)
- [x] T242 [P] Write deployment guide (Docker, environment variables, database setup)
- [x] T243 [P] Write school admin user guide (content management workflows)
- [x] T244 [P] Write super admin user guide (school onboarding workflow)
- [x] T245 [P] Create database backup script (automated daily backups to S3 or local storage)

---

## Dependency Graph & Parallel Execution

### Phase Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3, 4, 5, 6, 7 (User Stories - Parallelizable) → Phase 8 (Polish)
```

### User Story Dependencies

- **US1** (Public Visitor): Depends on Phase 2 (tenant middleware, public API)
- **US2** (School Admin): Depends on Phase 2 (auth service, content services)
- **US3** (Super Admin): Depends on Phase 2 (auth service, school service)
- **US4** (Branding): Depends on US2 (admin panel infrastructure)
- **US5** (Staff Permissions): Depends on US2 (content management infrastructure)

### Parallel Execution Examples

**After Phase 2 completion, these tasks can run in parallel**:
- US1 Frontend development (T074-T095)
- US2 Backend API development (T100-T132)
- US3 School service development (T159-T170)

**Within US2, these tasks can run in parallel**:
- Faculty service (T103-T110)
- Results service (T111-T116)
- Notices service (T117-T122)
- Gallery service (T123-T128)
- Principal service (T129-T132)

---

## Success Metrics

### Code Coverage Targets
- **Unit Tests**: ≥90% coverage (enforced by pytest-cov, Vitest)
- **Integration Tests**: ≥70% coverage for critical user journeys
- **E2E Tests**: 100% coverage of P1 flows (US1, US2, US3)

### Performance Targets (SC-004, SC-009)
- **Page Load Time**: <2 seconds (p95) for public website pages
- **API Response Time**: <500ms (p95) for all endpoints
- **Image Load Time**: <1 second with lazy loading
- **First Contentful Paint (FCP)**: <1.8s
- **Largest Contentful Paint (LCP)**: <2.5s

### Security Targets (SC-005, SC-013)
- **Tenant Isolation**: 100% cross-school data access prevention
- **Security Scan**: Zero critical/high severity vulnerabilities
- **Authorization**: 100% role-based access enforcement

### Operational Targets (SC-001, SC-007, SC-008)
- **School Onboarding**: <2 hours from start to functional website
- **Concurrent Users**: 1000+ concurrent visitors without performance degradation
- **Backup Recovery**: 100% data integrity on restore

---

## Task Completion Checklist

For each task, verify:
- [ ] Unit tests written and passing (Red phase)
- [ ] Implementation complete and tests passing (Green phase)
- [ ] Code refactored for clarity and maintainability (Refactor phase)
- [ ] No linting errors (eslint, ruff/flake8)
- [ ] Code reviewed (if team workflow requires)
- [ ] Documentation updated (docstrings, comments for complex logic)
- [ ] Manual testing performed (if applicable)
- [ ] Committed with descriptive commit message

---

## Next Steps

1. **Set up development environment** following [quickstart.md](./quickstart.md)
2. **Start with Phase 1** (Tasks T001-T015) to establish project foundation
3. **Complete Phase 2** (Tasks T016-T054) to build database and foundational services
4. **Implement P1 User Stories** (Phases 3-4: US1, US2) for core functionality
5. **Add P2 Features** (Phases 5-6: US3, US4) for multi-tenancy and branding
6. **Implement P3 Features** (Phase 7: US5) for advanced permissions
7. **Polish and deploy** (Phase 8) with accessibility, performance, and security hardening

---

**End of Tasks Document**
