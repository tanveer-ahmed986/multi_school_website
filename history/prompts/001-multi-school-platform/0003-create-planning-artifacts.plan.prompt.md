---
id: 0003
title: Create Planning Artifacts for Multi-School Platform
stage: plan
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-multi-school-platform
branch: 001-multi-school-platform
user: system
command: create planning artifacts
labels: ["planning", "data-model", "api-contracts", "quickstart", "documentation"]
links:
  spec: D:\multi_school_website\specs\001-multi-school-platform\spec.md
  ticket: null
  adr: null
  pr: null
files:
 - D:\multi_school_website\specs\001-multi-school-platform\data-model.md
 - D:\multi_school_website\specs\001-multi-school-platform\contracts\auth.openapi.yaml
 - D:\multi_school_website\specs\001-multi-school-platform\contracts\schools.openapi.yaml
 - D:\multi_school_website\specs\001-multi-school-platform\contracts\content.openapi.yaml
 - D:\multi_school_website\specs\001-multi-school-platform\contracts\public.openapi.yaml
 - D:\multi_school_website\specs\001-multi-school-platform\quickstart.md
tests:
 - No tests created (planning phase)
---

## Prompt

Create the remaining planning artifacts for the multi-school platform:

1. Create data-model.md at D:\multi_school_website\specs\001-multi-school-platform\data-model.md with:
   - All 7 entities from spec (School, User, Faculty, Result, Notice, GalleryImage, PrincipalProfile)
   - Fields with types, constraints, validation rules
   - Relationships between entities
   - PostgreSQL Row-Level Security (RLS) policies
   - Indexes for performance
   - Multi-tenant isolation strategy

2. Create contracts directory and API contracts:
   - D:\multi_school_website\specs\001-multi-school-platform\contracts\auth.openapi.yaml
   - D:\multi_school_website\specs\001-multi-school-platform\contracts\schools.openapi.yaml
   - D:\multi_school_website\specs\001-multi-school-platform\contracts\content.openapi.yaml
   - D:\multi_school_website\specs\001-multi-school-platform\contracts\public.openapi.yaml

3. Create quickstart.md at D:\multi_school_website\specs\001-multi-school-platform\quickstart.md with:
   - Prerequisites
   - Backend setup (FastAPI, PostgreSQL)
   - Frontend setup (Next.js)
   - How to onboard a test school
   - Running tests

Context:
- Backend: FastAPI (Python 3.11+), PostgreSQL 15+ with RLS, SQLAlchemy
- Frontend: Next.js 14+, TypeScript
- Auth: JWT with refresh tokens
- Multi-tenant: Row-level security in PostgreSQL

Reference the spec.md, plan.md, and research.md files in the same directory for requirements.

## Response snapshot

Successfully created all remaining planning artifacts for the multi-school platform:

**1. Data Model (data-model.md)**
- Comprehensive database schema with 7 core entities (School, User, Faculty, Result, Notice, GalleryImage, PrincipalProfile)
- 2 supporting tables (AuditLog, RefreshTokens)
- Complete field definitions with types, constraints, and validation rules
- PostgreSQL Row-Level Security (RLS) policies for all tenant-specific tables
- Multi-tenant isolation strategy using session variables (app.current_school_id)
- Performance indexes for all foreign keys and common query patterns
- Entity relationships with proper foreign key cascades
- Database initialization scripts (extensions, types, triggers)
- Migration strategy using Alembic
- Security testing examples for tenant isolation

**2. API Contracts (OpenAPI 3.0.3 specifications)**

**auth.openapi.yaml**:
- POST /auth/login - User authentication with JWT
- POST /auth/refresh - Refresh token rotation
- POST /auth/logout - Token revocation
- GET /auth/me - Current user profile
- POST /auth/select-school - Multi-school context switching
- Complete request/response schemas with examples

**schools.openapi.yaml** (Super Admin only):
- GET /schools - List all schools with pagination
- POST /schools - Create new school tenant
- GET /schools/{school_id} - Get school details
- PUT /schools/{school_id} - Update school configuration
- DELETE /schools/{school_id} - Delete school (with confirmation)
- GET /schools/{school_id}/stats - School usage statistics
- GET /schools/{school_id}/admins - List school administrators
- POST /schools/{school_id}/admins - Create school admin/staff

**content.openapi.yaml** (School Admin & Staff):
- Faculty management (CRUD operations with photo upload)
- Results management (CRUD with structured JSON data, audit logging)
- Notices management (CRUD with attachments, auto-expiry)
- Gallery management (image upload with storage tracking)
- Principal profile management (upsert with photo)
- Branding management (logo and color customization)
- All endpoints enforce RLS policies for tenant isolation

**public.openapi.yaml** (No authentication):
- GET /public/school - School information and branding
- GET /public/faculty - Public faculty directory
- GET /public/results - List available results
- GET /public/results/{year}/{class} - Specific result details
- GET /public/notices - Active notices (auto-filtered by expiry)
- GET /public/gallery - Gallery images with pagination
- GET /public/principal - Principal's profile and message
- All endpoints filtered by subdomain-resolved school_id

**3. Quickstart Guide (quickstart.md)**
- Prerequisites (Python 3.11+, Node.js 18+, PostgreSQL 15+, Git)
- Database setup (local PostgreSQL and Docker options)
- Backend setup with virtual environment, dependencies, environment variables
- Database schema initialization using Alembic
- Seed script for development data (Super Admin, demo school, school admin, staff)
- Frontend setup with Next.js, dependencies, environment configuration
- Subdomain routing setup for local development
- Test school onboarding walkthrough
- Running backend and frontend tests (pytest, Vitest, Playwright)
- Development workflow (daily setup, database migrations, TDD cycle)
- Comprehensive troubleshooting section
- Useful commands reference for backend, frontend, and database

## Outcome

- ✅ Impact: All planning artifacts created to support implementation phase. Developers can now set up local environment, understand data model, reference API contracts, and begin implementation tasks.
- 🧪 Tests: No tests created (planning phase). Test structure documented in quickstart.md for developers.
- 📁 Files: Created 6 files (1 data model, 4 API contracts, 1 quickstart guide)
- 🔁 Next prompts: Run /sp.tasks command to generate implementation tasks from plan.md
- 🧠 Reflection: Complete planning phase artifacts ensure consistent implementation. Data model with RLS policies provides database-level multi-tenant security. OpenAPI contracts enable contract-first development. Quickstart guide reduces onboarding friction for developers.

## Evaluation notes (flywheel)

- Failure modes observed: None - all artifacts created successfully
- Graders run and results (PASS/FAIL): N/A (planning phase, no code to test)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate implementation tasks using /sp.tasks to begin Red-Green-Refactor cycles
