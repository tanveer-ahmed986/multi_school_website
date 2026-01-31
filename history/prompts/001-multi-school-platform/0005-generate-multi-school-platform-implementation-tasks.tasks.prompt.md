---
id: 0005
title: Generate Multi-School Platform Implementation Tasks
stage: tasks
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-multi-school-platform
branch: 001-multi-school-platform
user: tanveer-ahmed986
command: /sp.tasks make tasks for implementation
labels: ["task-generation", "tdd-workflow", "user-stories", "implementation-roadmap"]
links:
  spec: specs/001-multi-school-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-multi-school-platform/tasks.md
tests:
  - null
---

## Prompt

User invoked `/sp.tasks make tasks for implementation` to generate comprehensive implementation tasks for the multi-school website platform based on the specification, plan, data model, and API contracts.

User context: "make tasks for implementation"

**Available Design Documents**:
- spec.md (5 user stories: US1-P1 public visitor, US2-P1 school admin, US3-P2 super admin, US4-P2 branding, US5-P3 staff)
- plan.md (FastAPI backend, Next.js frontend, PostgreSQL with RLS, JWT auth)
- data-model.md (7 entities with RLS policies)
- contracts/ (4 OpenAPI specs with 39 endpoints)
- research.md (technology stack decisions)

## Response snapshot

Generated comprehensive tasks.md file with **245 implementation tasks** organized into 8 phases following TDD Red-Green-Refactor workflow and user story prioritization.

**Task Organization (8 Phases)**:

1. **Phase 1: Project Setup & Infrastructure** (15 tasks)
   - Project structure creation per plan.md
   - Backend: FastAPI + SQLAlchemy + pytest setup
   - Frontend: Next.js + TypeScript + Tailwind setup
   - Database: PostgreSQL installation and configuration
   - Environment configuration (.env files)

2. **Phase 2: Database Schema & Foundational Services** (40 tasks) - BLOCKING
   - Database models for all 7 entities (School, User, Faculty, Result, Notice, GalleryImage, PrincipalProfile)
   - PostgreSQL Row-Level Security (RLS) policies for multi-tenant isolation
   - Alembic migrations for schema creation
   - Authentication service (JWT with refresh tokens)
   - Tenant middleware (subdomain extraction, session context)
   - File storage service abstraction (S3 migration path)
   - Security tests for tenant isolation (100% prevention of cross-school access)
   - Unit tests for all foundational services (≥90% coverage)

3. **Phase 3: User Story 1 - Public Website Visitor [P1]** (42 tasks)
   - **Independent Test**: Access subdomain and verify all public content with correct branding
   - Tests: E2E public visitor flow, unit tests for public services
   - Backend: Public API endpoints (config, home, faculty, results, notices, gallery, principal)
   - Frontend: Public pages (homepage, faculty, results, gallery, notices), layout components (Header, Footer, Navigation with tenant branding)
   - Components: Hero, NoticeBoard, GalleryGrid, ResultsTable, FacultyCard
   - Integration: Subdomain routing, school config loading, CDN caching
   - Acceptance: Verify all 5 acceptance scenarios from spec

4. **Phase 4: User Story 2 - School Admin Content Management [P1]** (62 tasks)
   - **Independent Test**: Login as school admin, perform CRUD operations, verify changes appear only on that school
   - Tests: E2E admin flow, integration tests for content API, unit tests for content services
   - Backend: Content management API (faculty, results, notices, gallery, principal CRUD)
   - Frontend: Admin panel pages (dashboard, faculty manager, result uploader, notice editor, gallery manager)
   - Components: ContentEditor, FileUploader, FacultyForm, ResultUploadForm
   - Security: Authorization checks (school_id scoping, role enforcement)
   - File handling: Image validation (5MB, jpg/png/webp), client + server validation
   - Acceptance: Verify all 7 acceptance scenarios including cross-school access denial

5. **Phase 5: User Story 3 - Super Admin School Onboarding [P2]** (17 tasks)
   - **Independent Test**: Create new school, assign admin, verify website immediately accessible
   - Tests: E2E onboarding flow, unit tests for school service
   - Backend: School management API (create, assign admin, folder structure generation)
   - Frontend: Super admin panel (school creation form, admin assignment)
   - Workflow: UUID generation, default config creation, school_id assignment
   - Acceptance: Verify all 5 acceptance scenarios including <2 hour onboarding target

6. **Phase 6: User Story 4 - School Branding Customization [P2]** (10 tasks)
   - **Independent Test**: Change branding settings, verify public website reflects changes immediately
   - Tests: Integration tests for branding API
   - Backend: Branding update API (logo upload, color customization)
   - Frontend: Branding settings page, color picker, logo uploader
   - Dynamic theming: Tailwind config with CSS variables for school colors
   - Acceptance: Verify all 4 acceptance scenarios

7. **Phase 7: User Story 5 - Staff Limited Permissions [P3]** (10 tasks)
   - **Independent Test**: Login as staff, verify limited access (notices/gallery only)
   - Tests: Authorization tests for staff role
   - Backend: Role-based permission checks in content API
   - Frontend: Staff dashboard (limited sections visible)
   - Acceptance: Verify all 4 acceptance scenarios including permission denial

8. **Phase 8: Polish & Cross-Cutting Concerns** (50 tasks)
   - Performance optimization (caching, CDN integration, lazy loading)
   - Security hardening (rate limiting, CSRF, input sanitization, CAPTCHA)
   - Accessibility (WCAG 2.1 AA compliance, screen reader testing, keyboard navigation)
   - Error handling (404 pages, error boundaries, user-friendly messages)
   - Observability (logging, monitoring, error tracking)
   - Documentation (API docs, developer guides, deployment guide)
   - E2E regression tests for all user stories
   - Load testing (1000 concurrent users target)
   - Security scanning (OWASP ZAP, dependency scanning)
   - Production deployment configuration

**Task Format Compliance** (All 245 tasks):
- ✅ Checkbox format: `- [ ]` prefix on every task
- ✅ Sequential IDs: T001 through T245
- ✅ Parallelization markers: `[P]` on 87 parallelizable tasks
- ✅ User story labels: `[US1]` through `[US5]` on 141 story tasks
- ✅ Exact file paths: All tasks include specific file paths (backend/src/..., frontend/src/...)

**TDD Workflow** (Red-Green-Refactor):
- **Red**: Test tasks appear BEFORE implementation tasks in each phase
- **Green**: Implementation tasks follow their corresponding test tasks
- **Refactor**: Implicit in task completion checklist
- Test pyramid enforced: Unit (≥90%), Integration (≥70%), E2E (100% P1 flows)

**Multi-Tenant Architecture Tasks**:
- T033-T034: PostgreSQL RLS policies for all tenant tables
- T044-T045: Tenant middleware (subdomain extraction, session context setting)
- T052-T054: Security tests verifying 100% tenant isolation
- T133-T135: File storage service with per-school_id isolation
- T209-T216: Authorization tests for all roles and cross-school access prevention

**Dependency Graph**:
- Phase 1 (Setup) → Phase 2 (Foundational) → User Stories (P1 → P2 → P3) → Phase 8 (Polish)
- Within each user story: Tests → Models → Services → Endpoints → UI → Integration
- US1 and US2 can proceed in parallel after Phase 2 completes
- US3, US4, US5 can proceed after US2 (dependency on auth/content management)

**Parallel Execution Examples**:
- Phase 2: T023-T032 (all 7 model files can be created in parallel)
- Phase 3 (US1): T070-T075 (public API endpoints can be implemented in parallel)
- Phase 4 (US2): T108-T115 (frontend components can be developed in parallel)
- 87 total tasks marked `[P]` for parallel execution

**Test Coverage Targets**:
- Unit tests: ≥90% for business logic (services, models, utilities)
- Integration tests: ≥70% for critical journeys (API endpoints, page flows)
- E2E tests: 100% for P1 user stories (US1, US2, US3)
- Security tests: 100% tenant isolation verification (cross-school access prevention)
- Accessibility tests: WCAG 2.1 AA compliance verification

**Constitution Compliance**:
- ✅ TDD: Test tasks before implementation throughout all phases
- ✅ Component Architecture: Clear separation (models → services → endpoints → UI)
- ✅ Accessibility: Dedicated tasks (T196-T202) for WCAG 2.1 AA
- ✅ Performance: Optimization tasks (T203-T208) for <2s page load
- ✅ Security: Comprehensive security tasks (T052-T054, T209-T216, T217-T222)
- ✅ Multi-Tenant: RLS policies, tenant middleware, isolation tests throughout

**MVP Scope Recommendation**:
- **Minimal MVP**: Phase 1 + Phase 2 + Phase 3 (US1 only) = 97 tasks
  - Delivers: Public website visitor can view school information
  - Value: Demonstrates multi-tenant platform with one P1 story
- **Recommended MVP**: Phase 1 + Phase 2 + Phase 3 + Phase 4 (US1 + US2) = 159 tasks
  - Delivers: Public website + School admin content management
  - Value: Fully functional platform for single school with admin capabilities

**Implementation Strategy**:
1. Complete Phase 1 (Setup) - 1-2 days
2. Complete Phase 2 (Foundational) - 3-5 days
3. Implement US1 (Public Visitor) - 3-4 days
4. Implement US2 (School Admin) - 5-7 days
5. Implement US3 (Super Admin) - 2-3 days
6. Implement US4 (Branding) - 1-2 days
7. Implement US5 (Staff) - 1-2 days
8. Complete Phase 8 (Polish) - 4-5 days
- **Total estimated effort**: 20-30 days (single developer, full-time)

## Outcome

- ✅ Impact: 245 comprehensive implementation tasks generated covering all 5 user stories with complete TDD workflow. Tasks organized by user story for independent implementation and testing. Clear MVP scope defined (US1+US2 = 159 tasks). Ready for immediate implementation.
- 🧪 Tests: Test tasks included for every feature area (unit, integration, E2E, security). Test pyramid enforced: ≥90% unit, ≥70% integration, 100% E2E for P1. TDD workflow: Red (test first) → Green (implement) → Refactor (implicit).
- 📁 Files: Created specs/001-multi-school-platform/tasks.md (245 tasks, 8 phases)
- 🔁 Next prompts: Begin implementation with Phase 1 (Setup). Use TDD Red-Green-Refactor workflow. Mark tasks complete as you progress. Run `/sp.implement` if autonomous implementation is desired.
- 🧠 Reflection: Task generation successfully maps all user stories to implementation work. Multi-tenant architecture (RLS, tenant middleware, isolation tests) thoroughly covered. TDD workflow enforced throughout. Parallelization opportunities identified (87 tasks marked [P]). MVP scope clearly defined. Constitutional principles (TDD, component architecture, accessibility, security) embedded in task structure.

## Evaluation notes (flywheel)

- Failure modes observed: None. Tasks generated successfully with all format requirements met.
- Graders run and results (PASS/FAIL): Format validation - PASS (all 245 tasks have checkbox, ID, file paths). TDD workflow - PASS (test tasks before implementation). User story organization - PASS (clear phases with independent test criteria). Constitution alignment - PASS (TDD, accessibility, security, performance tasks included).
- Prompt variant (if applicable): Standard /sp.tasks workflow with emphasis on user story organization and TDD compliance
- Next experiment (smallest change to try): Monitor implementation progress to validate task granularity (are tasks small enough for daily completion?) and dependency accuracy (are blocking relationships correct?). Consider if additional refactoring tasks should be explicit rather than implicit.
