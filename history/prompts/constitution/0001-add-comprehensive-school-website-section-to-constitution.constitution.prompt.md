---
id: 0001
title: Add comprehensive school website section to constitution
stage: constitution
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: system
command: /sp.constitution
labels: ["constitution", "school-websites", "education", "compliance", "multi-tenant", "ferpa", "coppa", "gdpr"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - No automated tests (constitution document)
---

## Prompt

read a constitution which i added, any improvement is required or this is quite enough to create school website?

## Response snapshot

### Assessment Provided
The existing constitution (v1.6.0) was comprehensive for general websites (e-commerce, SaaS, portfolios, blogs, entertainment, social media) but **completely lacked school-specific requirements**.

### User Requirements Gathered
Through targeted questions, confirmed the platform needs:
- Student Management System (student records, enrollment, attendance, grades, transcripts)
- Parent/Guardian Portal (parent communication, student progress monitoring)
- Academic Management (courses, schedules, assignments, grading, report cards)
- Multi-School Management (multi-tenant architecture with data isolation)
- Compliance: FERPA (US student privacy), GDPR (EU data protection), local education laws

### Constitution Amendment (v1.6.0 → v1.7.0)
Added comprehensive **"School Websites & Student Management Systems"** section (inserted at line 1517) covering:

**Core Educational Features:**
- Multi-tenant architecture with strict data isolation between schools
- Role-based access control (9 roles: Platform Admin, School Admin, Principal, Teacher, Counselor, Staff, Parent, Student, Guest)
- Student information system capabilities
- Grade book and academic tracking
- Attendance and enrollment management
- Parent-teacher communication
- Academic scheduling and timetabling
- Reporting and analytics

**Critical Compliance Requirements:**
- **FERPA compliance** (US education privacy): consent requirements, audit logging, directory information opt-out, access controls
- **COPPA compliance** (children under 13): parental consent, age gating, data minimization, no public posting by children
- **GDPR compliance** (EU): explicit consent, right to access/rectification/erasure, data portability, privacy by design, breach notification
- General data protection: encryption at rest/in transit, MFA, session timeouts, audit logs, data retention policies

**Enhanced Security & Privacy:**
- List of 25+ sensitive data types that MUST be protected
- Multi-factor authentication for staff
- Automatic session timeout (15 minutes)
- Comprehensive audit logging
- Data breach response procedures
- Annual security training requirements

**Technical Architecture:**
- Three recommended tech stack options:
  1. Next.js full-stack (Recommended) - modern, type-safe, excellent DX
  2. Django full-stack (Traditional) - battle-tested for educational SIS
  3. Microservices (Next.js + FastAPI) - scalable, AI-ready
- Database schema design for multi-tenancy with row-level security
- Integration requirements (SIS, LMS, SSO providers)

**Testing & Launch Requirements:**
- Multi-tenant security testing
- Compliance verification checklists
- Load testing for peak periods (registration)
- Accessibility testing with assistive technologies
- Comprehensive launch checklist (25+ items)

**AI-Powered Enhancements:**
- Student at-risk prediction
- Automated absence pattern detection
- Chatbot for parent/student questions
- Personalized learning recommendations
- Intelligent scheduling assistance
- Plagiarism detection
- Multilingual translation

### Sync Impact Report Updated
Updated HTML comment at top of constitution with:
- Version change: 1.6.0 → 1.7.0 (MINOR bump - new section added)
- Templates requiring updates (plan, spec, tasks templates)
- Follow-up TODOs: checklists for school launch, FERPA compliance, multi-tenant testing

## Outcome

- ✅ Impact: Constitution now comprehensively covers school website requirements with strict compliance standards (FERPA, COPPA, GDPR), multi-tenant architecture, and educational features. The platform can now be built with clear, enforceable standards.
- 🧪 Tests: No automated tests (documentation change). Manual validation: section inserted correctly, no broken formatting, compliance requirements thoroughly documented.
- 📁 Files: Modified `.specify/memory/constitution.md` (added ~500 lines, version 1.6.0 → 1.7.0)
- 🔁 Next prompts:
  - Create school website specification using `/sp.specify`
  - Update plan/spec/tasks templates to include school-specific sections
  - Create FERPA/COPPA compliance checklist
  - Design multi-tenant database schema
- 🧠 Reflection: The constitution was excellent for general websites but critically missing education-specific guidance. The amendment adds legally-required compliance standards (FERPA, COPPA, GDPR) and practical technical requirements (multi-tenancy, RBAC, data isolation) that are non-negotiable for school platforms handling sensitive student data.

## Evaluation notes (flywheel)

- Failure modes observed: None. Constitution amendment completed successfully with comprehensive coverage.
- Graders run and results (PASS/FAIL): N/A (no automated graders for documentation)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate constitution completeness by attempting to generate a school website specification and identifying any missing requirements.
